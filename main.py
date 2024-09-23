import infixToPostfix
import expressionBalance
import createTree as ct
import createNFA as nfa
import createDFA as dfa

with open("regex.txt", "r", encoding="UTF-8") as file:
    expressions = file.readlines()

balancedExpressions = expressionBalance.readExpressions(expressions)

for i, expression in enumerate(balancedExpressions):
    expression = expression.strip()
    if expression:
        postfixExpressions = infixToPostfix.infixToPostfix(expression)
        for postfixExpression in postfixExpressions:
            syntaxTree = ct.createTree(postfixExpression)

        Treefilename = f"syntaxTree{i + 1}"
        automatonFilename = f"nfa{i + 1}"
        automatonDFilename = f"dfa{i + 1}"

        ct.createGraph(syntaxTree, Treefilename)

        nonDeterministicAutomaton, alphabet = nfa.generateAutomatonFromTree(syntaxTree)
        nfa.createGraph(nonDeterministicAutomaton, automatonFilename)
        print("Autómata Finito No Determinista creado. \n\n")

        deterministicAutomaton = dfa.getNewStates(nonDeterministicAutomaton, alphabet)
        dfa.createGraph(deterministicAutomaton, automatonDFilename)
        print("Autómata Finito Determinista creado.")
