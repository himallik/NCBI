# Using readlines()
import os
import glob


def getSeqPositions(line):
    seqPositionsStrArray = line.strip().replace(
        '\n', '').replace('>', '').split('..')
    seqPositionsIntArray = [int(numeric_string)
                            for numeric_string in seqPositionsStrArray]
    return seqPositionsIntArray


# Read fasta file and prepare fasta sequence string
fastaFilePath = glob.glob("./data/*.fasta")
fastaFile = open(fastaFilePath[0], 'r')
fastaFileStr = ''
i = -1
for line in fastaFile:
    i = i+1
    if(i != 0):
        fastaFileStr = fastaFileStr+line.replace('\n', '')

genpeptFilePath = "./data/*.genpept"

for filename in glob.glob(genpeptFilePath):
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('VERSION'):
                version = line.split()[1]
                # Create folder with version name
                folderpath = "./data/"+version
                if not os.path.exists(folderpath):
                    os.makedirs(folderpath)

            if line.strip().upper().startswith('REGION'):
                positions = getSeqPositions(line.upper().split('REGION', 1)[1])
                filePath = "./data/"+version+"/"+version + \
                    "_"+str(positions[0])+"_"+str(positions[1])
                f = open(filePath, 'a')
                f.write(fastaFileStr[positions[0]-1:positions[1]-1])
                f.close()
