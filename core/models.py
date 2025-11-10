from django.db import models
from ckeditor.fields import RichTextField


class HomePage(models.Model):
    """Model for managing homepage content"""
    title = models.CharField(max_length=200, default="Welcome to KiyaGreen")
    subtitle = models.CharField(max_length=300, blank=True, default="Your trusted partner for eco-friendly and sustainable solutions")
    hero_image = models.ImageField(upload_to='homepage/', blank=True, null=True)
    content = RichTextField(blank=True)
    welcome_section = RichTextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Page"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Single instance model
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class InformationPage(models.Model):
    """Model for Information/About Us page"""
    title = models.CharField(max_length=200, default="About Us")
    content = RichTextField()
    mission = RichTextField(blank=True, help_text="Mission statement")
    vision = RichTextField(blank=True, help_text="Vision statement")
    image = models.ImageField(upload_to='information/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Information Page"
        verbose_name_plural = "Information Page"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Single instance model
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class ContactInfo(models.Model):
    """Model for contact information"""
    address = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    whatsapp = models.CharField(max_length=50, blank=True)
    working_hours = models.CharField(max_length=200, blank=True)
    map_embed = models.TextField(blank=True, help_text="Google Maps embed code")

    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return "Contact Information"

    def save(self, *args, **kwargs):
        # Single instance model
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
