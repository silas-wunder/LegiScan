from urllib.request import urlopen
import json, base64, zipfile, io

# Grab by API key
with open("./key.txt", "r") as f:
    api_key = f.read()

# TODO: check if this works
with open("./input-caches.json", "r") as f:
    last_update_hashes = json.loads(f.read())

# This operation will return a list of all available datasets
list_op = "getDatasetList"

# With dataset list, this will be a for loop that runs for every dataset

list_url = f"https://api.legiscan.com/?key={api_key}&op={list_op}"
list_response = urlopen(list_url)
list_json_data = json.loads(list_response.read())

for dataset in list_json_data["datasetlist"]:
    # TODO: check to see if this works
    current_hash = dataset["dataset_hash"]
    did = dataset["session_id"]
    if last_update_hashes[did][0] == current_hash:
        continue
    access = dataset["access_key"]
    dataset_url = f"https://api.legiscan.com/?key={api_key}&op=getDataset&id={did}&access_key={access}"
    response = urlopen(dataset_url)
    json_data = json.loads(response.read())
    b = base64.b64decode(json_data["dataset"]["zip"])
    z = zipfile.ZipFile(io.BytesIO(b))
    z.extractall("./input/")
    # TODO: check if this works
    last_update_hashes[did] = (current_hash, json_data["dataset"]["zip"])

# TODO: check if this works
with open("./input-caches.json", "w") as f:
    f.write(json.dumps(last_update_hashes))
