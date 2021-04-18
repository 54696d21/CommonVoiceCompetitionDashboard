cd $HOME/code/commonVoiceCompetition
python3 main.py
sleep 2
cd website
git add index.html
git commit -m "automatically updated $(date -u)"
# git push
git push --set-upstream origin gh-pages
