import sqlite3
from pathlib import Path


DB_FILE = Path("travel_tracker.db")


def get_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # ==================================================
    # BOOKINGS
    # ==================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            customer_name TEXT NOT NULL,
            mobile_number TEXT,
            email TEXT,

            total_travelers INTEGER NOT NULL,
            adults INTEGER NOT NULL,
            children INTEGER NOT NULL,

            coming_from TEXT,
            pickup_location TEXT,
            destination TEXT NOT NULL,

            arrival_date TEXT NOT NULL,
            departure_date TEXT NOT NULL,

            status TEXT NOT NULL,
            notes TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ==================================================
    # SERVICE PROVIDERS
    # ==================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            provider_name TEXT NOT NULL,
            provider_type TEXT NOT NULL,

            contact_person TEXT,
            phone TEXT,
            location TEXT,
            notes TEXT
        )
    """)

    # ==================================================
    # PROVIDER SERVICES
    # ==================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS provider_services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            provider_id INTEGER NOT NULL,

            service_name TEXT NOT NULL,
            service_description TEXT,

            price REAL,
            price_unit TEXT,

            capacity INTEGER,

            FOREIGN KEY (provider_id)
                REFERENCES providers(id)
        )
    """)

    # ==================================================
    # FOOD MENU ITEMS
    # ==================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS service_menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            provider_service_id INTEGER NOT NULL,

            item_name TEXT NOT NULL,
            category TEXT,

            FOREIGN KEY (provider_service_id)
                REFERENCES provider_services(id)
        )
    """)

    # ==================================================
    # BOOKING SERVICE MAPPING
    # ==================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS booking_services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            booking_id INTEGER NOT NULL,
            provider_id INTEGER NOT NULL,
            provider_service_id INTEGER,

            service_date TEXT NOT NULL,
            end_date TEXT,

            quantity INTEGER,
            price REAL,

            status TEXT DEFAULT 'Planned',
            notes TEXT,

            FOREIGN KEY (booking_id)
                REFERENCES bookings(id),

            FOREIGN KEY (provider_id)
                REFERENCES providers(id),

            FOREIGN KEY (provider_service_id)
                REFERENCES provider_services(id)
        )
    """)

    conn.commit()
    conn.close()


# ==================================================
# BOOKING FUNCTIONS
# ==================================================

def create_booking(data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO bookings (
            customer_name,
            mobile_number,
            email,
            total_travelers,
            adults,
            children,
            coming_from,
            pickup_location,
            destination,
            arrival_date,
            departure_date,
            status,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["customer_name"],
        data.get("mobile_number", ""),
        data.get("email", ""),

        data["total_travelers"],
        data["adults"],
        data["children"],

        data.get("coming_from", ""),
        data.get("pickup_location", ""),
        data["destination"],

        data["arrival_date"],
        data["departure_date"],

        data["status"],
        data.get("notes", "")
    ))

    booking_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return booking_id


def get_all_bookings():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM bookings
        ORDER BY arrival_date ASC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_booking(booking_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM bookings
        WHERE id = ?
    """, (booking_id,))

    row = cursor.fetchone()

    conn.close()

    return row


# ==================================================
# PROVIDER FUNCTIONS
# ==================================================

def get_all_providers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM providers
        ORDER BY provider_type, provider_name
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_provider(provider_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM providers
        WHERE id = ?
    """, (provider_id,))

    row = cursor.fetchone()

    conn.close()

    return row


def get_provider_services(provider_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM provider_services
        WHERE provider_id = ?
        ORDER BY service_name
    """, (provider_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_service_menu_items(service_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM service_menu_items
        WHERE provider_service_id = ?
        ORDER BY category, item_name
    """, (service_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


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

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO booking_services (
            booking_id,
            provider_id,
            provider_service_id,
            service_date,
            end_date,
            quantity,
            price,
            status,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        booking_id,
        provider_id,
        provider_service_id,
        service_date,
        end_date,
        quantity,
        price,
        status,
        notes
    ))

    conn.commit()
    conn.close()


def get_booking_services(booking_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            bs.*,
            p.provider_name,
            p.provider_type,
            ps.service_name,
            ps.service_description,
            ps.price_unit
        FROM booking_services bs

        JOIN providers p
            ON bs.provider_id = p.id

        LEFT JOIN provider_services ps
            ON bs.provider_service_id = ps.id

        WHERE bs.booking_id = ?

        ORDER BY bs.service_date ASC
    """, (booking_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_provider_bookings(provider_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            bs.*,
            b.customer_name,
            b.total_travelers,
            b.destination,
            ps.service_name
        FROM booking_services bs

        JOIN bookings b
            ON bs.booking_id = b.id

        LEFT JOIN provider_services ps
            ON bs.provider_service_id = ps.id

        WHERE bs.provider_id = ?

        ORDER BY bs.service_date ASC
    """, (provider_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==================================================
# CALENDAR FUNCTIONS
# ==================================================

def get_operations_by_date(selected_date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            bs.*,
            b.customer_name,
            b.total_travelers,
            b.destination,

            p.provider_name,
            p.provider_type,

            ps.service_name

        FROM booking_services bs

        JOIN bookings b
            ON bs.booking_id = b.id

        JOIN providers p
            ON bs.provider_id = p.id

        LEFT JOIN provider_services ps
            ON bs.provider_service_id = ps.id

        WHERE
            bs.service_date <= ?
            AND (
                bs.end_date IS NULL
                OR bs.end_date >= ?
            )

        ORDER BY p.provider_type, b.customer_name
    """, (selected_date, selected_date))

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_dashboard_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) AS count FROM bookings"
    )

    total_bookings = cursor.fetchone()["count"]

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM bookings
        WHERE status = 'Confirmed'
        """
    )

    confirmed = cursor.fetchone()["count"]

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM providers
        """
    )

    providers = cursor.fetchone()["count"]

    conn.close()

    return {
        "total_bookings": total_bookings,
        "confirmed": confirmed,
        "providers": providers
    }