"""
Demo content for `python manage.py seed_demo`.

Northstar Property Care is fictional. All names, emails (example.com) and phone
numbers (Ofcom drama range 07700 900xxx) are invented for this portfolio demo.
"""

from datetime import date

SERVICES = [
    {
        "slug": "home-renovations",
        "title": "Home renovations",
        "display_order": 1,
        "image": "service-renovations",
        "image_alt": "Bright living room with pale oak floors and tall sash windows",
        "short_description": "Whole-house and single-room renovations, planned around how you actually live.",
        "description": (
            "Whether it's one tired room or a whole house that needs bringing up to date, "
            "we start by understanding how you use your home day to day. From there we plan "
            "layouts, specify finishes and coordinate every trade, from plastering and "
            "electrics to joinery and decorating.\n\n"
            "You'll have one project lead from the first visit to handover, an itemised "
            "quote before anything starts, and a programme that tells you which rooms are "
            "out of use and for how long."
        ),
    },
    {
        "slug": "kitchens-bathrooms",
        "title": "Kitchens & bathrooms",
        "display_order": 2,
        "image": "service-kitchens",
        "image_alt": "Modern kitchen with oak cabinets and a white stone worktop",
        "short_description": "Design, fitting and finishing in the rooms that work hardest.",
        "description": (
            "From a single bathroom refit to a full kitchen with a new layout, we handle the "
            "design, plumbing, electrics, tiling and joinery under one project lead.\n\n"
            "Every quote is itemised, and we agree a programme before work starts so you "
            "know which rooms are out of action and for how long."
        ),
    },
    {
        "slug": "extensions-structural-work",
        "title": "Extensions & structural work",
        "display_order": 3,
        "image": "service-extensions",
        "image_alt": "Single-storey rear extension with full-width glazing onto a garden",
        "short_description": "Rear, side-return and loft extensions, including steelwork and openings.",
        "description": (
            "Adding space is the biggest change you can make to a home, and the one where "
            "planning matters most. We work with structural engineers and, where needed, "
            "architects to take you from first sketch through building control sign-off.\n\n"
            "That includes knocking through load-bearing walls, installing steel beams, "
            "and making sure the new space feels like it was always part of the house."
        ),
    },
    {
        "slug": "property-maintenance",
        "title": "Property maintenance",
        "display_order": 4,
        "image": "service-maintenance",
        "image_alt": "Carpenter fitting a timber window frame",
        "short_description": "Planned upkeep and repairs for homes and small portfolios.",
        "description": (
            "Good houses stay good because someone looks after them. Our maintenance plans "
            "cover seasonal checks, gutters and roofs, sealant and grouting, and the small "
            "repairs that stop becoming big ones.\n\n"
            "We also look after small rental portfolios, with one point of contact and a "
            "written record of every visit."
        ),
    },
]

