İlgil algoritmalar dosyaların altına bulumaktadır.         

# Needleman-Wunsch ve Smith Waterman için
######################################################################
Verilen score matrixleri pandas DataFrame'i olarak tanımlanmış olup aşağıdaki formdadır,
farklı score matrixleri ile algoritmayı çalıştırmadan önce match_score() fonksiyonu altında tanımlı olan 
data={'A':[5,-4,-4,-4],'T':[-4,5,-4,-4],'C':[-4,-4,5,-4],'G':[-4,-4,-4,5]} satırı değiştirmeniz gerekmektedir.
###################################################
Görseleştirmek için kullanmış olduğum uygulamalarda aynı dosyaların altında bulunmaktadır.



# Star Alignment için
#############################################################
Star Alg. arkada global optimum gerçekleştiren bir algoritma olduğu için Needleman-Wunsch classı import edilmiş ve böyle çalıştırılmıştır.

gap,match,mismatch değerleri ise parametre olarak classlara verilmiştir.
nw= Needleman_Wunsch(match,mismatch,gap) #instance of Needleman Wunsch

## Star Aligment için gerçekleştirilen iki uygulama:
 * sample(StarAlignment).py (Basic Uygulama) 
 * Star_alignment.py (Proje için istenen uygulama)
########################################


CLUSTALW için ise sadece hamming distance sonucunda elde edilen matrix oluşturulabilmiştir. Devamını yetiştiremedim :(


# Buna ek:
## Report'da verilen sonuçlar elde edilen en iyi sonuçlar(optimum score) olup diğer scoreları görebilmeniz için algoritmalar çalıştırmanız ve çıktılarına bakmanız yeterlidir.