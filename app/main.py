from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool

from app.models.event import Event
from app.models.profile import Profile
from app.models.planning_request import PlanningRequest

from app.data.booking_db import get_bookings
from app.data.package_store import (
    approved_packages,
    generated_packages,
)

from app.services.event_service import EventService
from app.services.vendor_service import VendorService
from app.services.vendor_ranking_service import VendorRankingService
from app.services.wedmegood_service import WedMeGoodService
from app.services.wedmegood_caterer_service import (
    WedMeGoodCatererService,
)
from app.services.wedmegood_decorator_service import (
    WedMeGoodDecoratorService,
)
from app.services.wedmegood_photographer_service import (
    WedMeGoodPhotographerService,
)

from app.services.approval_service import ApprovalService
from app.services.booking_service import BookingService
from app.services.constraint_service import ConstraintService
from app.services.form_service import FormService
from app.services.memory_service import MemoryService
from app.services.planning_service import PlanningService
from app.services.profile_service import ProfileService

from app.engine.package_generator import PackageGenerator
from app.agents.planner_agent import planner

from app.routers.chat import router as chat_router
from app.routers.package_explanation import (
    router as explanation_router,
)

app = FastAPI()

# ---------------- CORS ---------------- #

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(explanation_router)

# ---------------- ROOT ---------------- #

@app.get("/")
def root():
    return {
        "message": "Event Management Agent Running"
    }

# ---------------- EVENTS ---------------- #

@app.post("/create-event")
def create_event(event: Event):
    return EventService.create_event(event)

# ---------------- VENDORS ---------------- #

@app.get("/vendors")
def get_vendors():
    return VendorService.get_all_vendors()


@app.get("/filter-vendors")
def filter_vendors(
    location: str,
    guest_count: int,
    budget: float,
    vendor_type: str,
):
    return VendorService.filter_vendors(
        location,
        guest_count,
        budget,
        vendor_type,
    )


@app.get("/recommend-vendors")
def recommend_vendors(
    location: str,
    guest_count: int,
    budget: float,
    vendor_type: str,
):
    return VendorService.get_ranked_vendors(
        location,
        guest_count,
        budget,
        vendor_type,
    )

# ---------------- PACKAGES ---------------- #

@app.get("/generate-packages")
def generate_packages(
    location: str,
    guest_count: int,
    budget: float,
):
    return PackageGenerator.generate_packages(
        location,
        guest_count,
        budget,
    )


@app.post("/approve-package/{package_id}")
def approve_package(package_id: str):
    return ApprovalService.approve_package(package_id)


@app.get("/package-status/{package_id}")
def package_status(package_id: str):
    return ApprovalService.get_status(package_id)

# ---------------- PLANNER ---------------- #

@app.post("/plan-event")
def plan_event(data: PlanningRequest):

    event_details = PlanningService.parse_request(
        data.request
    )

    constraints = ConstraintService.extract_constraints(
        data.request
    )

    event_details["preferences"].update(
        constraints
    )

    venues = VendorRankingService.rank_vendors(
        WedMeGoodService.get_venues(),
        budget=event_details["budget"],
        guest_count=event_details["guest_count"],
        location=event_details["location"],
    )

    caterers = VendorRankingService.rank_vendors(
        WedMeGoodCatererService.get_caterers(),
        guest_count=event_details["guest_count"],
        location=event_details["location"],
    )

    decorators = VendorRankingService.rank_vendors(
        WedMeGoodDecoratorService.get_decorators(),
        location=event_details["location"],
    )

    photographers = VendorRankingService.rank_vendors(
        WedMeGoodPhotographerService.get_photographers(),
        location=event_details["location"],
    )

    return planner.invoke(
        {
            **event_details,
            "preferences": event_details["preferences"],
            "venues": venues,
            "caterers": caterers,
            "decorators": decorators,
            "photographers": photographers,
            "packages": [],
            "budget_analysis": {},
            "needs_replan": False,
        }
    )

# ---------------- PREFERENCES ---------------- #

@app.post("/save-preferences")
def save_preferences(preferences: dict):

    MemoryService.save_preferences(preferences)

    return {
        "status": "saved",
        "preferences": preferences,
    }


@app.get("/preferences")
def get_preferences():
    return MemoryService.get_preferences()

# ---------------- PROFILE ---------------- #

@app.post("/profile")
def save_profile(profile: Profile):
    return ProfileService.save_profile(
        profile.model_dump()
    )

# ---------------- BOOKING ---------------- #

@app.get("/prepare-booking/{package_id}")
def prepare_booking(package_id: str):

    if package_id not in approved_packages:
        return {"error": "Package not approved"}

    return FormService.prepare_booking(
        approved_packages[package_id]
    )


@app.post("/execute-booking/{package_id}")
def execute_booking(package_id: str):

    if package_id not in approved_packages:
        return {
            "error": "Package not approved"
        }

    BookingService.execute_browser_filling(
        {
            "booking_data":
            approved_packages[package_id]
        }
    )

    return {
        "message":
        "Booking execution started"
    }


@app.get("/agent-booking/{package_id}")
async def agent_booking(package_id: str):

    if package_id not in approved_packages:
        return {
            "error": "Package not approved"
        }

    return await BookingService.prepare(
        approved_packages[package_id]
    )


@app.post("/confirm-booking/{session_id}")
async def confirm_booking(session_id: str):
    return await BookingService.confirm(
        session_id
    )

# ---------------- BOOKING DATA ---------------- #

@app.get("/booking-data/{package_id}")
def booking_data(package_id: int):

    profile = ProfileService.get_profile()
    preferences = MemoryService.get_preferences()
    package = generated_packages[package_id]

    return {
        "name": profile.get("name"),
        "email": profile.get("email"),
        "phone": profile.get("phone"),
        "gender": profile.get("gender"),
        "event_type": preferences.get("event_type"),
        "guest_count": preferences.get("guest_count"),
        "budget": preferences.get("budget"),
        "venue": package["venue"],
        "caterer": package["caterer"],
        "decorator": package["decorator"],
        "photographer": package["photographer"],
    }

# ---------------- DEBUG ---------------- #

@app.get("/python-check")
async def python_check():

    import sys
    import playwright

    return {
        "python": sys.executable,
        "playwright": playwright.__file__,
    }


@app.get("/test-loop")
async def test_loop():

    import asyncio

    return {
        "loop":
        str(type(asyncio.get_running_loop()))
    }

# ---------------- SCRAPERS ---------------- #

@app.get("/wedmegood/venues")
async def wedmegood_venues():
    return await run_in_threadpool(
        WedMeGoodService.get_venues
    )


@app.get("/wedmegood/caterers")
def wedmegood_caterers():
    return WedMeGoodCatererService.get_caterers()


@app.get("/wedmegood/decorators")
def wedmegood_decorators():
    return WedMeGoodDecoratorService.get_decorators()


@app.get("/wedmegood/photographers")
def wedmegood_photographers():
    return WedMeGoodPhotographerService.get_photographers()

# ---------------- BOOKINGS ---------------- #

@app.get("/bookings")
def bookings():
    return get_bookings()

# ---------------- STARTUP ---------------- #

#@app.on_event("startup")
#def startup():

 #   print("Loading vendors...")

  #  VendorService.get_all_vendors()

   # print("Vendor cache ready")
