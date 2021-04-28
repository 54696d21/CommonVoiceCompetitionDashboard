import LangListSpeech
import json
import requests

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

    if len(b) > 0:
        with open("website/new_supported/index.html", "w") as f:
            f.write(str(b))
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

    # langCode = list(langArray.values())[0]
    # langName = list(langArray.keys())[0]
