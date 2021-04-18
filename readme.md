# Contributors ranking

this script is used to periodically generate a webpage with a dashboard for the German voice competition we'll run in May 2021

it is easily adaptable to any language Common Voice supports by setting the variable `LANG ` to the right language code

participants need to be enrolled by adding their names to the `enrolledContributors` list in `enrolledContributors.py`

the `run.sh` is periodically run to update the website. The `init.sh` is a rough guide how to setup the git repository the webpage will be pushed to. It's currently hosted on github pages.

currently hosted at 54696d21.github.io/commonVoiceGermanCompetiton
