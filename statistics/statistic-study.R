# --------------------ESTUDIO DESCRIPTIVO-------------


ABStable <- table(portatil$horas) # tabla en funcion de mi variable principal
lbls <- c("Menos de 1h", "1h", "2h","3h", "4h","5h", "6h", "7h") # opciones de mi variable principal
row.names(ABStable) <- lbls
ABStable

hist(portatil$horas, xlab = "Horas diarias", main = "Histogram")
boxplot(portatil$horas, xlab = "Horas diarias", main = "Boxplot")


#----------------------RESUMEN VARIABLE PRINCIPAL---------------

suppressWarnings(library(summarytools))
descr(portatil$horas)
#quantile(portatil$horas, probs = seq(0, 1, 0.1))


#--------------------------------------AJUSTE NORMAL---------------

library(fitdistrplus)
normalfit <- fitdistr(portatil$horas, "normal")
normalfit

Partition <- hist(portatil$horas, plot = FALSE)
Partition

CummulativeProbabilities = pnorm(c(-Inf, Partition$breaks[c(-1,-8)], Inf),
                                 normalfit$estimate[1], normalfit$estimate[2])
Probabilities = diff(CummulativeProbabilities)
Expected = length(portatil$horas)*Probabilities
chisq.test(Partition$counts, p = Probabilities)

pchisq(8.4482, df = 4, lower.tail = FALSE)


#-----------------------------------AJUSTE LOGNORMAL-----------------------

library(fitdistrplus)
lognormalfit <- fitdistr(portatil$horas, "lognormal")
lognormalfit

Partition <- hist(portatil$horas, plot = FALSE)
Partition

CummulativeProbabilities = plnorm(c(Partition$breaks[-8], Inf),
                                  lognormalfit$estimate[1], lognormalfit$estimate[2])
Probabilities = diff(CummulativeProbabilities)
Expected = length(portatil$horas)*Probabilities
chisq.test(Partition$counts, p = Probabilities)

pchisq(10.758, df = 4, lower.tail = FALSE)


#------------------------------------AJUSTE WEIBULL-----------------------

library(fitdistrplus)
weibullfit <- fitdistr(portatil$horas, "weibull")
weibullfit

Partition <- hist(portatil$horas, plot = FALSE)
Partition

CummulativeProbabilities = pweibull(c(Partition$breaks[-8], Inf),
                                    weibullfit$estimate[1], weibullfit$estimate[2])
Probabilities = diff(CummulativeProbabilities)
Expected = length(portatil$horas)*Probabilities
chisq.test(Partition$counts, p = Probabilities)


pchisq(7.4702, 4, lower.tail = FALSE)
#--------------------------------------HISTOGRAMA NORMAL--------------

hist(portatil$horas, probability = TRUE, xlab = "Horas")
curve(dnorm(x, mean(portatil$horas), sd(portatil$horas)), col = "blue", 
      lwd = 2, add = TRUE, yaxt = "n")


#--------------------------------------HISTOGRAMA LOGNORMAL--------------

hist(portatil$horas, probability = TRUE, xlab = "Horas")
curve(dlnorm(x, lognormalfit$estimate[1], lognormalfit$estimate[2]), col = "blue", 
      lwd = 2, add = TRUE, yaxt = "n")


#--------------------------------------HISTOGRAMA WEIBULL--------------

hist(portatil$horas, probability = TRUE, xlab = "Horas")
curve(dweibull(x, weibullfit$estimate[1], weibullfit$estimate[2]), col = "blue", 
      lwd = 2, add = TRUE, yaxt = "n")

#-------------------------------INTERVALOS DE CONFIANZA PARA MEDIA---------------

alpha = 0.05
n = length(portatil$horas)
xmean = mean(portatil$horas)
xsd = sd(portatil$horas)
z = qnorm(alpha/2, lower.tail = FALSE)
LowerLimit = xmean - z * xsd / sqrt(n)
UpperLimit = xmean + z * xsd / sqrt(n)
LowerLimit
UpperLimit

#----------------------------INTERVALOS DE CONFIANZA PARA DESVIACIÓN TÍPICA---------------

