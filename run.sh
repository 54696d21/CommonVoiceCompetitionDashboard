cd $HOME/code/commonVoiceCompetition
python3 mainDE.py
python3 mainEO.py
cp templates/rootIndex.html website/index.html
sleep 2
cd website
git add *
git commit -m "automatically updated $(date -u)"
git push
# git pull
#git push --set-upstream origin gh-pages
# git push -f origin gh-pages
