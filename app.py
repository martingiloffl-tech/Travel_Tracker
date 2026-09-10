import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Travel Tracker",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# MOBILE-FRIENDLY STYLING
# --------------------------------------------------
st.markdown("""
<style>
    .block-container {
        max-width: 600px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    div.stButton > button {
        width: 100%;
        min-height: 55px;
        font-size: 18px;
        border-radius: 12px;
    }

    h1 {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DATA FILE
# --------------------------------------------------
DATA_FILE = Path("trips.csv")


def load_trips():
    if DATA_FILE.exists():
        return pd.read_csv(DATA_FILE)

    return pd.DataFrame(
        columns=[
            "Traveler",
            "From",
            "Destination",
            "Start Date",
            "End Date",
            "Status"
        ]
    )


def save_trips(df):
    df.to_csv(DATA_FILE, index=False)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"


def go_to(page):
    st.session_state.page = page


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------
if st.session_state.page == "Home":

    st.title("✈️ Travel Tracker")

    st.write("### Welcome")

    st.button(
        "➕ Register New Trip",
        on_click=go_to,
        args=("Register",)
    )

    st.button(
        "📋 View Trips",
        on_click=go_to,
        args=("Trips",)
    )


# --------------------------------------------------
# REGISTER TRIP
# --------------------------------------------------
elif st.session_state.page == "Register":

    st.title("➕ Register Trip")

    traveler = st.text_input("Traveler Name")
    from_location = st.text_input("Travel From")
    destination = st.text_input("Destination")

    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    status = st.selectbox(
        "Status",
        ["Upcoming", "Active", "Completed"]
    )

    if st.button("💾 Save Trip"):

        if traveler and from_location and destination:

            trips = load_trips()

            new_trip = pd.DataFrame([{
                "Traveler": traveler,
                "From": from_location,
                "Destination": destination,
                "Start Date": start_date,
                "End Date": end_date,
                "Status": status
            }])

            trips = pd.concat(
                [trips, new_trip],
                ignore_index=True
            )

            save_trips(trips)

            st.success("Trip registered successfully! 🎉")

        else:
            st.warning("Please complete all required fields.")

    st.button(
        "⬅️ Back to Home",
        on_click=go_to,
        args=("Home",)
    )


# --------------------------------------------------
# VIEW TRIPS
# --------------------------------------------------
elif st.session_state.page == "Trips":

    st.title("📋 Registered Trips")

    trips = load_trips()

    if trips.empty:
        st.info("No trips registered yet.")

    else:
        for index, trip in trips.iterrows():

            with st.container(border=True):

                st.subheader(f"✈️ {trip['Destination']}")

                st.write(f"👤 **Traveler:** {trip['Traveler']}")
                st.write(f"📍 **From:** {trip['From']}")
                st.write(
                    f"📅 **Dates:** "
                    f"{trip['Start Date']} → {trip['End Date']}"
                )
                st.write(f"🔵 **Status:** {trip['Status']}")

    st.button(
        "⬅️ Back to Home",
        on_click=go_to,
        args=("Home",)
    )