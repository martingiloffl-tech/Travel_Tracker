import streamlit as st
from datetime import date

from database import (
    initialize_database,
    create_booking,
    get_all_bookings,
    get_booking,
    get_all_providers,
    get_provider,
    get_provider_services,
    get_service_menu_items,
    get_booking_services,
    get_provider_bookings,
    get_operations_by_date,
    get_dashboard_stats
)

from demo_data import seed_demo_data


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="SattVa",
    page_icon="assets/kerala_logo.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ==================================================
# MOBILE + DESKTOP RESPONSIVE STYLE
# ==================================================

st.markdown("""
<style>

/* ==================================================
   MAIN PAGE
================================================== */

.block-container {
    max-width: 700px;
    padding-top: 1rem;
    padding-bottom: 4rem;
    padding-left: 1rem;
    padding-right: 1rem;
}


/* ==================================================
   BUTTONS
================================================== */

div.stButton > button {
    width: 100%;
    min-height: 48px;
    font-size: 15px;
    border-radius: 10px;
    margin-bottom: 6px;
}

div[data-testid="stFormSubmitButton"] button {
    width: 100%;
    min-height: 52px;
    font-size: 16px;
    border-radius: 10px;
}


/* ==================================================
   NAVIGATION
================================================== */

div[data-testid="stRadio"] {
    margin-top: 0px;
    margin-bottom: 12px;
}


/* Navigation container */

div[data-testid="stRadio"] div[role="radiogroup"] {
    display: flex !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    gap: 4px !important;
    width: 100% !important;
    justify-content: space-between !important;
}


/* Navigation items */

div[data-testid="stRadio"] div[role="radiogroup"] label {
    flex: 1 1 0 !important;
    min-width: 0 !important;
    white-space: nowrap !important;
    font-size: 13px !important;
}


/* ==================================================
   HIDE STREAMLIT RADIO BUTTONS
================================================== */

/* Hide actual radio input */

div[data-testid="stRadio"] input[type="radio"] {
    display: none !important;
}


/* Hide BaseWeb radio circle */

div[data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {
    display: none !important;
}


/* Remove space reserved for the radio control */

div[data-testid="stRadio"] label {
    gap: 0 !important;
}


/* Navigation text */

div[data-testid="stRadio"] label p {
    margin: 0 !important;
    white-space: nowrap !important;
}


/* ==================================================
   DESKTOP / TABLET
================================================== */

@media (min-width: 601px) {

    .block-container {
        max-width: 700px;
    }

}


/* ==================================================
   MOBILE
================================================== */

@media (max-width: 600px) {

    .block-container {
        padding-top: 0.7rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
        padding-bottom: 3rem;
    }

    h1 {
        font-size: 30px !important;
    }

    h2 {
        font-size: 25px !important;
    }

    h3 {
        font-size: 21px !important;
    }


    /* Navigation smaller on mobile */

    div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 2px !important;
        justify-content: space-between !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] label {
        font-size: 11px !important;
    }

    div[data-testid="stRadio"] label p {
        font-size: 11px !important;
        white-space: nowrap !important;
    }


    /* Booking / provider cards */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 10px;
    }


    /* Buttons */

    div.stButton > button {
        min-height: 44px;
        font-size: 14px;
    }

}

</style>
""", unsafe_allow_html=True)


# ==================================================
# DATABASE + DEMO DATA
# ==================================================

initialize_database()
seed_demo_data()


# ==================================================
# SESSION STATE
# ==================================================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "selected_booking_id" not in st.session_state:
    st.session_state.selected_booking_id = None

if "selected_provider_id" not in st.session_state:
    st.session_state.selected_provider_id = None


def navigate(page):
    st.session_state.page = page


# ==================================================
# HEADER NAVIGATION
# ==================================================

# --- APP HEADER ---

logo_col, title_col = st.columns([1, 6])

with logo_col:
    st.image(
        "assets/kerala_logo.png",
        width=45
    )

