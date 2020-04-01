from base_classes.base_model import Base_model


# This is a very basic model template
class Template_model(Base_model):

    # put your initialization code here
    def __init__(self, saved_path):
        pass

    # this function is necessary and should perform the segmentation
    def predict(self, input_folder, output_folder):
        pass


# In this example template the model is created as a singleton
template_model = Template_model("your_saved_path")
