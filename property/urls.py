from django.urls import path

from property import views

urlpatterns = [
    path("",views.PropertyListView.as_view(),name="property-list"),
    path("property-detail/<int:pk>/",views.PropertyDetailView.as_view(),name="property-detail"),
    path("add-review/<int:pk>/",views.AddReviewView.as_view(),name="add-review"),
    path("signup/",views.SignupView.as_view(),name="signup"),
    path('bookings/', views.AdminBookingListView.as_view(), name='admin-bookings'),
    path('bookings/<int:pk>/approve/',views.ApproveBookingView.as_view(), name='approve-booking'),
    path('bookings/<int:pk>/reject/', views.RejectBookingView.as_view(), name='reject-booking'),
    path("booking-success/",views.BookingSuccessView.as_view(),name="booking-success"),
]

