
### Needleman-Wunsch ve Smith Waterman için
### Star Alignment için
### CLustaLW



# [Report](../master/Report.pdf)


# --------------------------
# -------------------------------



# DERİN ÖĞRENME AĞLARI İLE COVID-19 Sınıflandırma

## Açıklama

Gerçekleştirmiş olduğumuz çalışma 3 ayrı programdan oluşmaktadır. Bunun sebebi ise bilgisayarım sahip olduğu donanımın derin yapay sinir ağını eğitecek yeterlilikte olmamasıdır. Bu programlar şöyledir: 
1. preprocessing.py: Bu programda dateset klasöründe bulunan verilerimiz okunarak belirli ön işleme (preprocess) maruz bırakılır. Burada gerçekleştirilen ön işlem aşağıda daha ayrıntılı olarak anlatılmıştır. Daha sonra bu ön işlemden geçmiş veriler ve bu verilerin sahip oldukları etiketler(labels) NPZ dosya formatına dönüştürülerek daha sonra Google drive yüklenmek üzere bulunduğu dizine kaydedilir.
2. NameofModel_Num.Class.ipynb: Bu programın adı sahip olduğu mimariye ve gerçekleştirdiği sınıflandırma sayışa göre şekillenmektedir“Örnek:AlexNet_3class_..”. Bu dosyalar Google Colab’ın ücretsiz GPU servisinde kullanmak için tasarlanmıştır. Bu programlarda önce NPZ dosya formatında bulunan veriler ve etiketleri okunur daha sonra train ve test olmak üzere farklı kümeye bölünür. Daha sonra bu veriler tasarlanan model verilerek modelin öğrenmesi gerçekleştirilir. Model öğrenimi sırasında en yüksek validation accuracy’nin elde edildiği ağırlıklar ve eğitim sonunda da model HDF5/H5 formatında kayıt edilir. Bu kaydedilen model isterse bir uygulamamanın ara planında isterse de bizim gibi eğitim sonucunu değerlendirmek için yüklenip kullanılabilir. (Eğitim sonucunda kaydedilen modeller ve ağırlıklar test edebilmeniz için ipynb dosyaları ile birlikte verilmiştir.)
3. performance_model.ipynb: Bu programda eğitilmiş olan modele test verisi uygulanarak modelin performansı ölçülür. Önce modele test verisi verilir ve tahminler elde edilir. Elde edilen bu tahminler ışığında Roc curveler çizdirilir ve confusion matrixleri oluşturulur.

Devam eden kısımda gerçekleştirilen işlemeler ve Tasarlan Derin sinir ağlarında kullanılan yapılara ilişkin açıklamalar yer verilmiştir.


### Ön İşleme (Preprocessing)
Modeli eğitirken kullanmış olduğumuz veri kümesindeki mr görüntüleri çoğu farklı boyutta sahip olup farklı açılardan elde edilmiştir. Görüntülerin farklı açılarda olması bizim için bir problem doğurmazken, farklı resim boyutlarına sahip olmamız bizim için problem oluşturmaktadır. Veri kümemizdeki her resmi aynı sinir ağına uygulayacağımız için belirlenmiş bir boyuta resimleri kullanmamız gerekmektedir. Görsellerin boyutunu çift yönlü doğrusal interpolasyon yönteminde yararlanarak 350x350 boyutuna indirgeriz. Çift yönlü doğrusal interpolasyon yeniden örnekleme işlemi olup resmin boyunun ve enin farklı
oranlarda olduğu durumlarda bize resimlerimizde herhangi bir deformasyon oluşmadan boyutunda indirgeme yapmamıza olanak sağlamaktadır. Bazı durumlarda ise resim gri resme dönüştürülüp eğitim verilmiştir. Resmimiz 3 renk kanalından oluşuyordu bu renk kanalarından kurtularak resmimiz sadece 1 kanaldan oluşan pikselleri 0-255 arasında değerler alabilen bir gri resim halin getiriyoruz. Bunla da resmi ışığın vurma açası, parlaklık veya imzanın atıldığı kalemin rengi gibi parametrelerden bağımsız hale getiriyoruz. Ayrıca buna ek olarak 3 kanal üzerinde çalışmak yerine tek kanal üzerinde çalışarak hesaplama maliyetimizi de düşürmüş oluyoruz.
En sonunda ise görselleri eğitime vermeden normalizasyon uygularız. Böylelikle değerlerimiz [0-1] aralığına çekilmiş olur. Böylelikle maliyet fonksiyonun (cost fuction) yükü azalmış olur ve eğitim daha kolay hale gelir.


### Data Augmentation (Veri artırma)
Derin sinir ağlarında genellikle nispeten daha büyük ve çeşitli veri kümeleri üzerinde eğitilmiş sistemlerin diğerlerine nazaran daha sağlam (robust) olduğu bilinmektedir. Yeterli büyüklüğü ve veri çeşitliğin olmadığı sistemlerde sağlıklı çalışan tanıma sistemi oluşturmanın mümkün olmayacaktır. Buna çözüm olarak örnek sayısını artırma yoluna gideriz, mevcut veri kümemize döndürme(rotation), öteleme (translation) vb. işlemler uygulayarak sentetik veriler üretiriz.


