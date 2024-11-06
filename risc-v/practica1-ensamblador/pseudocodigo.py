def factorial(num: int) -> int: # utilizamos una función auxiliar para calcular
                                # el factorial de un número
    acum, i = 1, 1
    
    while i <= num:
        acum = acum * i
        i += 1
    return acum

def seno(x: int) -> float:
    resultado = 0
    for n in range(15): # 15 es la aproximación para que el error sea menor del 0.01
        b = 1
        a = 2*n
        a = a + 1   # Me guardo el 2n + 1
        
        for i in range(a): # Para calcular x^(2n + 1)
            b = b * x      # Multiplicamos por x hasta llegar a x^(2n + 1) 
        
        resto = n % 2
        
        if resto == 0:
            c = 1        # Si la n es par (-1)^n es 1
        else:
            c = -1       # Si la n es par (-1)^n es -1
            
        d = c * b        # (-1)^n * x^2n + 1
        
        e = factorial(a) # Calculamos el (2n + 1)!
        
        f = d/e          # Dividendo / divisor = ((-1)^n * x^2n + 1) / (2n + 1)!

        resultado += f   # Incrementamos la suma
    
    return resultado

def coseno(x: int) -> float:
    resultado = 0
    for n in range(15): # 15 es la aproximación para que el error sea menor del 0.01
        b = 1
        a = 2*n         # Me guardo el 2n + 1
        
        for i in range(a): # Para calcular x^(2n)
            b = b * x         # Multiplicamos por x hasta llegar a x^(2n) 
        
        resto = n % 2
        
        if resto == 0:
            c = 1        # Si la n es par (-1)^n es 1
        else:
            c = -1       # Si la n es par (-1)^n es -1
            
        d = c * b        # (-1)^n * x^2n
        
        e = factorial(a) # Calculamos el (2n)!
        
        f = d/e          # Dividendo / divisor = ((-1)^n * x^2n) / (2n)!

        resultado += f   # Incrementamos la suma
    
    return resultado
    

def tg(x: int) -> int:
    
    f1 = seno(x)
    f2 = coseno(x)
    
    return (f1/f2)

def E() -> int:
    total = 0
    
    for n in range(15):
        a = factorial(n)
        total = total + (1/a)
    
    return total
