from GlobalAlignment import Needleman_Wunsch
"""
The star alignment approach is not guaranteed to give
an optimal alignment due to the “once a gap, always a gap’

"""

f=open('dna_sequences.txt',"r")

arr_dna_seq=[]

for line in f:
    #print(line)
    arr_dna_seq.append(line)

#print(len(arr_dna_seq))

s1=arr_dna_seq[0] #center sequence
s2=arr_dna_seq[1]
s3=arr_dna_seq[2]
s4=arr_dna_seq[3]


gap=-1 
match=1 
mismatch=-1 
nw= Needleman_Wunsch(match,mismatch,gap) #instance of Needleman Wunsch

#Once Gap Always Gap
# Bu prensipli algoritmamızı çalıştırdığımız için alignment sonucunda elde etiğimiz yeni Center Sequnece'ımız
# Diğer alignmentlara parametre olarak veririz.


new_align1,new_align2,score1=nw.alignment(s1,s2) #

print("-----")
print("Score:"+str(score1))
print("Alignment1:" +str(new_align1))
print("Alignment2:" +str(new_align2))
print("--------")


new_align1v2,new_align3,score2=nw.alignment(new_align1,s3)

print("-----")
print("Score:"+str(score2))
print("Alignment1:" +str(new_align1v2))
print("Alignment3:" +str(new_align3))
print("--------")



center_Align1,new_align4,score3=nw.alignment(new_align1v2,s4)
print("-----")
print("Score:"+str(score3))
print("Alignment1:" +str(center_Align1))
print("Alignment4:" +str(new_align4))
print("--------")









list_of_Seq_Score=[]
list_of_Seq=[new_align1,new_align2,new_align3,new_align4]

new_list_of_Seq=[]
for i in list_of_Seq: #Tekrardan center Sequnce diğer Sequnceler ile align ederiz.
    new_align,new_align,new_score=nw.alignment(center_Align1,i)
    new_list_of_Seq.append(new_align)

    list_of_Seq_Score.append(new_score)#save new scores

consensus_sequence=""#most common letter


print("SON Durum")
print("Sequence.1 : {}" .format(new_list_of_Seq[0]))
for i  in range(1,len(new_list_of_Seq)):
    print("Sequence.{}:  {} Score:{}" .format(i+1,new_list_of_Seq[i],list_of_Seq_Score[i]))
    
print("-----------------------------------------------")


"""
2. Consensus score. The consensus of a multiple alignment
is a sequence of the most common characters in each column of the
alignment. For example,
"""


from collections import Counter
my_counts=Counter()

for i in range(0,len(new_list_of_Seq[0])):
    my_counts=Counter([new_list_of_Seq[0][i],new_list_of_Seq[1][i],new_list_of_Seq[2][i],new_list_of_Seq[3][i]])
    #print(my_counts)
    character=my_counts.most_common(1)
    consensus_sequence+=character[0][0]

print("Consensus:   "+str(consensus_sequence))