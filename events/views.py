from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q, Sum
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Event, Booking


def home(request):
    events = Event.objects.filter(
        event_date__gte=timezone.now()
    )

    search_query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()

    if search_query:
        events = events.filter(
            Q(title__icontains=search_query)
            | Q(location__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    valid_categories = [
        "music", "tech", "workshop",
        "college", "sports", "other"
    ]

    if category in valid_categories:
        events = events.filter(category=category)

    events = events.order_by("event_date")

    return render(request, "events/home.html", {
        "events": events,
        "search_query": search_query,
        "selected_category": category,
    })


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    booked_tickets = Booking.objects.filter(
        event=event,
        status="confirmed"
    ).aggregate(total=Sum("tickets"))["total"] or 0

    available_tickets = max(
        0, event.total_tickets - booked_tickets
    )

    sold_percentage = (
        int((booked_tickets / event.total_tickets) * 100)
        if event.total_tickets > 0
        else 0
    )

    return render(request, "events/detail.html", {
        "event": event,
        "booked_tickets": booked_tickets,
        "available_tickets": available_tickets,
        "sold_percentage": sold_percentage,
    })


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "events/signup.html", {
        "form": form
    })


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "events/login.html", {
        "form": form
    })


def user_logout(request):
    logout(request)
    return redirect("home")


@login_required
@require_POST
def book_event(request, event_id):
    try:
        tickets = int(request.POST.get("tickets", 1))
    except (TypeError, ValueError):
        messages.error(request, "Please enter a valid ticket quantity.")
        return redirect("event_detail", event_id=event_id)

    if tickets < 1 or tickets > 10:
        messages.error(request, "You can book between 1 and 10 tickets.")
        return redirect("event_detail", event_id=event_id)

    booking = None

    with transaction.atomic():
        event = get_object_or_404(
            Event.objects.select_for_update(),
            id=event_id
        )

        booked_tickets = Booking.objects.filter(
            event=event,
            status="confirmed"
        ).aggregate(total=Sum("tickets"))["total"] or 0

        available_tickets = max(
            0, event.total_tickets - booked_tickets
        )

        if event.event_date <= timezone.now():
            messages.error(request, "This event has already started.")

        elif available_tickets == 0:
            messages.error(request, "Sorry, all tickets are sold out.")

        elif tickets > available_tickets:
            messages.error(
                request,
                f"Only {available_tickets} tickets are available."
            )

        else:
            booking = Booking.objects.create(
                user=request.user,
                event=event,
                tickets=tickets
            )

    if booking:
        messages.success(request, "Your booking was successful!")
        return redirect(
            "booking_confirmation",
            booking_id=booking.booking_id
        )

    return redirect("event_detail", event_id=event_id)


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related("event", "user"),
        booking_id=booking_id,
        user=request.user
    )

    total_amount = booking.event.price * booking.tickets

    return render(
        request,
        "events/booking_confirmation.html",
        {
            "booking": booking,
            "total_amount": total_amount,
        }
    )


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user
    ).select_related("event").order_by("-booked_at")

    for booking in bookings:
        booking.total_amount = (
            booking.event.price * booking.tickets
        )

    return render(
        request,
        "events/my_bookings.html",
        {
            "bookings": bookings,
            "now": timezone.now(),
        }
    )


@login_required
@require_POST
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related("event"),
        booking_id=booking_id,
        user=request.user
    )

    if booking.status == "cancelled":
        messages.error(request, "This booking is already cancelled.")

    elif booking.event.event_date <= timezone.now():
        messages.error(
            request,
            "This event has already started. Cancellation is not allowed."
        )

    else:
        booking.status = "cancelled"
        booking.save(update_fields=["status"])
        messages.success(
            request,
            "Your booking has been cancelled successfully!"
        )

    return redirect("my_bookings")
