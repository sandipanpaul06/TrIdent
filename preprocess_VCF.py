import pandas as pd
import os
import re

import argparse

parser = argparse.ArgumentParser(description= 'VCF pre-processing: dividing CSV files exported from VCF files into window based subfiles')
parser.add_argument('V_name', type=str, help= 'file name')
parser.add_argument('outF', type=str, help= 'Output folder name')

args = parser.parse_args()


# In[40]:


filenamegz = args.V_name
writeFolder = args.outF
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

for i in range(2, a.shape[1]-1):
	b = list(a[i])
	c1 = []
	c2 = []
	for j in b:

		splt = j.split('|')
		d = int(splt[0])
		e = int(splt[1])
		c1.append(d)
		c2.append(e)

	new_df.append(c1)
	new_df.append(c2)

A = pd.DataFrame(new_df)

A.columns = list(a[1])

A.to_csv(path_write, index=False)

com3 = 'rm ./VCF/' + filename[:-4] + '.csv'
os.system(com3)

print('step 1 complete')

'''
subdiving files
'''
os.mkdir('./VCF/'+writeFolder)

Sites = A.columns
    
a = []
sites = []

#print(len(Sites))

for col_ in range(A.shape[1]):
    col1 = list(A.iloc[:, col_])
    
    if sum(col1) >2 and sum(col1) < 196:
        a.append(col1)
        sites.append(Sites[col_])
        
a = pd.DataFrame(a)
a = a.T
#print(len(Sites))
a.columns = sites


range_for = a.shape[1]//10

for i in range(range_for):
	start = i*10
	end = start+numm
	if end <= a.shape[1]:
		fname = "./VCF/"+ writeFolder + '/'+ filename[:-4] + "_" + str(i+1) + ".csv"
		a.iloc[:, start:end].to_csv(fname, index=False)

print('number of subfiles generated:', range_for)



