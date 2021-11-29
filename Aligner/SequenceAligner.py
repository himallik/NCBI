# Using readlines()
import os
import glob
import pandas as pd

# Read fasta file and prepare fasta sequence string
fastaFilePath = glob.glob("./data/*.fasta")
fastaFile1 = open(fastaFilePath[0], 'r')
print('fastaFile: ', fastaFile1)
fastaFile2 = open(fastaFilePath[1], 'r')
print('fastaFile: ', fastaFile2)

fastaFileStr = ''
i = -1
df1 = pd.DataFrame(columns=['Index', 'SeqName'])
for line in fastaFile1:
    i = i+1
    if(line.startswith('>')):
        seqName = line.split('[')[1].split(']')[0]
        df1 = df1.append({'Index': i, 'SeqName': seqName}, ignore_index=True)

i = -1
df2 = pd.DataFrame(columns=['Index', 'SeqName'])
for line in fastaFile2:
    i = i+1
    if(line.startswith('>')):
        seqName = line.split('[')[1].split(']')[0]
        df2 = df2.append({'Index': i, 'SeqName': seqName}, ignore_index=True)

print('df1  %%%%%%%%%%%% BEFORE SORT: ', df1)
df1 = df1.sort_values('SeqName')
# print('df1 #############  AFTER SORT: ', df1)

df2.sort_values('SeqName')

mdf1 = pd.DataFrame(columns=['Index', 'SeqName'])
mdf2 = pd.DataFrame(columns=['Index', 'SeqName'])
mj = 0
for i, irow in df1.iterrows():
    iSeqName = irow["SeqName"]
    matchNotFound = True
    for j, jrow in df2.iterrows():
        if(j > mj) and matchNotFound:
            jSeqName = jrow["SeqName"]
            if(iSeqName == jSeqName):
                #            matchFound = True
                # print('iSeqName: ', iSeqName, "   jSeqName: ", jSeqName)
                # if(iSeqName == jSeqName):
                # print('@@@ entered  iIndex: ', irow['Index'], '   jIndex: ', jrow['Index'])
                mdf1 = mdf1.append(
                    {'Index': irow['Index'], 'SeqName': iSeqName}, ignore_index=True)
                mdf2 = mdf2.append(
                    {'Index': jrow['Index'], 'SeqName': jSeqName}, ignore_index=True)
                mj = j
                matchNotFound = False

reorganizedFastaFileName1 = fastaFile1.name.split('fasta')[0]+'REORG.fasta'
reorganizedFastaFileName2 = fastaFile2.name.split('fasta')[0]+'REORG.fasta'

reorganizedFastaFile1 = open(reorganizedFastaFileName1, "w")
reorganizedFastaFile2 = open(reorganizedFastaFileName2, "w")

length = len(mdf1)
for i in range(length):
    index = mdf1.loc[i, "Index"]
    fastaFile1.seek(0)
    for position, line in enumerate(fastaFile1):
        if (index <= position):
            reorganizedFastaFile1.write(line)
            if line.strip() == '':
                break
reorganizedFastaFile1.close()

for i in range(length):
    index = mdf2.loc[i, "Index"]
    fastaFile2.seek(0)
    for position, line in enumerate(fastaFile2):
        if (index <= position):
            reorganizedFastaFile2.write(line)
            if line.strip() == '':
                break
reorganizedFastaFile2.close()
