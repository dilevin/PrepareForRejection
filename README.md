# Prepare For Rejection

This python script sets up my standard set of files for working on research papers. These are:
1. A Google Drive Folder containing
  - A Related Works Spreadsheet
  - A TODO Google Document
  - A Meeting Slides presentation
  - A Google Jam Whiteboard
2. A github repo entitled paper_{PROJECT_NAME} to store the paper latex. 
   The README.md will contain the link to the google folder. 

## Installation

Prior to running this script for the first time you will need to engage in a small amount of setup:

1. Setup google drive access by following the instructions here: https://developers.google.com/drive/api/v3/quickstart/python
2. (Sometimes) Install pip for python:
    ```sudo easy_install pip``` once python is installed

    **Remember to copy credentials.json to the same directory as start_project.py**
     
3. Install the Google APIs:
    ```pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib```

4. Install PyGitHub:
  ```pip install PyGithub```
  
## Running the script

At the command line:
```python start_project.py {PROJECT_NAME}```

You will be promped for your GitHub username and password.
