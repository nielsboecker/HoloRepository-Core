import os

import numpy as np
import SimpleITK as sitk
import tensorflow as tf

from mrbrains.data import Subjects
from mrbrains.models import cnn_3d_segmentation_1, resnet_3d_segmentation_1
from mrbrains.utils import batch_norm_3d, get_dsc, get_loss, re_arrange_array


class Brain_model():
    def __init__(self, saved_path):
        self.patch_size = [8, 24, 24]
        self.sess = tf.Session()
        tf.saved_model.loader.load(self.sess, [tf.saved_model.tag_constants.SERVING], saved_path)
        graph = tf.get_default_graph()
        # get the input and output tensors
        self.output = graph.get_tensor_by_name("cnn_3d_1/output/softmax:0")
        self.x_flair = graph.get_tensor_by_name('Placeholder:0')
        self.x_t1 = graph.get_tensor_by_name('Placeholder_1:0')
        self.x_ir = graph.get_tensor_by_name('Placeholder_2:0')

    def build_model(self, inputs, labels):
        x = batch_norm_3d(inputs=inputs,name="input/batch_norm")
        net = cnn_3d_segmentation_1(inputs=x)
        loss = get_loss(labels=labels,
        predictions=net["output"],
        loss_type='log_loss',
        scope='log_loss',
        huber_delta='0.3')
        dsc = get_dsc(labels=labels,
        predictions=net["output"])
        net["loss"] = loss
        net["dsc"] = dsc
        return net

    def predict(self, input_folder, output_folder):
        pz = self.patch_size[0]
        py = self.patch_size[1]
        px = self.patch_size[2]
        # load image and put into tensors
        flair_img = sitk.ReadImage(os.path.join(input_folder, "FLAIR.nii.gz"))
        t1_img = sitk.ReadImage(os.path.join(input_folder, "T1.nii.gz"))
        ir_img = sitk.ReadImage(os.path.join(input_folder, "IR.nii.gz"))
        flair_array = sitk.GetArrayFromImage(flair_img)
        t1_array = sitk.GetArrayFromImage(t1_img)
        ir_array = sitk.GetArrayFromImage(ir_img)
        shape = flair_array.shape
        label_shape = tuple([1]+list(shape)+[11])
        shape = tuple([1]+list(shape)+[1])
        flair_array = np.reshape(flair_array, shape)
        t1_array = np.reshape(t1_array, shape)
        ir_array = np.reshape(ir_array, shape)
        pred_array = np.zeros(label_shape)

        # make prediction
        for z in range(0,shape[1]-pz,int(pz/2)):
            for y in range(0,int(py/2)+1,int(py/2)):
                y2 = y + int((shape[2]-y)/py)*py
                for x in range(0,int(px/2)+1,int(px/2)):
                    x2 = x + int((shape[3]-x)/px)*px
                    tmp_flair = flair_array[:,z:z+pz,y:y2,x:x2]
                    tmp_shape = list(tmp_flair.shape)
                    tmp_flair = re_arrange_array(tmp_flair, tmp_shape, "input")
                    tmp_t1 = t1_array[:,z:z+pz,y:y2,x:x2]
                    tmp_t1 = re_arrange_array(tmp_t1, tmp_shape, "input")
                    tmp_ir = ir_array[:,z:z+pz,y:y2,x:x2]
                    tmp_ir = re_arrange_array(tmp_ir, tmp_shape, "input")
                    tmp_label = self.sess.run(self.output, feed_dict={\
                        self.x_flair: tmp_flair,
                        self.x_t1: tmp_t1,
                        self.x_ir: tmp_ir})
                    tmp_shape[-1] = pred_array.shape[-1]
                    tmp_label = re_arrange_array(tmp_label, tmp_shape, "output")
                    pred_array[:,z:z+pz,y:y2,x:x2] += tmp_label

        # save prediction in OUTPUT_FOLDER/segmented.nii.gz
        pred_array = pred_array/8
        pred_array = np.squeeze(pred_array)
        pred_array = np.argmax(pred_array, axis=3).astype(np.float32)
        result_img = sitk.GetImageFromArray(pred_array)
        result_img.CopyInformation(flair_img)
        img_path = os.path.join(output_folder, "segmented.nii.gz")
        sitk.WriteImage(result_img, img_path)
        return img_path

    def __exit__(self, exc_type, exc_value, traceback):
        self.sess.close()


# Singleton to prevent problems with cudnn when running on laptop with GPU
SAVED_MODEL_PATH = "./saved_model/"
brain_model = Brain_model(SAVED_MODEL_PATH)
