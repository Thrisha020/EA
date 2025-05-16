
import subprocess
import os
import argparse


def open_copybook_in_vscode(file_name,current_dir):
    """
    Open a copybook file in Visual Studio Code by searching in the current working directory and its subdirectories.
    """
    #current_dir = os.getcwd()  
    # Use os.walk to search through all directories and subdirectories
    for root, dirs, files in os.walk(current_dir):
        if file_name in files:
            file_path = os.path.join(root, file_name)  # Full path to the file
            print(f"Found {file_name} at {file_path}")  # Print where the file was found
            subprocess.run(["code", file_path])  # Open the file in VS Code
            return

    print(f"File {file_name} not found in the current directory or any subdirectory.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process repository name and base URL.")
    parser.add_argument("file_name", type=str, help="To open the copybook in the vscode editor")
    parser.add_argument("current_dir", type=str, help="Search the file in the current working directory")
    args = parser.parse_args()

    open_copybook_in_vscode(args.file_name, args.current_dir)


#open_copybook_in_vscode('epsmlis.cpy')


#    python3 open_copybook_ea.py epsmlis.cpy /Users/thrisham/Desktop/cobol_code/EA/MortgageApplication