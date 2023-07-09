#Imports
import PIL
from PIL import Image, ImageFilter 

class BlurImage(object):
    '''
        Applies Gaussian Blur on the image.
    '''

    def __init__(self, radius):
        '''
            Arguments:
            radius (int): radius to blur
        '''

        self.radius = radius
        # Write your code here
        

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL Image)

            Returns:
            image (numpy array or PIL Image)
        '''
        img = image
        
        if not isinstance(image,PIL.Image.Image):
            img = Image.fromarray(image)
        
        return img.filter(ImageFilter.GaussianBlur(radius = self.radius))
        
        # Write your code here
        

