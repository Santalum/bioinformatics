# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 16:10:44 2019

@author: vroom016
"""

#OnceaPunAtalianaintheWest
#This Thaleminator script counts Thale cress seeds and uses a model to correct for touching seeds.
#Together with manual germination scoring this script can help the user with calculating the germination rate.
#import matplotlib.pyplot as plt
import numpy as np
from skimage import (filters, color, exposure,
                     segmentation, morphology)
from skimage.measure import label,regionprops
from skimage.color import label2rgb
from skimage import restoration, img_as_float
#from skimage.exposure import histogram
from skimage.util import invert
from skimage.io import imread_collection, imsave
#make sure the working folder is in an experiment folder and named after the storage duration or other criterium
#for instance eXXXXXX/6w
from os import path, getcwd
#unrotated images are used for analysis (label_position='bottom right')
#in case rotated images are used replace "6-(3*j+k)" with "1+(3*j+k)"
seq = imread_collection("*.jpg", conserve_memory=True)
#read the table from which sample data can be extracted
sample_table=np.genfromtxt("sample_table.csv", delimiter=",", dtype='str')
#number of trays used in the experiment
ntrays = sample_table.shape[0]
#the order of trays may be shuffled thus ther results will be saved in a different array
result_table=np.empty((sample_table.shape[0]*2,sample_table.shape[1]), dtype=sample_table.dtype)
object_table=np.empty((sample_table.shape[0]*2,sample_table.shape[1]), dtype=sample_table.dtype)
object_area_table=np.empty((sample_table.shape[0]*2,sample_table.shape[1]), dtype=sample_table.dtype)
#result_log=np.empty(0, dtype=str)
for i in range(len(seq)):     
    full_image = seq[i]
    #create a dark image with the shape of full_image
    image_scan=np.zeros(full_image.shape)
    #Analysis of the binary number:
#    binnum = full_image[1800:,3560:]
    binnum = full_image[1400:1400+1000,3500:3500+400]
    binnum = invert(binnum)
#    fig, ax = plt.subplots()
#    ax.imshow(binnum);
    # change to greyscale for image analysis
    binnum=color.rgb2gray(binnum)

    eqim=exposure.equalize_adapthist(binnum)
    thrs=filters.threshold_yen(eqim) 
    
    binnum_thrs= eqim>thrs+0.2
    crs=segmentation.clear_border(binnum_thrs)
    # look for objects
    mrs=morphology.closing(crs,morphology.square(3))
    # label objects
    lrs=label(mrs)
    rrs=regionprops(lrs)
    # remove small objects around the seeds
    lbrs=morphology.remove_small_objects(lrs)
    binnum=label2rgb(lbrs,binnum)
    binnum=restoration.denoise_nl_means(binnum,multichannel=True)
    #analyse whether the number is 0 or 1 based on its area:
    objectarea=[]
    for l in range(len(np.unique(lbrs)[1:])):
        objectarea.append(np.sum(lbrs==np.unique(lbrs)[1:][l]))
    number=[]
    for j in range(len(np.unique(lbrs)[1:])):
        if np.sum(lbrs==np.unique(lbrs)[1:][j]) >= np.amax(objectarea)-np.amax(objectarea)/10:
            number.append(0)
        elif np.sum(lbrs==np.unique(lbrs)[1:][j]) >= np.amax(objectarea)/2-np.amax(objectarea)/10:
            number.append(1)
    #this format works for Experiment[space]Date[space]Time.jpg
    print('Experiment: ',seq.files[i].split()[0], 
          " Tray: ", ''.join(map(str, number)),
          ' Date: ', seq.files[i].split()[1], 
          ' Time: ',  seq.files[i].split()[2][0:2], ':',
                    seq.files[i].split()[2][2:4], ':',
                    seq.files[i].split()[2][4:6], sep='')
    #include the binary number for reference
    image_scan[1400:1400+1000,3500:3500+400]=img_as_float(binnum)
    #When the first germination batch is analysed:
    if i < ntrays:
        # there is a match with the binary number recognised and
        if len(np.where(sample_table==''.join(map(str, number)))[0])==1:
            result_table[2*i][0]= \
                str(sample_table[np.where(sample_table==''.join(map(str, number)))][0])
            object_table[2*i][0]=\
                str(sample_table[np.where(sample_table==''.join(map(str, number)))][0])
            object_area_table[2*i][0]=\
                str(sample_table[np.where(sample_table==''.join(map(str, number)))][0])
        else:
            result_table[2*i][0]= 'pic_'+str(i+1)
            object_table[2*i][0]= 'pic_'+str(i+1)
            object_area_table[2*i][0]= 'pic_'+str(i+1)
        result_table[2*i+1][0]='scount'
        object_table[2*i+1][0]= 'ocount'
        object_area_table[2*i+1][0]= 'oarea'
        for j in range(2):
            for k in range(3):
                #for this consider each spot's centre and move x,y away from there
                image = img_as_float(
                        full_image[150+1200*j:1150+1200*j, 150+1100*k:1150+1100*k])
                image_scan[150+1100*j:1150+1100*j, 150+1100*k:1150+1100*k] = image
                # change to greyscale for image analysis
                image=color.rgb2gray(image) 
#                hist, hist_centers = histogram(image)
    
                # equalise the lightning levels
                eqim=exposure.equalize_adapthist(image)
                thrs=filters.threshold_yen(eqim) 
                image_thrs= eqim>thrs
                crs=segmentation.clear_border(image_thrs)
                # look for objects
                mrs=morphology.closing(crs,morphology.square(3))
                # label objects
                lrs=label(mrs)
                rrs=regionprops(lrs)
                # remove small objects around the seeds
                lbrs=morphology.remove_small_objects(lrs)
                image=label2rgb(lbrs,image)
                image=restoration.denoise_nl_means(image,multichannel=True)
#                fig, ax = plt.subplots()
#                ax.imshow(image);
                #For each seed calculate the number of pixels and return that value
#                germinated=[]
                #objects may be one or several seeds
                objectarea=[]
                objectcount=len(np.unique(lbrs)[1:])
                #the first photo session should have the most accurate seed count
                for l in range(len(np.unique(lbrs)[1:])):
                    objectarea.append(np.sum(lbrs==np.unique(lbrs)[1:][l]))
                #based on 6w fit model: 1.2818*x - 11.8046
                seedcount=int(1.2818*objectcount - 11.8046)
                if len(np.where(sample_table==''.join(map(str, number)))[0])==1:
                    print("Result of sample", 
                         sample_table[
                            int(np.where(sample_table==
                                ''.join(map(str, number)))[0])][6-(3*j+k)],
                        ":", seedcount,
                         "seed(s) counted based on an object count of",
                         objectcount)
                    result_table[2*i][6-(3*j+k)]=sample_table[
                            int(np.where(sample_table==
                            ''.join(map(str, number)))[0])][6-(3*j+k)]
                    object_table[2*i][6-(3*j+k)]=sample_table[
                            int(np.where(sample_table==
                            ''.join(map(str, number)))[0])][6-(3*j+k)]
                    object_area_table[2*i][6-(3*j+k)]=sample_table[
                            int(np.where(sample_table==
                            ''.join(map(str, number)))[0])][6-(3*j+k)]
                else:    
                    print("Result of sample", 
                         6-(3*j+k),
                        ":", seedcount,
                         "seed(s) counted based on an object count of",
                         objectcount)
                    result_table[2*i][6-(3*j+k)]=str(6-(3*j+k))
                    object_table[2*i][6-(3*j+k)]=str(6-(3*j+k))
                    object_area_table[2*i][6-(3*j+k)]=str(6-(3*j+k))
                result_table[2*i+1][6-(3*j+k)] = str(seedcount)
                object_table[2*i+1][6-(3*j+k)] = str(objectcount)
                object_area_table[2*i+1][6-(3*j+k)] = str(np.mean(objectarea))
    #for the last batch of pictures they are only saved            
    elif len(seq) -i <= ntrays:
        for j in range(2):
            for k in range(3):
                #for this consider each spot's centre and move x,y away from there
                image = img_as_float(
                        full_image[150+1200*j:1150+1200*j, 150+1100*k:1150+1100*k])
                image_scan[150+1100*j:1150+1100*j, 150+1100*k:1150+1100*k] = image
    #for the first and last set of photo's save; remember i starts at 0 and ends at len(seq)-1
    if i < ntrays or len(seq) -i <= ntrays:
        #save man_ass_pic MANual ASSessment PICtures each with the i
#        image_name=seq.files[i][:-22] + str(i) + '.png'
        image_name=seq.files[i][:-22] + '_' + str(path.basename(getcwd())) + '_man_ass_pic_' + str(i+1) + '.png'
        imsave(image_name,image_scan)
np.savetxt("automatic_result_"+seq.files[i][:-22] + '_' + str(path.basename(getcwd()))+ ".csv", result_table, delimiter=",",fmt='%s')
np.savetxt("automatic_object_"+seq.files[i][:-22] + '_' + str(path.basename(getcwd()))+ ".csv", object_table, delimiter=",",fmt='%s')
np.savetxt("automatic_object_area_"+seq.files[i][:-22] + '_' + str(path.basename(getcwd()))+ ".csv", object_area_table, delimiter=",",fmt='%s')