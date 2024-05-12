#!/usr/bin/env python
from trip_planner_yb.crew import TripPlannerYbCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': 'AI LLMs'
    }
    TripPlannerYbCrew().crew().kickoff(inputs=inputs)