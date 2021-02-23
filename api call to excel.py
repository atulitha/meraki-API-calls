import json
import pandas as pd
import requests

if __name__ == "__main__":
    with open('networkslist.txt', 'r') as n:
        lines = [line.strip() for line in n]
        networks = lines
    device = networks
    outlist = []
    outlist2 = []
    for network in networks:
        print(network)
        try:
            payload = {}
            url = "https://api-mp.meraki.com/api/v1/networks/" + network + "/clients?perPage=999"
            headers = {
                'X-Cisco-Meraki-API-Key': 'Your API key here'
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            x = json.loads(response.text)

            if isinstance(x, dict):
                x.update({'Gi ven_id': network})
                outlist.append(x)
                print(pd.json_normalize(x))
            else:
                for i in x:
                    i.update({'Given_id': network})
                    outlist2.append(i)
                outlist += outlist2
        except Exception as e:
            print(e, "\ndevice is :", network)
            with open("errordevices.txt", "w") as ed:
                ed.writelines(["this is failed: \n", network, "\n", "-" * 10])
                outlist.append({'Given_id': network, "Error": 'this has failed'})
    print(outlist)
    df = pd.json_normalize([i for i in outlist])
    df.set_index('Given_id')
    df.to_excel('output.xlsx', index= True, header=True, engine='openpyxl',)


