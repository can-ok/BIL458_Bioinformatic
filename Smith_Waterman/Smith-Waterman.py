"""
the algorithm very similar to Needleman W.,the only difference here we have another option which is the zero
"""

import pandas as pd

#####
class SmithWaterman:
    
    def __init__(self,match,mismatch,GAP):
        self.match=match
        self.mismatch=mismatch
        self.GAP=GAP

    def match_score(self,s1,s2):#Score Matrix'den score değerleri elde edilir
        data={'A':[5,-4,-4,-4],'T':[-4,5,-4,-4],'C':[-4,-4,5,-4],'G':[-4,-4,-4,5]}
        df = pd.DataFrame(data, index =['A', 'T', 'C', 'G'])

        value=df.loc[s1,s2]
        return value



    def calculate_match(self,ch1,ch2):
        if(ch1==ch2):
            return self.match_score(ch1,ch2)
        elif(ch1=='-' or ch2=='-'):
            return self.GAP
        else:#mistmatch
            return self.match_score(ch1,ch2)

    def show(self,score):
        for line in score:
            print(line)


    def calculate_score(self,alignment1, alignment2,s1,s2):
        align1 = alignment1[::-1]    
        align2 = alignment2[::-1]    
        
        
        score = 0
        align_sequence=''
        for i in range(0,len(align1)):

            if(align1[i] !='-' and align2[i] != '-'): #if there is no gap check for match or mismatch
                if(align1[i]==align2[i]): #if match
                    align_sequence+=align1[i]
                    score+=self.calculate_match(align1[i],align2[i])
                elif(align1[i]!=align2[i]):#if mismatch
                    score+=self.calculate_match(align1[i],align2[i])
                    align_sequence+=align1[i]

            elif(align1[i]=='-' or align2[i]=='-'):
                score+=self.GAP
                align_sequence+='-'

        
        print("SCORE:"+str(score))
        print("Sequence 1: "+str(s1))
        print("Aligned sequence: "+str(align_sequence))
        print("Sequence 2: "+str(s2))
        
        return align1,align2,score


    def traceback(self,S,traceback_matrix,s1,s2):
        x,y=len(s1),len(s2)

        score_max,max_x,max_y=0,0,0      
        #Global Alg. gibi değil! max score array'ın sonunda olmak zorunda değil 
        #Seach holl array to find max_score
        for i in range(1,x+1):
            for j in range(1,y+1):
                if(S[i][j]>score_max):
                    score_max=S[i][j]
                    max_x=i 
                    max_y=j
        
        """
        max score elde edilen koordinatlar
        print(max_x)
        print(max_y)
        """
        #print("MAX score: "+str(score_max))
            
        #cut the array
        new_S=S[:max_x+1][:max_y+1]

        alignment1,alignment2='',''
        x,y=max_x,max_y

        while(traceback_matrix[x][y] != "ZERO"):
            
        
            if(traceback_matrix[x][y]=="DIAG"):#if match/mismtach
                alignment1+=s1[x-1]
                alignment2+=s2[y-1]
                x-=1
                y-=1

            elif(traceback_matrix[x][y]=="LEFT"):
                alignment1+=s1[x-1]
                alignment2+='-'
                x-=1

            elif(traceback_matrix[x][y]==' UP '):
                alignment1+='-'
                alignment2+=s2[y-1]
                y-=1



        align1,align2,score=self.calculate_score(alignment1,alignment2,s1,s2)
        
        return align1,align2,score



    def alignment(self,s1,s2):
        x,y=len(s1),len(s2)

        S=[[0 for j in range(y+1)] for i in range(x+1)]
        traceback_matrix=[['' for j in range(y+1)] for i in range(x+1)] #score matrix

    

        #Initialization
        #F(0,0)=0 F(0,j)=j F(i,0)=i

        #first row and first column initialized with 0's

        traceback_matrix[0][0]="ZERO"

        for i in range(1,x+1):#y
            S[i][0]=i*0
            traceback_matrix[i][0]="ZERO"
        
        for j in range(1,y+1):#x
            S[0][j]=j*0
            traceback_matrix[0][j]="ZERO"

        for i in range(1,x+1):
            for j in range(1,y+1):
                S[i][j]=max(
                        S[i-1][j-1]+self.calculate_match(s1[i-1],s2[j-1]),
                        S[i-1][j]+self.GAP,#deletion
                        S[i][j-1]+self.GAP,
                        0 #
                        )
            
                if(S[i][j]==S[i-1][j-1]+self.calculate_match(s1[i-1],s2[j-1])):
                    traceback_matrix[i][j]="DIAG"
                if(S[i][j]==S[i-1][j]+self.GAP):
                    traceback_matrix[i][j]="LEFT"
                if(S[i][j]==S[i][j-1]+self.GAP):
                    traceback_matrix[i][j]=' UP '

                if(S[i][j]==0): #and also we have zero option
                    traceback_matrix[i][j]="ZERO"

        #show(traceback_matrix)
        
        #self.show(S)
        align1,align2,score=self.traceback(S,traceback_matrix,s1,s2)
        return align1,align2,score


  


"""
a="TGTTACGG"
b="GGTTGACTA"

sm.alignment(a,b)
"""



sm=SmithWaterman(None,None,-6)

f=open('dna_sequences.txt',"r")

arr_dna_seq=[]

for line in f:
    line=line.replace("\n","")# delete \n 
    line=line.replace(" ","")#delete white spaces
    arr_dna_seq.append(line)


s1=arr_dna_seq[0]
del arr_dna_seq[0]



best_alignment_score=0
best_alignment_Seq1=''
best_alignment_Seq2=''

for i in range(0,len(arr_dna_seq)):#compare with the other sequences
    new_align1,new_align2,score=sm.alignment(s1,arr_dna_seq[i]) 
    if(best_alignment_score<score):
        best_alignment_score=score
        best_alignment_Seq1=new_align1
        best_alignment_Seq2=new_align2
        
    print("Score:"+str(score))
    print("Alignment1: " +str(new_align1))
    print("Alignment{}: {}".format(i+2,str(new_align2)))

print("*****************")
print("Score:"+str(best_alignment_score))
print("Sequence1: " +str(best_alignment_Seq1))
print("Sequence2:{}".format(str(best_alignment_Seq2)))

sub=''
for j in range(0,len(best_alignment_Seq1)):
    if(best_alignment_Seq1[j]==best_alignment_Seq2[j]):
        sub+="|"
    else:
        sub+=" "


print(best_alignment_Seq1)
print(sub)
print(best_alignment_Seq2)
