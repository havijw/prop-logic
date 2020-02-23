from ProofLine import ProofLine
from parsing_functions import *
from proof_checking_functions import *

def main():
    print('Write your proof here')
    print('--------------------------------')

    curr_line = input('1. show: ')
    curr_ProofLine = ProofLine('1. show: ' + curr_line)
    
    proof = [curr_ProofLine]

    line_number = 2
    shows = 1
    qeds  = 0

    while qeds < shows:
        curr_line = input('%i. ' % line_number)
        curr_ProofLine = ProofLine(str(line_number) + '. ' + curr_line)
        proof.append(curr_ProofLine)

        if curr_ProofLine.show:
            shows += 1
        if curr_ProofLine.qed:
            qeds += 1
        
        line_number += 1
    
    checkedProof = checkProof(proof)
    
    print('Done checking proof')
    
    if checkedProof[0] > 0:
        print('Proof is incorrect.\n',
              'Problem at line ', checkedProof[0],'\n',
              'Problem: ', checkedProof[1], sep='')
    else:
        print('Proof is correct. Well Done!\nYou proved:', checkedProof[1])

def test():
    exampleProofs=[
        """1. show: (p \\/ --p)
        2.	show: ----(p \\/ --p)
        3.		--(p \\/ --p) :AS
        4.		show: --p
        5.			p :AS
        6.			p \\/ --p :ADD 5
        7.		:ID 3 6
        8.		p \\/ --p :ADD 4
        9.	:ID 3 8
        10.	p \\/ --p :DNE 2
        11. :DD 10""",
        """1. show: (p -> q) \\/ (q -> r)
        2.	show: ----((p -> q) \\/ (q -> r))
        3.		--((p -> q) \\/ (q -> r)) :AS
        4.		show: q -> r
        5.			q :AS
        6.			show: p -> q
        7.				p :AS
        8.			:CD 5
        9.			(p -> q) \\/ (q -> r) :ADD 6
        10.			show: ----r
        11.				--r :AS
        12.			:ID 3 9
        13.			r :DNE 10
        14.		:CD 13
        15.		(p -> q) \\/ (q -> r) :ADD 4
        16.	:ID 3 15
        17.	(p -> q) \\/ (q -> r) :DNE 2
        18. :DD 17""",
        """1. show: --p
        2.	p :AS
        3.	p -> q :PR
        4.	q -> --p :PR
        5.	q :MP 2 3
        6.	--p :MP 4 5
        7. :ID 2 6""",
        """1. show: (p \\/ q) \\/ (q \\/ r)
        2.	p \\/ q :PR
        3.	(p \\/ q) \\/ (q \\/ r) :ADD 2
        4. :DD 3""",
        """1. show: (p \\/ q) /\\ (q \\/ r)
        2.	p \\/ q :PR
        3.	--p :PR
        4.	q :MTP 2 3
        5.	p \\/ q :ADD 4
        6.	q \\/ r :ADD 4
        7.	(p \\/ q) /\\ (q \\/ r) :ADJ 5 6
        8. :DD 7""",
        """1. show: --p
        2.	p :AS
        3.	p -> q :PR
        4.	p -> --q :PR
        5.	q :MP 2 3
        6.	--q :MP 2 4
        7. :ID 5 6""",
        """1. show: --p
        2.	p :AS
        3.	p -> q :PR
        4.	p -> --q :PR
        5.	q :MP 2 3
        6.	--q :MP 2 4
        7. :ID 5 6""",
        """1. show: p -> (--q \\/ r)
        2.	p :AS
        3.	p -> --q :PR
        4.	--q :MP 2 3
        5.	--q \\/ r :ADD 4
        6. :CD 5""",
        """1. show: p \\/ (q /\\ r)
        2.	(p \\/ q) /\\ (p \\/ r) :PR
        3.	p \\/ q :S 2
        4.	p \\/ r :S 2
        5.	show: ----(p \\/ (q /\\ r))
        6.		--(p \\/ (q /\\ r)) :AS
        7.		show: --p
        8.			p :AS
        9.			p \\/ (q /\\ r) :ADD 8
        10.		:ID 6 9
        11.		q :MTP 3 7
        12.		r :MTP 4 7
        13.		q /\\ r :ADJ 11 12
        14.		p \\/ (q /\\ r) :ADD 13
        15.	:ID 6 14
        16.	p \\/ (q /\\ r) :DNE 5
        17. :DD 16""",
        """1. show: q \\/ p
        2.	--q -> --r :PR
        3.	r \\/ s :PR
        4.	s -> q :PR
        5.	show: ----q
        6.		--q :AS
        7.		--r :MP 2 6
        8.		--s :MT 4 6
        9.		s :MTP 3 7
        10.	:ID 8 9
        11.	q :DNE 5
        12.	q \\/ p :ADD 11
        13. :DD 12""",
        """1. show: (p -> r) \\/ (q -> r)
        2.	(p \\/ q) -> r :PR
        3.	show: p -> r
        4.		p :AS
        5.		p \\/ q :ADD 4
        6.		r :MP 2 5
        7.	:CD 6
        8.	(p -> r) \\/ (q -> r) :ADD 3
        9. :DD 8""",
        """1. show: (p -> r) /\\ (q -> r)
        2.	(p \\/ q) -> r :PR
        3.	show: p -> r
        4.		p :AS
        5.		p \\/ q :ADD 4
        6.		r :MP 2 5
        7.	:CD 6
        8.	show: q -> r
        9.		q :AS
        10.		p \\/ q :ADD 9
        11.		r :MP 2 10
        12.	:CD 11
        13.	(p -> r) /\\ (q -> r) :ADJ 3 8
        14. :DD 13""",
        """1. show: ((--p -> r) /\\ (--q -> r)) -> (--(p /\\ q) -> r)
        2.	(--p -> r) /\\ (--q -> r) :AS
        3.	--p -> r :S 2
        4.	--q -> r :S 2
        5.	show: --(p /\\ q) -> r
        6.		--(p /\\ q) :AS
        7.		show: ----r
        8.			--r :AS
        9.			----p :MT 3 8
        10.			p :DNE 9
        11.			----q :MT 4 8
        12.			q :DNE 11
        13.			p /\\ q :ADJ 10 12
        14.		:ID 6 13
        15.		r :DNE 7
        16. :CD 15
        17. :CD 5""",
        """1. show: --P \\/ --Q
        2.	--(P /\\ Q) :PR
        3.	show: ----(--P \\/ --Q)
        4.		--(--P \\/ --Q) :AS
        5.		show: ----P
        6.			--P :AS
        7.			--P \\/ --Q :ADD 6
        8.		:ID 4 7
        9.		P :DNE 5
        10.		show: ----Q
        11.			--Q :AS
        12.			--P \\/ --Q :ADD 11
        13.		:ID 4 12
        14.		Q :DNE 10
        15.		P /\\ Q :ADJ 9 14
        16.	:ID 2 15
        17.	--P \\/ --Q :DNE 3
        18. :DD 17""",
        """1. show: --(P /\\ Q)
        2.	P /\\ Q :AS
        3.	--P \\/ --Q :PR
        4.	P :S 2
        5.	Q :S 2
        6.	----P :DNI 4
        7.	--Q :MTP 3 6
        8. :ID 5 7""",
        """1. show: --P /\\ --Q
        2.	--(P \\/ Q) :PR
        3.	show: --P
        4.		P :AS
        5.		P \\/ Q :ADD 4
        6.	:ID 2 5
        7.	show: --Q
        8.		Q :AS
        9.		P \\/ Q :ADD 8
        10.	:ID 2 9
        11.	--P /\\ --Q :ADJ 3 7
        12. :DD 11""",
        """1. show: --(P \\/ Q)
        2.	P \\/ Q :AS
        3.	--P /\\ --Q :PR
        4.	--P :S 3
        5.	--Q :S 3
        6.	Q :MTP 2 4
        7. :ID 5 6""",
        """1. show: (P /\\ Q) \\/ (P /\\ R)
        2.	P /\\ (Q \\/ R) :PR
        3.	P :S 2
        4.	Q \\/ R :S 2
        5.	show: ----((P /\\ Q) \\/ (P /\\ R))
        6.		--((P /\\ Q) \\/ (P /\\ R)) :AS
        7.		show: ----Q
        8.			--Q :AS
        9.			R :MTP 4 8
        10.			P /\\ R :ADJ 3 9
        11.			(P /\\ Q) \\/ (P /\\ R) :ADD 10
        12.		:ID 6 11
        13.		Q :DNE 7
        14.		P /\\ Q :ADJ 3 13
        15.		(P /\\ Q) \\/ (P /\\ R) :ADD 14
        16.	:ID 6 15
        17.	(P /\\ Q) \\/ (P /\\ R) :DNE 5
        18. :DD 17""",
        """1. show: P /\\ (Q \\/ R)
        2.	(P /\\ Q) \\/ (P /\\ R) :PR
        3.	show: ----P
        4.		--P :AS
        5.		show: --(P /\\ Q)
        6.			P /\\ Q :AS
        7.			P :S 6
        8.		:ID 4 7
        9.		P /\\ R :MTP 2 5
        10.		show: --(P /\\ R)
        11.			P /\\ R :AS
        12.			P :S 11
        13.		:ID 4 12
        14.	:ID 9 10
        15.	P :DNE 3
        16.	show: ----(Q \\/ R)
        17.		--(Q \\/ R) :AS
        18.		show: --(P /\\ Q)
        19.			P /\\ Q :AS
        20.			Q :S 19
        21.			Q \\/ R :ADD 20
        22.		:ID 17 21
        23.		P /\\ R :MTP 2 18
        24.		show: --(P /\\ R)
        25.			P /\\ R :AS
        26.			R :S 25
        27.			Q \\/ R :ADD 26
        28.		:ID 17 27
        29.	:ID 23 24
        30.	Q \\/ R :DNE 16
        31.	P /\\ (Q \\/ R) :ADJ 15 30
        32. :DD 31""",
        """1. show: (P \\/ Q) /\\ (P \\/ R)
        2.	P \\/ (Q /\\ R) :PR
        3.	show: ----(P \\/ Q)
        4.		--(P \\/ Q) :AS
        5.		show: --P
        6.			P :AS
        7.			P \\/ Q :ADD 6
        8.		:ID 4 7
        9.		Q /\\ R :MTP 2 5
        10.		show: --(Q /\\ R)
        11.			Q /\\ R :AS
        12.			Q :S 11
        13.			P \\/ Q :ADD 12
        14.		:ID 4 13
        15.	:ID 9 10
        16.	P \\/ Q :DNE 3
        17.	show: ----(P \\/ R)
        18.		--(P \\/ R) :AS
        19.		show: --P
        20.			P :AS
        21.			P \\/ R :ADD 20
        22.		:ID 18 21
        23.		Q /\\ R :MTP 2 19
        24.		show: --(Q /\\ R)
        25.			Q /\\ R :AS
        26.			R :S 25
        27.			P \\/ R :ADD 26
        28.		:ID 18 27
        29.	:ID 23 24
        30.	P \\/ R :DNE 17
        31.	(P \\/ Q) /\\ (P \\/ R) :ADJ 16 30
        32. :DD 31""",
        """1. show: P \\/ (Q /\\ R)
        2.	(P \\/ Q) /\\ (P \\/ R) :PR
        3.	P \\/ Q :S 2
        4.	P \\/ R :S 2
        5.	show: ----(P \\/ (Q /\\ R))
        6.		--(P \\/ (Q /\\ R)) :AS
        7.		show: --P
        8.			P :AS
        9.			P \\/ (Q /\\ R) :ADD 8
        10.		:ID 6 9
        11.		Q :MTP 3 7
        12.		R :MTP 4 7
        13.		Q /\\ R :ADJ 11 12
        14.		P \\/ (Q /\\ R) :ADD 13
        15.	:ID 6 14
        16.	P \\/ (Q /\\ R) :DNE 5
        17. :DD 16""",
        """1. show: ((P -> Q) -> R) -> ((R -> P) -> (S -> P))
        2.  (P -> Q) -> R :AS
        3.	show: (R -> P) -> (S -> P)
        4.		R -> P :AS
        5.		show: S -> P
        6.			S :AS
        7.			show: ----P
        8.				--P :AS
        9.				--R :MT 4 8
        10.				--(P -> Q) :MT 2 9
        11.				show: P -> Q
        12.					P :AS
        13.					show: ----Q
        14.						--Q :AS
        15.					:ID 8 12
        16.					Q :DNE 13
        17.				:CD 16
        18.			:ID 10 11
        19.			P :DNE 7
        20.		:CD 19
        21. :CD 5
        22. :CD 3""",
        """1. show: (P -> R) \\/ (Q -> R)
        2.	(P /\\ Q) -> R :PR
        3.	show: ----((P -> R) \\/ (Q -> R))
        4.		--((P -> R) \\/ (Q -> R)) :AS
        5.		show: --(P -> R)
        6.			P -> R :AS
        7.			(P -> R) \\/ (Q -> R) :ADD 6
        8.		:ID 4 7
        9.		show: --(Q -> R)
        10.			Q -> R :AS
        11.			(P -> R) \\/ (Q -> R) :ADD 10
        12.		:ID 4 11
        13.		show: --R
        14.			R :AS
        15.			show: P -> R
        16.				P :AS
        17.			:CD 14
        18.		:ID 5 15
        19.		--(P /\\ Q) :MT	2 13
        20.		show: ----P
        21.			--P :AS
        22.			show: P -> R
        23.				P :AS
        24.				show: ----R
        25.					--R :AS
        26.				:ID 21 23
        27.				R :DNE 24
        28.			:CD 27
        29.		:ID 5 22
        30.		show: ----(--P \\/ --Q)
        31.			--(--P \\/ --Q) :AS
        32.			show: ----P
        33.				--P :AS
        34.				--P \\/ --Q :ADD 33
        35.			:ID 31 34
        36.			show: ----Q
        37.				--Q :AS
        38.				--P \\/ --Q :ADD 37
        39.			:ID 31 38
        40.			P :DNE 32
        41.			Q :DNE 36
        42.			P /\\ Q :ADJ 40 41
        43.		:ID 19 42
        44.		--P \\/ --Q :DNE 30
        45.		--Q :MTP 20 44
        46.		show: Q -> R
        47.			Q :AS
        48.			show: ----R
        49.				--R :AS
        50.			:ID 45 47
        51.			R :DNE 48
        52.		:CD 51
        53.	:ID 9 46
        54.	(P -> R) \\/ (Q -> R) :DNE 3
        55. :DD 54"""
    ]

    print('Checking Proofs')
    errors = 0
    counter = 0
    for proof in exampleProofs:
        counter += 1
        print(counter)
        listProof = proof.split('\n')
        proof = [ProofLine(line) for line in listProof]
        
        checkedProof = checkProof(proof)

        if checkedProof[0] > 0:
            print('Proof is incorrect.\n',
                  'Trying to show:', proof[0].arg, '\n',
                  'Problem at line ', checkedProof[0],'\n',
                  'Problem: ', checkedProof[1], sep='')
            errors += 1
    print('Finished Checking Proofs.\nerrors:', errors, 'total checked:', len(exampleProofs))

