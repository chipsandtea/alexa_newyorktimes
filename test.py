import requests
import json

url = 'http://api.nytimes.com/svc/topstories/v1/home.json?api-key=4f085be2b93a4c4b8ca57c3d59aa1942'

r = requests.get(url)
parsed = json.loads(r.content)
print(parsed)
for i in range(len(parsed['results'])):
	print(parsed['results'][i]['title'])
