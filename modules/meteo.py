import urequests
import modules.api_txt as api_txt

def get_meteo(latitude, longitude): # Sur la prochaine heure
    
    if int(api_txt.get_api_counter()[1]) > 10000:
        print("Quota de demande dépassé !!! Vous ne pouvez pas faire de requête...")
        return False
    
    url = "https://api.open-meteo.com/v1/forecast?latitude={0}&longitude={1}&current=temperature_2m,precipitation&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto&forecast_days=3".format(latitude,longitude)
    json_meteo = urequests.get(url).json()
    
    api_txt.add_api_counter(1)
    
    return {"current":
            {"temperature":
             [
                 json_meteo["current"]["temperature_2m"],
                 json_meteo["current_units"]["temperature_2m"]
                 ],
             "precipitation":
             [
                 json_meteo["current"]["precipitation"],
                 json_meteo["current_units"]["precipitation"]
                 ]
             },
            "demain":
            {"temperature": [round((json_meteo["daily"]["temperature_2m_min"][1] + json_meteo["daily"]["temperature_2m_max"][1]) / 2, 1), json_meteo["daily_units"]["temperature_2m_min"]],
             "precipitation":
             [
                 json_meteo["daily"]["precipitation_sum"][1],
                 json_meteo["daily_units"]["precipitation_sum"]
                 ]
             },
            "apres-demain":
            {"temperature": [round((json_meteo["daily"]["temperature_2m_min"][2] + json_meteo["daily"]["temperature_2m_max"][2]) / 2, 1), json_meteo["daily_units"]["temperature_2m_min"]],
             "precipitation":[
                 json_meteo["daily"]["precipitation_sum"][2],
                 json_meteo["daily_units"]["precipitation_sum"]
                 ]
             }
            }
"""
    return {"current":
            {"temperature":
             [
                 json_meteo["current"]["temperature_2m"],
                 json_meteo["current_units"]["temperature_2m"]
                 ],
             "precipitation":
             [
                 json_meteo["current"]["precipitation"],
                 json_meteo["current_units"]["precipitation"]
                 ]
             },
            "demain":
            {"temperature_min":
             [
                 json_meteo["daily"]["temperature_2m_min"][1],
                 json_meteo["daily_units"]["temperature_2m_min"]
                 ],
             "temperature_max":
             [
                 json_meteo["daily"]["temperature_2m_max"][1],
                 json_meteo["daily_units"]["temperature_2m_max"]
                 ],
             "precipitation":
             [
                 json_meteo["daily"]["precipitation_sum"][1],
                 json_meteo["daily_units"]["precipitation_sum"]
                 ]
             },
            "apres-demain":
            {"temperature_min":
                [
                    json_meteo["daily"]["temperature_2m_min"][2],
                    json_meteo["daily_units"]["temperature_2m_min"]
                    ],
             "temperature_max":[
                 json_meteo["daily"]["temperature_2m_max"][2],
                 json_meteo["daily_units"]["temperature_2m_max"]
                 ],
             "precipitation":[
                 json_meteo["daily"]["precipitation_sum"][2],
                 json_meteo["daily_units"]["precipitation_sum"]
                 ]
             }
            }
"""