import random
import json
from github import Github


def loadOptions(goptions = {}):
    try:
        with open('options.json', 'r') as f:
            options = json.load(f)
            for k in options:
                setattr(goptions, k, options[k])
    except:
        print("Error loading options.json")
    return goptions

def main():
    goptions = loadOptions
    g = Github(goptions['github_access_token'])
    repo = g.get_repo(goptions['github_ca_backend_repo'])
    contents = repo.get_contents("proposals.json", ref="test")

    test_content = {
        id: random.randrange(1, 100),
        assessments: random.randrange(1, 5)
    }

    repo.update_file(contents.path, "Update assessments count", json.dumps(test_content), contents.sha)
