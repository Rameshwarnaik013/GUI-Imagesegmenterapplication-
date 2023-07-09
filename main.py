#Imports
from my_package.model import InstanceSegmentationModel
from my_package.data import Dataset
from my_package.analysis import plot_visualization
from my_package.data.transforms.blur import BlurImage
from my_package.data.transforms.crop import CropImage
from my_package.data.transforms.flip import FlipImage
from my_package.data.transforms.rescale import RescaleImage
from my_package.data.transforms.rotate import RotateImage
import numpy as np
from PIL import Image

def experiment(annotation_file, segmentor, transforms, outputs):
    '''
        Function to perform the desired experiments

        Arguments:
        annotation_file: Path to annotation file
        segmentor: The image segmentor
        transforms: List of transformation classes
        outputs: path of the output folder to store the images
    '''

    #This is the 
    dataobj = Dataset(annotation_file,None)

    boxFile = open(dataobj.path+"imgs/bboxes.txt","w")
    
    for i in range(len(dataobj.data)):
        inputImage = dataobj[i]['image'][0]
        pred_boxes, pred_masks, pred_class, pred_score = segmentor(inputImage)
        boxFile.write(str(pred_boxes)+"\n")
    boxFile.close()
    #Create the instance of the dataset

    datasetObj = Dataset(annotation_file, transforms)

    #Iterate over all data items 

    imageDictList = datasetObj[7]

    #imageDictList gives all the transformed images and their pngs along with bboxes, we need to visualise each of the 
    #image transformed
    lenght=1
    if transforms != None and len(transforms)!=0 :
        lenght = len(transforms)
        
    for i in range(lenght):
        # input image is the image which is to be fed into segementor
        inputImage = imageDictList['image'][i]
        #maskImage is the image where we will show top 3 boxes on image, as it is in [0,1], we will
        #convert it back to normal image by multiplying 255 and making it h,w,3 from 3,h,w
        maskImage = imageDictList['image'][i]
        maskImage = maskImage.transpose(1,2,0)
        maskImage = maskImage*255
        maskImage = Image.fromarray(maskImage.astype(np.uint8))
        #actual image is the image which we use to compare in subplot
        actualImg = imageDictList['image'][i]
        actualImg = actualImg.transpose(1,2,0)
        actualImg = actualImg*255
        actualImg = Image.fromarray(actualImg.astype(np.uint8))
        #png image is to enhance the segmentor output, will be used in plot_visualisation if passed as last argument
        pngImage = imageDictList['gt_png_ann'][i][0]
        pngImage = pngImage*255
        #getting output from segmentor
        pred_boxes, pred_masks, pred_class, pred_score = segmentor(inputImage)
        #passing all the parameters to the visualisation function
        path = outputs+"tranformation_"+str(i+1)+".png"
        plot_visualization(actualImg,maskImage,pred_boxes, pred_masks, pred_class, pred_score, path, None)
    
    #Get the predictions from the segmentor.

    

    #Draw the segmentation maps on the image and save them.



    #Do the required analysis experiments.
    




def main():
    segmentor = InstanceSegmentationModel()
    experiment('/home/jaswanth/Downloads/Python_DS_Assignment/data/annotations.jsonl', segmentor, None, "/home/jaswanth/Downloads/Python_DS_Assignment/data/imgs/") # Sample arguments to call experiment()

# [FlipImage(), BlurImage(5), RescaleImage(960), RescaleImage(240), RotateImage(-90), RotateImage(45)]

if __name__ == '__main__':
    main()
