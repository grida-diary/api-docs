import json
import os
import requests

if len(sys.argv) == 1:
    print("no system arguments")
    exit()

GH_TOKEN = sys.argv[1]

GH_API_BASED_URL = "https://api.github.com"
GH_API_BASED_HEADERS = {
    "Authorization": "Bearer {}".format(GH_TOKEN),
    "X-GitHub-Api-Version": "2022-11-28",
    "Accept": "application/vnd.github+json"
}


def get_recent_issue():
    endpoint = GH_API_BASED_URL + "/repos/grida-diary/api-docs/issues"
    parameters = {"per_page": 1, "page": 1}
    response = requests.get(
        endpoint,
        headers=GH_API_BASED_HEADERS,
        params=parameters
    ).json()

    return response[0]["body"]


def write_swagger_json(issue_body):
    json_data = json.loads(issue_body)

    if os.path.isfile("../swagger.json"):
            os.remove("../swagger.json")

    with open("../swagger.json", "w", encoding="utf-8") as swagger:
        json.dump(json_data, swagger, ensure_ascii=False, indent="\t")


issue = get_recent_issue()
write_swagger_json(issue)