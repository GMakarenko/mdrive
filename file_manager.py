import os
import shutil
import zipfile
from zipfile import ZipFile

from cryptography.fernet import Fernet


def retrieve_file_paths(dir_name):
    file_paths = []

    for root, directories, files in os.walk(dir_name):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)

    return file_paths


def zip_file(file_path):
    file_paths = retrieve_file_paths(file_path)

    print("The following list of files will be zipped:")
    for fileName in file_paths:
        print(fileName)

    file_name = f"{file_path}.zip"
    with zipfile.ZipFile(file_name, "w") as zip_ref:
        for file in file_paths:
            zip_ref.write(file)

    return file_name


def unzip_file(file_path):
    with ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall()
    return file_path


def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    try:
        return open("key.key", "rb").read()
    except FileNotFoundError:
        raise FileNotFoundError("You need to generate a key file")


def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(filename, "wb") as file:
        file.write(decrypted_data)


def delete_file_path(file_path):
    try:
        os.remove(file_path)
    except IsADirectoryError:
        shutil.rmtree(file_path)


def zip_and_crypt(file_path):
    key = load_key()
    file_name = zip_file(file_path)
    encrypt(file_name, key)
    return file_name


def decrypt_and_unzip(file_path):
    key = load_key()
    decrypt(file_path, key)
    file_name = unzip_file(file_path)
    return file_name
