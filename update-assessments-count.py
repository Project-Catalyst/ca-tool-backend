import random
import json
import requests
from github import Github


def loadOptions(goptions = {}):
    try:
        with open('./options.json', 'r') as f:
            options = json.load(f)
            for k in options:
                goptions[k] = options[k]
    except Exception as e:
        print(e)
        print("Error loading options.json")
    return goptions

def getAssessmentsCount(goptions):
    headers = {
        'api_token': goptions["ideascale_api_token"]
    }
    ideas = []
    for funnelStage in goptions["assess_funnel_stage_ids"]:
        url = goptions["ideascale_base_api_url"] + \
            goptions["assess_funnel_endpoint"].format(funnelStage)

        print("Requesting url: {}".format(url))
        r = requests.get(url, headers=headers)
        response = r.json()
        for idea in response:
            ideas.append({
                "id": idea['ideaId'],
                "assessments_count": idea['noOfAccessors']
            })
    return ideas

def main():
    goptions = loadOptions()
    ideas = getAssessmentsCount(goptions)
    if (len(ideas)):
        try:
            g = Github(goptions['github_access_token'])
            repo = g.get_repo(goptions['github_ca_backend_repo'])
            contents = repo.get_contents("proposals.json")
            with open('proposals.json', 'w') as outfile:
                json.dump(ideas, outfile)
            repo.update_file(contents.path, "Update assessments count", json.dumps(ideas), contents.sha)
        except Exception as e:
            print(e)

main()
