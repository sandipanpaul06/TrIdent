import pandas as pd
import os
import re

import argparse

parser = argparse.ArgumentParser(description= 'VCF pre-processing: dividing CSV files exported from VCF files into window based subfiles')
parser.add_argument('fileName', type=str, help= 'VCF file name')
parser.add_argument('outFolder', type=str, help= 'Output folder name')

args = parser.parse_args()


# In[40]:


filenamegz = args.fileName
writeFolder = args.outFolder
numm = 500  ###change this

filename = filenamegz[:-3]

com1 = 'gunzip -c ./VCF/' + filenamegz + ' > ./VCF/' + filename
os.system(com1)


path_read = "./VCF/" + str(filename)
with open(path_read, 'r') as file:
	text = file.readlines()

a = []
for i in range(len(text)):
	if text[i][0] != '#':
		col = re.split(r'\t+', text[i][:-1])
		row = []
		row.append(int(col[1]))
		row.extend(col[9:])
		a.append(row)

a = pd.DataFrame(a)
a.to_csv('./VCF/' + filename[:-4] + '.csv', index=False, header=False)

print('VCF to CSV: done')

com2 = 'rm ./VCF/' + filename

os.system(com2)
# In[33]:



path_write = "./VCF/"+ filename[:-4] + "_HT" + '.csv'


#a = pd.read_csv(path_read, header = None)

new_df = []


for i in range(1, a.shape[1]):
	row = list(a[i])
	r1 = []
	r2 = []
	for r in row:
		splt = r.split('|')
		r1.append(int(splt[0]))
		r2.append(int(splt[1]))
	new_df.append(r1)
	new_df.append(r2)

A = pd.DataFrame(new_df)

A.columns = list(a[0])

A.to_csv(path_write, index=False)

com3 = 'rm ./VCF/' + filename[:-4] + '.csv'
os.system(com3)

print('step 1 complete')

'''
subdiving files
'''
os.mkdir('./VCF/'+writeFolder)


range_for = A.shape[1]//10

for i in range(range_for):
	start = i*10
	end = start+numm
	if end <= A.shape[1]:
		fname = "./VCF/"+ writeFolder + '/'+ filename[:-4] + "_" + str(i+1) + ".csv"
		A.iloc[:, start:end].to_csv(fname, index=False)

print('number of subfiles generated:', range_for)
