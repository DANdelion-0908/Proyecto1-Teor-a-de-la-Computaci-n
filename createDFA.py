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
    closure = set([])
    stack = [state]

    while stack:
        currentState = stack.pop()
    
        if currentState != automaton.acceptState and 'ε' in automaton.transitions.get(currentState):
            for nextState in automaton.transitions[currentState]['ε']:
                if nextState not in closure:
                    closure.add(nextState)
                    stack.append(nextState)

    return closure

def move(automaton, state, symbol):
    closure = set([])
    stack = [state]

    while stack:
        currentState = stack.pop()

        if currentState != automaton.acceptState and symbol in automaton.transitions.get(currentState):
            for nextState in automaton.transitions[currentState][symbol]:
                if nextState not in closure:
                    closure.add(nextState)
                    stack.append(nextState)

    return closure


def getNewStates(automaton):
    sets = [{automaton.startState}]
    stack = [{automaton.startState}]

    transitions = {}

    while stack:
        for state in stack.pop():
            closure = eClosure(automaton, state)
            if closure:
                stack.append(closure)
                sets.append(closure)

        for state in stack.pop():
            for symbol in 'abc':
                moveClosure = move(automaton, state, symbol)
                if moveClosure:
                    stack.append(moveClosure)
                    sets.append(moveClosure)

    for setElement in sets:
        for state in setElement:
            if eClosure(automaton, state):
                transitions[frozenset(setElement)] = {'ε': frozenset(eClosure(automaton, state))}

            for symbol in 'abc':
                if move(automaton, state, symbol):
                    if frozenset(setElement) not in transitions.keys():
                        transitions[frozenset(setElement)] = {symbol: frozenset(move(automaton, state, symbol))}

                    else:
                        transitions[frozenset(setElement)].update({symbol: frozenset(move(automaton, state, symbol))})

    return DFA(frozenset(sets[0]), frozenset(sets[-1]), transitions)

def createGraph(automaton, filename):
    dot = graphviz.Digraph(comment="Autómata Finito Determinista")
    dot.attr(rankdir='LR')

    dot.node(f'{automaton.startState}', shape='rarrow')

    dot.node(f'{automaton.acceptState}', shape='doublecircle')

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

        ct.createGraph(syntaxTree, Treefilename)

        nonDeterministicAutomaton = nfa.generateAutomatonFromTree(syntaxTree)[0]
        nfa.createGraph(nonDeterministicAutomaton, automatonFilename)

        deterministicAutomaton = getNewStates(nonDeterministicAutomaton)
        print(deterministicAutomaton)
        createGraph(deterministicAutomaton, automatonFilename)