with title_col:
    st.markdown(
        """
        <div style="
            font-size: 32px;
            font-weight: 700;
            color: #262730;
            padding-top: 4px;
            white-space: nowrap;
        ">
            SattVa
        </div>
        """,
        unsafe_allow_html=True
    )


# --- NAVIGATION ---

nav = st.radio(
    "Navigation",
    [
        "🏠 Home",
        "📋 Bookings",
        "🏢 Services",
        "📅 Calendar"
    ],
    horizontal=True,
    label_visibility="collapsed"
)


# --- NAVIGATION MAPPING ---

nav_map = {
    "🏠 Home": "Dashboard",
    "📋 Bookings": "Bookings",
    "🏢 Services": "Providers",
    "📅 Calendar": "Calendar"
}


if nav_map[nav] != st.session_state.page:

    if st.session_state.page not in [
        "New Booking",
        "Booking Details",
        "Provider Details"
    ]:
        st.session_state.page = nav_map[nav]


# ==================================================
# DASHBOARD
# ==================================================

if st.session_state.page == "Dashboard":

    st.subheader("Operations Dashboard")

    stats = get_dashboard_stats()

    col1, col2, col3 = st.columns(3)

    col1.metric("Bookings", stats["total_bookings"])
    col2.metric("Confirmed", stats["confirmed"])
    col3.metric("Providers", stats["providers"])

    st.divider()

    st.subheader("Quick Actions")

    if st.button("➕ Create New Booking"):
        navigate("New Booking")
        st.rerun()

    if st.button("📋 View All Bookings"):
        navigate("Bookings")
        st.rerun()

    if st.button("🏢 Explore Service Providers"):
        navigate("Providers")
        st.rerun()

    if st.button("📅 View Daily Operations"):
        navigate("Calendar")
        st.rerun()


# ==================================================
# NEW BOOKING
# ==================================================

elif st.session_state.page == "New Booking":

    st.subheader("➕ New Booking")

    with st.form("booking_form"):

        st.markdown("### 👤 Customer")

        customer_name = st.text_input("Customer / Contact Name *")
        mobile_number = st.text_input("Mobile Number")
        email = st.text_input("Email")

        st.divider()

        st.markdown("### 👥 Travelers")

        col1, col2 = st.columns(2)

        with col1:
            adults = st.number_input(
                "Adults",
                min_value=0,
                value=1
            )

        with col2:
            children = st.number_input(
                "Children",
                min_value=0,
                value=0
            )

        total_travelers = adults + children

        st.info(f"Total Travelers: {total_travelers}")

        st.divider()

        st.markdown("### 📍 Travel")

        coming_from = st.text_input("Coming From")
        pickup_location = st.text_input("Tour Pickup / Start Location")
        destination = st.text_input("Destination *")

        col1, col2 = st.columns(2)

        with col1:
            arrival_date = st.date_input(
                "Arrival Date",
                value=date.today()
            )

        with col2:
            departure_date = st.date_input(
                "Departure Date",
                value=date.today()
            )

        st.divider()

        st.markdown("### 📌 Booking")

        status = st.selectbox(
            "Booking Status",
            [
                "Inquiry",
                "Tentative",
                "Confirmed",
                "Active",
                "Completed",
                "Cancelled"
            ]
        )

        notes = st.text_area(
            "Special Requirements / Notes"
        )

        submitted = st.form_submit_button(
            "💾 Create Booking"
        )

    if submitted:

        if not customer_name.strip():

            st.error("Please enter customer name.")

        elif not destination.strip():

            st.error("Please enter destination.")

        elif total_travelers <= 0:

            st.error("At least one traveler is required.")

        elif departure_date < arrival_date:

            st.error(
                "Departure date cannot be before arrival date."
            )

        else:

            create_booking({
                "customer_name": customer_name.strip(),
                "mobile_number": mobile_number.strip(),
                "email": email.strip(),

                "total_travelers": total_travelers,
                "adults": adults,
                "children": children,

                "coming_from": coming_from.strip(),
                "pickup_location": pickup_location.strip(),
                "destination": destination.strip(),

                "arrival_date": str(arrival_date),
                "departure_date": str(departure_date),

                "status": status,
                "notes": notes.strip()
            })

            st.success(
                "🎉 Booking created successfully!"
            )

    if st.button("⬅️ Back"):
        navigate("Dashboard")
        st.rerun()


