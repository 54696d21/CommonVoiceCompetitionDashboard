# import os
# import logging
# import time
import requests
import json
import datetime
from Contributor import Contributor
from enrolledContributors import enrolledContributors
from constants import LANG
from jinja2 import Environment, FileSystemLoader
from pprint import pprint
# https://ttl255.com/jinja2-tutorial-part-1-introduction-and-variable-substitution/
# https://zetcode.com/python/jinja/

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
    HTML1 = """    """
    HTML2 = """   """
    HTML3 = f"""  """
    file_loader = FileSystemLoader('templates')


    env = Environment(loader=file_loader)

    template = env.get_template('about.html')
    # template = env.get_template('index.html')

    a = list()
    for idx, contributor in enumerate(sortedContribList):
      a.append({
        "index": idx+1,
        "username":contributor.username,
        "recordedClips": contributor.recordedClipsDelta,
        "validatedClips": contributor.validatedClipsDelta,
        "score": contributor.competitionScore,
      })

    content = {
        "scoreboardTable": a,
        "timestamp": date_time
    }
    pprint(a)
    FOLDER = 'website'
    output = template.render(content=content)
    # print(output)
    # output_from_parsed_template = template.render('test.html', foo="Hello World!")
    with open(f"{FOLDER}/index.html", "w") as f:
      f.write(output)

    # content = {
    #     "hostname": "core-sw-waw-01",
    #     "name_server_pri": "1.1.1.1",
    #     "name_server_sec": "8.8.8.8",
    #     "ntp_server_pri": "0.pool.ntp.org",
    #     "ntp_server_sec": "1.pool.ntp.org",
    # }
    # 
    # with open(f"{FOLDER}/index.html", "w") as htmlout:
    #     content = {
    #         "hostname": contributor.username,
    #     }
    #     htmlout.write(HTML1)
    #     for idx, contributor in enumerate(sortedContribList):
    #         htmlout.write(f"<tr><td>{idx+1}</td><td>{contributor.username}</td> <td>{contributor.recordedClipsDelta}</td> <td>{contributor.validatedClipsDelta}</td> <td>{contributor.competitionScore}</td></tr>")

    #     htmlout.write(HTML2)
    #     htmlout.write(HTML3)


if __name__ == "__main__":
    data = Data()
    data.fetchDataFromApi()
    data.buildDashboard()
    data.buildRanking()
    sortedContribList = data.buildRanking()
    writeWebsite(sortedContribList)
