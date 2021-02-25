import requests

url = "https://api-nba-v1.p.rapidapi.com/standings/standard/2020/teams/teamId/2"

headers = {
    'x-rapidapi-key': "839a83d5ddmsha26712eb18dfcb0p1d6a72jsndb84331d89b5",
    'x-rapidapi-host': "api-nba-v1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

print(response.text)


# "teams":[{"city":"Boston","fullName":"Boston Celtics","teamId":"2","nickname":"Celtics","logo":"https:\/\/upload.wikimedia.org\/wikipedia\/fr\/thumb\/6\/65\/Celtics_de_Boston_logo.svg\/1024px-Celtics_de_Boston_logo.svg.png","shortName":"BOS","allStar":"0","nbaFranchise":"1","leagues":{"standard":{"confName":"East","divName":"Atlantic"}}}
