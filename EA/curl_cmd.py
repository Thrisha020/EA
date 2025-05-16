import requests

# Define the URL and headers
url = "http://10.190.226.42:1248/api/workspaces/BankingDemoWS/ObjectDirectRelationship"
params = {"id": "COBOL|37"}
headers = {"accept": "application/json"}

# Send the GET request
response = requests.get(url, headers=headers, params=params)

# Print the response
if response.status_code == 200:
    print(response.json())  # Prints the response as JSON
else:
    print(f"Error: {response.status_code} - {response.text}")
