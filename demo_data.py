from database import (
    supabase,
    create_booking,
    add_booking_service
)


def seed_demo_data():

    # ==================================================
    # CHECK WHETHER DEMO DATA ALREADY EXISTS
    # ==================================================

    existing_providers = (
        supabase
        .table("service_providers")
        .select("id")
        .limit(1)
        .execute()
    )

    if existing_providers.data:
        return


    # ==================================================
    # PROVIDERS
    # ==================================================

    providers = [
        {
            "provider_name": "ABC Mountain Hotel",
            "provider_type": "Hotel",
            "contact_person": "Arun Kumar",
            "phone": "9000000001",
            "location": "Hill View",
            "notes": "Premium hotel accommodation"
        },
        {
            "provider_name": "Green Valley Resort",
            "provider_type": "Hotel",
            "contact_person": "Priya Nair",
            "phone": "9000000002",
            "location": "Green Valley",
            "notes": "Resort accommodation"
        },
        {
            "provider_name": "ABC Food Services",
            "provider_type": "Food",
            "contact_person": "Ravi",
            "phone": "9000000003",
            "location": "Town Center",
            "notes": "Breakfast, lunch and dinner packages"
        },
        {
            "provider_name": "Blue Lake Boat Services",
            "provider_type": "Boat",
            "contact_person": "Suresh",
            "phone": "9000000004",
            "location": "Lake Area",
            "notes": "Boat and cruise services"
        },
        {
            "provider_name": "Mountain Adventures",
            "provider_type": "Trekking",
            "contact_person": "Anil",
            "phone": "9000000005",
            "location": "Mountain Base",
            "notes": "Guided hiking and trekking"
        }
    ]

    provider_ids = {}

    for provider in providers:

        response = (
            supabase
            .table("service_providers")
            .insert(provider)
            .execute()
        )

        provider_ids[
            provider["provider_name"]
        ] = response.data[0]["id"]


    # ==================================================
    # PROVIDER SERVICES
    # ==================================================

    services = [
        {
            "provider_id": provider_ids["ABC Mountain Hotel"],
            "service_name": "Deluxe Room",
            "service_description": "Comfortable room for two adults",
            "price": 4500,
            "price_unit": "Per Night",
            "capacity": 2
        },
        {
            "provider_id": provider_ids["ABC Mountain Hotel"],
            "service_name": "Family Room",
            "service_description": "Large room suitable for families",
            "price": 7500,
            "price_unit": "Per Night",
            "capacity": 4
        },
        {
            "provider_id": provider_ids["ABC Mountain Hotel"],
            "service_name": "Private Cottage",
            "service_description": "Independent cottage for large families",
            "price": 12000,
            "price_unit": "Per Night",
            "capacity": 6
        },
        {
            "provider_id": provider_ids["Green Valley Resort"],
            "service_name": "Garden Room",
            "service_description": "Room with garden view",
            "price": 5000,
            "price_unit": "Per Night",
            "capacity": 2
        },
        {
            "provider_id": provider_ids["Green Valley Resort"],
            "service_name": "Family Suite",
            "service_description": "Large suite for families",
            "price": 9000,
            "price_unit": "Per Night",
            "capacity": 5
        },
        {
            "provider_id": provider_ids["ABC Food Services"],
            "service_name": "Breakfast Package",
            "service_description": "Morning breakfast package",
            "price": 350,
            "price_unit": "Per Person",
            "capacity": None
        },
        {
            "provider_id": provider_ids["ABC Food Services"],
            "service_name": "Lunch Package",
            "service_description": "Complete lunch package",
            "price": 500,
            "price_unit": "Per Person",
            "capacity": None
        },
        {
            "provider_id": provider_ids["ABC Food Services"],
            "service_name": "Dinner Package",
            "service_description": "Complete dinner package",
            "price": 600,
            "price_unit": "Per Person",
            "capacity": None
        },
        {
            "provider_id": provider_ids["ABC Food Services"],
            "service_name": "Full Board",
            "service_description": "Breakfast, lunch and dinner",
            "price": 1350,
            "price_unit": "Per Person / Day",
            "capacity": None
        },
        {
            "provider_id": provider_ids["Blue Lake Boat Services"],
            "service_name": "Standard Boat Ride",
            "service_description": "One hour lake ride",
            "price": 3000,
            "price_unit": "Per Boat",
            "capacity": 8
        },
        {
            "provider_id": provider_ids["Blue Lake Boat Services"],
            "service_name": "Sunset Cruise",
            "service_description": "Two hour sunset cruise",
            "price": 6500,
            "price_unit": "Per Boat",
            "capacity": 12
        },
        {
            "provider_id": provider_ids["Mountain Adventures"],
            "service_name": "Sunrise Trek",
            "service_description": "Easy three hour guided trek",
            "price": 1200,
            "price_unit": "Per Person",
            "capacity": 15
        },
        {
            "provider_id": provider_ids["Mountain Adventures"],
            "service_name": "Valley Trek",
            "service_description": "Moderate six hour guided trek",
            "price": 2000,
            "price_unit": "Per Person",
            "capacity": 12
        }
    ]

    service_ids = {}

    for service in services:

        response = (
            supabase
            .table("provider_services")
            .insert(service)
            .execute()
        )

        service_ids[
            (
                service["provider_id"],
                service["service_name"]
            )
        ] = response.data[0]["id"]


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
        {
            "provider_service_id": breakfast_id,
            "item_name": "Bread",
            "category": "Main"
        },
        {
            "provider_service_id": breakfast_id,
            "item_name": "Butter",
            "category": "Side"
        },
        {
            "provider_service_id": breakfast_id,
            "item_name": "Jam",
            "category": "Side"
        },
        {
            "provider_service_id": breakfast_id,
            "item_name": "Omelette",
            "category": "Main"
        },
        {
            "provider_service_id": breakfast_id,
            "item_name": "Tea",
            "category": "Drink"
        },
        {
            "provider_service_id": breakfast_id,
            "item_name": "Coffee",
            "category": "Drink"
        },
        {
            "provider_service_id": breakfast_id,
            "item_name": "Fresh Fruit",
            "category": "Fruit"
        },

        {
            "provider_service_id": lunch_id,
            "item_name": "Rice",
            "category": "Main"
        },
        {
            "provider_service_id": lunch_id,
            "item_name": "Vegetable Curry",
            "category": "Main"
        },
        {
            "provider_service_id": lunch_id,
            "item_name": "Chicken Curry",
            "category": "Main"
        },
        {
            "provider_service_id": lunch_id,
            "item_name": "Salad",
            "category": "Side"
        },
        {
            "provider_service_id": lunch_id,
            "item_name": "Dessert",
            "category": "Dessert"
        },

        {
            "provider_service_id": dinner_id,
            "item_name": "Soup",
            "category": "Starter"
        },
        {
            "provider_service_id": dinner_id,
            "item_name": "Rice",
            "category": "Main"
        },
        {
            "provider_service_id": dinner_id,
            "item_name": "Bread",
            "category": "Main"
        },
        {
            "provider_service_id": dinner_id,
            "item_name": "Vegetable Curry",
            "category": "Main"
        },
        {
            "provider_service_id": dinner_id,
            "item_name": "Chicken Curry",
            "category": "Main"
        },
        {
            "provider_service_id": dinner_id,
            "item_name": "Dessert",
            "category": "Dessert"
        }
    ]

    (
        supabase
        .table("food_menu_items")
        .insert(menu_items)
        .execute()
    )


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
