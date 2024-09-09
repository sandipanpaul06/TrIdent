import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import cv2
import argparse

parser = argparse.ArgumentParser(description= 'Generate images from .ms files')
parser.add_argument('pref', type=str, help= '.ms file prefix')
parser.add_argument('outF', type=str, help= 'Output filename')
parser.add_argument('nStrand', type=int, help= 'Number of haplotypes')
parser.add_argument('subfolder_name', type=str, help= 'Name of the subfolder')
parser.add_argument('number', type=int, help= 'Number of .ms files of the chosen class')
parser.add_argument('start', type=int, help= 'Start number of .ms files')
parser.add_argument('img_dim', type=int, help= 'Image dimension. For 299 x 299, put 299')

args = parser.parse_args()


# In[40]:


val = args.pref
nS = args.nStrand
num_ = args.number
outFile = args.outF
subf = args.subfolder_name
strt = args.start
dim_ = args.img_dim



# In[33]:

path1 = "./Datasets"


######


def image_gen(num_text_file, num_strands, dim, window_length, num_stride):
    
        
    path = path1 + "/"
    path+= subf + "/" + val + "_"
    path+= str(num_text_file)+".ms"
    with open(path, 'r') as file:
        text = file.readlines()
    if len(text) == 0:
        return []
    elif text[2][:20] == 'trajectory too bigly':
        return []
    segsites = text[5][11:-2]

    strands = num_strands
    stride = num_stride

    Sites = [float(segsites[x*9 : x*9+8])for x in range((len(segsites)+1)//9)]
    data = np.zeros((strands, len(Sites)))
    for a in range(strands):
        binary = text[a+6][:-2]
        for b in range(len(binary)):
            data[a][b]= int(binary[b])
    Dataset = pd.DataFrame(data)


    Dataset.columns = Sites
    
    dataset = []
    sites = []
    
    for col_ in range(Dataset.shape[1]):
        col1 = list(Dataset.iloc[:, col_])
        
        if sum(col1) >2 and sum(col1) < 196:
            dataset.append(col1)
            sites.append(Sites[col_])
            
    dataset = pd.DataFrame(dataset)
    dataset = dataset.T
    
    dataset.columns = sites
    
    #print(len(sites))

    
    
    err = float('inf')
    idx= None
    for pos in sites:
        error = abs(pos-0.5)
        if error<err:
            err = error
            idx = sites.index(pos)

    if idx<250 or len(sites) -idx < 250:
        return []


    window = window_length
    data_range = 500
    #print(data_range)
    
    
    DF = dataset.iloc[:, idx-data_range//2:idx+data_range//2]
    
    all_cols = []

    all_mids = []

    d = 0
    
    while 1:

        if d*stride+ window >= data_range:
            break
    
    
        df = DF.iloc[:, d*stride: d*stride+ window ]
        
        #print(df.shape)
        
        reref = []
        
        for col in range(df.shape[1]):
            lst = np.array(df.iloc[:, col])
            sum_ = np.sum(lst)
            if sum_ > 127:
                lst[lst == 1] =2
                lst[lst == 0] =1
                lst[lst == 2] =0
                
                reref.append(list(lst))
            else:
                reref.append(list(lst))
                
        
        reref_df = pd.DataFrame(reref).T
        
        #print(reref_df.shape)
        
        reref_aligned = []
        
        for row in range(reref_df.shape[0]):
            lstt = list(reref_df.iloc[row, :])
            reref_aligned.append(lstt)
            
        column = list(np.linalg.norm(reref_aligned,axis=1, ord=1))
        
        column.sort()
        
        all_cols.append(column)

        d+=1
    
    cols_DF = pd.DataFrame(all_cols).T
    
    img =np.asmatrix(cols_DF)
    
    #print(img)
    
    dims = [dim, dim]
    
    resized_img = cv2.resize(img, dims, interpolation = cv2.INTER_LINEAR)
    
    #print(resized_img)
    
    return resized_img


image_dataset = np.zeros((num_, dim_, dim_, 3))

counter = strt

element_counter = 0

#for i in range(strt, strt+num_):
while element_counter < num_:
    
    image = image_gen(num_text_file = counter ,num_strands= nS, dim = dim_, window_length=25, num_stride=2)
    
    counter+=1

    if len(image)==0:
        print('fail')
    
    elif len(image) != 0:
        
        for r in range(dim_):
            for c in range(dim_):
                image_dataset[element_counter][r][c][0] = image[r][c]
                image_dataset[element_counter][r][c][1] = image[r][c]
                image_dataset[element_counter][r][c][2] = image[r][c]
        element_counter+=1
        print(element_counter, counter-1)     
    else:
        print('fail')   


mean_image = np.zeros((dim_, dim_))

for r in range(dim_):
    for c in range(dim_):
        lst = []
        for i in range(num_):
            lst.append(image_dataset[i][r][c][0])
        mean_image[r][c] = np.mean(lst)
        
#import matplotlib.pyplot as plt
        
#fig = plt.imshow(mean_image, interpolation='bilinear',  aspect='auto', cmap='bone')

#plt.savefig("./Figs/" +sub+ ".png")




np.save('./Image_datasets/' + outFile + '.npy', image_dataset)