# ==================================================
# BOOKINGS
# ==================================================

elif st.session_state.page == "Bookings":

    st.subheader("📋 All Bookings")

    bookings = get_all_bookings()

    if not bookings:

        st.info("No bookings available.")

    for booking in bookings:

        with st.container(border=True):

            st.markdown(
                f"### 👤 {booking['customer_name']}"
            )

            st.write(
                f"📍 {booking['coming_from']} → "
                f"{booking['destination']}"
            )

            st.write(
                f"👥 {booking['total_travelers']} Travelers"
            )

            st.write(
                f"📅 {booking['arrival_date']} → "
                f"{booking['departure_date']}"
            )

            st.write(
                f"📌 **{booking['status']}**"
            )

            if st.button(
                "View Booking",
                key=f"booking_{booking['id']}"
            ):

                st.session_state.selected_booking_id = (
                    booking["id"]
                )

                navigate("Booking Details")
                st.rerun()

    if st.button("➕ New Booking"):
        navigate("New Booking")
        st.rerun()


# ==================================================
# BOOKING DETAILS
# ==================================================

elif st.session_state.page == "Booking Details":

    booking = get_booking(
        st.session_state.selected_booking_id
    )

    if booking is None:

        st.error("Booking not found.")

    else:

        st.subheader(
            f"👤 {booking['customer_name']}"
        )

        st.write(
            f"📱 {booking['mobile_number'] or '-'}"
        )

        st.write(
            f"👥 {booking['total_travelers']} Travelers "
            f"({booking['adults']} Adults, "
            f"{booking['children']} Children)"
        )

        st.divider()

        st.markdown("### 📍 Travel")

        st.write(
            f"Coming From: "
            f"**{booking['coming_from'] or '-'}**"
        )

        st.write(
            f"Pickup: "
            f"**{booking['pickup_location'] or '-'}**"
        )

        st.write(
            f"Destination: "
            f"**{booking['destination']}**"
        )

        st.write(
            f"Dates: "
            f"**{booking['arrival_date']} → "
            f"{booking['departure_date']}**"
        )

        st.divider()

        st.markdown("### 🧩 Assigned Services")

        services = get_booking_services(
            booking["id"]
        )

        if not services:

            st.info(
                "No services assigned yet."
            )

        for service in services:

            with st.container(border=True):

                st.write(
                    f"**{service['provider_type']}**"
                )

                st.write(
                    f"🏢 {service['provider_name']}"
                )

                st.write(
                    f"📦 {service['service_name']}"
                )

                st.write(
                    f"📅 {service['service_date']}"
                    + (
                        f" → {service['end_date']}"
                        if service["end_date"]
                        else ""
                    )
                )

                st.write(
                    f"🔢 Quantity: "
                    f"{service['quantity'] or '-'}"
                )

                st.write(
                    f"💰 ₹{service['price'] or 0:,.0f}"
                )

        st.divider()

        st.markdown("### 📝 Notes")

        st.write(
            booking["notes"] or "-"
        )

    if st.button("⬅️ Back to Bookings"):
        navigate("Bookings")
        st.rerun()


# ==================================================
# PROVIDERS
# ==================================================

