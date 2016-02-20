

###########################################
#
# COMP 1551
# Core Programming
#
# Coursework 2 - Mini Project
#
# George Loines
# 200836065
#
# 02 Feb 2015
#
###########################################


import urllib.request
import json


class Leaderboard:
    """
    Handles a leaderboard, backed by an azure REST api.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.application_url = "http://gl-tower-defence.azurewebsites.net/tables/scoreboardentry"
        self.application_headers = {"x-zumo-application": "cwrbABoHBGWKMhIiHrkVChWHoDcmAa78"}
        self.entries = []

    def retrieve(self):
        """
        Updates the leaderboard from the REST api.
        """
        try:
            request = urllib.request.Request(self.application_url, headers=self.application_headers)
            response = urllib.request.urlopen(request)
        
            raw = response.read().decode()
            data = json.loads(raw)

            self.entries = [LeaderboardEntry(d) for d in data]
            self.entries.sort(key = lambda e: e.score, reverse = True)
        
        except:
            print("Error downloading leaderboard")

    def add(self, level, name, score, wave):
        """
        Adds a new entry to the leaderboard.
        Saves it using the REST api.
        
        Args:
            level (str): The level the score is for.
            name (str): The displayed user's name.
            score (int): The displayed score.
            wave (int): The displayed wave number.

        """
        try:
            raw = {"level": level, "name": name, "score": score, "wave": wave}
            data = json.dumps(raw).encode()

            request = urllib.request.Request(self.application_url, data, self.application_headers)
            request.add_header("Content-Type", "application/json")
            request.add_header("Content-Length", len(data))
            response = urllib.request.urlopen(request)

        except:
            print("Error updating scoreboard")


class LeaderboardEntry:
    """
    A single entry in the leaderboard.
    """

    def __init__(self, data):
        """
        Constructor.

        Args:
            data (dict): The entry data from json.

        """
        self.level = data["level"]
        self.name = data["name"]
        self.score = int(data["score"])
        self.wave = int(data["wave"])