### ModelCheckpoint 
Model 30 periyot (epoch) buyunca eğitilir fakat ModelCheckpoint kullanarak eğitimi sırasında en iyi başarımın elde edildiği (epoch) periyottaki modelin ağırlık değerleri saklanır. Bu sayede eğitim sırasında global ya da iyi lokale erişildikten sonra gerçekleşebilecek uzaklaşmaların sonucunda kaybolacak optimum ağırlıkların kaybolmaması sağlanmış olunur. Burada en iyi başarımı tanımlama için validation accuracy değerini kullandık. Bu anlamı eğitimin testi sırasında gerçekleşen en yüksek doğruluğun olduğu periyottaki ağırlıkları saklayacağız. Early Stopping Genellikle eğitim sırasında öğrenmenin gerçekleşmediği ya da overfitting oluştuğu durumlarda modelin eğitimin devam etmesini istemeyiz. Bu durumlarada erken durdurmadan yararlanabiliriz. Erkan durdurma için parametreleri her modele göre değiştirmiş olsam da bütün modellere uygulamış bulunmaktayım.

### Early Stopping 
Genellikle eğitim sırasında öğrenmenin gerçekleşmediği ya da overfitting oluştuğu durumlarda modelin eğitimin devam etmesini istemeyiz. Bu durumlarada erken durdurmadan yararlanabiliriz. Erkan durdurma için parametreleri her modele göre değiştirmiş olsam da bütün modellere uygulamış bulunmaktayım.


![2class](https://user-images.githubusercontent.com/47722483/88718182-3d918500-d12a-11ea-8961-466fcb8ef0e2.png)
![3class](https://user-images.githubusercontent.com/47722483/88718184-3e2a1b80-d12a-11ea-992c-5e494e326b5f.png)
![4class](https://user-images.githubusercontent.com/47722483/88718185-3e2a1b80-d12a-11ea-9e91-a5c33ba92668.png)

-----------------------
---------------------
## CanNET
Tasarlana ağ ile ne AlexNet kadar karmaşık düzeyi yüksek ne de LeNet kadar basit bir ağ tasarlamak istenmiştir. AlexNet karmaşıklığına sahip olmayarak ağda başarılı öğrenme gerçekleştirilecek ve LeNet daha başarılı sınıflandırma elde edilecektir. Bu iki önemli mimarinin arasında yer alacak ve daha hızlı tepki veren, daha iyi öğrenen bir ağ tasarlanmak istenmiştir. Bu bağlamda ağ tasarlanırken AlexNet’den feyz alınarak 3lü Conv katmanına (Triple Conv) yer verilmiş ve kullanılan filtre boyutlarında küçülmeye gidilmiştir. Ağın parametreleri ve mimarisi aşağıdaki tabloda verilmiştir.
|Katmna   | Boyut   |Parametre   |
|---|---|---|
| Konvolüsyon Katmanı 1  | 32x4x4  |Stride=2   |
| Havuzlama Katmanı 1  |32x2x2   | Stride=0 ; Padding=’valid’  |
| Konvolüsyon Katmanı 2| 16x4x4  | Stride=2  |
|Havuzlama Katmanı 2   |  16x2x2 |  Stride=2 ; Padding=’valid’ |
|  Konvlüsyon Katmanı 3_a |  32x1x1 |  Stride=1 |
| Konvlüsyon Katmanı 3_b  |  32x1x1 | Stride=1  |
|Konvlüsyon Katmanı 3_c   | 32x1x1  | Stride=1  |
|  Havuzlama Katmanı 3 |  32x2x2 |  Stride=2 ; Padding=’valid’ |
| Tam Bağlı Katman 1 + Dropout 1  | 1024  | Rate=0.4  |
|  Tam Bağlı Katman 2+Dropout 2 | 1024  | Rate=0.4  |


#### 2 Class (Covid-Normal)
##### RMSprop

![RMSPROP_conf](https://user-images.githubusercontent.com/47722483/88717854-d5db3a00-d129-11ea-93e2-6a5df98f4f54.PNG)
![RMSPROP_basarim](https://user-images.githubusercontent.com/47722483/88717853-d542a380-d129-11ea-9c5d-afa602868f52.PNG)

##### SGD

![SGD_conf](https://user-images.githubusercontent.com/47722483/88717884-e095cf00-d129-11ea-9057-2610b132b9b9.PNG)
![SGD_basarim](https://user-images.githubusercontent.com/47722483/88717881-df64a200-d129-11ea-997f-2407e353e12c.PNG)


#### 3 Class (Covid-Normal-Bacteria)
##### Adam
![Adam_Confunsion](https://user-images.githubusercontent.com/47722483/88717730-a5939b80-d129-11ea-8c9e-411685190baa.PNG)
![Adam_Basarim](https://user-images.githubusercontent.com/47722483/88717735-a88e8c00-d129-11ea-9f86-f39c2a6809a6.PNG)

##### RMSprop
![RMSPROP-Confusion](https://user-images.githubusercontent.com/47722483/88717764-b512e480-d129-11ea-901c-0280db8779af.PNG)
![RMSPORP-Basirimi](https://user-images.githubusercontent.com/47722483/88717762-b47a4e00-d129-11ea-80cf-87a823fbcbd8.PNG)


#### 4 Class (Bacteria-Virus-Covid-Normal)

##### Adadelta
![Adadelta_Confunsion](https://user-images.githubusercontent.com/47722483/88717523-551c3e00-d129-11ea-8a1c-8cd4ab41bd39.PNG)

##### Adam
![Adam_Confunsion](https://user-images.githubusercontent.com/47722483/88717632-7d0ba180-d129-11ea-95f5-1bff999bdf56.PNG)
![Adam_Basarim](https://user-images.githubusercontent.com/47722483/88717655-85fc7300-d129-11ea-94f6-7f165ecbe75b.PNG)




## Report(Turkish): [Can Okan Taşkıran 100042773.pdf](https://github.com/can-ok/BIL458_Bioinformatic/files/4991029/Can.Okan.Taskiran.100042773.pdf)