PROJECTS = [
    {
        "slug": "the-orchard-house",
        "title": "The Orchard House",
        "category": "extension",
        "service": "extensions-structural-work",
        "location": "Clifton",
        "completed_at": date(2026, 6, 15),
        "is_featured": True,
        "is_published": True,
        "image": "project-orchard-house",
        "featured_image_alt": "Glazed rear extension opening onto a garden",
        "summary": "Rear extension and open-plan kitchen",
        "description": (
            "A dark, cramped kitchen at the back of a Victorian semi became a light-filled "
            "family room. We replaced the original lean-to with a single-storey extension, "
            "opened up the rear wall with a steel beam, and added full-width glazing onto "
            "the garden.\n\n"
            "Underfloor heating, a vaulted ceiling with roof lights, and reclaimed brick to "
            "match the original house complete the space."
        ),
        "gallery": [
            {
                "image": "project-orchard-house-before",
                "kind": "before",
                "alt_text": "The original kitchen with a low ceiling and small window",
                "caption": "The original lean-to kitchen",
            },
            {
                "image": "project-orchard-house-after",
                "kind": "after",
                "alt_text": "Open-plan kitchen and dining space flooded with daylight",
                "caption": "The finished kitchen and dining room",
            },
        ],
    },
    {
        "slug": "redland-terrace",
        "title": "Redland Terrace",
        "category": "bathroom",
        "service": "kitchens-bathrooms",
        "location": "Redland",
        "completed_at": date(2026, 3, 20),
        "is_featured": True,
        "is_published": True,
        "image": "project-redland-terrace",
        "featured_image_alt": "Bathroom with a freestanding bath and panelled walls",
        "summary": "Family bathroom restoration",
        "description": (
            "The family bathroom in this Edwardian terrace had been refitted in the 1990s "
            "with little regard for the house. We stripped it back, levelled the floor, "
            "and rebuilt it around a freestanding bath under the window.\n\n"
            "Painted panelling, encaustic-style floor tiles and a walk-in shower behind a "
            "slim glass screen give the room space and character."
        ),
        "gallery": [
            {
                "image": "project-redland-terrace-before",
                "kind": "before",
                "alt_text": "Dated bathroom with a corner bath and worn tiles",
                "caption": "Before: the 1990s refit",
            },
            {
                "image": "project-redland-terrace-after",
                "kind": "after",
                "alt_text": "Walk-in shower with a slim glass screen beside panelled walls",
                "caption": "After: walk-in shower and panelling",
            },
        ],
    },
    {
        "slug": "lansdown-villa",
        "title": "Lansdown Villa",
        "category": "renovation",
        "service": "home-renovations",
        "location": "Bath",
        "completed_at": date(2025, 11, 8),
        "is_featured": True,
        "is_published": True,
        "image": "project-lansdown-villa",
        "featured_image_alt": "Georgian stone villa with sash windows",
        "summary": "Whole-house renovation",
        "description": (
            "A whole-house renovation of a Georgian villa that had been split into flats. "
            "We returned it to a single family home, rewired and replumbed throughout, and "
            "restored the original cornicing, shutters and fireplaces.\n\n"
            "Working within a listed building meant close coordination with the "
            "conservation officer at every stage."
        ),
    },
    {
        "slug": "harbourside-flat",
        "title": "Harbourside Flat",
        "category": "kitchen",
        "service": "kitchens-bathrooms",
        "location": "Bristol",
        "completed_at": date(2026, 1, 30),
        "is_featured": False,
        "is_published": True,
        "image": "project-harbourside-flat",
        "featured_image_alt": "Compact galley kitchen with handleless cabinets",
        "summary": "Compact galley kitchen",
        "description": (
            "A small apartment kitchen redesigned to work much harder. Full-height "
            "handleless units, an integrated fridge and a slimline dishwasher fit into a "
            "galley that previously held barely half as much storage.\n\n"
            "Work was scheduled around the building's quiet hours and completed in under "
            "three weeks."
        ),
    },
    {
        "slug": "chew-valley-barn",
        "title": "Chew Valley Barn",
        "category": "renovation",
        "service": "home-renovations",
        "location": "Chew Valley",
        "completed_at": date(2025, 9, 12),
        "is_featured": False,
        "is_published": True,
        "image": "project-chew-valley-barn",
        "featured_image_alt": "Converted barn living space with exposed oak beams",
        "summary": "Barn conversion interior",
        "description": (
            "The second phase of a barn conversion: we completed the interior, insulated "
            "the roof to modern standards while keeping the oak frame on show, and fitted "
            "a wood-burning stove as the centrepiece of the main living space."
        ),
    },
    {
        "slug": "portishead-loft",
        "title": "Portishead Loft",
        "category": "extension",
        "service": "extensions-structural-work",
        "location": "Portishead",
        "completed_at": date(2026, 8, 2),
        "is_featured": False,
        "is_published": True,
        "image": "project-portishead-loft",
        "featured_image_alt": "Loft bedroom with roof windows and built-in storage",
        "summary": "Loft conversion with en-suite",
        "description": (
            "A dormer loft conversion adding a main bedroom with en-suite shower room. "
            "Built-in storage under the eaves and two large roof windows make the most of "
            "every metre of floor space."
        ),
    },
    {
        "slug": "keynsham-care-plan",
        "title": "Keynsham Family Home",
        "category": "maintenance",
        "service": "property-maintenance",
        "location": "Keynsham",
        "completed_at": date(2026, 9, 5),
        "is_featured": False,
        "is_published": True,
        "image": "project-keynsham-care-plan",
        "featured_image_alt": "Freshly painted front door of a 1930s house",
        "summary": "Annual maintenance plan",
        "description": (
            "Part of an annual maintenance plan: gutter clearance, repointing, external "
            "joinery repairs and a fresh coat of paint for the front of the house, all "
            "logged in a written report for the owners."
        ),
    },
    {
        # Unpublished draft: proves drafts never appear on the public site.
        "slug": "hill-road-kitchen",
        "title": "Hill Road Kitchen",
        "category": "kitchen",
        "service": "kitchens-bathrooms",
        "location": "Clevedon",
        "completed_at": None,
        "is_featured": False,
        "is_published": False,
        "image": "project-hill-road-kitchen",
        "featured_image_alt": "Shaker-style kitchen in sage green",
        "summary": "Shaker kitchen (in progress)",
        "description": "Write-up to follow once the project is complete.",
    },
]

