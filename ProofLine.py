from parsing_functions import normalize

class ProofLine:
    # format for raw string should be:
    # (line number).(*whitespace)(argument) :(justification) (*ref number 1) (*ref number 2)
    # where * indicates an optional part
    def __init__(self, raw):
        raw = raw.strip()

        lNum = ''
        while raw[0].isnumeric():
            lNum += raw[0]
            raw = raw[1:]
        self.lNum = int(lNum)
        
        # delete period after line number
        while raw[0] == '.' or raw[0] == ' ':
            raw = raw[1:]
        
        while raw[0] == '\t' or raw[0] == ' ':
            raw = raw[1:]
        
        # check for show line
        if raw[0:4].lower() == 'show':
            self.show = True
            raw = raw[4:]
            if raw[0] == ':':
                raw = raw[1:]
        else:
            self.show = False
        
        # check for qed line
        if raw[1:3].upper() in ['DD', 'CD', 'ID']:
            self.qed = True
        else:
            self.qed = False
        
        self.arg = ''
        while not (raw == '' or raw[0] == ':'):
            if not (raw[0] == ' ' or raw[0] == '\t'):
                self.arg += raw[0]
            raw = raw[1:]
        self.arg = normalize(self.arg)
        
        if self.qed:
            self.arg = 'QED'
        
        while not (raw == '') and (raw[0] == ' ' or raw[0] == ':'):
            raw = raw[1:]
        
        self.just = ''
        while not raw == '' and raw[0].isalpha():
            self.just += raw[0].upper()
            raw = raw[1:]
        
        while not (raw == '' or raw[0].isnumeric()):
            raw = raw[1:]
        
        refLn1 = ''
        while not raw == '' and raw[0].isnumeric():
            refLn1 += raw[0]
            raw = raw[1:]
        
        if refLn1 == '':
            self.refLine1 = 0
        else:
            self.refLine1 = int(refLn1)
        
        while not (raw == '' or raw[0].isnumeric()):
            raw = raw[1:]
        
        if raw == '':
            self.refLine2 = 0
        else:
            while not (raw == '' or raw[0].isnumeric()):
                raw = raw[1:]
            
            if raw == '':
                self.refLine2 = 0
            else:
                refLn2 = ''
                while not raw == '' and raw[0].isnumeric():
                    refLn2 += raw[0]
                    raw = raw[1:]
                self.refLine2 = int(refLn2)
    
    def __repr__(self):
        if self.qed:
            if self.refLine1 == 0:
                return str(self.lNum) + '. ' + ':' + self.just
            elif self.refLine2 == 0:
                return str(self.lNum) + '. ' + ':' + self.just + ' ' + str(self.refLine1)
            else:
                return str(self.lNum) + '. ' + ':' + self.just + ' ' + str(self.refLine1) + ' ' + str(self.refLine2)
        
        if self.show:
            return str(self.lNum) + '. ' + 'Show: ' + self.arg
        
        if self.refLine1 == 0:
            return str(self.lNum) + '. ' + self.arg + ':' + self.just
        elif self.refLine2 == 0:
            return str(self.lNum) + '. ' + self.arg + ':' + self.just + ' ' + str(self.refLine1)
        else:
            return str(self.lNum) + '. ' + self.arg + ':' + self.just + ' ' + str(self.refLine1) + ' ' + str(self.refLine2)
    
    def __str__(self):
        return self.__repr__()

    def output(self):
        print('Line number:      ', self.lNum, '\n',
              'Argument:         ', self.arg,  '\n',
              'Justification:    ', self.just, '\n',
              sep='',end='')
        
        if self.refLine1 == 0:
            print()
        else:
            print('Reference Line 1: ', self.refLine1, sep='', end='\n')
        
        if self.refLine2 == 0:
            print()
        else:
            print('Reference Line 2: ', self.refLine2, sep='', end='\n\n')