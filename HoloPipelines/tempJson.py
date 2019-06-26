#to generate json and to play around with it. this py wont be implemented in final build
import json

data = {}
data["pipeline"] = []
data['pipeline'].append({
	"name": "sample0",
	"id": "0",
	"src": "sample.py",
	"info": "A pipline for testing. It will printout 'Hello World! from 0'",
	"addDate": "26/06/2019",
	"modDate": "26/06/2019"
	})
data['pipeline'].append({
	"name": "sample1",
	"id": "1",
	"src": "sample.py",
	"info": "A pipline for testing. It will printout 'Hello World! from 1'",
	"addDate": "26/06/2019",
	"modDate": "26/06/2019"
	})

with open("json/piplineList.json", "w") as outfile:
	json.dump(data, outfile)

print("done")