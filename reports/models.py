from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Report(models.Model):

    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('pending_verification', 'Pending Verification'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]

    rejection_reason = models.TextField(
    blank=True,
    default=''
)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)

    date_reported = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(
        upload_to='reports/',
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='reports'
    )

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='reports'
    )

    assigned_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_reports'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='submitted'
    )

    def __str__(self):
        return self.title