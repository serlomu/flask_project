from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Authenticate and create the PyDrive client
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth)

# Path to the file you want to upload
file_path = 'bert_model/tf_model.h5'

# Create & upload a file
gfile = drive.CreateFile({'title': 'tf_model.h5'})
gfile.SetContentFile(file_path)
gfile.Upload()

print('File uploaded successfully.')
