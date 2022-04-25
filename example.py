import requests

api_link = "https://whyapi.fusionsid.xyz/api/ricklang"

data = {
    "code" : 'take me to ur heart\n    i just wanna tell u how im feeling "I am cool"\nsay goodbye',
    "language" : "rickroll-lang"
}
response = requests.post(api_link, json=data).json()
print(response["output"])