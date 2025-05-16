import os
import requests

def get_object_id(file_path):
    """
    Step 1: Get the object ID by replacing the file path in the API request.
    """
    url = "http://10.190.226.42:1248/api/workspaces/BankingDemoWS/ObjectByPath"
    params = {
        "path": file_path
    }
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        object_id = result.get("id")  # Assuming the response has an 'id' field
        return object_id
    else:
        print(f"Error getting object ID: {response.status_code}")
        print(response.text)
        return None


def get_dependencies(object_id):
    """
    Step 2: Get dependencies by replacing the object ID in the API request.
    """
    url = "http://10.190.226.42:1248/api/workspaces/BankingDemoWS/ObjectDirectRelationship"
    params = {"id": object_id}
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        dependencies = response.json()
        return dependencies
    else:
        print(f"Error getting dependencies: {response.status_code}")
        print(response.text)
        return None


def display_dependencies(dependencies):
    """
    Step 3: Display dependencies in a chat-like format.
    """
    print("Chat: Please find the list of dependency code:")
    for dep in dependencies:
        print(f"{dep['name']} (Type: {dep['type']}, Relation: {dep['relation']})")


def main():
    # Base directory for the file path (replace with your base path)
    base_path = r"C:\Users\Administrator.GRT-EA-WDC2\Downloads\Rocket EA\Banking_Demo_Sources\cobol"
    

    file_name = input("Please enter the COBOL file name: ")
    
    
    file_path = os.path.join(base_path, file_name)
    
    
    file_path = os.path.normpath(file_path)
    

    file_path = file_path.replace("/", "\\")

    # Display the constructed file path (for debugging purposes)
    print(f"Constructed file path: {file_path}")
    
    # Check if the file path exists
    # if not os.path.exists(file_path):
    #     print(f"Error: The file '{file_name}' does not exist at the specified path.")
    #     return
    
    print(f"Fetching object ID for the given file '{file_name}'...")
    object_id = get_object_id(file_path)
    
    if object_id:
        print(f"Object ID retrieved: {object_id}")
        print("Fetching dependencies...")
        
        dependencies = get_dependencies(object_id)
        if dependencies:
            display_dependencies(dependencies)
        else:
            print("No dependencies found.")
    else:
        print("Failed to retrieve object ID.")


if __name__ == "__main__":
    main()
