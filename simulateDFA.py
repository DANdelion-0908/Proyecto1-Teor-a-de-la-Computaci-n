def chainSimulation(chain, automaton, alphabet):
    currentState = automaton.startState
        
    for character in chain:
        if character not in alphabet:
            return f"La cadena '{chain}' no pertenece al lenguaje"

        currentState = move(automaton, currentState, character)

        if not currentState:
            return f"La cadena '{chain}' no pertenece al lenguaje"

    isAccepted = currentState in automaton.acceptStates
    return f"La cadena '{chain}' {'pertenece' if isAccepted else 'no pertenece'} al lenguaje"


def move(automaton, state, symbol):
    moveSet = set()

    if symbol in automaton.transitions.get(state, {}):
        moveSet.update(automaton.transitions[state][symbol])

    return frozenset(moveSet)