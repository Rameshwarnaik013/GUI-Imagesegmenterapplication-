#Imports
from PIL import Image
import random
import PIL

class CropImage(object):
    '''
        Performs either random cropping or center cropping.
    '''

    def __init__(self, shape, crop_type='center'):
        '''
            Arguments:
            shape: output shape of the crop (h, w)
            crop_type: center crop or random crop. Default: center
        '''

        self.shape = shape
        self.type = crop_type
        # Write your code here

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        img = image

        if not isinstance(image,PIL.Image.Image):
            img = Image.fromarray(image)

        h, w = img.size
        cropH, cropW = self.shape

        if h < cropH or w<cropW :
            return img
        if self.type == 'center':
            
            left = (w - cropW) / 2
            up = (h - cropH) / 2
            right = (w + cropW) / 2
            bottom = (h + cropH) / 2
            res = img.crop((left, up, right, bottom))

        else:
            up = random.uniform(0, h-cropH)
            left = random.uniform(0, w-cropW)
            res = img.crop((left, up, left+cropW, up+cropH))

        return res