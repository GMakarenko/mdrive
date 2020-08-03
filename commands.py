from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from file_manager import zip_and_crypt, decrypt_and_unzip, delete_file_path

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive()


def send_file(file_path):
    file_name = zip_and_crypt(file_path)
    try:
        print("sending")
        mdrive_file_name = file_name.replace(".zip", "")
        file = drive.CreateFile({"title": mdrive_file_name})
        file.SetContentFile(file_name)
        file.Upload()
        print(f"New mdrive file created: {mdrive_file_name}")
    except Exception:
        print("There was a problem connecting google")
        return
    print(f"Removing local mdrive file")
    delete_file_path(file_name)


def get_file(file_path):
    print(f"getting file {file_path}")
    file_name = decrypt_and_unzip(file_path)
    print(f"New version of: {file_name}")
    print(f"Removing ")
    # delete_file_path(file_name)
    return file_name
