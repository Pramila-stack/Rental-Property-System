from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Booking


@receiver(pre_save, sender=Booking)
def booking_approval_email(sender, instance, **kwargs):

    if instance.pk:
        old_instance = Booking.objects.get(pk=instance.pk)

        # ONLY when status changes to approved
        if old_instance.status != "approved" and instance.status == "approved":

            send_mail(
                subject="🎉 Booking Approved",
                message=f"""
Hi {instance.user.username},

Your booking for {instance.property.title} has been approved.

Start: {instance.start_date}
End: {instance.end_date}

Thank you for using our platform!
""",
                from_email="pramilatmg.np@gmail.com",
                recipient_list=[instance.user.email],
                fail_silently=False,
            )
