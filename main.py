# import os
# import logging
# import time
import requests
import json
import datetime
from Contributor import Contributor
from enrolledContributors import enrolledContributors
from constants import LANG


URL_VALIDATED = f"https://commonvoice.mozilla.org/api/v1/{LANG}/clips/votes/leaderboard?cursor=[1,23565]"
URL_RECORDED = f"https://commonvoice.mozilla.org/api/v1/{LANG}/clips/leaderboard?cursor=[1,23565]"


class Data:
    def __init__(self) -> None:
        self.validatedApiResonseContent = None
        self.recordedApiResonseContent = None

    def fetchDataFromApi(self) -> None:
        r = requests.get(URL_VALIDATED)
        self.validatedApiResonseContent = json.loads(r.content)
        for i in self.validatedApiResonseContent:
            i["avatarClipUrl"] = None
            i["avatar_url"] = None

        r = requests.get(URL_RECORDED)
        self.recordedApiResonseContent = json.loads(r.content)
        for i in self.recordedApiResonseContent:
            i["avatarClipUrl"] = None
            i["avatar_url"] = None

    def buildDashboard(self) -> None:
        pass
        for contributor in enrolledContributors:
            for j in self.recordedApiResonseContent:
                if j["username"] == contributor.username:
                    contributor.currentRecordedClips = j.get("total")
            for j in self.validatedApiResonseContent:
                if j["username"] == contributor.username:
                    contributor.currentValidatedClips = j.get("total")
            contributor.populateDeltas()
            contributor.populateScore()

    def buildRanking(self) -> None:
        return sorted(
            enrolledContributors, key=lambda contributor: contributor.competitionScore, reverse=True)


def writeWebsite(sortedContribList):
    now = datetime.datetime.now()
    date_time = now.strftime("%d.%m.%y %H:%M")
    HTML1 = """<!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Common Voice Competition Leaderboard</title>
    </head>
    <body>
    <ul>
    """
    HTML2 = """</ul>
    </body>
    </html>"""
    HTML3 = f"""<footer>
    <p>zuletzt aktualisiert: {date_time} MESZ</p>
    </footer>"""

    FOLDER = 'website'
    with open(f"{FOLDER}/index.html", "w") as htmlout:
        htmlout.write(HTML1)

        for idx, contributor in enumerate(sortedContribList):
            htmlout.write(
                f"<li>{idx+1}. {contributor.username} | {contributor.competitionScore} Punkte</li>\n")

        htmlout.write(HTML2)
        htmlout.write(HTML3)


if __name__ == "__main__":
    data = Data()
    data.fetchDataFromApi()
    data.buildDashboard()
    data.buildRanking()
    sortedContribList = data.buildRanking()
    writeWebsite(sortedContribList)
