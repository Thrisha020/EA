import subprocess
import json


def execute_curl_command(curl_command):
    """
    Executes a given curl command using subprocess and returns the parsed JSON response.
    """
    try:
        # Execute the curl command and capture the output
        result = subprocess.run(curl_command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Check if the command was successful
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"Error executing curl: {result.stderr}")
            raise Exception("Failed to execute curl command.")
    except json.JSONDecodeError:
        raise Exception("Failed to parse JSON response.")


def get_program_id(base_url, workspace, program_path):
    """
    Fetch the unique ID for the COBOL program using the ObjectByPath API via curl.
    """
    curl_command = (
        f"curl -X 'GET' "
        f"'{base_url}/api/workspaces/{workspace}/ObjectByPath?path={program_path}' "
        f"-H 'accept: application/json'"
    )
    print(f"Executing: {curl_command}")
    response = execute_curl_command(curl_command)

    if "id" in response:
        print(f"Program ID: {response['id']}")
        return response["id"]
    else:
        raise ValueError("Program ID not found in the response.")


def get_dependencies(base_url, workspace, program_id):
    """
    Fetch the dependencies of the COBOL program using the ObjectDirectRelationship API via curl.
    """
    curl_command = (
        f"curl -X 'GET' "
        f"'{base_url}/api/workspaces/{workspace}/ObjectDirectRelationship?id={program_id}' "
        f"-H 'accept: application/json'"
    )
    print(f"Executing: {curl_command}")
    return execute_curl_command(curl_command)


def display_dependencies(dependencies):
    """
    Display the list of COPYBOOK dependencies in a user-friendly format.
    """
    print("\nDependencies (COPYBOOK files):")
    for dep in dependencies:
        if dep.get("type") == "COPYBOOK":
            print(f"- {dep.get('name')}")
    print("\nEnd of dependency list.")


def main():
    # Configuration
    base_url = "http://10.190.226.42:1248"
    workspace = "BankingDemoWS"
    program_path = "C:\Users\Administrator.GRT-EA-WDC2\Downloads\Rocket EA\MortgageAppllication-main"  # Update this path on your system

    try:
        # Step 1: Get Program ID
        program_id = get_program_id(base_url, workspace, program_path)

        # Step 2: Get Dependencies
        dependencies = get_dependencies(base_url, workspace, program_id)

        # Step 3: Display Dependencies
        display_dependencies(dependencies)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
