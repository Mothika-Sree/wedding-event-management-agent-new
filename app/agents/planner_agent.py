from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph import END

from app.services.vendor_service import VendorService
from app.engine.package_generator import PackageGenerator
from app.agents.budget_optimizer import BudgetOptimizer


class PlannerState(TypedDict):

    location: str
    guest_count: int
    budget: float
    event_type: str

    venues: list
    caterers: list
    decorators: list
    photographers: list

    packages: list
    preferences: dict
    budget_analysis: dict

    needs_replan: bool


def budget_node(state):

    result = BudgetOptimizer.optimize_budget(
        state["guest_count"],
        state["budget"]
    )

    print("BUDGET NODE EXECUTED")
    print("BUDGET ANALYSIS:", result)

    state["budget_analysis"] = result

    return state


def venue_node(state):

    state["venues"] = VendorService.get_ranked_vendors(
        state["location"],
        state["guest_count"],
        state["budget"],
        "venue",
        state["preferences"]
    )

    return state


def catering_node(state):

    state["caterers"] = VendorService.get_ranked_vendors(
        state["location"],
        state["guest_count"],
        state["budget"],
        "catering"
    )

    return state


def decorator_node(state):

    state["decorators"] = VendorService.get_ranked_vendors(
        state["location"],
        state["guest_count"],
        state["budget"],
        "decoration"
    )

    return state


def photographer_node(state):

    state["photographers"] = VendorService.get_ranked_vendors(
        state["location"],
        state["guest_count"],
        state["budget"],
        "photography"
    )

    return state


def decision_node(state):

    print("DECISION NODE RUNNING")

    if len(state["venues"]) == 0:

        print("NO VENUES FOUND -> REPLAN")

        state["needs_replan"] = True

    else:

        print("VENUES FOUND -> CONTINUE")

        state["needs_replan"] = False

    return state


def package_node(state):

    state["packages"] = PackageGenerator.generate_packages(
        state["location"],
        state["guest_count"],
        state["budget"],
        state["preferences"]
    )

    return state


def replan_node(state):

    print("REPLAN NODE RUNNING")

    state["budget"] += 50000

    print(f"NEW BUDGET: {state['budget']}")

    state["venues"] = VendorService.get_ranked_vendors(
        state["location"],
        state["guest_count"],
        state["budget"],
        "venue"
    )

    return state


def route_decision(state):

    if state["needs_replan"]:
        return "replan"

    return "continue"


def build_planner():

    workflow = StateGraph(PlannerState)

    workflow.add_node(
        "budget_analysis",
        budget_node
    )

    workflow.add_node(
        "venue_search",
        venue_node
    )

    workflow.add_node(
        "decision",
        decision_node
    )

    workflow.add_node(
        "replan",
        replan_node
    )

    workflow.add_node(
        "catering_search",
        catering_node
    )

    workflow.add_node(
        "decorator_search",
        decorator_node
    )

    workflow.add_node(
        "photographer_search",
        photographer_node
    )

    workflow.add_node(
        "package_generation",
        package_node
    )

    workflow.set_entry_point(
        "budget_analysis"
    )

    workflow.add_edge(
        "budget_analysis",
        "venue_search"
    )

    workflow.add_edge(
        "venue_search",
        "decision"
    )

    workflow.add_conditional_edges(
        "decision",
        route_decision,
        {
            "continue": "catering_search",
            "replan": "replan"
        }
    )

    workflow.add_edge(
        "replan",
        "catering_search"
    )

    workflow.add_edge(
        "catering_search",
        "decorator_search"
    )

    workflow.add_edge(
        "decorator_search",
        "photographer_search"
    )

    workflow.add_edge(
        "photographer_search",
        "package_generation"
    )

    workflow.add_edge(
        "package_generation",
        END
    )

    return workflow.compile()


planner = build_planner()