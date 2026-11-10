# Register your models here.

from django.contrib import admin
from .models import Event, Booking


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "location",
        "event_date",
        "price",
        "total_tickets",
    )

    list_filter = ("category", "event_date")
    search_fields = ("title", "location")
    ordering = ("event_date",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "event",
        "tickets",
        "booked_at",
    )

    list_filter = ("booked_at",)
    search_fields = ("user__username", "event__title")

