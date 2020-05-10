import pandas as pd
import seaborn as sns
#####
class Needleman_Wunsch:

    def __init__(self,match,mismatch,GAP):
        self.match=match
        self.mismatch=mismatch
        self.GAP=GAP

    def match_score(self,s1,s2):
        data={'A':[5,-1,-4,-4],'T':[-1,8,-3,-4],'C':[-4,-3,4,-4],'G':[-4,-4,-4,6]} 
        df = pd.DataFrame(data, index =['A', 'T', 'C', 'G'])
        #print(df)
        value=df.loc[s1,s2]
        return value


    

    def calculate_match(self,s1,s2):
        if(s1==s2):
            return self.match_score(s1,s2)

        elif (s1=='-' or s2=='-'):#backtrackin yaparken
            return self.GAP
        else:
            return self.match_score(s1,s2)

    def show(self,score):
        for line in score:
            print(line)
        
            


    def calculate_score(self,alignment1, alignment2):
        align1 = alignment1[::-1]    
        align2 = alignment2[::-1]    
        
        
        score = 0
        for i in range(0,len(align1)):

            if(align1[i] !='-' and align2[i] != '-'): #if there is no gap check for match or mismatch
                if(align1[i]==align2[i]): #if match
                    score+=self.calculate_match(align1[i],align2[i])
                elif(align1[i]!=align2[i]):#if mismatch
                    score+=self.calculate_match(align1[i],align2[i])

            elif(align1[i]=='-' or align2[i]=='-'):
                score+=self.GAP
        
        """
        print("SCORE:"+str(score))
        print("Alignment1: "+str(align1))
        print("Alignment2: "+str(align2))
        """
        return align1,align2,score


    def traceback(self,s1,s2,traceback_matrix):
        # Traceback and compute the alignment 
        alignment1,alignment2='',''
        x,y=len(s1),len(s2)

        while(x>0 and y>0):
            
        
            if(traceback_matrix[x][y]=="DIAG"):
                alignment1+=s1[x-1]
                alignment2+=s2[y-1]
                x-=1
                y-=1
            elif(traceback_matrix[x][y]=="LEFT"):
                alignment1+=s1[x-1]
                alignment2+='-'
                x-=1
            elif(traceback_matrix[x][y]==" UP "):
                alignment1+='-'
                alignment2+=s2[y-1]
                y-=1
        
        #fill with gap
        while x > 0:
            alignment1 += s1[x-1]
            alignment2 += '-'
            x -= 1
        while y > 0:
            alignment1 += '-'
            alignment2 += s2[y-1]
            y -= 1
        
        align1,align2,score=self.calculate_score(alignment1,alignment2)

        return align1,align2,score


    def alignment(self,s1,s2):
        x,y=len(s1),len(s2)


        F=[[0 for j in range(y+1)] for i in range(x+1)]#score matrix
        traceback_matrix=[['' for j in range(y+1)] for i in range(x+1)]#score matrix

        #create dynamic array

        #Initialization
        #F(0,0)=0 F(0,j)=j F(i,0)=i
        for i in range(1,x+1):#y
            F[i][0]=i*self.GAP
            traceback_matrix[i][0]=" GP "
        
        for j in range(1,y+1):#x
            F[0][j]=j*self.GAP
            traceback_matrix[0][j]="GP "

        


        for i in range(1,x+1):
            for j in range(1,y+1):
                #alignement, deletion , insertion
                F[i][j]=max(
                            F[i-1][j-1]+self.calculate_match(s1[i-1],s2[j-1]),
                            F[i-1][j]+self.GAP,#deletion
                            F[i][j-1]+self.GAP
                            )
                if(F[i][j]==F[i-1][j-1]+self.calculate_match(s1[i-1],s2[j-1])):
                    traceback_matrix[i][j]="DIAG"
                if(F[i][j]==F[i-1][j]+self.GAP):
                    traceback_matrix[i][j]="LEFT"
                if(F[i][j]==F[i][j-1]+self.GAP):
                    traceback_matrix[i][j]=" UP "
                


        #self.show(F)
        #print("TRACBACK MATRİX \n")
        #self.show(traceback_matrix)
        #print("Best alignments")
        align1,align2,score=self.traceback(s1,s2,traceback_matrix)#give sequences and traceback matrix as parameter
        return align1,align2,score
            







a="GCATGCT"
b="GATTACA"



f=open('dna_sequences.txt',"r")

arr_dna_seq=[]

for line in f:
    line=line.replace("\n","")# delete \n 
    line=line.replace(" ","")#delete white spaces
    arr_dna_seq.append(line)


s1=arr_dna_seq[0]#take the first seq
del arr_dna_seq[0]


GAP=-6
nw= Needleman_Wunsch(None,None,GAP) #instance of Needleman Wunsch

best_alignment_score=0
best_alignment_Seq1=''
best_alignment_Seq2=''

for i in range(0,len(arr_dna_seq)):#compare with the other sequences
    new_align1,new_align2,score=nw.alignment(s1,arr_dna_seq[i]) 
    if(best_alignment_score<score):
        best_alignment_score=score
        best_alignment_Seq1=new_align1
        best_alignment_Seq2=new_align2
        
    print("Score:"+str(score))
    print("Alignment1: " +str(new_align1))
    print("Alignment{}: {}".format(i+2,str(new_align2)))

print("*****************")
print("Score:"+str(best_alignment_score))
print("Alignment1: " +str(best_alignment_Seq1))
print("Alignment2:{}".format(str(best_alignment_Seq2)))

sub=''
for j in range(0,len(best_alignment_Seq1)):
    if(best_alignment_Seq1[j]==best_alignment_Seq2[j]):
        sub+="|"
    else:
        sub+=" "


print(best_alignment_Seq1)
print(sub)
print(best_alignment_Seq2)



