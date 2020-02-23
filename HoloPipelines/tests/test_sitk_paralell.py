import SimpleITK as sitk
import time
from multiprocessing.pool import ThreadPool

input_file_path = "/home/immanuel/Documents/HoloRepository-Core/HoloPipelines/tests/data/"

reader = sitk.ImageSeriesReader()

dicom_name = reader.GetGDCMSeriesFileNames(input_file_path)
reader.SetFileNames(dicom_name)

p = ThreadPool()


start = time.time()
p.map(sitk.ReadImage, dicom_name)
end = time.time()
print(end-start)

