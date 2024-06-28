import requests
import json
import time

API_KEY = '25908485d1d7ca338d0e1427d00801a2180bc0090d165a60df8ce2703b88a697'

def print_analysis_stats(stats):
    if stats is None:
        print("VirusTotal: No last analysis stats available.")
    else:
        print(f"VirusTotal: URL is marked malicious {stats['malicious']} times.")
        print(f"VirusTotal: URL is undetected by {stats['undetected']} scanners.")
        print(f"VirusTotal: URL is marked harmless by {stats['harmless']} scanners.")
        print(f"VirusTotal: URL is marked suspicious by {stats['suspicious']} scanners.")
        print(f"VirusTotal: URL timed out on {stats['timeout']} scanners.")

def check_virustotal_url(url, api_key):
    headers = {'x-apikey': api_key}
    response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url}", headers=headers)
    data = json.loads(response.text)

    if response.status_code == 200:
        attributes = data['data']['attributes']
        stats = attributes['stats']
        print_analysis_stats(stats)
    elif response.status_code == 404:
        headers = {'x-apikey': api_key, 'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data=f"url={url}")
        data = json.loads(response.text)

        if response.status_code == 200:
            data_id = data['data']['id']
            print(f"VirusTotal: URL submitted for analysis. ID: {data_id}")

            # Store the ID of the URL scan
            url_scan_id = data_id

            # Wait for the scan to complete
            print("Waiting for the scan to complete...")
            while True:
                time.sleep(30)
                response = requests.get(f"https://www.virustotal.com/api/v3/analyses/{url_scan_id}", headers=headers)
                data = json.loads(response.text)
                if response.status_code == 200:
                    attributes = data['data']['attributes']
                    stats = attributes['stats']
                    if attributes['status'] == 'completed':
                        print("Scan completed.")
                        print_analysis_stats(stats)
                        break
                    else:
                        print("Scan in progress. Checking again in 30 seconds.")
                else:
                    print(f"VirusTotal: Error occurred. Status code: {response.status_code}. Message: {data['error']['message']}")
                    break
        else:
            print(f"VirusTotal: Error occurred. Status code: {response.status_code}. Message: {data['error']['message']}")
    else:
        print(f"VirusTotal: Error occurred. Status code: {response.status_code}. Message: {data['error']['message']}")

def main():
    url = input("Enter the URL to check: ").strip()
    check_virustotal_url(url, API_KEY)

if __name__ == '__main__':
    main()