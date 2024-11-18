import argparse
from falconpy import Hosts
import os
import subprocess
import requests
from requests.auth import HTTPBasicAuth
import urllib3
from datetime import datetime
import subprocess as sp

# Suppress the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# CrowdStrike API credentials
CLIENT_ID = 'Client ID'
CLIENT_SECRET = 'Client Secret'

# InsightVM API details
BASE_URL = "https://Rapid 7 URL.com:3780/api/3"
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
        return risk_score
    else:
        print(f"Failed to retrieve asset data. Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return "Risk score not available"

def create_report(ticket_number, hostname, risk_score):
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Format the content
    report_content = f"""Server Build – Cyber Team Checklist:

Server Name: {hostname}
1. CrowdStrike Agent- Installed
2. Rapid7 Agent- Installed
3. Validate Vulnerability Posture (R7 Scan) – Risk Score: {risk_score}

Cyber Specialist Name: Enter Your Name Here
Date: {today}
"""
    
    # Define the file name and path
    file_path = f"C:Enter Your own filepath Cyber Security Server Build Final Check {ticket_number}.txt"
    
    # Write the content to the file
    with open(file_path, 'w') as file:
        file.write(report_content)
    
    print(f"Report saved as {file_path}")
    
    # Open the document
    sp.Popen(['notepad.exe', file_path])  # Change 'notepad.exe' to your preferred text editor if needed

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Check server security status.")
    parser.add_argument('ticket_number', type=str, help="The ticket number for the report.")
    parser.add_argument('hostname', type=str, help="The hostname of the server to check.")
    
    # Parse arguments
    args = parser.parse_args()
    ticket_number = args.ticket_number
    hostname = args.hostname
    
    # Check if the asset exists in CrowdStrike
    asset_exists, asset_online = is_asset_in_crowdstrike(hostname)
    
    if asset_exists:
        print(f"The asset with hostname '{hostname}' is in CrowdStrike.")
    else:
        print(f"The asset with hostname '{hostname}' is not in CrowdStrike.")
    
    # Check for the asset in InsightVM and get its risk score
    asset_id = search_asset_by_hostname(hostname)
    risk_score = get_asset_risk_score(asset_id) if asset_id else "N/A"
    
    # Create the report
    create_report(ticket_number, hostname, risk_score)

if __name__ == "__main__":
    main()
