import base64import osimport requestsfrom ICEDP1X import RunMainLoopfrom showMessage import showAlert# Set the repository owner and nameowner = "45i"repo = "ICEP1X"# Set the API endpoint URL for the repository contentsurl = f"https://api.github.com/repos/{owner}/{repo}/contents"showAlert("Running Auto-Update, please wait...\n*Application may freeze for some time, while the data is retrieved*","Ok, I'll wait")try:# Send a GET request to the API endpoint    response = requests.get(url)    # print(response.json())        # Check if the request was successful    if response.status_code == 200:        # Get the list of files from the response        files = response.json()            # Iterate over every file in the repository        for file in files:         print(file["name"])            # Check if the file is a Python file         if file["name"].endswith(".py"):                # Get the content of the file from the response            uri = file["html_url"]            res = requests.get(uri)            print(res.json())             if response.status_code == 200:        # Get the content of the file from the response                content = res.json()["blob"]["rawLines"]                # Decode the content from base64 encoding                decoded_content = base64.b64decode(content).decode("utf-8")                    # Get the path of the local file                local_path = os.path.join(repo, file["path"])                    # Check if the local file exists                if os.path.exists(local_path):                    # Read the contents of the local file                    with open(local_path, "r") as f:                        local_content = f.read()                        # Check if the local file is up-to-date                    if local_content == decoded_content:                        print(f"{local_path} is up-to-date")                    else:                        # Write the contents of the remote file to the local file                        with open(local_path, "w") as f:                            f.write(decoded_content)                        print(f"{local_path} updated")                else:                    # Create the local directory if it does not exist                    os.makedirs(os.path.dirname(local_path), exist_ok=True)                        # Write the contents of the remote file to the local file                    with open(local_path, "w") as f:                        f.write(decoded_content)                    print(f"{local_path} created")    else:        # Print an error message if the request was not successful        print(f"Error: {response.status_code} - {response.json()['message']}")    RunMainLoop()except Exception as e :    showAlert("An Exception Occurred! Auto-Update Failed! \nOpening Editor...")    RunMainLoop()