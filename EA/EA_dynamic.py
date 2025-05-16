import os
import subprocess
import requests

def get_object_id(file_path):
    """
    Step 1: Get the object ID by replacing the file path in curl command 2.
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
    Step 2: Get dependencies by replacing the object ID in curl command 1.
    """
    url = f"http://10.190.226.42:1248/api/workspaces/BankingDemoWS/ObjectDirectRelationship"
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

def open_in_vscode(file_path):
    """
    Open the specified file in VS Code.
    """
    try:
        subprocess.run(["code", file_path], check=True)
        print(f"Opened {file_path} in Visual Studio Code.")
    except FileNotFoundError:
        print("VS Code is not installed or not added to the system PATH.")
    except Exception as e:
        print(f"Error opening file in VS Code: {e}")

def search_file(file_name, base_directory):
    """
    Search for the file in all subdirectories starting from the base directory.
    """
    for root, dirs, files in os.walk(base_directory):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

def main():
    # Prompt user to enter the file name
    file_name = input("SBANK00P.cbl")

    # Define the base directory to search
    base_directory = r"C:\Users\Administrator.GRT-EA-WDC2\Downloads\Rocket EA\Banking_Demo_Sources"

    # Construct the full file path by searching
    file_path = search_file(file_name, base_directory)

    print(file_path)

    if not file_path:
        print("The specified file does not exist in the directory or its subdirectories. Please check the file name and try again.")
        return

    print(f"File found: {file_path}")

    # Open the file in VS Code
    open_in_vscode(file_path)

    # Fetch object ID and dependencies
    print("Fetching object ID for the given file...")
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