def testadd_negation():
    toTest = [
        'A',
        'A -> B',
        'A /\\ B',
        'A \\/ B',
        '--A',
        '(A -> B) /\\ C',
        'C /\\ (A -> B)',
        '((A -> B) /\\ (C -> D))',
        '(A -> B) /\\ (C -> D)',
        '(--A -> B) \\/ --(A -> C \\/ D)',
        '(A)',
        '((A))'
    ]

    for arg in toTest:
        print('argument', arg,
              '\nnegated: ', add_negation(arg), sep='', end='\n\n')

def testProofLine():
    lines = [
        '1. show: (p \\/ --p)',
        '2.	show: ----(p \\/ --p)',
        '3.		--(p \\/ --p) :AS',
        '4.		show: --p',
        '5.			p :AS',
        '6.			p \\/ --p :ADD 5',
        '7.		:ID 3 6',
        '8.		p \\/ --p :ADD 4',
        '9.	:ID 3 8',
        '10.	p \\/ --p :DNE 2',
        '11. :DD 10'
    ]

    proofLines = [ProofLine(line) for line in lines]

    for line in proofLines:
        print(line.lNum, line.arg)
        if line.show:
            print('show line above')

def testNormalize():
    toTest = [
        'A',
        'A -> B',
        'A /\\ B',
        'A \\/ B',
        '--A',
        '(A -> B) /\\ C',
        'C /\\ (A -> B)',
        '((A -> B) /\\ (C -> D))',
        '(A -> B) /\\ (C -> D)',
        '(--A -> B) \\/ --(A -> C \\/ D)',
        '(A)',
        '((A))',
        '----(p \\/ --p)',
        '((--p -> r) /\\ (--q -> r)) -> (--(p /\\ q) -> r)',
        '(--(p /\\ q) -> r)',
        '(--p -> r) /\\ (--q -> r)'
    ]

    for arg in toTest[-3:]:
        print('argument: ', arg,
              '\nnormalized: ', normalize(arg),
              '\nfirst part of normalized: ', firstPart(normalize(arg)),
              '\nsecond part of normalized: ', secondPart(normalize(arg)),
              sep='', end='\n\n')

if __name__ == '__main__':
    main()