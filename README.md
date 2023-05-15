# Toyota RAV-4 Sticker and Hole Automation Program
![image](https://github.com/AminAmbike/Toyota_Machine_Vision/assets/113309178/2b2dd7ff-de53-4542-b810-062faa4cc4dc)

Development Team: Amin Ambike, Hangyeom Lee, Spiros Goros, Jason Ling, Brent Morris - All first year engineering students at the University of Waterloo

**Problem:**

The main focus of the TMMC (Toyota Motors Manufacturing Canada) Engineering project team is to find a reliable solution for using automation to peel off the stickers from the sticker roll and apply them over the body hole using vision integrated robotics. However, TMMC are seeking help on how to inspect the quality of the sticker application.

**Requirements:**

An inspection method/system is required to:

Confirm the presence of all 7 stickers applied by the robot
Confirm the body holes are fully covered by the stickers. A perfectly positioned sticker has at least 3mm between the edge of the sticker and the edge of the hole to ensure proper coverage
Confirm that the stickers are flush with the surface (e.g. no wrinkles) The total inspection time for all 7 stickers should not exceed 15 seconds For this challenge, you can ignore the time required to move the camera during inspection operations

# Solution overview

This proposal presents a dependable approach to leverage automation in order to identify and examine openings in engine compartments that require sticker coverage. These stickers are applied to minimize cabin noise, ensuring a more comfortable driving experience while protecting the engine bay's internal systems from harm. The aim is to create a program that can analyze a live feed or photographs of an engine bay during the sticker application process. This program will automatically detect any uncovered holes and transmit that information to the existing automated system.

**Image Processing and Analysis:**

1. Preprocessing: Implement image preprocessing techniques to improve the quality of the image and eliminate any unwanted noise or artifacts that could disrupt subsequent analysis stages. This process includes performing operations like noise reduction, image enhancement, and calibration to enhance the overall clarity and reliability of the image.

2. Hole Detection: Utilize computer vision techniques to identify potential locations of holes. This entails employing edge detection, contour analysis, and grayscale adaptive thresholding methods to pinpoint regions where stickers are missing, indicating the presence of holes. These techniques enable the detection and localization of areas that require further attention due to the absence of stickers.

3. Precision Measurement: Calculate the distance between the centroids of stickers and holes found within the image using computer vision analysis. If the distance is less than the sum of the radii, we can determine that a sticker was improperly placed.

**Machine Learning Model**

Developed a machine learning model which can conclusivley determine weather a circle captured by computer vision technology is a sticker or an open hole, and detect wrinkles in said sticker. We used a data set of 300 test images to train this model, it's effective implemntation remains a work in progress. 

# Next Steps

1. implement live video feed
2. improve machine learning model

# Technologies

- Python
- Numpy
- Matplotlib
- Opencv
- TensorFlow

# Sample Screenshots

**Test Image**

![image](https://github.com/AminAmbike/Toyota_Machine_Vision/assets/113309178/1b94d53b-a2e9-4c9f-887d-70caa4f22843)

**Coloured object detection and image thresholding**

![image](https://github.com/AminAmbike/Toyota_Machine_Vision/assets/113309178/63013956-432e-423e-a2f0-8bd8e9d12545)

**Futher thresholding and shape detection**

![image](https://github.com/AminAmbike/Toyota_Machine_Vision/assets/113309178/95f5d137-3898-4379-8f9c-2dcbb008195e)

**Improperly placed sticker detection**

![image](https://github.com/AminAmbike/Toyota_Machine_Vision/assets/113309178/28f44419-7657-4ccf-89d6-c378dd57c63e)

**Irregular countour detection**

![image](https://github.com/AminAmbike/Toyota_Machine_Vision/assets/113309178/52773e91-fd96-4583-afff-aafc902df1fe)







