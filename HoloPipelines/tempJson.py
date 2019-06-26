#to generate json and to play around with it. this py wont be implemented in final build
import json

data = {}
data["s0"] = []
data["s0"].append({
	"name": "sample0",
	"src": "sample0.py",
	"info": "A pipline for testing. It will printout 'Hello World! from 0'",
	"addDate": "26/06/2019",
	"modDate": "26/06/2019"
	})
data["s1"] = []
data["s1"].append({
	"name": "sample1",
	"src": "sample1.py",
	"info": "A pipline for testing. It will printout 'Hello World! from 1'",
	"addDate": "26/06/2019",
	"modDate": "26/06/2019"
	})

with open("json/pipelineList.json", "w") as outfile:
	json.dump(data, outfile)

print("done")