import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt
#from google.colab.patches import cv2_imshow


import sys
sys.path.append('/content/')

import imaging_interview
from imaging_interview import compare_frames_change_detection
from imaging_interview import preprocess_image_change_detection

import numpy as np
import shutil
import glob
import os
from os.path import join

def createPreprocessedImagesInTemp(original,temp):
    # create temp or delete existing temp
    if not os.path.exists(temp):
        os.makedirs(temp)
    else:
        shutil.rmtree(temp)
        os.makedirs(temp)
    # iterate through each image of the dataset
    for (j, fileName) in enumerate(os.listdir(original)):
        imagePath = join(original, fileName)
        image = cv2.imread(imagePath)
        if image is not None:
            # Draw mask for each image and convert it to gray scale using the given function.
            image=  preprocess_image_change_detection(image)
            cv2.imwrite(os.path.join(temp, fileName), image)

            # If needed resize the preprocessed image
            #resized_image = cv2.resize(image, (256, 256))
            # resized_image = np.array(resized_image)
            #cv2.imwrite(os.path.join(temp, fileName), resized_image)
    print("Preprocessed images are copied to temp folder")

def deleteSimilarImagesFromTemp(searchedImageName,temp):
        
    searchedImgPath = join(temp, searchedImageName)
    # iterate through all images in temp directory and compare it with searchedImageName
    for (j, compareImageName) in enumerate(os.listdir(temp)):
        # if search image is same as compared image then dont delete the compared image
        if compareImageName == searchedImageName:
            pass
        # if search image and compared image names are different, then calculate the score 
        else:
            compareImgPath = join(temp, compareImageName)
            try:
                searchedImgTemp = cv2.imread(searchedImgPath, cv2.IMREAD_GRAYSCALE)
                compareImgTemp = cv2.imread(compareImgPath, cv2.IMREAD_GRAYSCALE)
                # compute the contour area scores of both the images using the provided function with min_contourarea
                score,res_cnts, thresh=compare_frames_change_detection(searchedImgTemp, compareImgTemp,3000)
                                  
            except:
                continue

            # When contour area score is less than threshold, images are more similar
            if score < 24000:
                # From the temp directory delete the compared image
                os.remove(compareImgPath)
                print("Search image: "+searchedImageName+", removed: "+ compareImageName+" Score:"+ str(score))

#Use this for an O(n) search
def deleteSimilarImagesFromTempLinearly(tempDir):
        # Starting image 
        imageList = os.listdir(tempDir).sort()
        currentImageName = imageList[0]
        # iterate through all images in temp directory and compare it with searchedImageName 
        # skipping the first image
        for (j, nextImageName) in enumerate(imageList[1:]):
            # if search image and compared image names are different, then calculate the score 
            try:
                currentImagePath = join(tempDir, currentImageName)
                nextImagePath = join(tempDir, nextImageName)

                currentImage = cv2.imread(currentImagePath, cv2.IMREAD_GRAYSCALE)
                nextImage = cv2.imread(nextImagePath, cv2.IMREAD_GRAYSCALE)
                # compute the contour area scores of both the images using the provided function with min_contourarea
                score, res_cnts, thresh=compare_frames_change_detection(currentImage, nextImage, 3000)
                print("Search image: "+currentImageName+", compare image: "+ nextImageName+" Score:"+ str(score)) 
                             
            except BaseException as error:
                print('An exception occurred: {}'.format(error))

            # When contour area score is less than threshold images are more similar
            if score < 24000:
                # From the temp directory delete the compared image
                os.remove(nextImagePath)
            else:
                currentImageName = nextImageName
                
                
def main():
    dataPath = '/content/'  #path to image dataset folder
    origDataDir = join(dataPath,  "c23")
    # Create another directory to copy all the preprocessed images
    temp = join(dataPath,  "temp")
    #function to copy all preprocessed to another temp folder
    createPreprocessedImagesInTemp(origDataDir,temp)
    imagesBeforeCleaning = glob.glob(origDataDir + '/*.png')
   
    # deleteSimilarImagesFromTempLinearly(temp)  #USE THIS FOR O(n) SEARCH
    
    for (i, searchedImageName) in enumerate(os.listdir(origDataDir)):
        # Search for all similar images in temp folder when compared to searchedImageName
        deleteSimilarImagesFromTemp(searchedImageName,temp)
    
    # Iterate over original image directory
    # To clean original dir, compare the temp and original directory and remove files from original which are not present in temp
    tempFiles= os.listdir(temp)
    for img in os.listdir(origDataDir):
      if ((img not in tempFiles) and (img.endswith(".png"))):
        
        os.remove(os.path.join(origDataDir, img))

    imagesAfterCleaning = glob.glob(origDataDir + '/*.png')
    print("Images before cleaning ",len(imagesBeforeCleaning))
    print("Images after cleaning ",len(imagesAfterCleaning))
    delcount= len(imagesBeforeCleaning)-len(imagesAfterCleaning)
    print(" Images deleted ",delcount)

if __name__ == "__main__":
    main()


