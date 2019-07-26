import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import platform
import pathlib

cwd = pathlib.Path.cwd()

numpyPath = cwd.parents[0].joinpath("numpy")

imgs_to_process = np.load(str(numpyPath.joinpath(sys.argv[1]))).astype(np.float64)

plt.hist(imgs_to_process.flatten(), bins=50, color="c")
plt.xlabel("Hounsfield Units (HU)")
plt.ylabel("Frequency")
plt.show()
