from falconpy import Hosts
import os
import subprocess
import requests
from requests.auth import HTTPBasicAuth
import urllib3

# Suppress the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# CrowdStrike API credentials
CLIENT_ID = 'CLIENT ID'
CLIENT_SECRET = 'SECRET'

# InsightVM API details
BASE_URL = "https://INSIGHTVMADDRESS:3780/api/3"
USERNAME = "Username"
PASSWORD = "Password"

# Initialize the FalconPy Hosts API
hosts_api = Hosts(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

def is_asset_in_crowdstrike(hostname):
    # Query for the host by hostname in CrowdStrike
    response = hosts_api.query_devices_by_filter(filter=f"hostname:'{hostname}'")
    
    # Check if the response is successful and if there are any devices found
    if response["status_code"] == 200:
        resources = response["body"]["resources"]
        if resources:
            # Get the device details
            device_id = resources[0]
            details_response = hosts_api.get_device_details(ids=device_id)
            if details_response["status_code"] == 200:
                device_details = details_response["body"]["resources"][0]
                # Check if the asset is online in CrowdStrike
                is_online = device_details.get("status", "").lower() == "online"
                return True, is_online
            else:
                print(f"Error retrieving device details: {details_response['body']['errors']}")
                return False, None
        else:
            return False, None
    else:
        # Handle API error response
        print(f"Error: {response['body']['errors']}")
        return False, None

def ping_host(hostname, count=4):
    # Determine the ping command based on the operating system
    param = '-n' if subprocess.run('ver', shell=True, stdout=subprocess.PIPE).returncode == 0 else '-c'
    
    try:
        # Run the ping command
        result = subprocess.run(['ping', param, str(count), hostname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Decode the output
        output = result.stdout.decode()
        
        if result.returncode == 0:
            print(f"Ping successful!\n{output}")
        else:
            print(f"Failed to ping {hostname}.\n{output}")
    except Exception as e:
        print(f"An error occurred: {e}")

def search_asset_by_hostname(hostname):
    url = f"{BASE_URL}/assets/search"
    
    # Set the search payload for InsightVM
    payload = {
        "match": "all",
        "filters": [
            {
                "field": "host-name",
                "operator": "is",
                "value": hostname
            }
        ]
    }

    # Perform the POST request to search for the asset in InsightVM
    response = requests.post(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), 
                             json=payload, verify=False)

    if response.status_code == 200:
        data = response.json()
        assets = data.get("resources", [])
        if assets:
            return assets[0]['id']  # Return the first asset's ID
        else:
            print("No assets found for the given hostname.")
            return None
    else:
        print(f"Failed to search for asset. Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def get_asset_risk_score(asset_id):
    url = f"{BASE_URL}/assets/{asset_id}"

    # Perform the GET request with HTTP Basic Auth
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), verify=False)

    if response.status_code == 200:
        data = response.json()
        risk_score = data.get("riskScore", "Risk score not available")
        print(f"Risk Score for asset ID {asset_id}: {risk_score}")
    else:
        print(f"Failed to retrieve asset data. Status Code: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    hostname = input("Enter the hostname to check: ")
    
    # Check if the asset exists in CrowdStrike
    asset_exists, asset_online = is_asset_in_crowdstrike(hostname)
    
    if asset_exists:
        if asset_online:
            print(f"The asset with hostname '{hostname}' is in CrowdStrike and is online.")
        else:
            print(f"The asset with hostname '{hostname}' is in CrowdStrike but is offline.")
        
        # Ping the host
        print("\nAttempting to ping the host...")
        ping_host(hostname)
    else:
        print(f"The asset with hostname '{hostname}' is not in CrowdStrike.")

    # Check for the asset in InsightVM and get its risk score
    asset_id = search_asset_by_hostname(hostname)
    if asset_id:
        get_asset_risk_score(asset_id)
