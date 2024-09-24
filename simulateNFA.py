from createDFA import eClosure, move

def chainSimulation(chain, automaton, alphabet):
    currentStates = eClosure(automaton, automaton.startState)
    
    for character in chain:
        if character not in alphabet:
            return f"La cadena '{chain}' no pertenece al lenguaje"

        nextStates = set()
        for state in currentStates:
            moveStates = move(automaton, {state}, character)
            nextStates.update(list(moveStates))

        currentStates = set().union(*(eClosure(automaton, s) for s in nextStates))

        if not currentStates:
            return f"La cadena '{chain}' no pertenece al lenguaje"

    isAccepted = automaton.acceptState in currentStates
    return f"La cadena '{chain}' {'pertenece' if isAccepted else 'no pertenece'} al lenguaje"