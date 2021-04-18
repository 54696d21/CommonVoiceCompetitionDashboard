import requests
import json
import datetime
import os
import logging
import time
from Contributor import Contributor
from enrolledContributors import enrolledContributors

LANG = 'de'

URL_VALIDATED = f"https://commonvoice.mozilla.org/api/v1/{LANG}/clips/votes/leaderboard?cursor=[1,23565]"
URL_RECORDED = f"https://commonvoice.mozilla.org/api/v1/{LANG}/clips/leaderboard?cursor=[1,23565]"


class Data:
    def __init__(self) -> None:
        # def __init__(self, **kwargs):
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
        # print('ok')
        for contributor in enrolledContributors:
            # print(i.username)
            # repr(i)
            for j in self.recordedApiResonseContent:
                # print(i)
                if j["username"] == contributor.username:
                    # print(j["username"])
                    contributor.currentRecordedClips = j.get("total")
            for j in self.validatedApiResonseContent:
                # print(i)
                if j["username"] == contributor.username:
                    # print(j["username"])
                    contributor.currentValidatedClips = j.get("total")
                    # i.currentValidatedClips
                    # i.currentValidatedClips
            contributor.populateDeltas()
            contributor.populateScore()
            # for i in data:
            # user = i["username"]
            # if user in contributorsCompetition.USERS:
            #     # user contributorsCompetition.USERS2[user]
            #     for j in contributorsCompetition.USERS2:
            #         if j["user"] == user:
            #             oldContrib = j["contrib"]
            #             delta = i["total"] - oldContrib
            #             o.append({'user': user, 'delta': delta})

    def buildRanking(self) -> None:
        return sorted(
            enrolledContributors, key=lambda contributor: contributor.competitionScore, reverse=True)


def writeWebsite(sortedContribList):
    utcnow = datetime.datetime.utcnow()
    date_time = utcnow.strftime("%d.%m.%y %H:%M")
    HTML1 = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
    <ul>
    """
    HTML2 = """</ul>
    </body>
    </html>"""
    HTML3 = f"""<footer>
    <p>last updated: {date_time} UTC</p>
    </footer>"""

    FOLDER = 'website'
    with open(f"{FOLDER}/index.html", "w") as htmlout:
        htmlout.write(HTML1)
        htmlout.write(HTML2)

        for idx, contributor in enumerate(sortedContribList):
            htmlout.write(
                f"<li>{idx+1}. {contributor.username} {contributor.competitionScore}</li>\n")

        htmlout.write(HTML3)


if __name__ == "__main__":
    data = Data()
    data.fetchDataFromApi()
    data.buildDashboard()
    data.buildRanking()
    sortedContribList = data.buildRanking()
    # print(sortedContribList)
    writeWebsite(sortedContribList)