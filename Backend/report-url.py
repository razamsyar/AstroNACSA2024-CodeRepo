import requests

API_KEY = '540b085d3aeaaf314c12ae782b31c5b5ae1740db7466c5406bf33b2ab051a63276b540624d9b534e'
URL = 'https://www.abuseipdb.com/api/v2/report'

def report_phishing_ip(api_key, ip_address, categories, comment):
    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }
    data = {
        'ip': ip_address,
        'categories': categories,
        'comment': comment
    }

    response = requests.post(URL, headers=headers, data=data)
    result = response.json()

    if response.status_code == 200:
        print(f"The IP address '{ip_address}' has been reported. Response: {result}")
    else:
        print(f"Failed to report the IP address '{ip_address}'. Status code: {response.status_code}. Response: {result}")

def main():
    ip_address = input("Enter the phishing IP address to report: ").strip()
    categories = '14'  # Category for Phishing
    comment = 'Phishing site detected'
    report_phishing_ip(API_KEY, ip_address, categories, comment)

if __name__ == '__main__':
    main()