"""
24toCodeHackathon

Copyright © 2020 Joy Cross, Kaitlyn Frickensmith, Brenna Levenick, Brandan Naef

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

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

# find latency and bandwidth

import os
from time import time
import logging
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

from tcp_latency import measure_latency

try:
    from tcp_latency import measure_latency
except ImportError:
    os.system("python -m pip install tcp_latency")
    from tcp_latency import measure_latency

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


def getUploadSpeed(total_seconds, total_number):
    uploadSpeed = total_number / total_seconds
    # log latency metric
    logging.info(f"Latency: {total_seconds/total_number} ms per file")
    
    # log file per s metric
    logging.info(
        f"{total_number} files was uploaded in {total_seconds} amount of seconds")
    logging.info(
        f"Upload Speed: {uploadSpeed} files/second")


def file_upload(folder_path, container_name=""):

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

    total_number = 0
    total_upload_time = 0
    for filename in os.listdir(folder_path):
        path = Path(folder_path) / filename

        # checks file extension to only upload .csv type
        if path.suffix == '.csv':
            # Upload the created file, use local_file_name for the blob name
            # try catch to handle file already exists error
            total_number += 1
            start_time = time()
            try:
                blob_client = blob_service_client.get_blob_client(
                    container=container_name, blob=filename)
                with open(path, "rb") as data:
                    blob_client.upload_blob(data)
                total_upload_time += (time() - start_time)
            except Exception:
                logging.warning(f'Skipping file {filename} due to duplicate')


    # log bandwidth metric
    #s = speedtest.Speedtest()
    #logging.info(f"Bandwidth Upload Speed: {s.upload()/1000000} Mbps")

    # last upload speed 11 files/second
    getUploadSpeed(total_upload_time, total_number)


def main():
    # GUI to select folder to upload to the cloud
    folder_path = ""
    container_name = ""
    log = Path('logging.log')
    if log.exists():
        os.remove(log)
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
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

        file_upload(folder_path, container_name.lower())
    except:
        folder_path = ""


if __name__ == "__main__":
    main()
