import requests

print("Enter IP:")
ip_add = input()


url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_add}"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0",
    "x-apikey": "b221c495a4e5654c82fbc7928804bf665d0b04d1ece9818e453c92fe8f5664a6"
}
r = requests.get(url, headers=headers).json()
dict_web = r["data"]["attributes"]["last_analysis_results"]
tot_engine_c = 0
tot_detect_c = 0
result_eng = []
eng_name = []
count_harmless = 0

for i in dict_web:
    tot_engine_c += 1
    if dict_web[i]["category"] in ["malicious", "suspicious"]:
        result_eng.append(dict_web[i]["result"])
        eng_name.append(dict_web[i]["engine_name"])
        tot_detect_c += 1

# Remove duplicate results
result_eng = list(set(result_eng))

if tot_detect_c > 0:
    print(f"The IP {ip_add} was rated as {', '.join(result_eng)} on {tot_detect_c} engine(s) out of {tot_engine_c} engines. The engines which reported this are: {', '.join(eng_name)}.")
else:
    print(f"The IP {ip_add} has been marked harmless and clean on VirusTotal.")
