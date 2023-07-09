#Imports
from PIL import Image
import PIL

class RotateImage(object):
    '''
        Rotates the image about the centre of the image.
    '''

    def __init__(self, degrees):
        '''
            Arguments:
            degrees: rotation degree.
        '''
        self.degrees=degrees
        # Write your code here

    def __call__(self, sample):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        img = sample
        if not isinstance(sample,PIL.Image.Image):
            img = Image.fromarray(sample)
            
        return img.rotate(self.degrees)