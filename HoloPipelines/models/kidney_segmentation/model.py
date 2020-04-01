from base_classes import Base_model
import os
from miscnn.data_loading.interfaces.nifti_io import NIFTI_interface
from miscnn.data_loading.data_io import Data_IO
from miscnn.processing.data_augmentation import Data_Augmentation
from miscnn.processing.subfunctions.normalization import Normalization
from miscnn.processing.subfunctions.clipping import Clipping
from miscnn.processing.subfunctions.resampling import Resampling
from miscnn.processing.preprocessor import Preprocessor
from miscnn.neural_network.architecture.unet.standard import Architecture
from miscnn.neural_network.model import Neural_Network
from miscnn.neural_network.metrics import dice_soft, dice_crossentropy, tversky_loss


class Kidney_model(Base_model):
    def __init__(self, saved_path, upload_folder="./"):
        interface = NIFTI_interface(pattern="case_00[0-9]*", 
                                    channels=1, classes=3)

        data_path = os.path.abspath(upload_folder)
        data_io = Data_IO(interface, data_path)

        data_aug = Data_Augmentation(cycles=2, scaling=True, rotations=True, elastic_deform=True, mirror=True,
                                     brightness=True, contrast=True, gamma=True, gaussian_noise=True)

        sf_normalize = Normalization(z_score=True)
        sf_clipping = Clipping(min=-79, max=304)
        sf_resample = Resampling((3.22, 1.62, 1.62))

        subfunctions = [sf_resample, sf_clipping, sf_normalize]

        pp = Preprocessor(data_io, data_aug=data_aug, batch_size=1, subfunctions=subfunctions, prepare_subfunctions=True, 
                          analysis="patchwise-crop", patch_shape=(48, 128, 128))
        pp.patchwise_overlap = (12, 32, 32)

        unet_standard = Architecture()
        self.model = Neural_Network(preprocessor=pp, architecture=unet_standard, loss=tversky_loss, metrics=[dice_soft, dice_crossentropy],
                                    batch_queue_size=1, workers=1, learninig_rate=0.0001)

        self.model.load(saved_path)

    def predict(self, input_folder, output_folder):
        # predict the image called imaging.nii in the specified folder and saves the result in predictions/foldername.nii
        self.model.predict([input_folder])


SAVED_MODEL_PATH = "kidney_model_miscnn"
kidney_model = Kidney_model(SAVED_MODEL_PATH)
