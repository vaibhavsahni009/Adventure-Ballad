import time
from typing import Dict
import requests
import json

base_url = 'http://localhost:3000'


def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = requests.get(url)
    return response.json()

def suno(song:Dict[str, str]):
    url = f"{base_url}/api/custom_generate"
    payload = {
        "prompt": song.get("song","We're no strangers to love You know the rules and so do I (do I) A full commitment's what I'm thinking of You wouldn't get this from any other guy I just wanna tell you how I'm feeling Gotta make you understand Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you We've known each other for so long Your heart's been aching, but you're too shy to say it (say it) Inside, we both know what's been going on (going on) We know the game and we're gonna play it And if you ask me how I'm feeling Don't tell me you're too blind to see Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you We've known each other for so long Your heart's been aching, but you're too shy to say it (to say it) Inside, we both know what's been going on (going on) We know the game and we're gonna play it I just wanna tell you how I'm feeling Gotta make you understand"),
        "tags": song.get("song_style","ballad"),
        "make_instrumental": False,
        "wait_audio": False
    }
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    data=response.json()
    ids = f"{data[0]['id']},{data[1]['id']}"
    print(f"ids: {ids}")

    for _ in range(60):
        data = get_audio_information(ids)
        if data[0]["status"] == 'streaming':
            print(f"{data[0]['id']} ==> {data[0]['audio_url']}")
            print(f"{data[1]['id']} ==> {data[1]['audio_url']}")
            return data[0]
        # sleep 5s
        time.sleep(5)
    
    

if __name__ == "__main__":
    #testing the api
    song = { "song": "Intro: ओ भोलेनाथ, देखो सावन का महीना आया, पवन करे शोर, दिल में खुशियों का समंदर छाया। Chorus: सावन का महीना, पवन करे शोर, भोलेनाथ, आपकी कृपा से, मन में है हर्षोल्लास। पार्वती माता संग आपका, प्रेम है अनुपम, हम भक्तों के जीवन में, है आपका वर्चस्व महान। Verse 1: महादेव, आपकी महिमा, सावन में है छाई, हरियाली की चादर, सृष्टि पर बिछाई। समुद्र मंथन की कथा, याद दिलाती है, नीला गला आपका, हर बूँद में दिखाती है। Bridge: भोलेनाथ, आपके साथ, ये सावन कितना प्यारा, हर बूँद में बसी, आपकी शक्ति का सहारा। सोमवार के व्रत, हम रखते दिल से, आपकी भक्ति में, हमें मिलता सुकून।",
            "song_style": "ballad"}
    #convert following json into dictionary and print
    
    song_dict = json.loads(json.dumps(suno(song)))
    print(song_dict['audio_url'])
    


