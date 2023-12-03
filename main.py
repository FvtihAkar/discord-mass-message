import requests as req
import time,json,random,threading

url = "https://discord.com/api/v9/channels/-id-/messages"
url2 = "https://discord.com/api/v9/users/@me/channels"



config = json.loads(open("config.json","r").read())
headers = {
    "Authorization": random.choice(config["tokens"]),
    "content-type": "application/json"
}

json_data = {
    "content" : config["message"],
    "flags" : 0,
    "mobile_network_type" : "unknown",
    "tts" : False   
}

res = req.get(url2,headers=headers)
data = res.json()
print(data)
if config["target"] == "multi":
    data = reversed(data)
    fails = []
    for user in data:
        res = req.post(url.replace("-id-",user["id"]),data=json_data,headers=headers).status_code
        if res != 200:
            print(f"failed to send message to : {user['id']}")
            fails.append(user["id"])
        else:
            print(f"message sent to : {user['id']}")
        time.sleep(50/1000)

    while len(fails) != 0:
        for user in fails:
            res = req.post(url.replace("-id-",user),data=json_data,headers=headers).status_code
            if res != 200:
                print(f"failed to send message to : {user}")
                fails.append(user)
            else:
                print(f"message sent to : {user}")
                fails.remove(user)
            time.sleep(100/1000)
        print("New length of failed messages :",len(fails))
        print("Retrying in 5 secs.")
        time.sleep(5)

    print("Messages successfully sent to all dm channels.")

if config["target"] == "single":
    user = config["id"]
    username = ""
    channel_id = 0

    if user == "":
        print("User id is not specified.")
        exit()
    for channel in data:
        if channel["type"] == 1:
            if channel["recipients"][0]["id"] == user:
                 channel_id = channel["id"]
                 username = channel["recipients"][0]["username"]
    if channel_id == 0:
         print("any open dm not found with given user id.")
         print("trying to create an dm with given user.")
         payload = {
                    "recipients": [
                        user
                    ]
                }
         ress = req.post(url2,json=payload,headers=headers).json()
         print(ress)
         channel_id = ress["id"]
         username = ress["recipients"][0]["username"]
         print("success.")

    
    
    def thread():
        global user,username,channel_id
        i = 1
        while i > 0:
            headers = {
                "Authorization": random.choice(config["tokens"])
            }
            res = req.post(url.replace("-id-",channel_id),data=json_data,headers=headers)
            if res.status_code != 200:
                    err = res.json()
                    print(err)
                    if err["message"] == "The write action you are performing on the channel has hit the write rate limit.":
                        time.sleep(err["retry_after"])
                    else:
                        print(f"failed to send message to : {username}")
                        time.sleep(config["delay"] / 1000)
            else:
                    print(f"message sent to : {username}")
            i = 0
    thread()
    
    

