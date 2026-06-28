import json
import uuid
from datetime import datetime
from pathlib import Path

BOOKING_FILE = Path(
    "app/data/bookings.json"
)


def save_booking(profile, package):

    booking = {
        "booking_id": str(uuid.uuid4()),
        "created_at": datetime.now().isoformat(),
        "status": "CONFIRMED",
        "user": profile,
        "package": package
    }

    if BOOKING_FILE.exists():

        with open(
            BOOKING_FILE,
            "r"
        ) as f:

            bookings = json.load(f)

    else:

        bookings = []

    bookings.append(booking)

    with open(
        BOOKING_FILE,
        "w"
    ) as f:

        json.dump(
            bookings,
            f,
            indent=4
        )

    return booking


def get_bookings():

    if not BOOKING_FILE.exists():
        return []

    with open(
        BOOKING_FILE,
        "r"
    ) as f:

        return json.load(f)