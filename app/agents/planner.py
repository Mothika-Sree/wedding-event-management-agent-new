def planner(state):

    if not state.get("event_type"):
        return "What type of event are you planning?"

    if not state.get("city"):
        return "Which city will the event take place in?"

    if not state.get("guests"):
        return "Approximately how many guests are you expecting?"

    if not state.get("budget"):
        return "What's your approximate budget?"

    if not state.get("date"):
        return "What date is the event?"

    return "Perfect! I'll now look for suitable venues."