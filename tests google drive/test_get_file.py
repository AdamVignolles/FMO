import os
import pickle
import google.auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# Set up authentication and authorization
creds = None
SCOPES = ['https://www.googleapis.com/auth/drive.file']

if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

service = build('drive', 'v3', credentials=creds)
# get the file back

file_id = "1F9IXR--E5cDQpnrIW92yoD39oHRGICnK"
request = service.files().get_media(fileId=file_id)
file = service.files().get(fileId=file_id).execute()

# Download the file
request = service.files().get_media(fileId=file_id)
file = service.files().get(fileId=file_id).execute()
fh = open('test_get.txt', 'wb')
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print(f"Download {int(status.progress() * 100)}.")
fh.close()