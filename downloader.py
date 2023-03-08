from urllib.request import urlopen
import json, base64, zipfile, io

# Grab by API key
with open("./key.txt", "r") as f:
    api_key = f.read()

# Determine what operation we'll be doing
# In this case, CO's 2020 Regular Session
operation = "getDataset&id=1722&access_key=V4WfLj8mr7zu5xRrz8T2O"

# Ping the API with my key and the operation, then save the response
url = f"https://api.legiscan.com/?key={api_key}&op={operation}"
response = urlopen(url)
json_data = json.loads(response.read())

# Grab the encoded zip file from the response data and turn it into our actual input
b = base64.b64decode(json_data["dataset"]["zip"])
z = zipfile.ZipFile(io.BytesIO(b))
z.extractall("./input/")
