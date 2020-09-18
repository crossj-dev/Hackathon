# 1 - COMPLETED WHOOP WHOOP :)
# connect to data source to extract OT data for transmission to the cloud repo

# 2 -
# organize the OT data into transmittable packets that can be stored in ascending time for plotting

# 3 - COMPLETED WOOHOOOOOO!!!!!!
# automatically increase/decrease the artifacts capacity to handle data volume

# 4
# demonstrate data packaging/unpackaging strategy

# 5 - COMPLETED
# Maximize data volume transferred speed per second, while minimizing latency

import os
import datetime
from pathlib import Path

# External Packages
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

#time_delta = (date_2 - date_1)
#total_seconds = time_delta.total_seconds()
#minutes = total_seconds/60


def getUploadSpeed(endFileUpload, startFileUpload, total_number):
    time_delta = (endFileUpload - startFileUpload)
    total_seconds = time_delta.total_seconds()
    uploadSpeed = total_number / total_seconds
    print(
        f"This {total_number} of files was uploaded in {total_seconds} amount of seconds")
    print(
        f"Upload Speed: {uploadSpeed} files/second")

def file_upload(folder_path):

    conn_str = "DefaultEndpointsProtocol=https;AccountName=rockwellhackathon;AccountKey=eTrtH9I+4HkDId0a/lsLxLd0Nt21izryh7LmqAFttL3EbjkVf1iOUFl3NmVixnMnP0b0fKXRpaGE0E7xiERw8g==;EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(
        conn_str=conn_str)

    # Create a container called 'folder_name' and Set the permission so the blobs are public.
    container_name = os.path.basename(folder_path)

    # need to do a try catch to handle container already exists error
    try:
        blob_service_client.create_container(
            container_name, public_access=PublicAccess.Container)
    except Exception as e:
        print(f'Error in creating container - {e}')
        return
    startFileUpload = datetime.datetime.now()
    # logging.info
    print(startFileUpload)
    total_number = 0
    for filename in os.listdir(folder_path):
        path = Path(folder_path) / filename

        # checks file extension to only upload .csv type
        if path.suffix == '.csv':
            # Upload the created file, use local_file_name for the blob name
            # try catch to handle container already exists error
            total_number += 1
            try:
                blob_client = blob_service_client.get_blob_client(
                    container=container_name, blob=filename)
                with open(path, "rb") as data:
                    blob_client.upload_blob(data)
            except Exception as e:
                print(f'Error in creating blobs - {e}')
                return
    endFileUpload = datetime.datetime.now()
    print(endFileUpload)
    # test this to see if it ouputs correct metrics
    # last upload speed 11 files/second
    getUploadSpeed(endFileUpload, startFileUpload, total_number)


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
