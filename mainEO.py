import requests
import json
import datetime
from Contributor import Contributor
from enrolledContributorsEO import enrolledContributors
from jinja2 import Environment, FileSystemLoader

LANG = "eo"

# https://commonvoice.mozilla.org/api/v1/eo/clips/votes/leaderboard?cursor=[1,23565]
# https://commonvoice.mozilla.org/api/v1/eo/clips/leaderboard?cursor=[1,23565]
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
    now = datetime.datetime.utcnow()+datetime.timedelta(hours=2)
    date_time = now.strftime("%d.%m.%y %H:%M")
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('indexEO.html')
    scoreTableData = list()

    for idx, contributor in enumerate(sortedContribList):
      scoreTableData.append({
          "index": idx+1,
          "username": contributor.username,
          "recordedClips": contributor.recordedClipsDelta,
          "validatedClips": contributor.validatedClipsDelta,
          "score": contributor.competitionScore,
      })

    content = {
        "scoreboardTable": scoreTableData,
        "timestamp": date_time
    }

    OUT_FOLDER = 'website'
    htmlout = template.render(content=content)
    with open(f"{OUT_FOLDER}/eo/index.html", "w") as f:
      f.write(htmlout)


if __name__ == "__main__":
    data = Data()
    data.fetchDataFromApi()
    data.buildDashboard()
    data.buildRanking()
    sortedContribList = data.buildRanking()
    writeWebsite(sortedContribList)
