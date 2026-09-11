import streamlit as st
from supabase import create_client


# ==================================================
# SUPABASE CONNECTION
# ==================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ==================================================
# DATABASE INITIALIZATION
# ==================================================

def initialize_database():
    """
    Tables are already created in Supabase.
    This function is kept so existing app.py calls
    continue to work.
    """
    return


# ==================================================
# BOOKING FUNCTIONS
# ==================================================

def create_booking(data):

    payload = {
        "customer_name": data["customer_name"],
        "mobile_number": data.get("mobile_number", ""),
        "email": data.get("email", ""),

        "total_travelers": data["total_travelers"],
        "adults": data["adults"],
        "children": data["children"],

        "coming_from": data.get("coming_from", ""),
        "pickup_location": data.get("pickup_location", ""),
        "destination": data["destination"],

        "arrival_date": str(data["arrival_date"]),
        "departure_date": str(data["departure_date"]),

        "status": data["status"],
        "notes": data.get("notes", "")
    }

    response = (
        supabase
        .table("bookings")
        .insert(payload)
        .execute()
    )

    return response.data[0]["id"]


def get_all_bookings():

    response = (
        supabase
        .table("bookings")
        .select("*")
        .order("arrival_date")
        .execute()
    )

    return response.data


def get_booking(booking_id):

    response = (
        supabase
        .table("bookings")
        .select("*")
        .eq("id", booking_id)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


# ==================================================
# PROVIDER FUNCTIONS
# ==================================================

def get_all_providers():

    response = (
        supabase
        .table("service_providers")
        .select("*")
        .order("provider_type")
        .order("provider_name")
        .execute()
    )

    return response.data


def get_provider(provider_id):

    response = (
        supabase
        .table("service_providers")
        .select("*")
        .eq("id", provider_id)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


def get_provider_services(provider_id):

    response = (
        supabase
        .table("provider_services")
        .select("*")
        .eq("provider_id", provider_id)
        .order("service_name")
        .execute()
    )

    return response.data


def get_service_menu_items(service_id):

    response = (
        supabase
        .table("food_menu_items")
        .select("*")
        .eq("provider_service_id", service_id)
        .order("category")
        .order("item_name")
        .execute()
    )

    return response.data


# ==================================================
# BOOKING ↔ SERVICE FUNCTIONS
# ==================================================

def add_booking_service(
    booking_id,
    provider_id,
    provider_service_id,
    service_date,
    end_date,
    quantity,
    price,
    status="Planned",
    notes=""
):

    payload = {
        "booking_id": booking_id,
        "provider_id": provider_id,
        "provider_service_id": provider_service_id,

        "service_date": str(service_date),
        "end_date": str(end_date) if end_date else None,

        "quantity": quantity,
        "price": price,

        "status": status,
        "notes": notes
    }

    response = (
        supabase
        .table("booking_services")
        .insert(payload)
        .execute()
    )

    return response.data


def get_booking_services(booking_id):

    response = (
        supabase
        .table("booking_services")
        .select("""
            *,
            service_providers (
                provider_name,
                provider_type
            ),
            provider_services (
                service_name,
                service_description,
                price_unit
            )
        """)
        .eq("booking_id", booking_id)
        .order("service_date")
        .execute()
    )

    rows = []

    for row in response.data:

        provider = row.pop("service_providers", None) or {}
        service = row.pop("provider_services", None) or {}

        row["provider_name"] = provider.get("provider_name")
        row["provider_type"] = provider.get("provider_type")

        row["service_name"] = service.get("service_name")
        row["service_description"] = service.get(
            "service_description"
        )
        row["price_unit"] = service.get("price_unit")

        rows.append(row)

    return rows


def get_provider_bookings(provider_id):

    response = (
        supabase
        .table("booking_services")
        .select("""
            *,
            bookings (
                customer_name,
                total_travelers,
                destination
            ),
            provider_services (
                service_name
            )
        """)
        .eq("provider_id", provider_id)
        .order("service_date")
        .execute()
    )

    rows = []

    for row in response.data:

        booking = row.pop("bookings", None) or {}
        service = row.pop("provider_services", None) or {}

        row["customer_name"] = booking.get("customer_name")
        row["total_travelers"] = booking.get("total_travelers")
        row["destination"] = booking.get("destination")

        row["service_name"] = service.get("service_name")

        rows.append(row)

    return rows


# ==================================================
# CALENDAR FUNCTIONS
# ==================================================

def get_operations_by_date(selected_date):

    selected_date = str(selected_date)

    response = (
        supabase
        .table("booking_services")
        .select("""
            *,
            bookings (
                customer_name,
                total_travelers,
                destination
            ),
            service_providers (
                provider_name,
                provider_type
            ),
            provider_services (
                service_name
            )
        """)
        .lte("service_date", selected_date)
        .or_(
            f"end_date.is.null,end_date.gte.{selected_date}"
        )
        .execute()
    )

    rows = []

    for row in response.data:

        booking = row.pop("bookings", None) or {}
        provider = row.pop("service_providers", None) or {}
        service = row.pop("provider_services", None) or {}

        row["customer_name"] = booking.get("customer_name")
        row["total_travelers"] = booking.get("total_travelers")
        row["destination"] = booking.get("destination")

        row["provider_name"] = provider.get("provider_name")
        row["provider_type"] = provider.get("provider_type")

        row["service_name"] = service.get("service_name")

        rows.append(row)

    rows.sort(
        key=lambda x: (
            x.get("provider_type") or "",
            x.get("customer_name") or ""
        )
    )

    return rows


# ==================================================
# DASHBOARD FUNCTIONS
# ==================================================

def get_dashboard_stats():

    bookings_response = (
        supabase
        .table("bookings")
        .select("id", count="exact")
        .execute()
    )

    confirmed_response = (
        supabase
        .table("bookings")
        .select(
            "id",
            count="exact"
        )
        .eq("status", "Confirmed")
        .execute()
    )

    providers_response = (
        supabase
        .table("service_providers")
        .select(
            "id",
            count="exact"
        )
        .execute()
    )

    return {
        "total_bookings": bookings_response.count or 0,
        "confirmed": confirmed_response.count or 0,
        "providers": providers_response.count or 0
    }
