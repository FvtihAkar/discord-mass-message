import requests as req
import time,json

url = "https://discord.com/api/v9/channels/-id-/messages"
url2 = "https://discord.com/api/v9/users/@me/channels"

config = json.loads(open("config.json","r").read())
headers = {
    "Authorization": config["token"]
}

json = {
    "content" : config["message"],
    "flags" : 0,
    "mobile_network_type" : "unknown",
    "tts" : False
}

res = req.get(url2,headers=headers)
data = res.json()
data = reversed(data)
fails = []

for user in data:
    res = req.post(url.replace("-id-",user["id"]),data=json,headers=headers).status_code
    if res != 200:
        print(f"failed to send message to : {user['id']}")
        fails.append(user["id"])
    else:
        print(f"message sent to : {user['id']}")
    time.sleep(50/1000)

while len(fails) != 0:
    for user in fails:
        res = req.post(url.replace("-id-",user),data=json,headers=headers).status_code
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
