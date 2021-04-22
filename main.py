# import os
# import logging
# import time
import requests
import json
import datetime
from Contributor import Contributor
from enrolledContributors import enrolledContributors
from constants import LANG


"https://commonvoice.mozilla.org/api/v1/de/clips/votes/leaderboard?cursor=[1,23565]"
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
  <title>Common Voice Spenden Challenge</title>
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@300&display=swap" rel="stylesheet">

  <style>
    body {
      font-family: 'Zilla Slab', serif;
      max-width: 750px;
      margin: 0 auto;
      padding: 25px 20px 10px 20px;
      background-color: #fefefe;
      font-size: larger;
    }
    img {
      max-width: 750px;
      width: 100%;
    }
    table {
      width: 100%;
      max-width: 750px;
      border-collapse: collapse;
      margin-top: 30px;
    }
    th {
      border: 1px solid #eee;
      text-align: left;
      padding: 12px 8px;
      background-color: black;
      color: #fff;
    }
    td {
      border: 1px solid #eee;
      padding: 4px 8px;
    }
    td:nth-child(2),
    th:nth-child(2) {
      max-width: 150px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    tr:nth-child(even) {
      background-color: #f2f2f2;
    }
    tr:hover {
      background-color: #ddd;
    }

    @media screen and (max-width: 600px) {
      td:nth-child(3),
      th:nth-child(3),
      td:nth-child(4),
      th:nth-child(4) {
        display: none;
      }
    }
  </style>

</head>
<body>
  <img src="https://i.imgur.com/wHxnc4h.png">

  <h1>Topliste der Common Voice Spenden Challenge Mai 2021</h1>
  <p>Willkommen auf dem Leaderboard der Common Voice Spenden Challenge. Hier tracken wir einen Monat lang wer wieviel spendet und die Plätze 1-20 erhalten als Dankeschön Sticker zugeschickt. </p>
  <p>Wenn auch Du in der Liste auftauchen und beider Challenge mitmachen willst willst dann brauchst Du ein Profil auf <a href="https://commonvoice.mozilla.org/de">commonvoice.mozilla.org/de</a> und das Profil muss auf "sichtbar" gestellt sein. Schick uns deinen Benutzernamen entweder über <a href="">dieses Formular</a> oder im <a href="https://discourse.mozilla.org/c/voice/239">Mozilla Forum</a>. </p>
  <p>Du kannst deine Stimme spenden oder die Aufnahmen von anderen kontrollieren. Benutze die <a href="https://commonvoice.mozilla.org/de">Webseite</a> oder die Android App (<a href="https://f-droid.org/de/packages/org.commonvoice.saverio/">F-Droid</a> / <a href="https://play.google.com/store/apps/details?id=org.commonvoice.saverio">Play Store</a>). Außerdem lohnt es sich immer die <a href="https://discourse.mozilla.org/t/vorlaufige-richtlinien-fur-das-validieren-von-satzen/62328">Richtlinien für das Validieren</a> zu lesen.  </p>
  <table>
    
    <tr>
      <th>#</th>
      <th>Nutzername</th>
      <th>Aufnahmen</th>
      <th>Validierungen</th>
      <th>Score</th>
    </tr>
    """
    HTML2 = """  </tr>
    </table>"""
    HTML3 = f"""<footer>
    <p>zuletzt aktualisiert: {date_time} MESZ</p>
    </footer>
    </body>
    </html>"""

    FOLDER = 'website'
    with open(f"{FOLDER}/index.html", "w") as htmlout:
        htmlout.write(HTML1)

        for idx, contributor in enumerate(sortedContribList):
            htmlout.write(
                f"<tr><td>{idx+1}</td><td>{contributor.username}</td> <td>{contributor.recordedClipsDelta}</td> <td>{contributor.validatedClipsDelta}</td> <td>{contributor.competitionScore}</td></tr>")

        htmlout.write(HTML2)
        htmlout.write(HTML3)


if __name__ == "__main__":
    data = Data()
    data.fetchDataFromApi()
    data.buildDashboard()
    data.buildRanking()
    sortedContribList = data.buildRanking()
    writeWebsite(sortedContribList)


# <table style = "width:100%" >