alpha = 0.05
n = length(portatil$horas)
s2 = var(portatil$horas)
chi.lower = qchisq(1-alpha/2, df = n-1)
chi.upper = qchisq(alpha/2, df = n-1)
LowerLimit = (n-1) * s2 / chi.lower
UpperLimit = (n-1) * s2 / chi.upper
LowerLimit
UpperLimit
sqrt(LowerLimit)
sqrt(UpperLimit)

#---------------------HIPOTESIS CON NUESTRA MEDIA---------------

t.test(portatil$horas, mu = 3.06)
pnorm(0.0016001, lower.tail = FALSE)

#--------------------HIPOTESIS CON VALOR FUERA DE INTERVALO-------

t.test(portatil$horas, mu = 1.8)
pnorm(5.8483, lower.tail = FALSE)

#-------------------REGRESIÓN MÚLTIPLE PRINCIPAL---------------

model <- lm(horas ~ edad + ocupacion_texto + marca_texto, data = portatil)
summary(model)

#-------------------REGRESIÓN MÚLTIPLE MODULARIZADA INICIAL---------------

portatil$ocupacion0 = (portatil$ocupacion == 0) # Ninguna
portatil$ocupacion1 = (portatil$ocupacion == 1) # Estudiante
portatil$ocupacion2 = (portatil$ocupacion == 2) # Trabajador

portatil$marca1 = (portatil$marca == 1) # Lenovo
portatil$marca2 = (portatil$marca == 2) # Dell
portatil$marca4 = (portatil$marca == 4) # Hp
portatil$marca5 = (portatil$marca == 5) # Asus
portatil$marca6 = (portatil$marca == 6) # Huawei
portatil$marca7 = (portatil$marca == 7) # Appler
portatil$marca8 = (portatil$marca == 8) # MSI
portatil$marca9 = (portatil$marca == 9) # Otros

model <- lm(horas ~ edad + ocupacion0 + ocupacion1 + ocupacion2 + marca1 + marca2+
              marca4 + marca5 + marca6 + marca7 + marca8 + marca9, data = portatil)
summary(model)

#-------------------QUITO MARCA 7---------------

model <- lm(horas ~ edad + ocupacion0 + ocupacion1 + ocupacion2 + marca1 + marca2+
              marca4 + marca5 + marca6 + marca8 + marca9, data = portatil)
summary(model)

#-------------------QUITO OCUPACIÓN 2---------------

model <- lm(horas ~ edad + ocupacion0 + ocupacion1 + marca1 + marca2+
              marca4 + marca5 + marca6 + marca8 + marca9, data = portatil)
summary(model)

#-------------------QUITO EDAD---------------

model <- lm(horas ~ ocupacion0 + ocupacion1 + marca1 + marca2+
              marca4 + marca5 + marca6 + marca8 + marca9, data = portatil)
summary(model)

#-------------------QUITO MARCA 8---------------

model <- lm(horas ~ ocupacion0 + ocupacion1 + marca1 + marca2+
              marca4 + marca5 + marca6 + marca9, data = portatil)
summary(model)

#-------------------QUITO MARCA 9---------------

model <- lm(horas ~ ocupacion0 + ocupacion1 + marca1 + marca2+
              marca4 + marca5 + marca6, data = portatil)
summary(model)

#-------------------QUITO MARCA 6---------------

model <- lm(horas ~ ocupacion0 + ocupacion1 + marca1 + marca2+
              marca4 + marca5, data = portatil)
summary(model)

#-------------------QUITO OCUPACIÓN 0---------------

model <- lm(horas ~ ocupacion1 + marca1 + marca2+
              marca4 + marca5, data = portatil)
summary(model)

#-------------------QUITO MARCA 2---------------

model <- lm(horas ~ ocupacion1 + marca1+
              marca4 + marca5, data = portatil)
summary(model)

#-------------------QUITO MARCA 1---------------

model <- lm(horas ~ ocupacion1+
              marca4 + marca5, data = portatil)
summary(model)

#-------------------QUITO MARCA 5---------------

model <- lm(horas ~ ocupacion1+
              marca4, data = portatil)
summary(model)

par(mfrow = c(2,2))
plot(model)
