from __future__ import print_function
import pickle
import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# github stuff
import getpass
import github
from github import Github
from github import GithubException

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    if len(sys.argv) < 2:
        print("Project name not provided as command line argument, nothing created")
        sys.exit()

    print("Setting up ", sys.argv[1])

    #Create folder in your google drive for the project
    file_metadata = {
        'name': sys.argv[1],
        'mimeType': 'application/vnd.google-apps.folder'
    }

    file = service.files().create(body=file_metadata,
                                  fields='id').execute()
    
    #create related work spreadsheet
    related_metadata = {
        'name': 'Related Work',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents' : [file.get('id')]
    }

    related = service.files().create(body=related_metadata,
                                  fields='id').execute()

    #create todo list
    todo_metadata = {
        'name': 'TODO',
        'mimeType': 'application/vnd.google-apps.document',
        'parents' : [file.get('id')]
    }

    todo = service.files().create(body=todo_metadata,
                                  fields='id').execute()

    #create google slides
    slides_metadata = {
        'name': 'Meeting Slides',
        'mimeType': 'application/vnd.google-apps.presentation',
        'parents' : [file.get('id')]
    }

    slides = service.files().create(body=slides_metadata,
                                  fields='id').execute()


    #create jamboard
    whiteboard_metadata = {
        'name': 'Whiteboard',
        'mimeType': 'application/vnd.google-apps.jam',
        'parents' : [file.get('id')]
    }

    whiteboard = service.files().create(body=whiteboard_metadata,
                                  fields='id').execute()


    #create github repo for paper 
    #github login
    username = raw_input("Github Username:")
    pw = getpass.getpass()
    g = Github(username, pw)
    user = g.get_user() #get user

    repo_name = "paper_"+sys.argv[1]
    user.create_repo(
        repo_name, # name -- string
        "Project Paper Repo", # description -- string
        "", # homepage -- string
        True, # private -- bool
        True, # has_issues -- bool
        True, # has_wiki -- bool
        True, # has_downloads -- bool
        auto_init=True,
        gitignore_template="Python")

    #get the repo 
    repo = user.get_repo(repo_name)
    readme = repo.get_contents("/README.md")


    # update
    repo.update_file(readme.path, "add drive link","[Google Drive Folder](https://drive.google.com/drive/folders/"+file.get('id')+")", readme.sha)


if __name__ == '__main__':
    main()