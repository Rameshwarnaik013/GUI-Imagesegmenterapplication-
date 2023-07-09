# Imports
from importlib.resources import path
from typing import List
from my_package.data.transforms.blur import BlurImage
from my_package.data.transforms.crop import CropImage
from my_package.data.transforms.flip import FlipImage
from my_package.data.transforms.rescale import RescaleImage
from my_package.data.transforms.rotate import RotateImage
import numpy as np
from PIL import Image
import json
# import jsonlines

class Dataset(object):
    '''
        A class for the dataset that will return data items as per the given index
    '''

    def __init__(self, annotation_file, transforms=None):
        '''
            Arguments:
            annotation_file: path to the annotation file
            transforms: list of transforms (class instances)
                        For instance, [<class 'RandomCrop'>, <class 'Rotate'>]
        '''

        self.transform = transforms
        self.data = []
        ind=-1
        #Given path of annotation file remove the name of it to get the path to directory
        #performing the same operation (because the images path in file are given realtive to the directory)
        for i in range(len(annotation_file)):
            if annotation_file[i]=="/":
                ind=i
        self.path = annotation_file[:ind+1]
        #opening annotation file 
        with open(annotation_file) as f:
            for line in f:
                temp=json.loads(line)
                self.data.append(temp)

    def __len__(self):
        '''
            return the number of data points in the dataset
        '''
        return len(self.data)


    def __getitem__(self, idx):
        '''
            return the dataset element for the index: "idx"
            Arguments:
                idx: index of the data element.

            Returns: A dictionary with:
                image: image (in the form of a numpy array) (shape: (3, H, W))
                gt_png_ann: the segmentation annotation image (in the form of a numpy array) (shape: (1, H, W))
                gt_bboxes: N X 5 array where N is the number of bounding boxes, each 
                            consisting of [class, x1, y1, x2, y2]
                            x1 and x2 lie between 0 and width of the image,
                            y1 and y2 lie between 0 and height of the image.

            You need to do the following, 
            1. Extract the correct annotation using the idx provided.
            2. Read the image, png segmentation and convert it into a numpy array (wont be necessary
                with some libraries). The shape of the arrays would be (3, H, W) and (1, H, W), respectively.
            3. Scale the values in the arrays to be with [0, 1].
            4. Perform the desired transformations on the image.
            5. Return the dictionary of the transformed image and annotations as specified.
        '''

        #find idx th element in the parsed file
        data = self.data
        #using the path open the image
        img_path = self.path+data[idx]['img_fn']
        png_path = self.path+data[idx]['png_ann_fn']
        bboxes = data[idx]['bboxes']
        image = Image.open(img_path)
        png_img = Image.open(png_path)

        finalImg = []
        finalpng = []
        boxes = []

        #if there is an operation to perform then go into loop
        if self.transform != None and len(self.transform)!=0:
            for obj in self.transform:
                #tranform the image
                res = obj(image)
                res = np.array(res)
                #converting to array, making all values to lie in [0,1], and then appending
                res = res.transpose((2,0,1))
                finalImg.append(res/255)

                #tranforming png image, making all values to lie in [0,1], and then appending
                res = obj(png_img)
                res = np.array(res)

                finalpng.append(res/255)

                boxes.append(bboxes)
        else :
            res = np.array(image)
            #converting to array, making all values to lie in [0,1], and then appending
            res = res.transpose((2,0,1))
            finalImg.append(res/255)

            #tranforming png image, making all values to lie in [0,1], and then appending
            res = np.array(png_img)

            finalpng.append(res/255)

            boxes.append(bboxes)
        #making a dictionary
        imgDict = dict({"image":finalImg,"gt_png_ann":finalpng,"gt_bboxes":boxes})

        return imgDict
        
        


