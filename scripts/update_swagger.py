import json
import os
import requests
import sys
import time

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
    with open("./meta-data.json", "r") as meta:
        meta_data = json.load(meta)

        json_data = json.loads(issue_body)
        json_data["info"] = meta_data["info"]
        json_data["info"]["description"] = "last updated : " + time.strftime('%Y-%m-%d %H:%M:%S')
        json_data["servers"] = meta_data["servers"]

        if meta["authorize"]["enable"]:
            json_data["components"]["securitySchemes"] = meta["authorize"]["securitySchemes"]
            json_data["security"] = meta["authorize"]["security"]

        if os.path.isfile("./swagger.json"):
            os.remove("./swagger.json")

        with open("./swagger.json", "w", encoding="utf-8") as swagger:
            json.dump(json_data, swagger, ensure_ascii=False, indent="\t")


issue = get_recent_issue()
write_swagger_json(issue)
