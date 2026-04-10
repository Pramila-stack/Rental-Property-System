# Automatic email sender when cliced approved=True in the admin panel.
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Booking

@receiver(pre_save, sender=Booking)
def booking_approval_email(sender, instance, **kwargs):

    if instance.pk:
        old_instance = Booking.objects.get(pk=instance.pk)

        # only when admin approves
        if not old_instance.approved and instance.approved:

            send_mail(
                subject="🎉 Booking Approved",
                message=f"""
Hi {instance.user.username},

Your booking for {instance.property.title} has been approved.

Start: {instance.start_date}
End: {instance.end_date}

Thank you for using our platform!
""",
                from_email="your_email@gmail.com",
                recipient_list=[instance.user.email],
                fail_silently=False,
            )

# @receiver(pre_save,sender="Booking")

# pre_save
👉 This means:
“Run this code BEFORE Booking is saved to database”


# @receiver(pre_save, sender=Booking)

👉 This connects signal to model.
Meaning:
“When Booking is about to be saved, run this function.”

# def booking_approval_email(sender,instance,**kwargs):
Parameter	 ------------------------------------------> Meaning
sender	   ------------------------------------------> Booking model
instance   ------------------------------------------> current object being saved
kwargs     ------------------------------------------> extra Django data

# if instance.pk:
“Only run this if booking already exists in database”

# old_instance = Booking.objects.get(pk=instance.pk)
👉 This fetches previous saved version from database.

# if not old_instance.approved and instance.approved:
“Send email ONLY when the booking was NOT approved before, but is approved NOW.”
changed From False to True.
this is old

# if old_instance.status != "approved" and instance.status == "approved":
ONLY when status changes to approved
This is new


# And last send mail

# Working 
Admin opens booking in /admin
        ↓
Changes approved = True
        ↓
Django saves model
        ↓
pre_save signal triggers
        ↓
old_instance fetched
        ↓
compare old vs new
        ↓
approval detected
        ↓
send_mail() runs
        ↓
Gmail sends email
        ↓
User receives notification

# apps.py
from django.apps import AppConfig

class PropertyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'property'

    def ready(self):
        import property.signals

# 👉 AppConfig is Django’s way of configuring your app when the project starts.

It runs when:
python manage.py runserver
or
Django starts project

# default_auto_field = 'django.db.models.BigAutoField'

👉 This means:
Django will use BigAutoField for primary keys
Example:
id = 1, 2, 3...

<!-- def ready(self):
    import property.signals
🧠 What does ready() do? -->

👉 It runs when Django fully starts your app.
Think of it like:
“Run this code when the app is fully loaded and ready.”

# import property.signals
👉 It means:
“Load the signals file so Django connects all @receiver functions”