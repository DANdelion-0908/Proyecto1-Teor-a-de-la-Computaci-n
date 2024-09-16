import graphviz
import infixToPostfix
import expressionBalance
import createTree as ct

class NFA:
    def __init__(self, startState, acceptState, transitions):
        self.startState = startState
        self.acceptState = acceptState
        self.transitions = transitions

    def __str__(self):
        return f'{self.startState}, {self.acceptState}, {self.transitions}'
    
def createAutomaton(value, index):
    startState = index
    acceptState = index + 1
    transitions = {
        startState : {value : [acceptState]}
    }

    return NFA(startState, acceptState, transitions)

def concatAutomatons(automaton1, automaton2): # ¬
    startState = automaton1.startState

    print("CONCAT", automaton1.transitions, automaton2.transitions)

    print(automaton2.transitions)
    acceptState = automaton2.acceptState
    transitions = automaton1.transitions
    transitions.update(automaton2.transitions)
    transitions[automaton1.acceptState] = {'ε': [automaton2.startState]}
    
    return NFA(startState, acceptState, transitions)

def unionAutomatons(automaton1, automaton2, index): # |
    startState = index
    acceptState = index + 1
    transitions = {
        startState: {'ε': [automaton1.startState, automaton2.startState]},
        automaton1.acceptState: {'ε': [acceptState]},
        automaton2.acceptState: {'ε': [acceptState]}
    }

    transitions.update(automaton1.transitions)
    transitions.update(automaton2.transitions)

    return NFA(startState, acceptState, transitions)

def kleeneAutomaton(automaton, index): # *
    startState = index
    acceptState = index + 1
    transitions = {
        startState : {'ε' : [automaton.startState, acceptState]},
        automaton.acceptState: {'ε': [automaton.startState, acceptState]} 
    }

    transitions.update(automaton.transitions)

    return NFA(startState, acceptState, transitions)

def ceroOrMoreAutomaton(automaton, index): # ?
    startState = index
    acceptState = index + 1
    transitions = {
        startState : {'ε' : [automaton.startState, acceptState]}
    }

    transitions.update(automaton.transitions)

    return NFA(startState, acceptState, transitions)

def oneOrMoreAutomaton(automaton, index): # +
    startState = index
    acceptState = index + 1
    transitions = {
        startState: {'ε': [automaton.startState]},
        automaton.acceptState: {'ε': [automaton.startState, acceptState]}
    }

    transitions.update(automaton.transitions)

    return NFA(startState, acceptState, transitions)

def generateAutomatonFromTree(tree):
    stack = []
    index = 0 
    def postOrder(node):
        nonlocal index

        if node.left:
            postOrder(node.left)
        if node.right:
            postOrder(node.right)

        if node.value.isalnum():
            nfa = createAutomaton(node.value, index)
            index += 2
            stack.append(nfa)

        elif node.value == '¬':
            automaton2 = stack.pop()
            automaton1 = stack.pop()
            nfa = concatAutomatons(automaton1, automaton2)
            stack.append(nfa)

        elif node.value == '|':
            automaton2 = stack.pop()
            automaton1 = stack.pop()
            nfa = unionAutomatons(automaton1, automaton2, index)
            index += 2
            stack.append(nfa)

        elif node.value == '*':
            automaton1 = stack.pop()
            nfa = kleeneAutomaton(automaton1, index)
            index += 2
            stack.append(nfa)

        elif node.value == '?':
            automaton1 = stack.pop()
            nfa = ceroOrMoreAutomaton(automaton1, index)
            index += 2
            stack.append(nfa)

        elif node.value == '+':
            automaton1 = stack.pop()
            nfa = oneOrMoreAutomaton(automaton1, index)
            index += 2
            stack.append(nfa)

    postOrder(tree)
    return[stack.pop()]

def createGraph(automaton, filename):
    print("CREATE", automaton.transitions)
    dot = graphviz.Digraph(comment="Autómata Finito No Determinista")
    counter = 0

    for startState, transitions in automaton.transitions.items():
        for symbol, finalStates in transitions.items():
            for state in finalStates:
                dot.edge(f'{startState}', f'{state}', label=symbol)

    dot.render(f'results/automatons/nfa/{filename}', format='pdf', cleanup=True)

with open("regex.txt", "r", encoding="UTF-8") as file:
    expressions = file.readlines()

balancedExpressions = expressionBalance.readExpressions(expressions)

for i, expression in enumerate(balancedExpressions):
    expression = expression.strip()
    if expression:
        postfixExpressions = infixToPostfix.infixToPostfix(expression)
        for postfixExpression in postfixExpressions:
            syntaxTree = ct.createTree(postfixExpression)

        Treefilename = f"syntaxTree{i+1}"
        automatonFilename = f"nfa{i+1}"
        ct.createGraph(syntaxTree, Treefilename)
        createGraph(generateAutomatonFromTree(syntaxTree)[0], automatonFilename)