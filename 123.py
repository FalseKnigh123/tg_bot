import requests

url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries/RU"

headers = {
	"X-RapidAPI-Key": "871aadb731msh302174792d744b8p1b59bdjsn482167023d41",
	"X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

print(response.text)