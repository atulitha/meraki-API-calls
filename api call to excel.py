import json

import pandas as pd
import requests

if __name__ == "__main__":
    with open('networkslist.txt', 'r') as n:
        lines = [line.strip() for line in n]
        networks = lines
    device = networks
    print(networks)
    outlist = []
    for network in networks:
        print(network)
        try:
            payload = {}
            url = "https://api-mp.meraki.com/api/v1/networks/" + network + "/devices"
            headers = {
                'X-Cisco-Meraki-API-Key': 'Your api key here'
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            x = json.loads(response.text)

            if isinstance(x, dict):
                outlist.append(x)
            else:
                outlist += x
        except Exception as e:
            print(e, "\ndevice is :", network)
            with open("errordevices.txt", "w") as ed:
                ed.writelines(["this is failed: \n", network, "\n", "-" * 10])
                outlist.append({"Error": 'this has failed'})

    print(outlist)
    print(networks)

    df = pd.json_normalize(
        [i for i in outlist])  # .to_excel('output.xlsx', index="networkId", header=True, engine='openpyxl')
    df.insert(0, "Device", device, True)
    df.to_excel('output.xlsx', index=False, header=True, engine='openpyxl')
