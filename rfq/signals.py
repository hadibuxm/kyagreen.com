import logging
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import RFQRequest

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=RFQRequest)
def store_previous_status(sender, instance, **kwargs):
    """Capture existing status so we can detect changes in post_save."""
    if not instance.pk:
        instance._previous_status = None
        return

    try:
        previous = sender.objects.get(pk=instance.pk)
        instance._previous_status = previous.status
    except sender.DoesNotExist:
        instance._previous_status = None


@receiver(post_save, sender=RFQRequest)
def send_rfq_confirmation_email(sender, instance, created, **kwargs):
    """Send confirmation email to client when new RFQ is created."""
    if not created:
        return

    subject = "We have received your request for quotation"
    message_lines = [
        f"Hello {instance.name},",
        "",
        "Thank you for submitting a request for quotation with Kiya Green.",
        f"Your Request ID: {instance.id}",
        "",
        "We have received your request and our team will review it shortly.",
        "You will receive an email update once we have prepared a quotation for you.",
        "",
        "If you have any questions in the meantime, feel free to reply to this email.",
        "Thank you for choosing Kiya Green.",
    ]

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@kyagreen.com")

    try:
        send_mail(
            subject,
            "\n".join(message_lines),
            from_email,
            [instance.email],
            fail_silently=False,
        )
        logger.info(f"RFQ confirmation email sent to {instance.email} for RFQ ID {instance.id}")
    except Exception as e:
        logger.error(f"Failed to send RFQ confirmation email to {instance.email}: {str(e)}")


@receiver(post_save, sender=RFQRequest)
def send_status_change_email(sender, instance, created, **kwargs):
    """Notify the client when their quotation status changes."""
    if created:
        return

    previous_status = getattr(instance, "_previous_status", None)
    if not previous_status or previous_status == instance.status:
        return

    subject = f"Your quotation status changed to {instance.get_status_display()}"
    message_lines = [
        f"Hello {instance.name},",
        "",
        f"We have updated the status of your quotation request (ID: {instance.id}).",
        f"New status: {instance.get_status_display()}",
    ]

    if instance.admin_notes:
        message_lines.extend(["", "Notes from our team:", instance.admin_notes])

    message_lines.extend(
        [
            "",
            "If you have any questions, feel free to reply to this email.",
            "Thank you for choosing Kiya Green.",
        ]
    )

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@kyagreen.com")

    try:
        send_mail(
            subject,
            "\n".join(message_lines),
            from_email,
            [instance.email],
            fail_silently=False,
        )
        logger.info(f"RFQ status change email sent to {instance.email} for RFQ ID {instance.id}")
    except Exception as e:
        logger.error(f"Failed to send RFQ status change email to {instance.email}: {str(e)}")


@receiver(post_save, sender=RFQRequest)
def notify_admin_new_rfq(sender, instance, created, **kwargs):
    """Notify admin when a new RFQ is submitted."""
    if not created:
        return

    admin_email = getattr(settings, "ADMIN_EMAIL", None)
    if not admin_email:
        return

    subject = f"New RFQ Request #{instance.id} from {instance.name}"
    message_lines = [
        f"New Request for Quotation received",
        "",
        f"Customer: {instance.name}",
        f"Email: {instance.email}",
        f"Phone: {instance.phone}",
        f"Company: {instance.company or 'N/A'}",
        f"Subject: {instance.subject or 'N/A'}",
        f"Quantity: {instance.quantity}",
        f"Product: {instance.product.name if instance.product else 'General Inquiry'}",
        "",
        f"Message/Requirements:",
        instance.message,
        "",
        f"View in admin: {instance.id}",
    ]

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@kyagreen.com")

    try:
        send_mail(
            subject,
            "\n".join(message_lines),
            from_email,
            [admin_email],
            fail_silently=False,
        )
        logger.info(f"Admin notification email sent for new RFQ ID {instance.id}")
    except Exception as e:
        logger.error(f"Failed to send admin notification email for RFQ ID {instance.id}: {str(e)}")
