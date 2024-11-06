from MFIS_Read_Functions import *


def process_app(fuzzy_file, rules_file, values):

    fuzzy(fuzzy_file, values)

    # Inicializamos el trapecio solución a 0 tanto su x como su y
    trapecio_solucion_x = np.arange(0, 101, 1)
    trapecio_solucion_y = np.zeros(101)

    # Hallar el resultado para cada regla y su valor strength (min de antecedentes)
    for rule in rules_file:

        # Actualizamos el antecedente
        eval_antecedente(fuzzy_file, rule)

        # Lo cargamos de nuevo para cada regla y evaluamos el consecuente
        risks_file = read_fuzzy_sets_file('Files/Risks.txt')
        eval_consecuente(risks_file, rule)

        # Unión de todos los resultados de las reglas
        agregacion(rule, trapecio_solucion_y)

    # Cálculo del centro de masas y lo devolvemos
    return skf.centroid(trapecio_solucion_x, trapecio_solucion_y)


def fuzzy(fuzzy_file, values):
    """La función fuzzy realiza la borrosificación, es decir, actualiza el
    grado de pertenencia para cada conjunto borroso (memDegree)"""
    age, income_level, assets, amount, job, history = \
        values[0], values[1], values[2], values[3], values[4], values[5]
    # Borrosificación de los antecedentes según valores de InputVarSets
    for fuzzy_item in fuzzy_file.items():
        if fuzzy_item[1].var == 'Age':
            y_value = fuzzy_item[1].y[age]
            fuzzy_item[1].memDegree = y_value
        elif fuzzy_item[1].var == 'IncomeLevel':
            y_value = fuzzy_item[1].y[income_level]
            fuzzy_item[1].memDegree = y_value
        elif fuzzy_item[1].var == 'Assets':
            y_value = fuzzy_item[1].y[assets]
            fuzzy_item[1].memDegree = y_value
        elif fuzzy_item[1].var == 'Amount':
            y_value = fuzzy_item[1].y[amount]
            fuzzy_item[1].memDegree = y_value
        elif fuzzy_item[1].var == 'Job':
            y_value = fuzzy_item[1].y[job]
            fuzzy_item[1].memDegree = y_value
        elif fuzzy_item[1].var == 'History':
            y_value = fuzzy_item[1].y[history]
            fuzzy_item[1].memDegree = y_value


def eval_antecedente(fuzzy_file, rule):
    """Esta función evalúa el antecedente añadiendo el grado de pertenencia de
    todos los antecedentes y seleccionando el mínimo con el que se actualiza el
    strength de cada regla (grado de pertenencia del conjunto borroso riesgo)"""
    memdegree_antecedents = []
    for antecedente in rule.antecedent:
        for fuzzy_item in fuzzy_file.items():
            if antecedente == fuzzy_item[0]:
                memdegree_antecedents.append(fuzzy_item[1].memDegree)
                break
    rule.strength = min(memdegree_antecedents)


def eval_consecuente(risks_file, rule):
    """Esta función evalúa el consecuente rellenando la lista de los valores de
    "y" que toma el consecuente para cada regla"""
    # Borrosificación del consecuente según los valores de Risks.txt
    for risk in risks_file.items():
        if rule.consequent == risk[0]:
            rule.consequentX = risk[1].x
            for i in range(len(risk[1].y)):
                if risk[1].y[i] > rule.strength:
                    risk[1].y[i] = rule.strength
            rule.consequentY = risk[1].y


def agregacion(rule, trapecio_solucion_y):
    """Esta función de agregación realiza el último paso de la inferencia que
    consiste en la unión de los resultados de las reglas, trazando el trapecio solución"""
    for i in range(len(trapecio_solucion_y)):
        if rule.consequentY[i] > trapecio_solucion_y[i]:
            trapecio_solucion_y[i] = rule.consequentY[i]


# ---------------Applications iteration---------------

def main():
    app_file = read_applications_file()
    fuzzy_file = read_fuzzy_sets_file('Files/InputVarSets.txt')
    rules_file = read_rules_file()
    outputfile = open('Results.txt', 'w')

    values = []
    for app in app_file:
        for i in range(len(app.data)):
            values.append(app.data[i][1])
        riesgo = process_app(fuzzy_file, rules_file, values)
        values = []

        # Limitamos riesgo a dos decimales
        riesgo = "{:.3f}".format(riesgo)
        riesgo = str(riesgo)

        # Abre el archivo en modo escritura ('w')
        outputfile.write("AppId: " + app.appId + ", Risk: " + riesgo + "\n")

    outputfile.close()


# -------------------------------------------------------

if __name__ == '__main__':
    main()
