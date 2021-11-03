# Programming Challenge
1) `imaging_interview.py` - The provided Python file that contains functions for preprocessing and calculating similarity scores.
2) `task_kopernikus.ipynb` - A colab repository that contains all the functions used for the challenge also it contains some visualizations. The complete experiments were run in google colab.
3) The functions used are:
 - `createPreprocessedImagesInTemp()` - This function calls the method `preprocess_image_change_detection()` in `imaging_interview.py` for the entire dataset and copy the            preprocessed images to another `temp` folder.    
- `deleteSimilarImagesFromTemp()` - This function takes each image and compares it with all images in the temp folder. When comparing it calls the function `compare_frames_change_detection()` in `imaging_interview.py` and returns a score, based on a threshold for the score we decide that all images below this threshold are similar and need to be removed. The complexity of this method is `O(n^2)` 
- `deleteSimilarImagesFromTempLinearly()` - This function performs a linear search instead of the above method to reduce the complexity to `O(n)`.
8) `deleteSimilarImages.py` - Contains the above functions for preprocessing and deleting similar images from the entire dataset using the functions from `imaging_interview.py`
9) `deleteSimilarImagesUsingSSIM.py` - contains the same preprocessing functions but similarity scores after preprocessing are computed using SSIM library
10) Detailed Answer [Ml_challenge_answers.pdf](https://github.com/steffyalbert/Programming_challenge/blob/287fbfcdf0d350d29363993d36d7a20ab29880ec/Ml_challenge_answers.pdf)
