from parsing_functions import *

# checks a line against a set of allowable lines
# LINE CANNOT BE A SHOW OR QED LINE (these are checked in checkProof)
def checkLine(line, currLines):
    # find lines referenced by line in consideration
    for thisLine in currLines:
        if thisLine.lNum == line.refLine1:
            rLine1 = thisLine
        elif thisLine.lNum == line.refLine2:
            rLine2 = thisLine
    
    # RULES OF INFERENCE
    #---------------------------------------------------------------------------
    # new rules can be added with more elif statements

    # assumptions and premises are always correct
    if line.just == 'AS' or line.just == 'PR':
        return 1
    
    # double negation elimination
    elif line.just == 'DNE':
        if add_negation(add_negation(line.arg)) == rLine1.arg:
            return 1
    
    # double negation introduction
    elif line.just == 'DNI':
        if line.arg == add_negation(add_negation(rLine1.arg)):
            return 1
    
    # modus ponens
    elif line.just == 'MP':
        if ((main_connective(rLine1.arg) == '->' and
          first_part(rLine1.arg) == rLine2.arg and second_part(rLine1.arg) == line.arg)
          or
          (main_connective(rLine2.arg)   == '->' and
          first_part(rLine2.arg) == rLine1.arg and second_part(rLine2.arg) == line.arg)):
            return 1
    
    # modus tollens
    elif line.just == 'MT':
        if (((main_connective(rLine1.arg) == '->'       and
          add_negation(second_part(rLine1.arg)) == rLine2.arg and
          add_negation(first_part(rLine1.arg))  == line.arg)  or
          (main_connective(rLine2.arg)    == '->'       and
          add_negation(second_part(rLine2.arg)) == rLine1.arg and
          add_negation(first_part(rLine2.arg))  == line.arg))):
            return 1
    
    # adjunction
    elif line.just == 'ADJ':
        if (main_connective(line.arg) == '/\\' and
          (rLine1.arg == first_part(line.arg) and rLine2.arg == second_part(line.arg)) or
          (rLine2.arg == first_part(line.arg) and rLine1.arg == second_part(line.arg))):
            return 1
    
    # simplification
    elif line.just == 'S':
        if (main_connective(rLine1.arg) == '/\\' and
          (line.arg == first_part(rLine1.arg) or line.arg == second_part(rLine1.arg))):
            return 1
    
    # addition
    elif line.just == 'ADD':
        if ((main_connective(line.arg) == '\\/' and
          (rLine1.arg == first_part(line.arg) or rLine1.arg == second_part(line.arg)))):
            return 1
    
    # modus tollendo ponens/disjunctive syllogism
    elif line.just == 'MTP':
        if   main_connective(rLine1.arg) == '\\/':
            if   line.arg == first_part(rLine1.arg)  and rLine2.arg == add_negation(second_part(rLine1.arg)):
                return 1
            elif line.arg == second_part(rLine1.arg) and rLine2.arg == add_negation(first_part(rLine1.arg)):
                return 1
        elif main_connective(rLine2.arg) == '\\/':
            if   line.arg == first_part(rLine2.arg)  and rLine1.arg == add_negation(second_part(rLine2.arg)):
                return 1
            elif line.arg == second_part(rLine2.arg) and rLine1.arg == add_negation(first_part(rLine2.arg)):
                return 1
    
    # if none of these match, return 0 for a bad line.
    return 0

# checks proof by checking each line and dealing with
# show and qed lines separately
# proof should be a list of ProofLines
def checkProof(proof):
    currLines = [] # stores current allowable lines
    toShow    = [] # stores the current open show lines
    for line in proof:
        # for a show line, add the line to list of lines to be shown
        if line.show:
            toShow.append(line)
        
        # qed lines are checked
        elif line.qed:
            showLine = toShow[-1] # show line that is being closed
            
            currProof = [aLine for aLine in currLines if aLine.lNum > showLine.lNum]
            
            # checks to make sure there is at most 1 assumption
            # assigns the assumed line to asLine
            numAssumptions = 0
            for aLine in currProof:
                if aLine.just == 'AS':
                    numAssumptions += 1
                    asLine = aLine
            if numAssumptions > 1:
                return (line.lNum, 'Too many assumptions')
            # finding referenced lines, with a default to check if they exist
            
            rLine1 = ''
            rLine2 = ''
            for aLine in currLines:
                if aLine.lNum == line.refLine1:
                    rLine1 = aLine
                elif aLine.lNum == line.refLine2:
                    rLine2 = aLine
            
            # direct derivation
            if line.just == 'DD':
                if rLine1 == '':
                    return (line.lNum, 'Not enough references')
                if not rLine1.arg == showLine.arg:
                    return (line.lNum, 'Referenced line does not justify show line')
            
            # conditional derivation
            elif line.just == 'CD':
                if rLine1 == '':
                    return (line.lNum, 'Not enough references')
                    
                if main_connective(showLine.arg) == '->':
                    if not asLine.arg == first_part(showLine.arg):
                        return (line.lNum, 'Incorrect assumption for CD')
                    if not rLine1.arg == second_part(showLine.arg):
                        return (line.lNum, 'Referenced line does not justify show line')
                else:
                    return (line.lNum, 'CD must be used for conditional show line')
            
            # indirect derivation
            elif line.just == 'ID':
                if rLine1 == '' or rLine2 == '':
                    return (line.lNum, 'Not enough references')
                
                if main_connective(showLine.arg) == '--':
                    if not add_negation(asLine.arg) == showLine.arg:
                        return (line.lNum, 'Incorrect assumption for ID')
                    
                    if not (rLine1.arg == add_negation(rLine2.arg)
                            or rLine2.arg == add_negation(rLine1.arg)):
                        return (line.lNum, 'Referenced lines must be negations of each other for ID')
                else:
                        return (line.lNum, 'ID must be used for negated show line')
            
            # at the end of checking, remove all lines that are no longer in use,
            # add the show line as an allowable line, and remove show line from
            # list of lines that still need to be shown
            for aLine in currProof:
                currLines.remove(aLine)
            currLines.append(showLine)
            toShow.remove(showLine)
        
        # normal lines of proof are handled by checkLine
        else:
            if checkLine(line, currLines):
                currLines.append(line)
            else:
                return (line.lNum, 'Problem with justification')
    
    # if not all the lines were used up, return the last show line that was not closed
    if not toShow == []:
        return (toShow[-1].lNum, 'Open proof with no qed line')
    
    # figuring out what was proved
    premises = []
    conclusion = proof[0]
    for line in proof:
        # make 1st show line the conclusion
        if line.show and line.lNum < conclusion.lNum:
            conclusion = line
        
        # identify each of the premises
        elif line.just == 'PR':
            premises.append(line.arg)
    
    # if no premises, start the argument with the symbol T
    if premises == []:
        argument = 'T'
    
    # otherwise, list the premises
    else:
        argument = premises[0]
        for arg in premises[1:]:
            argument += ', ' + arg
    
    # add turnstyle and conclusion
    argument += ' |- ' + conclusion.arg

    return (0, argument)