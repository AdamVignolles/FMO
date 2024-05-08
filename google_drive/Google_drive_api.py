# Author : Adam Vignolles
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload


class google_drive_api():
    '''Class to manage the google drive api'''
    def __init__(self) -> None:
        '''Constructor of the class, it initialize the scopes and the credentials of the api'''
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive.metadata']
        self.creds = self.Creds()

    def Creds(self) -> Credentials:
        '''Function to get the credentials of the api'''
        creds = None
        try : 
            if os.path.exists("google_drive/token.json"):
                creds = Credentials.from_authorized_user_file("google_drive/token.json", self.SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file("google_drive/credentials.json", self.SCOPES)
                    creds = flow.run_local_server(port=0)
                with open("google_drive/token.json", "w") as token:
                    token.write(creds.to_json())
            return creds
        except Exception as e:
            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
                    creds = flow.run_local_server(port=0)
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
            return creds
    
    def search_file(self) -> list:
        '''Function to search a file in the google drive'''
        try:
            service = build("drive", "v3", credentials=self.creds)
            results = (
                service.files()
                .list(
                    q="mimeType='text/plain' and trashed=false",
                    pageSize=10, 
                    fields="nextPageToken, files(id, name)"
                )
                .execute()
            )
            items = results.get("files", [])
            if not items:
                print("No files found.")
                return

            return items
        
        except HttpError as error:
            print(f"An error occurred: {error}")

    def search_file_by_name(self, file_name) -> list:
        '''Function to search a file by name in the google drive'''
        try:
            service = build("drive", "v3", credentials=self.creds)
            files = []
            page_token = None
            while True:
                response = (
                    service.files()
                    .list(
                        q=f"name='{file_name}' and trashed=false",
                        spaces="drive",
                        fields="nextPageToken, files(id, name)",
                        pageToken=page_token,
                    )
                    .execute()
                )
                return response.get("files", [])
                
        except HttpError as error:
            print(f"An error occurred: {error}")

    def upload_file(self, file_path: str) -> str:
        '''Function to upload a file in the google drive'''
        try:
            service = build('drive', 'v3', credentials=self.creds)
            file_metadata = {'name': os.path.basename(file_path)}
            media = MediaFileUpload(file_path, mimetype='application/octet-stream')
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            
            return f"File uploaded successfully! File ID: {file.get('id')}"
        
        except HttpError as error:
            print(f"An error occurred: {error}")

    def download_file(self, file_id:int, destination=None) -> bool:
        '''Function to download a file from the google drive'''
        try:
            service = build('drive', 'v3', credentials=self.creds)
            request = service.files().get_media(fileId=file_id)
            file = service.files().get(fileId=file_id).execute()
            if destination is None:
                destination = file.get("name")
            fh = open(destination, "wb")
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}.")
            fh.close()
            return True
        except HttpError as error:
            print(f"An error occurred: {error}")

if __name__ == "__main__":
    gda = google_drive_api()
    print(gda.search_file())
    print(gda.search_file_by_name('music.mp3'))
    #print(gda.upload_file('../music.mp3'))
    print(gda.download_file("1nEqo4YTRiKEfYsKPwc2Wj0J2dNtsqPI-"))
    