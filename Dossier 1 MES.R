rm(list = ls())
library(wooldridge)
library(stargazer)
library(ggplot2)
library(data.table)
library(tibble)
library(lmtest)
library(sandwich)
library(corrplot)
library(dplyr)
library(lmtest)
library(systemfit)
library(tidyverse)
library(AER)
library(stargazer)
library(plm)
data(beauty)
summary(beauty)                                   

data= wooldridge::beauty
data=data.frame(data[1],data[17],data[5],data[6],data[10],data[13],data[11],
                data[9],data[7],data[16])

# Graphique de la répartition des hommes et femmes dans l'échantillon

x=c(824,436)
noms_barres <- c("Hommes","Femmes")
barplot(x,ylim=c(0,900),col=c("blue","orchid2"),ylab="Effectif",
        main="Répartition entre hommes et femmes dans notre population")
legend(x="top",legend=c("Hommes 824 (65,4%)","Femmes 436 (34,6%)"),
       fill=c("blue","orchid2"))
box()

# Répartition des notations "looks" dans un diagramme circulaire 

table(beauty$looks)

valeurs <- c(13,142,722,364,19)
pie(valeurs,col=c("darkblue", "brown1", "green3", "lightblue1", "mediumorchid2")
    ,labels=c("1","2","3","4","5"), 
    main="Répartition des notations 'Looks'",cex=1)

# Faire une comparaison des moyennes de salaire (et des min et max)
# selon le genre et le rang de beauté 

#### FEMMES

summary(data %>% filter(female == '1',looks == '5') %>% select (wage))
# moyenne = 3.902 médiane = 4.175

summary(data %>% filter(female == '1',looks == '4') %>% select (wage))
# moyenne = 4.745 médiane = 3.805

summary(data %>% filter(female == '1',looks == '3') %>% select (wage))
# moyenne = 4.208 médiane = 3.750

summary(data %>% filter(female == '1',looks == '2') %>% select (wage))
# moyenne = 3.829 médiane = 3.415

summary(data %>% filter(female == '1',looks == '1') %>% select (wage))
# moyenne = 2.154 médiane = 2.150


#### HOMMES 

summary(data %>% filter(female == '0',looks == '1') %>% select (wage))
# moyenne = 6.164 médiane = 6.625

summary(data %>% filter(female == '0',looks == '2') %>% select (wage))
# moyenne = 6.249 médiane = 5.355

summary(data %>% filter(female == '0',looks == '3') %>% select (wage))
# moyenne = 7.599 médiane = 6.730

summary(data %>% filter(female == '0',looks == '4') %>% select (wage))
# moyenne = 7.226 médiane = 6.310

summary(data %>% filter(female == '0',looks == '5') %>% select (wage))
# moyenne = 9.924 médiane = 7.960

#HISTOGRAMME POUR METTRE EN AVANT CES COMPARAISONS

x = c(2.150,3.415,3.750,3.805,4.175) 
y = c(6.625,5.355,6.730,6.310,7.960) 
type = c("1","2","3","4", "5") 
moyennes = c(x,y) 
moyennes = matrix(moyennes,nc=5, nr=2, byrow=T) 
colnames(moyennes) = type 
barplot(moyennes,beside=T,col=c("violetred1","mediumblue"),
        main="Comparaison du salaire horaire médian en fonction du genre et 
        de l'apparence",
        xlab="Looks (pink : women ; blue : men)",ylab="Wage",ylim=c(0,10)) ; 
box()

#Régressions ~
#
reg1 <- lm(beauty$lwage ~ beauty$looks)
summary(reg1)
plot(beauty$looks, beauty$lwage, main="Salaire en fonction de l'apparence", 
     xlab="Notation de l'apparence", ylab="Logarithme salaire horaire en $ 
     canadien") 
abline(lm(beauty$lwage ~ beauty$looks), col="red")
stargazer(reg1, header=FALSE,type="text")

#Explication de la rég1 : 
#Ici c'est un modèle log-lin
#On veut savoir si la beauté influence le salaire -> corrélation positive
#Une augmentation d'un point de beauté fait augmenter le salaire de 5% 
#Impressionnant mais R2 faible 

reg2 <- lm(beauty$lwage ~ beauty$looks +  beauty$educ +  beauty$exper +  beauty$expersq +  beauty$female)
summary(reg2)
stargazer(reg2, header=FALSE,type="text")

#Apres avoir calculé l'élasticité on voit que au bout de 20 ans d'expérience, 
#Le salaire augmente à un taux décroissant : la théorie du capital humain suggère 
#Une une relation concave par rapport à l'expérience ; on la retrouve ici !!!!!
#Une augmentation d'une année d'éduc fait augmenter le salaire de 6%
#Une augmentation d'une année d'exper fait augmenter le salaire de 4,1%
#Les femmes sélectionnées pour cette étude gagnent 4,5% de salaire par heure en 
#Moins que les hommes TCEPA


############## MES #############   

#IV : The syntax for ivreg is as follows: ivreg(Y ~ X + W | W + Z, ... ), 
#where X is endogenous variable(s), Z is instrument(s), and W is exogenous 
#controls (not instruments).

equ1 <- lm(beauty$lwage ~ beauty$educ +  beauty$exper +  beauty$looks 
           + beauty$female + beauty$bigcity)
summary(equ1)
stargazer(equ1, header=FALSE,type="text")

#2MC |
equ11 <- ivreg(beauty$lwage ~ beauty$educ +  beauty$exper +  beauty$looks 
               + beauty$female + beauty$bigcity | .-educ + black + union + belavg 
               + abvavg + service, data = beauty)
summary(equ11)
stargazer(equ11, header=FALSE,type="text")

equ2 <- lm(beauty$educ ~ beauty$lwage + beauty$bigcity + beauty$female 
           + beauty$black + beauty$looks)
summary(equ2)             
stargazer(equ2, header=FALSE,type="text")

#2MC
equ22 <- ivreg(beauty$educ ~ beauty$lwage + beauty$bigcity + beauty$female 
               + beauty$black + beauty$looks  | .-lwage + exper + union + south 
               + smllcity + married, data = beauty )
summary(equ22) 
stargazer(equ22, header=FALSE,type="text")

# On remarque des R2 faibles peut-etre mauvais instrument ou de mauvaises 
# variables explicatives
# Vn aurait dû changer les variabls explicatives ??????????

#Test de correlation
eequ1 <-  lm(beauty$lwage ~ beauty$educ +  beauty$exper +  beauty$looks + beauty$female +beauty$bigcity)
summary(eequ1)

eequ2 <- lm(beauty$educ ~ beauty$lwage + beauty$bigcity + beauty$female + beauty$black + beauty$looks)
summary(eequ2)


cor(beauty$lwage, summary(eequ1)$residuals) #v.endogene
cor(beauty$educ, summary(eequ2)$residuals) #v.endogene
