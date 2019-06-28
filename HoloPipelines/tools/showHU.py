import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import platform

#-----------Unix uses "/", whereas Windows uses "\"-----------
slash = "/"
runningPlatform = platform.system()
if runningPlatform == "Windows":
	slash = "\\"
#-------------------------------------------------------------

cwd = os.getcwd() + slash

numpyPath = cwd[:-6] + "numpys" + slash

imgs_to_process = np.load(numpyPath + sys.argv[1]).astype(np.float64) 

plt.hist(imgs_to_process.flatten(), bins=50, color='c')
plt.xlabel("Hounsfield Units (HU)")
plt.ylabel("Frequency")
plt.show()