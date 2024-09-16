from collections import deque

def getEscape(character):
    escape_dict = {
        'n'
    }

    if character in escape_dict:
        return True

def getPrecedence(operator):
    precedences_dict = {
        '(': 1,
        '[': 1,
        '|':  2,
        '¬': 3,
        '?': 4,
        '*': 4,
        '+': 4,
        '^': 5
    }

    precedence = 0

    if operator in precedences_dict:
        precedence = precedences_dict[operator]

    return precedence

def formatRegEx(regex):
    allOperators = ['|', '?', '+', '*', '^', '\n', '']
    operationsToTransform = ['?']
    binaryOperators = ['^', '|', '\n', '\\']
    groupingOpenOperators = ['(', '[']
    groupingCloseOperators = [')', ']']
    c3 = ""

    for i in range(len(regex)):
        c1 = regex[i]

        if (i + 1 < len(regex)):
            c2 = regex[i + 1]
            
        else:
            c2 = ''

        if c1 != "\n":
            if c2 in operationsToTransform:
                if c2 == '?':
                    c3 += c1
                    c3 += "|ε"

            else:
                if c1 not in operationsToTransform:
                    c3 += c1

        if c2 == "\n":
            formatedString.append(c3)
            c3 = ""
        
        if (c1 not in groupingOpenOperators and c2 not in groupingCloseOperators and c2 not in allOperators and c1 not in binaryOperators):
            c3 += '¬'

    formatedString.append(c3)

    return formatedString


def infixToPostfix(regex):
    postfix = ""
    stack = deque()
    formattedRegEx = formatRegEx(regex)
    groupingOpenOperators = ['(', '[', '{']
    groupingCloseOperators = [')', ']', '}']
    postfixToReturn = []
    slashFlag = False
    step = 1

    for element in formattedRegEx:
        print(f"Expresión a convertir: {element}")
        for character in element:
            if character.isalnum() and not slashFlag:
                postfix += character
                print(f"{step}. Agregando '{character}' alfanumérico.")
                step += 1

            elif character in groupingOpenOperators and not slashFlag:
                stack.append(character)
                print(f"{step}. Agregando '{character}' al stack.")
                step += 1

            elif character in groupingCloseOperators and not slashFlag:
                if character == "]":
                    postfix += "|"
                    print(f"{step}. Convirtiendo '[]' a '|'.")
                    step += 1

                while stack and stack[-1] not in groupingOpenOperators:
                    postfix += stack.pop()
                    print(f"{step}. Sacando operadores del stack.")
                    step += 1

                if stack:    
                    stack.pop()
                    print(f"{step}. Vaciando stack.")
                    step += 1

            elif character == '\\':
                slashFlag = True
                print(f"{step}. Caracter de escape detectado.")
                step += 1

            elif slashFlag:
                if getEscape(character):
                    postfix += f"\n"
                    print(f"{step}. Secuencia de escape insertada.")
                    step += 1
                
                else:
                    postfix += character
                    slashFlag = False

            else:
                while stack and getPrecedence(stack[-1]) >= getPrecedence(character):
                    itemChecker = stack.pop()

                    if itemChecker not in groupingOpenOperators:
                        postfix += itemChecker

                stack.append(character)

        while stack:
            postfix += stack.pop()

        postfixToReturn.append(postfix)
        postfix = ""
        print(f"Expresión {element} convertida exitosamente a {postfixToReturn[-1]}.\n\n")
        step = 1

    return postfixToReturn

formatedString = []