from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path(
        "event/<int:event_id>/",
        views.event_detail,
        name="event_detail"
    ),

    path(
        "event/<int:event_id>/book/",
        views.book_event,
        name="book_event"
    ),

    path(
        "booking-confirmation/<uuid:booking_id>/",
        views.booking_confirmation,
        name="booking_confirmation"
    ),

    path(
        "booking/<uuid:booking_id>/cancel/",
        views.cancel_booking,
        name="cancel_booking"
    ),

    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("logout/", views.user_logout, name="logout"),
]