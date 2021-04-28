import LangListSpeech
import json
import requests
import datetime


HTML1 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
<p>
"""

HTML2 = """
</p>
</body>
</html>
"""

if __name__ == "__main__":

    reqData = requests.get(
        "https://commonvoice.mozilla.org/api/v1/language_stats"
    ).content

    j = json.loads(reqData)
    # print(j)
    b = list()
    for lang in j["launched"]:
        b.append(lang.get("locale"))

    # print(b)

    for k in LangListSpeech.langs:
        # print(k.values())
        # print(k.keys())
        # a = k.values()
        langCode = list(k.values())[0]
        # print(langCode)
        b.remove(langCode)

    with open("website/new_supported/index.html", "w") as f:
        f.write(HTML1)

        if len(b) > 0:
            f.write(str(b))
            f.write("<p></p>")
            for i in b:
                c = j["launched"]

                # for e in c:
                #     if e[""]
                #     print(e)
                # for j in c:
                # print(j)
                # c = reqData
                # print(c)
        else:
            print("probably no new languages added")

        now = datetime.datetime.utcnow()+datetime.timedelta(hours=2)
        date_time = now.strftime("%d.%m.%y %H:%M")

        f.write(f"\nlast updated: {date_time}")
        f.write(HTML2)

    # langCode = list(langArray.values())[0]
    # langName = list(langArray.keys())[0]
