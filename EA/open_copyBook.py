# import os
# import subprocess
# import requests

# def get_object_id(file_path):
#     """
#     Step 1: Get the object ID by replacing the file path in curl command 2.
#     """
#     url = "http://10.190.226.42:1248/api/workspaces/BankingDemoWS/ObjectByPath"
#     params = {
#         "path": file_path
#     }
#     headers = {"accept": "application/json"}

#     response = requests.get(url, headers=headers, params=params)
#     if response.status_code == 200:
#         result = response.json()
#         object_id = result.get("id")  # Assuming the response has an 'id' field
#         return object_id
#     else:
#         print(f"Error getting object ID: {response.status_code}")
#         print(response.text)
#         return None

# def get_dependencies(object_id):
#     """
#     Step 2: Get dependencies by replacing the object ID in curl command 1.
#     """
#     url = f"http://10.190.226.42:1248/api/workspaces/BankingDemoWS/ObjectDirectRelationship"
#     params = {"id": object_id}
#     headers = {"accept": "application/json"}

#     response = requests.get(url, headers=headers, params=params)
#     if response.status_code == 200:
#         dependencies = response.json()
#         return dependencies
#     else:
#         print(f"Error getting dependencies: {response.status_code}")
#         print(response.text)
#         return None

# def display_dependencies_and_open(dependencies, base_directory):
#     """
#     Step 3: Display dependencies and open them in VS Code if found.
#     """
#     print("Chat: Please find the list of dependency code:")
#     for dep in dependencies:
#         print(f"{dep['name']} (Type: {dep['type']}, Relation: {dep['relation']})")
#         file_name = dep['name']
#         file_path = search_file(file_name, base_directory)
#         if file_path:
#             print(f"Opening {file_name} in Visual Studio Code...")
#             open_in_vscode(file_path)
#         else:
#             print(f"File {file_name} not found in {base_directory}.")

# def open_in_vscode(file_path):
#     """
#     Open the specified file in VS Code.
#     """
#     try:
#         subprocess.run(["code", file_path], check=True)
#     except FileNotFoundError:
#         print("VS Code is not installed or not added to the system PATH.")
#     except Exception as e:
#         print(f"Error opening file in VS Code: {e}")

# def search_file(file_name, base_directory):
#     """
#     Search for the file in all subdirectories starting from the base directory.
#     """
#     for root, dirs, files in os.walk(base_directory):
#         if file_name in files:
#             return os.path.join(root, file_name)
#     return None

# def main():
#     # File path for Hello.cbl (replace with your desired file)
#     base_directory = r"C:\Users\Administrator.GRT-EA-WDC2\Downloads\Rocket EA\Banking_Demo_Sources"
#     file_path = os.path.join(base_directory, "cobol", "SBANK00P.cbl")
    

#     print("Fetching object ID for the given file...")
#     object_id = get_object_id(file_path)

#     if object_id:
#         print(f"Object ID retrieved: {object_id}")
#         print("Fetching dependencies...")

#         dependencies = get_dependencies(object_id)
#         if dependencies:
#             display_dependencies_and_open(dependencies, base_directory)
#         else:
#             print("No dependencies found.")
#     else:
#         print("Failed to retrieve object ID.")

# if __name__ == "__main__":
#     main()

import os
import requests
import subprocess

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


# def open_copybook_in_vscode(file_name):
#     """
#     Open a copybook file in Visual Studio Code, searching in the current working directory.
#     """
#     current_dir = os.getcwd()  # Get the current working directory
#     file_path = os.path.join(current_dir, file_name)  # Look for the file in the current directory

#     if os.path.exists(file_path):
#         subprocess.run(["code", file_path])  # Open the file in VS Code
#     else:
#         print(f"File not found in the current working directory: {file_path}")

def open_copybook_in_vscode(file_name):
    """
    Open a copybook file in Visual Studio Code by searching in the current working directory and its subdirectories.
    """
    current_dir = os.getcwd()  # Get the current working directory

    # Use os.walk to search through all directories and subdirectories
    for root, dirs, files in os.walk(current_dir):
        if file_name in files:
            file_path = os.path.join(root, file_name)  # Full path to the file
            print(f"Found {file_name} at {file_path}")  # Print where the file was found
            subprocess.run(["code", file_path])  # Open the file in VS Code
            return

    print(f"File {file_name} not found in the current directory or any subdirectory.")

def display_dependencies(dependencies, base_path):
    """
    Step 3: Display dependencies and optionally open copybooks in Visual Studio Code.
    """
    print("Chat: Please find the list of dependency code:")
    for dep in dependencies:
        print(f"{dep['name']} (Type: {dep['type']}, Relation: {dep['relation']})")
        # Automatically open copybooks in VS Code
        if dep['type'] == "COPYBOOK":
            open_copybook_in_vscode(dep['name'])



def main():
  
    base_path = r"C:\Users\Administrator.GRT-EA-WDC2\Downloads\Rocket EA\Banking_Demo_Sources\copybook"
    #base_path = r"C:\Users\Administrator.GRT-EA-WDC2\Downloads\Rocket EA\Banking_Demo_Sources\cobol"

    file_name = input("Please enter the COBOL file name: ")
    
    
    file_path = os.path.join(base_path, file_name)
    
    
    file_path = os.path.normpath(file_path)
    

    file_path = file_path.replace("/", "\\")

    # Display the constructed file path (for debugging purposes)
    print(f"Constructed file path: {file_path}")
   

    print(f"Fetching object ID for the given file '{file_name}'...")
    object_id = get_object_id(file_path)

    if object_id:
        print(f"Object ID retrieved: {object_id}")
        print("Fetching dependencies...")

        dependencies = get_dependencies(object_id)
        if dependencies:
            display_dependencies(dependencies, base_path)
        else:
            print("No dependencies found.")
    else:
        print("Failed to retrieve object ID.")


if __name__ == "__main__":
    main()


# SBANK00P.cbl

#epsmlis.cpy


#  MBANKZZ.cpy