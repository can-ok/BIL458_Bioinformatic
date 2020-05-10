from HammingDistance import HammindDistance
import numpy as np
import pandas as pd

f=open('dna_sequences.txt',"r")

arr_dna_seq=[]

for line in f:
    #print(line)
    arr_dna_seq.append(line)

#print(len(arr_dna_seq))

s1=arr_dna_seq[0] #center sequence
s2=arr_dna_seq[1]

match=1
mismatch=-1
hm=HammindDistance(match,mismatch)

x=len(arr_dna_seq)  # create 27x27 matrix which contains hamming distance of Sequnces 
HammindDistance_Matrix=[[0 for j in range(x)] for i in range(x)]#score matrix



for i in range(0,27):
    for j in range(0,27):
        s1=arr_dna_seq[i]
        s2=arr_dna_seq[j]
        seq1,seq2,score=hm.alignment(s1,s2)
        HammindDistance_Matrix[i][j]=score

HammindDistance_Array=np.asarray(HammindDistance_Matrix)
df = pd.DataFrame(data=HammindDistance_Array)

df = df.where(np.triu(np.ones(df.shape)).astype(np.bool))


