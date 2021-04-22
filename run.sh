cd $HOME/code/commonVoiceCompetition
python3 mainDE.py
python3 mainEO.py
sleep 2
cd website
git add *.html
git commit -m "automatically updated $(date -u)"
# git push
git push --set-upstream origin gh-pages
