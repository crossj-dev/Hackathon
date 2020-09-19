"""
    24toCodeHackathon

    Copyright © 2020 Joy Cross, Kaitlyn Frickensmith, Brenna Levenick, Brandan Naef

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
from os import listdir
from os.path import isfile, join
from time import time
import logging
from pathlib import Path
import concurrent

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
    import speedtest
except ImportError:
    os.system("python -m pip install speedtest-cli")
    import speedtest

try:
    import PySimpleGUI as sg
except ImportError:
    os.system("python -m pip install pysimplegui")
    import PySimpleGUI as sg

# Local Imports
from window import guiWindow


def logMetrics(total_seconds, total_number, total_bytes_transferred):
    uploadSpeed = total_number / total_seconds 
    normalizedUploadSpeed = (total_bytes_transferred / total_seconds)/1000
    
    # log file per s metric
    logging.info(
        f"{total_bytes_transferred} bytes was uploaded in {total_seconds} amount of seconds")
    logging.info(
        f"{total_number} files was uploaded in {total_seconds} amount of seconds")
    logging.info(
        f"Upload Speed: {uploadSpeed} files/second")
    logging.info(
        f"Normalized Upload Rate: {normalizedUploadSpeed} KB/s")

def upload_to_azure(folder_path, container_name=""):

    conn_str = "DefaultEndpointsProtocol=https;AccountName=rockwellhackathon;AccountKey=eTrtH9I+4HkDId0a/lsLxLd0Nt21izryh7LmqAFttL3EbjkVf1iOUFl3NmVixnMnP0b0fKXRpaGE0E7xiERw8g==;EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(
        conn_str=conn_str)

    # Create a container called 'folder_name' and Set the permission so the blobs are public.
    if container_name == "":
        container_name = os.path.basename(folder_path)

    # try catch to handle container already exists error
    try:
        blob_service_client.create_container(
            container_name, public_access=PublicAccess.Container)
    except Exception:
        pass

    files_to_upload = [f for f in listdir(folder_path) if isfile(Path(folder_path) / f) and Path(f).suffix == '.csv']
    
    total_bytes_transferred = 0
    for f in files_to_upload:
        total_bytes_transferred += os.path.getsize(Path(folder_path) / f)

    total_number = len(files_to_upload)

    # inner method for file upload
    def upload_file(filename):
        try:
            blob_client = blob_service_client.get_blob_client(
                container=container_name, blob=filename)
            with open((Path(folder_path) / filename), "rb") as data:
                blob_client.upload_blob(data)
        except Exception:
            logging.warning(f'Skipping file {filename} due to duplicate')

    # multi-threading 
    start_time = time()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)
    futures = [executor.submit(upload_file, filename) for filename in files_to_upload]
    concurrent.futures.wait(futures)
    total_upload_time = time() - start_time

    logMetrics(total_upload_time, total_number, total_bytes_transferred)


def main():
    # GUI to select folder to upload to the cloud
    folder_path = ""
    container_name = ""
    log = Path('logging.log')
    if log.exists():
        os.remove(log)
    logging.basicConfig(filename='logging.log',format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('NEW RUN OF FILE')

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
                container_name = values['container_name_user']
                break

        # log bandwidth metric
        #s = speedtest.Speedtest()
        #print(f"Bandwidth Upload Speed: {s.upload()/1000} KB/s")

        upload_to_azure(folder_path, container_name.lower())
    except:
        folder_path = ""


if __name__ == "__main__":
    main()
