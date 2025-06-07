from modules.connection import search_wlan
import ustruct as struct
import urequests as requests
import ujson as json
import modules.api_txt as api_txt


def getLocation(api_key): # Avec Google maps API + sécurité sur le nombre de requête.    
    
    if int(api_txt.get_api_counter()[0]) > 24000:
        print("Quota de demande dépassé !!! Vous ne pouvez pas faire de requête...")
        return False
    
    list_wlan = search_wlan()
    data = {
        "considerIp": False,
        "wifiAccessPoints": []
    }

    for wifi in list_wlan:
        entry = {
            "macAddress": "%02x:%02x:%02x:%02x:%02x:%02x" % struct.unpack("BBBBBB", wifi[1]),
            "signalStrength": wifi[3],
            "channel": wifi[2]
        }
        data["wifiAccessPoints"].append(entry)
    
    headers = {"Content-Type": "application/json"}
    url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + api_key
    response = requests.post(url, headers=headers, data=json.dumps(data))

    api_txt.add_api_counter(0)

    return json.loads(response.content)["location"]