if [ -e "bandit_baseline_results.html" ]
then
    echo "File 'bandit_baseline_results.html' already exists!"
    exit 1
fi

rm _bandit_baseline_run.json_

# get the current branch name
ORIGINAL_BRANCH=`git rev-parse --abbrev-ref HEAD`

# find the commit ID of the parent commit
PARENT_ID=`git log -2 --first-parent --pretty=oneline | cut -d " " -f1 | sed -n 2p`

# checkout parent branch
git checkout $PARENT_ID

# run Bandit baseline with whatever paremeters were passed
bandit $@ -f json -o _bandit_baseline_run.json_

# run Bandit on original branch and generate baseline results
git checkout $ORIGINAL_BRANCH
bandit $@ -b _bandit_baseline_run.json_ -f html -o bandit_baseline_results.html

