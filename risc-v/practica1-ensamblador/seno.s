factorial:
    li t1 1  # Resultado del factorial (acum)
    li t0 1  # Condicion del bucle (i)

    bucle_f: bgt t0 a0 end_f
                      # En a0 esta el parametro de la funcion
        mul t1 t1 t0  # Incrementamos el factorial
        addi t0 t0 1  # Incrementamos el siguiente valor a multiplicar
        j bucle_f     # Volvemos al loop

    end_f: 
        mv a0 t1      # Movemos el resultado a a0
        jr ra         # Vamos a la siguiente instruccion tras el factorial

seno:
    # a0 es el parametro "x" que se le pasa a la función
    li t2 4   # Aprox para cumplir con un error menor de 0.001 (aprox)
    # li t3 0 # Valor que vamos a devolver
    li t4 0   # Contador del bucle sen(n)
    li t5 -1  # Numero -1
    li t6 0   # Contador del bucle dividendo
    li s1 2   # Numero 2
    li s2 0   # Guardamos (2n + 1)
    li s3 1   # Nos guardamos x^2n + 1
    li s4 0   # Nos guardamos (-1)^n
    li s5 0   # Nos guardamos el dividendo = (-1)^n * x^2n + 1
    li s6 0   # Calculamos el divisor = (2n + 1)

    fcvt.s.w fs3 zero  # Almacenará toda la suma del seno (total)
    mv s7 a0           # Me guardo el valor de a0 para no perderlo

    bucle_sen: bgt t4 t2 end_sen

        mul s2 s1 t4    # Me guardo el 2n
        addi s2 s2 1    # Me guardo el 2n + 1
        bucle_dividendo: bge t6 s2 end_dividendo  # Bucle para x^2n + 1
        
            mul s3 s3 s7
            addi t6 t6 1 # Incrementamos el contador que tiene que llegar a 2n + 1

            j bucle_dividendo

        end_dividendo:
            li t6 0        # Reinicio el contador
            
            # Para ver si el resto es positivo o negativo
            rem s4 t4 s1   
            beq s4 zero positivo
                li s4 -1   # Si la n es impar (-1)^n es -1
            positivo:
                li s4 1    # Si la n es par (-1)^n es 1  

            mul s5 s3 s4   # (-1)^n * x^2n + 1

    # Calculamos el (2n + 1)!
    # Usaré el mismo registro s2 ya que tiene el valor de 2n + 1
        mv a0 s2            # Movemos s2 a a0 para pasar el parametro a la funcion factorial
        jal ra factorial    # Invocamos a factorial, devuelve resultado a0
        fcvt.s.w fs0 a0		# Convierto a0 (resultado del factorial) a coma flotante (fs0)
        fcvt.s.w fs1 s5     # Convierto s5 (dividendo) a coma flotante (fs1)
        fdiv.s fs2 fs1 fs0  # Dividendo / divisor = ((-1)^n * x^2n + 1) / (2n + 1)!
        fadd.s fs3 fs3 fs2  # Incrementamos la suma

        addi t4 t4 1        # Incremento el contador (n)
        li s3 1             # Reinicio el valor de x^2n + 1
        j bucle_sen
    end_sen:
        fmv.x.w a0 fs3  # Movemos el resultado a a0
        jr ra           # Vamos a la instruccion posterior a la llamada a "seno"