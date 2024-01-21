import json
import os

import fastf1
import numpy as np
import pandas as pd
import requests
import utils
YEAR = 2020


events = [
    'Austrian Grand Prix', 
'Styrian Grand Prix', 
    'Hungarian Grand Prix',
    'British Grand Prix', 
    '70th Anniversary Grand Prix', 
    'Spanish Grand Prix', 'Belgian Grand Prix', 
    'Italian Grand Prix', 'Tuscan Grand Prix', 
    'Russian Grand Prix',
    'Eifel Grand Prix', 
    'Portuguese Grand Prix', 'Emilia Romagna Grand Prix', 
    'Turkish Grand Prix', 
    'Abu Dhabi Grand Prix',
    'Bahrain Grand Prix', 'Sakhir Grand Prix',   
]

def top_speed(year: int, event: str | int, session: str) -> any:
    f1session = fastf1.get_session(year, event, session)
    f1session.load(telemetry=False, weather=False, messages=False)
    laps = f1session.laps
    # team_colors = utils.team_colors(year)

    fastest_speedtrap = (
        laps[["SpeedI1", "SpeedI2", "SpeedST", "SpeedFL"]]
        .idxmax(axis=1)
        .value_counts()
        .index[0]
    )

    speed_df = (
        laps[[fastest_speedtrap, "Driver", "Compound", "Team"]]
        .groupby("Driver")
        .max()
        .sort_values(fastest_speedtrap, ascending=False)
        .reset_index()
    )
    # add team colors to dataframe
    # speed_df["fill"] = speed_df["Team"].apply(lambda x: team_colors[x])

    # rename fastest speedtrap column to TopSpeed
    speed_df.rename(columns={fastest_speedtrap: "TopSpeed"}, inplace=True)

    # remove nan values in any column
    speed_df = speed_df.dropna()

    # Convert to int
    speed_df["TopSpeed"] = speed_df["TopSpeed"].astype(int)

    speed_dict = speed_df.to_dict(orient="records")

    return {"topSpeed": speed_dict}


def sessions_available(year: int, event: str | int) -> any:
    # get sessions available for a given year and event
    event = str(event)
    data = utils.LatestData(year)
    sessions = data.get_sessions(event)
    return sessions


# Your list of events
events_list = events

# Loop through each event
for event in events_list:
    sessions = sessions_available(YEAR, event)
    
    if event == "Styrian Grand Prix":
        sessions = ["Practice 1", "Practice 2", "Qualifying", "Race"]
    if event == "Eifel Grand Prix":
         sessions = ["Practice 3", "Qualifying", "Race"]
    if event == "Emilia Romagna Grand Prix":
        sessions = ["Practice 1", "Qualifying", "Race"]
    for session in sessions:
        top_speed_dict = top_speed(YEAR, event, session)

        # Specify the file path where you want to save the JSON data
        file_path = f"{event}/{session}/top_speeds.json"

        # Save the dictionary to a JSON file
        with open(file_path, "w") as json_file:
            json.dump(top_speed_dict, json_file)

        print(f"Dictionary saved to {file_path}")
