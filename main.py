import os
import csv
from pathlib import Path

# External Packages
try:
    import asyncio
except ImportError:
    os.system("python -m pip install asyncio")
    import asyncio

try:
    from azure.iot.device import IoTHubDeviceClient, Message
    from azure.core.exceptions import AzureError
    from azure.storage.blob import BlobClient, BlobServiceClient, PublicAccess, ContainerClient
except ImportError:
    os.system("python -m pip install azure-iot-device")
    os.system("python -m pip install azure.storage.blob")
    os.system("python -m pip install azure-iothub-device-client")
    from azure.iot.device import IoTHubDeviceClient, Message
    from azure.storage.blob import BlobClient, BlobServiceClient, PublicAccess, ContainerClient
    from azure.core.exceptions import AzureError

try:
    import PySimpleGUI as sg
except ImportError:
    os.system("python -m pip install pysimplegui")
    import PySimpleGUI as sg

# Local Imports
from window import guiWindow


def file_upload(folder_path):

    conn_str = "DefaultEndpointsProtocol=https;AccountName=rockwellhackathon;AccountKey=eTrtH9I+4HkDId0a/lsLxLd0Nt21izryh7LmqAFttL3EbjkVf1iOUFl3NmVixnMnP0b0fKXRpaGE0E7xiERw8g==;EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(
        conn_str=conn_str)

    # Create a container called 'folder_name' and Set the permission so the blobs are public.
    container_name = os.path.basename(folder_path)
    
    # need to do a try catch to handle container already exists error
    blob_service_client.create_container(
        container_name, public_access=PublicAccess.Container)

    """
        # Create Sample folder if it not exists, and create a file in folder Sample to test the upload and download.
        local_path = os.path.expanduser("~/Sample")
        if not os.path.exists(local_path):
            os.makedirs(os.path.expanduser("~/Sample"))
        local_file_name = "test1.csv"
        full_path_to_file = os.path.join(local_path, local_file_name)
    """
    # everything above this line is wokring

    for filename in os.listdir(folder_path):
        path = Path(folder_path) / filename
        
        # checks file extension to only upload .csv type
        if path.suffix == '.csv':
            # Upload the created file, use local_file_name for the blob name
            # need to do a try catch to handle container already exists error
            blob_client = blob_service_client.get_blob_client(
                container=container_name, blob=filename)
            with open(path, "rb") as data:
                blob_client.upload_blob(data)

    # List the blobs in the container
    container = blob_service_client.get_container_client(
        container=container_name)
    generator = container.list_blobs()
    for blob in generator:
        print("\t Blob name: " + blob.name)  # delete this after confirmation


def main():
    # GUI to select folder to upload to the cloud
    folder_path = ""
    try:
        window = guiWindow()
        while True:
            event, values = window.read()
            if values['chosen_folder'] == '':
                continue
            if event == sg.WIN_CLOSED:
                break
            if event == "Continue":
                folder_path = values['chosen_folder']
                break
    except:
        folder_path = ""

    file_upload(folder_path)


if __name__ == "__main__":
    main()
    #loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
