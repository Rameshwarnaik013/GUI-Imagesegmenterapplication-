#Imports
from PIL import Image
import PIL
from torch import imag

class FlipImage(object):
    '''
        Flips the image.
    '''

    def __init__(self, flip_type='horizontal'):
        '''
            Arguments:
            flip_type: 'horizontal' or 'vertical' Default: 'horizontal'
        '''

        self.type = flip_type

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
            
        if self.type == 'horizontal' :
            res = img.transpose(Image.FLIP_LEFT_RIGHT)
        else :
            res = img.transpose(Image.FLIP_TOP_BOTTOM)
        
        return res   