#!/usr/bin/env python
from ecovesti_v2.crew import EcovestiV2Crew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'user_URL': input('Copy and Paste the product you would like to check: ')
    }
    EcovestiV2Crew().crew().kickoff(inputs=inputs)