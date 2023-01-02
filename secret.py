import json

senderEmail = "*your email id*"
epwd = "*password*"

with open("database.json","r") as f:
    data=json.load(f)

phone_no=data["phone_no"]
to=data["emails"]

em = data["em"]