elif st.session_state.page == "Providers":

    st.subheader("🏢 Service Providers")

    providers = get_all_providers()

    provider_types = sorted(
        list({
            provider["provider_type"]
            for provider in providers
        })
    )

    selected_type = st.selectbox(
        "Filter Provider Type",
        ["All"] + provider_types
    )

    for provider in providers:

        if (
            selected_type != "All"
            and provider["provider_type"] != selected_type
        ):
            continue

        with st.container(border=True):

            st.markdown(
                f"### {provider['provider_name']}"
            )

            st.write(
                f"🏷️ {provider['provider_type']}"
            )

            st.write(
                f"📍 {provider['location'] or '-'}"
            )

            if st.button(
                "View Provider",
                key=f"provider_{provider['id']}"
            ):

                st.session_state.selected_provider_id = (
                    provider["id"]
                )

                navigate("Provider Details")
                st.rerun()


# ==================================================
# PROVIDER DETAILS
# ==================================================

elif st.session_state.page == "Provider Details":

    provider = get_provider(
        st.session_state.selected_provider_id
    )

    if provider is None:

        st.error("Provider not found.")

    else:

        st.subheader(
            f"🏢 {provider['provider_name']}"
        )

        st.write(
            f"🏷️ **{provider['provider_type']}**"
        )

        st.write(
            f"👤 Contact: "
            f"{provider['contact_person'] or '-'}"
        )

        st.write(
            f"📱 Phone: "
            f"{provider['phone'] or '-'}"
        )

        st.write(
            f"📍 Location: "
            f"{provider['location'] or '-'}"
        )

        st.divider()

        st.markdown("### 📦 Services Offered")

        services = get_provider_services(
            provider["id"]
        )

        for service in services:

            with st.container(border=True):

                st.write(
                    f"### {service['service_name']}"
                )

                st.write(
                    service[
                        "service_description"
                    ] or ""
                )

                if service["price"] is not None:

                    st.write(
                        f"💰 ₹{service['price']:,.0f} "
                        f"{service['price_unit'] or ''}"
                    )

                if service["capacity"]:

                    st.write(
                        f"👥 Capacity: "
                        f"{service['capacity']}"
                    )

                menu_items = get_service_menu_items(
                    service["id"]
                )

                if menu_items:

                    st.write("🍽️ Includes:")

                    for item in menu_items:

                        st.write(
                            f"• {item['item_name']} "
                            f"({item['category']})"
                        )

        st.divider()

        st.markdown(
            "### 👥 Customers / Bookings"
        )

        bookings = get_provider_bookings(
            provider["id"]
        )

        if not bookings:

            st.info(
                "No customers assigned yet."
            )

        for booking in bookings:

            with st.container(border=True):

                st.write(
                    f"👤 **{booking['customer_name']}**"
                )

                st.write(
                    f"📦 {booking['service_name']}"
                )

                st.write(
                    f"👥 {booking['total_travelers']} "
                    f"Travelers"
                )

                st.write(
                    f"📅 {booking['service_date']}"
                    + (
                        f" → {booking['end_date']}"
                        if booking["end_date"]
                        else ""
                    )
                )

    if st.button("⬅️ Back to Providers"):
        navigate("Providers")
        st.rerun()


# ==================================================
# CALENDAR
# ==================================================

elif st.session_state.page == "Calendar":

    st.subheader("📅 Daily Operations")

    selected_date = st.date_input(
        "Select Date",
        value=date.today()
    )

    selected_date_text = str(selected_date)

    operations = get_operations_by_date(
        selected_date_text
    )

    if not operations:

        st.info(
            "No operations scheduled for this date."
        )

    else:

        st.caption(
            f"{len(operations)} operations scheduled"
        )

        for operation in operations:

            with st.container(border=True):

                st.markdown(
                    f"### 👤 "
                    f"{operation['customer_name']}"
                )

                st.write(
                    f"🏢 "
                    f"{operation['provider_name']}"
                )

                st.write(
                    f"🏷️ "
                    f"{operation['provider_type']}"
                )

                st.write(
                    f"📦 "
                    f"{operation['service_name']}"
                )

                st.write(
                    f"👥 "
                    f"{operation['total_travelers']} "
                    f"Travelers"
                )

                if operation["notes"]:

                    st.caption(
                        operation["notes"]
                    )