# Neither account can log in: the seed gives them unusable passwords.
STAFF = [
    {"username": "sarah.jones", "first_name": "Sarah", "last_name": "Jones", "is_active": True},
    {"username": "tom.reed", "first_name": "Tom", "last_name": "Reed", "is_active": False},
]

# days_ago values are floats so timestamps fall at different times of day.
# history: (new_status, staff_username, days_ago); notes: (staff_username, body, days_ago)
ENQUIRIES = [
    {
        "name": "Hannah Clarke", "email": "hannah.clarke@example.com", "phone": "07700 900101",
        "service": "kitchens-bathrooms", "postcode": "BS8 2PL", "preferred_contact_method": "phone",
        "project_description": "We'd like to replace our kitchen and knock through to the dining room. Victorian terrace, roughly 4m x 3m kitchen.",
        "days_ago": 0.2,
    },
    {
        "name": "James Patel", "email": "james.patel@example.com", "phone": "",
        "service": "extensions-structural-work", "postcode": "BS6 7QR", "preferred_contact_method": "email",
        "project_description": "Considering a side-return extension. Can you advise on whether we'd need planning permission?",
        "days_ago": 1.4,
    },
    {
        "name": "Olivia Bennett", "email": "olivia.bennett@example.com", "phone": "07700 900102",
        "service": "property-maintenance", "postcode": "BS31 1HJ", "preferred_contact_method": "",
        "project_description": "Gutters overflowing at the back of the house and some damp showing inside. Hoping for someone to take a look soon.",
        "days_ago": 2.6,
    },
    {
        "name": "Daniel Hughes", "email": "daniel.hughes@example.com", "phone": "",
        "service": None, "postcode": "BA1 5LS", "preferred_contact_method": "email",
        "project_description": "Not sure which service fits. We've just bought a 1960s bungalow that needs updating throughout.",
        "days_ago": 3.1,
    },
    {
        "name": "Sophie Turner", "email": "sophie.turner@example.com", "phone": "07700 900103",
        "service": "kitchens-bathrooms", "postcode": "BS21 7AB", "preferred_contact_method": "phone",
        "project_description": "Ensuite shower room refit. Existing tray is leaking.",
        "days_ago": 5.3,
        "history": [("contacted", "sarah.jones", 4.8)],
        "notes": [("sarah.jones", "Spoke on the phone. Site visit booked for Thursday morning.", 4.8)],
    },
    {
        "name": "Mark Wilson", "email": "mark.wilson@example.com", "phone": "",
        "service": "home-renovations", "postcode": "BS7 9NE", "preferred_contact_method": "email",
        "project_description": "Full redecoration and new flooring for a three-bed semi before we move in next spring.",
        "days_ago": 8.2,
        "history": [("contacted", "sarah.jones", 7.5)],
    },
    {
        "name": "Priya Shah", "email": "priya.shah@example.com", "phone": "07700 900104",
        "service": "extensions-structural-work", "postcode": "BS20 6PZ", "preferred_contact_method": "phone",
        "project_description": "Loft conversion with a dormer. Two children sharing a room at the moment.",
        "days_ago": 12.7,
        "history": [("contacted", "sarah.jones", 11.9)],
        "notes": [("sarah.jones", "Sent our loft conversion guide. Waiting on measured drawings from the client.", 11.9)],
    },
    {
        "name": "Ben Carter", "email": "ben.carter@example.com", "phone": "",
        "service": "kitchens-bathrooms", "postcode": "BS9 3HG", "preferred_contact_method": "email",
        "project_description": "New kitchen, roughly 5m wall run plus an island. Have some ideas from showrooms already.",
        "days_ago": 16.4,
        "history": [("contacted", "sarah.jones", 15.8), ("quoted", "sarah.jones", 9.2)],
        "notes": [("sarah.jones", "Quote sent: kitchen supply and fit, island with power.", 9.2)],
    },
    {
        "name": "Emily Foster", "email": "emily.foster@example.com", "phone": "07700 900105",
        "service": "home-renovations", "postcode": "BA2 4QT", "preferred_contact_method": "phone",
        "project_description": "Rewire and replaster two bedrooms and the landing.",
        "days_ago": 21.5,
        "history": [("contacted", "tom.reed", 20.9), ("quoted", "sarah.jones", 14.1)],
        "notes": [
            ("tom.reed", "Visited. Wiring is original 1970s, full rewire recommended.", 20.1),
            ("sarah.jones", "Took over from Tom. Quote issued.", 14.1),
        ],
    },
    {
        "name": "Ryan Murphy", "email": "ryan.murphy@example.com", "phone": "",
        "service": "property-maintenance", "postcode": "BS1 6TY", "preferred_contact_method": "email",
        "project_description": "Annual maintenance for three rental flats in the same building.",
        "days_ago": 26.0,
        "history": [("contacted", "tom.reed", 25.2), ("quoted", "tom.reed", 22.4)],
    },
    {
        "name": "Charlotte Evans", "email": "charlotte.evans@example.com", "phone": "07700 900106",
        "service": "extensions-structural-work", "postcode": "BS8 4LD", "preferred_contact_method": "phone",
        "project_description": "Single-storey rear extension to create a kitchen-diner.",
        "days_ago": 48.3,
        "history": [
            ("contacted", "tom.reed", 47.6),
            ("quoted", "tom.reed", 40.2),
            ("won", "sarah.jones", 31.0),
        ],
        "notes": [
            ("tom.reed", "Structural engineer recommended. Client happy to proceed with drawings.", 44.0),
            ("sarah.jones", "Deposit received. Start date agreed for early next month.", 31.0),
        ],
    },
    {
        "name": "Thomas Reid", "email": "thomas.reid@example.com", "phone": "",
        "service": "kitchens-bathrooms", "postcode": "BS6 6BX", "preferred_contact_method": "email",
        "project_description": "Family bathroom refit with a separate shower.",
        "days_ago": 39.6,
        "history": [
            ("contacted", "sarah.jones", 39.0),
            ("quoted", "sarah.jones", 33.5),
            ("won", "sarah.jones", 28.2),
        ],
    },
    {
        "name": "Grace Morgan", "email": "grace.morgan@example.com", "phone": "07700 900107",
        "service": "home-renovations", "postcode": "BA1 2HN", "preferred_contact_method": "phone",
        "project_description": "Kitchen and living room renovation in a ground-floor flat.",
        "days_ago": 44.8,
        "history": [
            ("contacted", "tom.reed", 44.1),
            ("quoted", "tom.reed", 37.9),
            ("lost", "sarah.jones", 27.4),
        ],
        "notes": [("sarah.jones", "Client has decided to postpone until next year.", 27.4)],
    },
    {
        "name": "Lewis Price", "email": "lewis.price@example.com", "phone": "",
        "service": "property-maintenance", "postcode": "BS31 2DE", "preferred_contact_method": "email",
        "project_description": "One-off job: replace a section of fence and two fence posts.",
        "days_ago": 35.2,
        "history": [("contacted", "sarah.jones", 34.7), ("lost", "sarah.jones", 34.7)],
        "notes": [("sarah.jones", "Too small for us. Recommended a local fencing contractor.", 34.7)],
    },
]