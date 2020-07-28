# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 03:55:52 2020

@author: canok
"""


import sys 
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np

import pandas as pd 
from keras.preprocessing.image import ImageDataGenerator


current_dir = os.path.dirname(__file__)

dataset_path=os.path.join(current_dir, 'dataset/')


training_images=[]
training_labels=[]

dim=(272,272)

for filename in os.listdir(dataset_path):
    folder_label=os.path.join(dataset_path,filename)
    print(folder_label)
    for file in os.listdir(folder_label):
        image_path=os.path.join(folder_label,file)
        image=cv2.imread(image_path)
        image=cv2.resize(image,dim,interpolation = cv2.INTER_AREA)
        
        #gray_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)#Convert image to gray
        #normalized_image=gray_image/255
        #_,thres_img=cv2.threshold(gray_image)
        #img_expanded = gray_image[:, :, np.newaxis]#expand it (3.column eklendi)
        
        training_images.append(image)
        
        training_labels.append(filename)
        #you can add here scaling or resizing   

# Using numpy's savez function to store our loaded data as NPZ files
np.savez('data_NPZ/4class_forCan_all_training_data.npz', np.array(training_images))
np.savez('data_NPZ/4class_forCan_all_training_label.npz', np.array(training_labels))

"""
from sklearn.model_selection import train_test_split
training_images = pd.DataFrame(training_images)
training_labels = pd.DataFrame(training_labels)


train_set, val_set = train_test_split(training_images,train_labels,test_size=0.3,random_state=0)
"""


#ilgili datasetinden elde edilen random görüntüler
for i in range(1,5):
    random = np.random.randint(0, len(training_images))
    cv2.imshow("image_"+str(i), training_images[random])
    print(training_labels[random])
    cv2.waitKey(0)
    
cv2.destroyAllWindows()

