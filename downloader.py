from urllib.request import urlopen
from datetime import datetime, timezone
import json, base64, zipfile, io

# Grab by API key
with open("legiscan_key.txt", "r") as f:
    api_key = f.read()

# Grab cached info to check for changes
try:
    with open(r"D:\Big Input Data Stuff\LegiScan\input-caches.json", "r") as f:
        last_update_hashes = json.loads(f.read())
except FileNotFoundError:
    SystemExit(1)
    last_update_hashes = {}

# Check if we have a cached version before making api call again
# NOTE: if you are running with the intention of finding new data, delete old list_cache.json
try:
    with open("./list_cache.json", "r") as f:
        list_json_data = json.loads(f.read())
except FileNotFoundError:
    # if we don't have a cached version, make a call again
    list_url = f"https://api.legiscan.com/?key={api_key}&op=getDatasetList"
    list_response = urlopen(list_url)
    list_json_data = json.loads(list_response.read())

    # save for testing, datasetlist is updated weekly so no need to re-call every time
    with open("./list_cache.json", "w") as f:
        f.write(json.dumps(list_json_data))

# Run through the list of all available datasets and check for changes
# If there are changes, redownload that dataset and save to input
for dataset in list_json_data["datasetlist"]:
    current_hash = dataset["dataset_hash"]
    did = f"{dataset['session_id']}"
    if did in last_update_hashes and last_update_hashes[did][0] == current_hash:
        continue
    access = dataset["access_key"]
    dataset_url = f"https://api.legiscan.com/?key={api_key}&op=getDataset&id={did}&access_key={access}"
    response = urlopen(dataset_url)
    json_data = json.loads(response.read())
    b = base64.b64decode(json_data["dataset"]["zip"])
    z = zipfile.ZipFile(io.BytesIO(b))
    z.extractall(r"D:\Big Input Data Stuff\LegiScan\input")
    last_update_hashes[did] = (current_hash, json_data["dataset"]["zip"])

# Write out hashes for change detection
with open("./input-caches.json", "w") as f:
    f.write(json.dumps(last_update_hashes))

with open("./times.txt", "rw") as f:
    old_data = f.readlines()
    if len(old_data) >= 1:
        old_data[
            0
        ] = f"Last download happened at #{datetime.now(timezone.utc).strftime(f'%d/%m/%y %H:%M:%S')}"
    else:
        old_data.append(
            f"Last download happened at #{datetime.now(timezone.utc).strftime(f'%d/%m/%y %H:%M:%S')}"
        )
    f.write(old_data)
