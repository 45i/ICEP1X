import os
import requests
from ICEDP1X import RunMainLoop
from showMessage import showMsgCustom,showAlert

def update():
  owner = "45i"
  repo = "ICEP1X"
  alert=""
    # Set the API endpoint URL for the repository contents
  urls = [f"https://api.github.com/repos/{owner}/{repo}/contents","https://api.github.com/repos/45i/ICEP1X/contents/ICEP1X?ref=Main"]
  resp=showAlert("Preparing to run Auto-Update, please wait...\n*Application may freeze for some time, while the data is retrieved*")
  if (resp!="Skip Auto-Update"):  
    try:
        
     for i in urls:    # Send a GET request to the API endpoint
        response = requests.get(i)
        # print(response.json())
        log=""
        # Check if the request was successful
        if response.status_code == 200:
            # Get the list of files from the response
            files = response.json()
            # print(files)
            print("Files Found: ")
            # Iterate over every file in the repository

            for file in files:
                if file["name"].endswith(".py"):
                    print(file["name"])
            print("Updating Files...")
            for file in files:
                # Check if the file is a Python file
                if file["name"].endswith(".py"):
                    # Get the content of the file from the response
                    uri = file["html_url"]
                    res = requests.get(uri)
                    # print(res.json())
                    if res.status_code == 200:
                        # Get the content of the file from the response
                        content = res.json()["payload"]["blob"]["rawLines"]
                        # Decode the content from base64 encoding
                        #decoded_content = base64.b64decode(content).decode("utf-8")
            
                        # Get the path of the local file
                        local_path = os.path.join(repo, file["path"].split("/")[-1])
            
                        # Check if the local file exists
                        if os.path.exists(local_path):
                            # Read the contents of the local file
                            with open(local_path, "r+") as f:
                                local_content = f.read().split("\n")
                            
                            # Check if the local file is up-to-date
                            
                                # Write the contents of the remote file to the local file
                            for j in content:
                                f=open(local_path,"a")
                                if j not in local_content:
                                    f.write(j)
                                    f.write("\n")
                            print(f"{local_path} updated")
                            log+=f"{local_path} updated\n"

                            
                        else:
                            # Create the local directory if it does not exist
                            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
                            # Write the contents of the remote file to the local file
                            with open(local_path, "w+") as f:
                                f.writelines(content)
                            print(f"{local_path} created")
                            log+=f"{local_path} created\n"
            alert=f"Auto-Update Completed Successfully!\n{len(log.splitlines())} files updated!"
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code} - {response.json()['message']}")
            alert=f"Error: {response.status_code} - {response.json()['message']}"
     showAlert(alert)
     RunMainLoop() 
    except Exception as e :
        print(f"An Exception Occurred! Auto-Update Failed! \n{e} \nOpening Editor...")
        showAlert(f"An Exception Occurred! Auto-Update Failed! \n{e} \nOpening Editor...")
        RunMainLoop()
  else:
    RunMainLoop()
  
    
