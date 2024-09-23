import graphviz
import infixToPostfix
import expressionBalance
import createTree as ct
import createNFA as nfa


class DFA:
    def __init__(self, startState, acceptStates, transitions):
        self.startState = startState
        self.acceptStates = acceptStates
        self.transitions = transitions

    def __str__(self):
        return f'Start State: {self.startState}, Accept States: {self.acceptStates}, Transitions: {self.transitions}'


def eClosure(automaton, state):
    closure = set([state])
    stack = [state]

    while stack:
        currentState = stack.pop()
        if 'ε' in automaton.transitions.get(currentState, {}):
            for nextState in automaton.transitions[currentState]['ε']:
                if nextState not in closure:
                    closure.add(nextState)
                    stack.append(nextState)
    return frozenset(closure)


def move(automaton, states, symbol):
    moveSet = set()

    for state in states:
        if symbol in automaton.transitions.get(state, {}):
            moveSet.update(automaton.transitions[state][symbol])

    return frozenset(moveSet)


def getNewStates(automaton, alphabet):
    startSet = eClosure(automaton, automaton.startState)
    statesSet = {startSet}
    unprocessed = [startSet]
    transitions = {}
    acceptStates = set()

    while unprocessed:
        currentSet = unprocessed.pop()
        transitions[currentSet] = {}

        for symbol in alphabet:
            moveSet = move(automaton, currentSet, symbol)
            closureSet = frozenset().union(*(eClosure(automaton, s) for s in moveSet))

            if closureSet and closureSet not in statesSet:
                statesSet.add(closureSet)
                unprocessed.append(closureSet)

            transitions[currentSet][symbol] = closureSet

            if automaton.acceptState in closureSet:
                acceptStates.add(closureSet)

    return DFA(startSet, acceptStates, transitions)


def createGraph(automaton, filename):
    dot = graphviz.Digraph(comment="Autómata Finito Determinista")
    dot.attr(rankdir='LR')

    dot.node(str(automaton.startState), shape='rarrow')

    for state in automaton.acceptStates:
        dot.node(str(state), shape='doublecircle')

    for startState, trans in automaton.transitions.items():
        for symbol, finalStates in trans.items():
            if finalStates:
                dot.edge(str(startState), str(finalStates), label=symbol)

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

        Treefilename = f"syntaxTree{i + 1}"
        automatonFilename = f"nfa{i + 1}"
        automatonDFilename = f"dfa{i + 1}"

        ct.createGraph(syntaxTree, Treefilename)

        nonDeterministicAutomaton, alphabet = nfa.generateAutomatonFromTree(syntaxTree)
        nfa.createGraph(nonDeterministicAutomaton, automatonFilename)

        deterministicAutomaton = getNewStates(nonDeterministicAutomaton, alphabet)
        print(deterministicAutomaton)
        createGraph(deterministicAutomaton, automatonDFilename)
