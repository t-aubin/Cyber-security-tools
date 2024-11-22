# To run 'python script.py <ticket_number> <hostname> <client_secret> <password>'

import argparse
from falconpy import Hosts
import requests
from requests.auth import HTTPBasicAuth
import urllib3
from datetime import datetime

# Suppress the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# InsightVM API details
BASE_URL = "BASE URL"
USERNAME = "USERNAME"

def is_asset_in_crowdstrike(hosts_api, hostname):
    # Query for the host by hostname in CrowdStrike
    response = hosts_api.query_devices_by_filter(filter=f"hostname:'{hostname}'")
    
    if response["status_code"] == 200:
        resources = response["body"]["resources"]
        if resources:
            # Get the device details
            device_id = resources[0]
            details_response = hosts_api.get_device_details(ids=device_id)
            if details_response["status_code"] == 200:
                device_details = details_response["body"]["resources"][0]
                is_online = device_details.get("status", "").lower() == "online"
                return True, is_online
            else:
                print(f"Error retrieving device details: {details_response['body']['errors']}")
                return False, None
        else:
            return False, None
    else:
        print(f"Error: {response['body']['errors']}")
        return False, None

def search_asset_by_hostname(hostname, password):
    url = f"{BASE_URL}/assets/search"
    
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

    response = requests.post(url, auth=HTTPBasicAuth(USERNAME, password), 
                             json=payload, verify=False)

    if response.status_code == 200:
        data = response.json()
        assets = data.get("resources", [])
        if assets:
            return assets[0]['id']
        else:
            print("No assets found for the given hostname.")
            return None
    else:
        print(f"Failed to search for asset. Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def get_asset_risk_score(asset_id, password):
    url = f"{BASE_URL}/assets/{asset_id}"

    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, password), verify=False)

    if response.status_code == 200:
        data = response.json()
        risk_score = data.get("riskScore", "Risk score not available")
        return risk_score
    else:
        print(f"Failed to retrieve asset data. Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return "Risk score not available"

def create_report(ticket_number, hostname, risk_score, crowdstrike_status):
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Adjust status for CrowdStrike agent
    cs_agent_status = "Installed" if crowdstrike_status else "N/A"
    
    report_content = f"""Server Build – Cyber Team Checklist:

Server Name: {hostname}
1. CrowdStrike Agent- {cs_agent_status}
2. Rapid7 Agent- Installed
3. Validate Vulnerability Posture (R7 Scan) – Risk Score: {risk_score}

Cyber Specialist Name: YOUR NAME HERE
Date: {today}
"""
    
    file_path = rf"C:\Users\$USERNAME\Documents\Cyber Security Server Build Final Check {ticket_number}.txt"
    
    with open(file_path, 'w') as file:
        file.write(report_content)
    
    print(f"Report saved as {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Check server security status.")
    parser.add_argument('ticket_number', type=str, help="The ticket number for the report.")
    parser.add_argument('hostname', type=str, help="The hostname of the server to check.")
    parser.add_argument('client_secret', type=str, help="The CrowdStrike API client secret.")
    parser.add_argument('password', type=str, help="The InsightVM API password.")
    
    args = parser.parse_args()
    ticket_number = args.ticket_number
    hostname = args.hostname
    client_secret = args.client_secret
    password = args.password

    hosts_api = Hosts(client_id="CLIENT ID", client_secret=client_secret)

    asset_exists, asset_online = is_asset_in_crowdstrike(hosts_api, hostname)
    
    if asset_exists:
        print(f"The asset with hostname '{hostname}' is in CrowdStrike.")
    else:
        print(f"The asset with hostname '{hostname}' is not in CrowdStrike.")
    
    asset_id = search_asset_by_hostname(hostname, password)
    risk_score = get_asset_risk_score(asset_id, password) if asset_id else "N/A"
    
    create_report(ticket_number, hostname, risk_score, asset_exists)

if __name__ == "__main__":
    main()
