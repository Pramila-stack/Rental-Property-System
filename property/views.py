from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView,CreateView,View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.shortcuts import redirect
from .models import Booking, Property, Review
from .forms import BookingForm, ReviewForm, SignupForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages

from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required




class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("property-list")

    def form_valid(self, form):
        user=form.save()
        login(self.request,user)
        return super().form_valid(form)

# 🔹 Property List
class PropertyListView(ListView):
    model = Property
    template_name = 'property_list.html'
    context_object_name = 'properties'

    def get_queryset(self):
        return Property.objects.filter(is_active=True)


# 🔹 Property Detail + Booking
class PropertyDetailView(LoginRequiredMixin, DetailView, FormView):
    model = Property
    template_name = 'property_detail.html'
    context_object_name = 'property'
    form_class = BookingForm

    # ✅ filter active properties
    def get_queryset(self):
        return Property.objects.filter(is_active=True)

    # ✅ add reviews to context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        property = self.object
        context['reviews'] = property.reviews.all()
        return context

    # ✅ handle POST (booking)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # VERY IMPORTANT
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.user = self.request.user
        booking.property = self.object

        start = booking.start_date
        end = booking.end_date

        conflict = Booking.objects.filter(
            property = self.object,
            status = "approved"
        ).filter(
            Q(start_date__lt=end) & Q(end_date__gt=start)
        ).exists()

        if conflict:
            messages.error(self.request,"This property has already been booked for given dates.")
            return self.form_invalid(form)

        days = (end-start).days
        booking.total_price = days * self.object.price_per_night

        booking.save()  # admin will approve later
        return redirect('booking-success')
    
class BookingSuccessView(TemplateView):
    template_name = "booking_success.html"

# 🔹 Add Review
class AddReviewView(LoginRequiredMixin, FormView):
    template_name = 'add_review.html'
    form_class = ReviewForm

    def get_queryset(self):
        return Review.objects.all().order_by("id")

    

    def dispatch(self, request, *args, **kwargs):
        self.property = get_object_or_404(
            Property,
            pk=self.kwargs['pk'],
            is_active=True
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        review = form.save(commit=False)
        review.user = self.request.user
        review.property = self.property
        review.save()  # admin approves

        return redirect('property-detail', pk=self.property.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property'] = self.property
        return context

@method_decorator(staff_member_required,name="dispatch")
class AdminBookingListView(ListView):
    model = Booking
    template_name = "bookings.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return Booking.objects.all().order_by("-id")

 
@method_decorator(staff_member_required,name="dispatch")
class ApproveBookingView(View):
    def post(self,request,pk):
        booking = get_object_or_404(Booking,pk=pk)
        booking.status = "approved"
        booking.save()

        messages.success(request,"Booking approved successfully.")
        return redirect("admin-bookings")
    
@method_decorator(staff_member_required,name="dispatch")
class RejectBookingView(View):
    def post(self,request,pk):
        booking = get_object_or_404(Booking,pk=pk)
        booking.status = "rejected"
        booking.save()
        messages.error(request,"Booking rejected successfully.")
        return redirect("admin-bookings")
