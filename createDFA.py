import graphviz
import infixToPostfix
import expressionBalance
import createTree as ct
import createNFA as nfa

class DFA:
    def __init__(self, startState, acceptState, transitions):
        self.startState = startState
        self.acceptState = acceptState
        self.transitions = transitions

    def __str__(self):
        return f'{self.startState}, {self.acceptState}, {self.transitions}'

def eClosure(automaton, state):
    closure = set([state])

    if 'ε' in automaton.transitions[state].keys():
        sets = automaton.transitions[state]['ε']

    if sets:
        for element in sets:
            closure.add(element)

    print(closure)

    return frozenset(closure)

def move(automaton, states, symbol):
    closure = set([])
    transitions = {}

    for state in states:
        if symbol in automaton.transitions[state].keys():
            sets = automaton.transitions[state][symbol]

            if sets:
                for element in sets:
                    closure.add(element)
    
    transitions[frozenset(states)] = {symbol: closure}

    print(symbol, closure)

    print("MUEVE", transitions)

    return [frozenset(closure), transitions]

def getNewStates(automaton, alphabet):
    statesSet = set([])
    visitedStates = set([])
    finalSets = set([])
    transitions = {}

    initialSet = eClosure(automaton, automaton.startState)

    statesSet.add(initialSet)
    visitedStates.add(automaton.startState)

    while statesSet.difference(visitedStates) != set():
        for symbol in alphabet:
            moveClosure = move(automaton, statesSet, symbol)

            if moveClosure[0] not in statesSet:
                statesSet.add(moveClosure[0])
                transitions.update(moveClosure[1])
   
    return DFA(initialSet, finalSets, transitions)

def createGraph(automaton, filename):
    dot = graphviz.Digraph(comment="Autómata Finito Determinista")
    dot.attr(rankdir='LR')

    dot.node(f'{automaton.startState}', shape='rarrow')

    for state in automaton.acceptState:
        dot.node(f'{state}', shape='doublecircle')

    for startState, transitions in automaton.transitions.items():
        for symbol, finalStates in transitions.items():
            dot.edge(f'{startState}', f'{finalStates}', label=symbol)

    dot.render(f'results/automatons/dfa/{filename}', format='pdf', cleanup=True)

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
        automatonDFilename = f"dfa{i+1}"

        ct.createGraph(syntaxTree, Treefilename)

        nonDeterministicAutomaton, alphabet = nfa.generateAutomatonFromTree(syntaxTree)
        nfa.createGraph(nonDeterministicAutomaton, automatonFilename)

        # deterministicAutomaton = getNewStates(nonDeterministicAutomaton, alphabet)
        # print(deterministicAutomaton)
        # createGraph(deterministicAutomaton, automatonDFilename)