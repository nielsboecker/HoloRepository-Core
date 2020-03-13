import SimpleITK as sitk
import time

input_file_path = "/home/immanuel/Documents/HoloRepository-Core/HoloPipelines/tests/data/"

reader = sitk.ImageSeriesReader()

dicom_name = reader.GetGDCMSeriesFileNames(input_file_path)
reader.SetFileNames(dicom_name)
start = time.time()
image = reader.Execute()
end = time.time()
print(end-start)

numpy_array_image = sitk.GetArrayFromImage(image)
