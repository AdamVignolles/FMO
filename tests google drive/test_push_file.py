import os
import pickle
import google.auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# Define your file and folder details
file_path = 'test.txt'
folder_id = 'your-folder-id'

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

# Upload the file
file_metadata = {'name': os.path.basename(file_path)}
media = MediaFileUpload(file_path, mimetype='application/octet-stream')
file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

# get the file back

file_id = file.get('id')
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


print(f"File uploaded successfully! File ID: {file.get('id')}")