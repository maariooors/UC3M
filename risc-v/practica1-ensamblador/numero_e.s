factorial:
    li s1 1  # Resultado del factorial (acum)
    li s0 1  # Condicion del bucle (i)

    bucle_f: bgt s0 a0 end_f
                      # En a0 esta el parametro de la funcion
        mul s1 s1 s0  # Incrementamos el factorial
        addi s0 s0 1  # Incrementamos el siguiente valor a multiplicar
        j bucle_f     # Volvemos al loop

    end_f: 
        mv a0 s1      # Movemos el resultado a a0
        jr ra         # Vamos a la siguiente instruccion tras el factorial

E:

    li s2 0  # Contador del buble (n)
    li s3 4  # Aprox para cumplir con un error menor de 0.001 (aprx)
    li t0 0
    fcvt.s.w fs0 t0   # Divison 1/n!
    fcvt.s.w fs1 t0   # Numero "e" (total)
    li t1 1           # Numero 1
    fcvt.s.w fs2 t1

    bucle_e: bgt s2 s3 end_e
                            # factorial(s0)
        mv a0 s2            # Movemos s2 a a0 para pasar el parametro a la funcion factorial
        jal ra factorial    # Invocamos a factorial, devuelve resultado a0
        fcvt.s.w fs3 a0		# Convierto a0 (resultado del factorial) a coma flotante (fs3)
        fdiv.s fs0 fs2 fs3  # 1/n!
        fadd.s fs1 fs1 fs0  # total = total + 1/n!
        addi s2 s2 1
        j bucle_e
    
    end_e:
        fmv.x.w a0 fs1  # Movemos el resultado a a0
        jr ra           # Vamos a la instruccion posterior a la llamada a "e"