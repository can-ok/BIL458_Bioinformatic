import pandas as pd

#####
class HammindDistance:

    def __init__(self,match,mismatch):
        self.match=match
        self.mismatch=mismatch
        

    def match_score(self,s1,s2):
        data={'A':[5,-1,-4,-4],'T':[-1,8,-3,-4],'C':[-4,-3,4,-4],'G':[-4,-4,-4,6]} 
        df = pd.DataFrame(data, index =['A', 'T', 'C', 'G'])
        #print(df)
        value=df.loc[s1,s2]
        return value


    

    def calculate_match(self,s1,s2):
        if(s1==s2):
            return self.match  #match_score(s1,s2)
        else:
            return self.mismatch

    def show(self,score):
        for line in score:
            print(line)



    def calculate_score(self,alignment1, alignment2):
        align1 = alignment1[::-1]    #reverse sequence 1
        align2 = alignment2[::-1]    #reverse sequence 2
        
        
        score = 0
        for i in range(0,len(align1)):

            if(align1[i] !='-' and align2[i] != '-'): #if there is no gap check for match or mismatch
                if(align1[i]==align2[i]): #if match
                    score+=self.calculate_match(align1[i],align2[i])
                elif(align1[i]!=align2[i]):#if mismatch
                    score+=self.calculate_match(align1[i],align2[i])

           
        
       
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
            F[i][0]=i*0
            traceback_matrix[i][0]=" GP "
        
        for j in range(1,y+1):#x
            F[0][j]=j*0
            traceback_matrix[0][j]="GP "

        


        for i in range(1,x+1):
            for j in range(1,y+1):
                #alignement, deletion , insertion
                F[i][j]=F[i-1][j-1]+self.calculate_match(s1[i-1],s2[j-1])
                            
                            
                if(F[i][j]==F[i-1][j-1]+self.calculate_match(s1[i-1],s2[j-1])):
                    traceback_matrix[i][j]="DIAG"
                
                


        #self.show(F)
        #print("TRACBACK MATRİX \n")
        #self.show(traceback_matrix)
        #print("Best alignments")
        align1,align2,score=self.traceback(s1,s2,traceback_matrix)#give sequences and traceback matrix as parameter
        return align1,align2,score
            



