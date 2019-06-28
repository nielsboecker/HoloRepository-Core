#to generate json and to play around with it. this py wont be implemented in final build
#????src allow multiple py files
#????look at json file sturcture(e.g.do we need tags? more field?)
import json

data = {}
data["s0"] = []
data["s0"].append({
	"name": "sample0",
	"src": "sample0.py",
	"info": "A pipline for testing. It will printout 'Hello World! from 0'",
	"addDate": "26/06/2019",
	"modDate": "26/06/2019",
	"param": "0"
	})
data["s1"] = []
data["s1"].append({
	"name": "sample1",
	"src": "sample1.py",
	"info": "A pipline for testing. It will printout 'Hello World! from 1'",
	"addDate": "26/06/2019",
	"modDate": "26/06/2019",
	"param": "0"
	})
data["i0"] = []
data["i0"].append({
	"name": "dicom2numpy",
	"src": "dicom2numpy.py",
	"info": "Convert dicom to numpy",
	"addDate": "26/06/2019",
	"modDate": "26/06/2019",
	"param": "0"
	})
data["i1"] = []
data["i1"].append({
	"name": "nifti2numpy",
	"src": "nifti2numpy.py",
	"info": "Convert nifti to numpy",
	"addDate": "26/06/2019",
	"modDate": "26/06/2019",
	"param": "0"
	})
data["m0"] = []
data["m0"].append({
	"name": "numpy2obj",
	"src": "numpy2obj.py",
	"info": "Generate mesh from numpy",
	"addDate": "26/06/2019",
	"modDate": "26/06/2019",
	"param": "0"
	})
data["p0"] = []
data["p0"].append({
	"name": "nifti2obj",
	"src": "nifti2obj.py",
	"info": "Generate obj mesh from nifti",
	"addDate": "27/06/2019",
	"modDate": "27/06/2019",
	"param": "2"
	})
data["p1"] = []
data["p1"].append({
	"name": "nifti2glb",
	"src": "nifti2glb.py",
	"info": "Generate glb mesh from nifti",
	"addDate": "28/06/2019",
	"modDate": "28/06/2019",
	"param": "2"
	})

with open("json/pipelineList.json", "w") as outfile:
	json.dump(data, outfile)

print("done")