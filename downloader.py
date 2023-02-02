from urllib.request import urlopen
import json, base64, zipfile, os

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

# Grab the encoded zip file from the response data
zip_encoded = json_data["dataset"]["zip"]

# Turn the encoded zip file into an actual file
with open("./output.zip", "wb") as f:
    f.write(base64.b64decode(zip_encoded))

# Unzip the file into our input folder
with zipfile.ZipFile("./output.zip", "r") as f:
    f.extractall("./input/")

# Clean up after ourselves
dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(dir_path, "output.zip")
os.remove(path)
