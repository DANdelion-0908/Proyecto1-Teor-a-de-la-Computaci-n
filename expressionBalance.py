def readExpressions(regexList):
    stack = []
    counter = 1
    step = 1
    balanced = []

    for expression in regexList:
        for character in expression:
            if character != "\n":
                if (character == "(" or character == "{" or character == "["):
                    print(f"{step}. Signo de agrupación {character} encontrado. Almacenándolo en la pila...")
                    step += 1
                    stack.append(character)

                elif (character == ")" or character == "}" or character == "]"):
                    print(f"{step}. Signo de agrupación {character} encontrado. Eliminando su contraparte de la pila...")
                    step += 1
                    if stack:
                        stack.pop()

                    else:
                        print(f"ERROR: no se pudo encontrar la contraparte del signo de agrupación. Expresión {counter} no balanceada. \n")
                        step = 1
                        stack.append("chapuz")

        else: 
            if not stack:
                print(f"Expresión número {counter} balanceada. \n")
                balanced.append(expression)        

            counter += 1
            stack = []
            step = 1

    return balanced