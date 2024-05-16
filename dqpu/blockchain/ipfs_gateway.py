# Copyright 2024 Davide Gessa

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import subprocess

import requests


def start_ipfs_daemon():
    try:
        # Launch the IPFS daemon
        ipfs_process = subprocess.Popen(["ipfs", "daemon"])
        print("IPFS daemon started successfully.")
        return ipfs_process
    except FileNotFoundError:
        print(
            "IPFS executable not found. Please install IPFS first: "
            "https://docs.ipfs.tech/install/command-line/#install-official-binary-distributions"
        )
    except Exception as e:
        print(f"An error occurred while starting the IPFS daemon: {e}")


def stop_ipfs_daemon(ipfs_process):
    ipfs_process.terminate()


class IPFSGateway:
    def __init__(self, uri="http://localhost:5001", gateway="http://127.0.0.1:8080"):
        self.gateway = gateway
        self.uri = uri

    def upload(self, file_path):
        url = self.uri + "/api/v0/add"

        with open(file_path, "rb") as file:
            files = {"file": file}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            ipfs_hash = response.text
            return json.loads(ipfs_hash)["Hash"]
        else:
            print(f"Error adding file to IPFS: {response.text}")

    def get(self, ipfs_hash, destination_file=None, timeout=60):
        # Set the URL for the IPFS daemon
        url = self.gateway + "/ipfs/"

        # Send a GET request to the IPFS daemon with the IPFS hash
        response = requests.get(f"{url}/{ipfs_hash}", timeout=timeout)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the file content
            file_content = response.content

            if destination_file:
                with open(destination_file, "wb") as file:
                    file.write(file_content)
            return file_content
        else:
            print(f"Error retrieving file from IPFS: {response.text}")
