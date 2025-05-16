import requests

# Define the URL and headers
url = "http://10.190.226.42:1248/api/workspaces/BankingDemoWS/ObjectByPath"
params = {
    "path": "C:\\Users\\Administrator.GRT-EA-WDC2\\Downloads\\Rocket EA\\Banking_Demo_Sources\\cobol\\SBANK00P.cbl"
}
headers = {"accept": "application/json"}

# Send the GET request
response = requests.get(url, headers=headers, params=params)

# Check the response and print the result
if response.status_code == 200:
    print("Response JSON:")
    print(response.json())  # Print the JSON response
else:
    print(f"Error: {response.status_code}")
    print(response.text)
