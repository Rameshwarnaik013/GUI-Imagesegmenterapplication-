#Imports
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageDraw, ImageFont 
import random 

def plot_visualization(image, maskImage, pred_boxes, pred_masks, pred_class, pred_score, output_path, enhancer): # Write the required arguments

	# converting pred_masks into array
	pred_masks = np.array(pred_masks)
	#taking H,W from 1,1,H,W
	pred_masks = pred_masks[0][0]
	#multiplied with 255 since the values are in [0,1]
	pred_masks = pred_masks*255
	#using the png enhancing the predictor_mask, this can be commented, won't effect the working
	if enhancer!=None :
		pred_masks = (pred_masks*(255-enhancer))/255

	#making a dictionary of predscore,pred_boxes,pred_class
	newdict = dict(zip(pred_score,zip(pred_boxes,pred_class)))
	dictitems = newdict.items()
	#sorting the dict to get top three scores(top 3 highest at last)
	sortedItems = sorted(dictitems)

	#loading pixels of the image which we want to mask 
	pixel_map = maskImage.load()

	#from top 3 highest scores, using pred_masks, changing the tint color of a particular region 
	#logic is to check whether a region in a box has any pixels which are white and coloring them(applying tint)
	for i in range(min(len(sortedItems),3)):
		#shape gives the bounding boxes (x1,y1) and (x2,y2)
		shape = (sortedItems[len(sortedItems)-1-i][1][0]) 
		#generating 3 random numbers in [0,1/1.1] to tint the pixels
		c1=random.random()/1.1
		c2=random.random()/1.1
		c3=random.random()/1.1
		# checking in the bounding box region for white pixels in pred_masks 
		for j in range(int(shape[0][1]),int(shape[1][1])):
			for k in range(int(shape[0][0]),int(shape[1][0])):
				if pred_masks[j][k]>=150 :
					#applying tint
					pixel_map[k,j]=(int(pixel_map[k,j][0]*c1),int(pixel_map[k,j][1]*c2),int(pixel_map[k,j][2]*c3))

	#using matplotlib making subplots and size (50,50)
	fig = plt.figure(figsize=(50, 50), dpi=40)
	#for drawing on maskImage
	draw = ImageDraw.Draw(maskImage)
	font = ImageFont.truetype("/home/jaswanth/Downloads/Python_DS_Assignment/my_package/analysis/arial.ttf", 22)
	for i in range(min(len(sortedItems),3)):

		shape = (sortedItems[len(sortedItems)-1-i][1][0]) 
		#drwaing rectangle with red border and a text (2 lines - line 1 for class and line 2 for score)
		draw.rectangle(shape,outline ="red")
		draw.multiline_text(sortedItems[len(sortedItems)-1-i][1][0][0], str(sortedItems[len(sortedItems)-1-i][1][1])+"\n"+str(sortedItems[len(sortedItems)-1-i][0]*10000//100), font=font,fill=(10, 255, 255, 255))

	#plotting actual image first
	subPlot = fig.add_subplot(1, 2, 1)
	#this is to remove the markers on x and y axis
	subPlot.set_xticks([])
	subPlot.set_yticks([])
	subPlot.imshow(image)
	#plotiing masked image
	subPlot = fig.add_subplot(1, 2, 2)
	subPlot.set_xticks([])
	subPlot.set_yticks([])
	subPlot.imshow(maskImage)
	#saving output in output_path
	fig.savefig(output_path, dpi=40, bbox_inches='tight')

    # The function should plot the predicted segmentation maps and the bounding boxes on the images and save them.
    # Tip: keep the dimensions of the output image less than 800 to avoid RAM crashes.