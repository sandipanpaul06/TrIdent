import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import cv2
import argparse

parser = argparse.ArgumentParser(description= 'Generate dataset for vcf')
parser.add_argument('folder', type=str, help= 'folder within VCF folder where subfiles are saved')
parser.add_argument('strands', type=int, help= 'number of haplotypes')
parser.add_argument('prefix', type=str, help= 'file prefix')
parser.add_argument('start', type=int, help= 'Start number of files with the file prefix')
parser.add_argument('stop', type=int, help= 'Stop number of files with the file prefix')
parser.add_argument('img_dim', type=int, help= 'Image dimension. For 299 x 299, put 299')
parser.add_argument('outP', type=str, help= 'Output dataset name')

args = parser.parse_args()


# In[40]:


n_strands = args.strands
strt = args.start
stp = args.stop

num_ = (stp+1) - strt
subf = args.folder
pref = args.prefix
dim_ = args.img_dim
outFile = args.outP


# In[33]:


path1 = "./VCF/" + subf + '/'
path2 = "./VCF/"


######


def image_gen(num_text_file, num_strands, dim, window_length, num_stride):
    
        
    path_n  = path1 + pref + '_'+ str(num_text_file) + '.csv'
    
    dataset = pd.read_csv(path_n)
    siteS = list(dataset.columns)
    sites = [float(site) for site in siteS]
    strands = num_strands
    stride = num_stride
    
    
    window = window_length
    data_range = 500    #######change this
    #print(data_range)
    
    
    DF = dataset.copy()
    
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

        win_coL = list(df.columns)
        win_col = [float(winc) for winc in win_coL]

        win_mid = win_col[12]

        all_mids.append(win_mid)

        

        d+=1
    
    cols_DF = pd.DataFrame(all_cols).T
    
    img =np.asmatrix(cols_DF)
    
    #print(img)
    
    dims = [dim, dim]
    
    resized_img = cv2.resize(img, dims, interpolation = cv2.INTER_LINEAR)
    #print('mid: ', len(all_mids))

    mid_len = len(all_mids)//2
    
    SNP_mid = (all_mids[mid_len-1] + all_mids[mid_len]) / 2
    
    #print(SNP_mid)
    
    return resized_img, SNP_mid


image_dataset = np.zeros((num_, dim_, dim_, 3))
mids = []

for i in range(strt, stp+1):
    
    image, mid = image_gen(num_text_file = i ,num_strands= n_strands, dim = dim_, window_length=wind, num_stride=2)
    mids.append(mid)
    print(i)
    
    for r in range(dim_):
        for c in range(dim_):
            image_dataset[i-strt][r][c][0] = image[r][c]
            image_dataset[i-strt][r][c][1] = image[r][c]
            image_dataset[i-strt][r][c][2] = image[r][c]
    if i%1000 == 0:
        np.save('./VCF/'+outFile+'.npy', image_dataset)
        np.save('./VCF/'+outFile+'_pos.npy', np.array(mids))






np.save('./VCF/'+outFile+'.npy', image_dataset)
np.save('./VCF/'+outFile+'_pos.npy', np.array(mids))
