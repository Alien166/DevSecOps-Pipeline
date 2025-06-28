import requests

try:
    response = requests.get("http://localhost:3000/")
    if response.status_code == 200:
        exit(0)
    else:
        exit(1)
except:
    exit(1)
