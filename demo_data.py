from database import (
    get_connection,
    create_booking,
    add_booking_service
)


def seed_demo_data():

    conn = get_connection()
    cursor = conn.cursor()

    # Don't create demo data again if it already exists
    cursor.execute("SELECT COUNT(*) AS count FROM providers")

    if cursor.fetchone()["count"] > 0:
        conn.close()
        return

    # ==================================================
    # PROVIDERS
    # ==================================================

    providers = [
        (
            "ABC Mountain Hotel",
            "Hotel",
            "Arun Kumar",
            "9000000001",
            "Hill View",
            "Premium hotel accommodation"
        ),
        (
            "Green Valley Resort",
            "Hotel",
            "Priya Nair",
            "9000000002",
            "Green Valley",
            "Resort accommodation"
        ),
        (
            "ABC Food Services",
            "Food",
            "Ravi",
            "9000000003",
            "Town Center",
            "Breakfast, lunch and dinner packages"
        ),
        (
            "Blue Lake Boat Services",
            "Boat",
            "Suresh",
            "9000000004",
            "Lake Area",
            "Boat and cruise services"
        ),
        (
            "Mountain Adventures",
            "Trekking",
            "Anil",
            "9000000005",
            "Mountain Base",
            "Guided hiking and trekking"
        )
    ]

    provider_ids = {}

    for provider in providers:

        cursor.execute("""
            INSERT INTO providers (
                provider_name,
                provider_type,
                contact_person,
                phone,
                location,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, provider)

        provider_ids[provider[0]] = cursor.lastrowid

    conn.commit()

    # ==================================================
    # PROVIDER SERVICES
    # ==================================================

    services = [
        (
            provider_ids["ABC Mountain Hotel"],
            "Deluxe Room",
            "Comfortable room for two adults",
            4500,
            "Per Night",
            2
        ),
        (
            provider_ids["ABC Mountain Hotel"],
            "Family Room",
            "Large room suitable for families",
            7500,
            "Per Night",
            4
        ),
        (
            provider_ids["ABC Mountain Hotel"],
            "Private Cottage",
            "Independent cottage for large families",
            12000,
            "Per Night",
            6
        ),
        (
            provider_ids["Green Valley Resort"],
            "Garden Room",
            "Room with garden view",
            5000,
            "Per Night",
            2
        ),
        (
            provider_ids["Green Valley Resort"],
            "Family Suite",
            "Large suite for families",
            9000,
            "Per Night",
            5
        ),
        (
            provider_ids["ABC Food Services"],
            "Breakfast Package",
            "Morning breakfast package",
            350,
            "Per Person",
            None
        ),
        (
            provider_ids["ABC Food Services"],
            "Lunch Package",
            "Complete lunch package",
            500,
            "Per Person",
            None
        ),
        (
            provider_ids["ABC Food Services"],
            "Dinner Package",
            "Complete dinner package",
            600,
            "Per Person",
            None
        ),
        (
            provider_ids["ABC Food Services"],
            "Full Board",
            "Breakfast, lunch and dinner",
            1350,
            "Per Person / Day",
            None
        ),
        (
            provider_ids["Blue Lake Boat Services"],
            "Standard Boat Ride",
            "One hour lake ride",
            3000,
            "Per Boat",
            8
        ),
        (
            provider_ids["Blue Lake Boat Services"],
            "Sunset Cruise",
            "Two hour sunset cruise",
            6500,
            "Per Boat",
            12
        ),
        (
            provider_ids["Mountain Adventures"],
            "Sunrise Trek",
            "Easy three hour guided trek",
            1200,
            "Per Person",
            15
        ),
        (
            provider_ids["Mountain Adventures"],
            "Valley Trek",
            "Moderate six hour guided trek",
            2000,
            "Per Person",
            12
        )
    ]

    service_ids = {}

    for service in services:

        cursor.execute("""
            INSERT INTO provider_services (
                provider_id,
                service_name,
                service_description,
                price,
                price_unit,
                capacity
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, service)

        service_ids[
            (service[0], service[1])
        ] = cursor.lastrowid

    conn.commit()

    # ==================================================
    # FOOD MENU ITEMS
    # ==================================================

    breakfast_id = service_ids[
        (
            provider_ids["ABC Food Services"],
            "Breakfast Package"
        )
    ]

    lunch_id = service_ids[
        (
            provider_ids["ABC Food Services"],
            "Lunch Package"
        )
    ]

    dinner_id = service_ids[
        (
            provider_ids["ABC Food Services"],
            "Dinner Package"
        )
    ]

    menu_items = [
        (breakfast_id, "Bread", "Main"),
        (breakfast_id, "Butter", "Side"),
        (breakfast_id, "Jam", "Side"),
        (breakfast_id, "Omelette", "Main"),
        (breakfast_id, "Tea", "Drink"),
        (breakfast_id, "Coffee", "Drink"),
        (breakfast_id, "Fresh Fruit", "Fruit"),

        (lunch_id, "Rice", "Main"),
        (lunch_id, "Vegetable Curry", "Main"),
        (lunch_id, "Chicken Curry", "Main"),
        (lunch_id, "Salad", "Side"),
        (lunch_id, "Dessert", "Dessert"),

        (dinner_id, "Soup", "Starter"),
        (dinner_id, "Rice", "Main"),
        (dinner_id, "Bread", "Main"),
        (dinner_id, "Vegetable Curry", "Main"),
        (dinner_id, "Chicken Curry", "Main"),
        (dinner_id, "Dessert", "Dessert")
    ]

    cursor.executemany("""
        INSERT INTO service_menu_items (
            provider_service_id,
            item_name,
            category
        )
        VALUES (?, ?, ?)
    """, menu_items)

    conn.commit()
    conn.close()

    # ==================================================
    # DEMO BOOKINGS
    # ==================================================

    booking_1 = create_booking({
        "customer_name": "John Smith Family",
        "mobile_number": "9876543210",
        "email": "john@example.com",

        "total_travelers": 4,
        "adults": 2,
        "children": 2,

        "coming_from": "Chennai",
        "pickup_location": "Kochi",
        "destination": "Munnar",

        "arrival_date": "2026-09-15",
        "departure_date": "2026-09-19",

        "status": "Confirmed",

        "notes": "Vegetarian option required for children."
    })

    booking_2 = create_booking({
        "customer_name": "Mary Johnson Group",
        "mobile_number": "9876543211",
        "email": "mary@example.com",

        "total_travelers": 6,
        "adults": 5,
        "children": 1,

        "coming_from": "Bangalore",
        "pickup_location": "Kochi",
        "destination": "Munnar",

        "arrival_date": "2026-09-18",
        "departure_date": "2026-09-22",

        "status": "Confirmed",

        "notes": "One guest requires a separate room."
    })

    # ==================================================
    # BOOKING 1 SERVICES
    # ==================================================

    add_booking_service(
        booking_1,
        provider_ids["ABC Mountain Hotel"],
        service_ids[
            (
                provider_ids["ABC Mountain Hotel"],
                "Family Room"
            )
        ],
        "2026-09-15",
        "2026-09-17",
        1,
        7500,
        "Confirmed",
        "Two-night stay"
    )

    add_booking_service(
        booking_1,
        provider_ids["ABC Food Services"],
        service_ids[
            (
                provider_ids["ABC Food Services"],
                "Breakfast Package"
            )
        ],
        "2026-09-16",
        "2026-09-19",
        4,
        350,
        "Confirmed",
        "Breakfast for all travelers"
    )

    add_booking_service(
        booking_1,
        provider_ids["Blue Lake Boat Services"],
        service_ids[
            (
                provider_ids["Blue Lake Boat Services"],
                "Standard Boat Ride"
            )
        ],
        "2026-09-17",
        None,
        4,
        3000,
        "Confirmed",
        "Morning boat ride"
    )

    add_booking_service(
        booking_1,
        provider_ids["Mountain Adventures"],
        service_ids[
            (
                provider_ids["Mountain Adventures"],
                "Sunrise Trek"
            )
        ],
        "2026-09-18",
        None,
        4,
        1200,
        "Confirmed",
        "Sunrise guided trek"
    )

    # ==================================================
    # BOOKING 2 SERVICES
    # ==================================================

    add_booking_service(
        booking_2,
        provider_ids["Green Valley Resort"],
        service_ids[
            (
                provider_ids["Green Valley Resort"],
                "Family Suite"
            )
        ],
        "2026-09-18",
        "2026-09-22",
        2,
        9000,
        "Confirmed",
        "Two suites"
    )

    add_booking_service(
        booking_2,
        provider_ids["ABC Food Services"],
        service_ids[
            (
                provider_ids["ABC Food Services"],
                "Full Board"
            )
        ],
        "2026-09-18",
        "2026-09-22",
        6,
        1350,
        "Confirmed",
        "All meals included"
    )

    add_booking_service(
        booking_2,
        provider_ids["Blue Lake Boat Services"],
        service_ids[
            (
                provider_ids["Blue Lake Boat Services"],
                "Sunset Cruise"
            )
        ],
        "2026-09-20",
        None,
        6,
        6500,
        "Confirmed",
        "Evening sunset cruise"
    )