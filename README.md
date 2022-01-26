# prop-logic

Tools for Propositional Logic.

## Usage

The main functionality is to check a proof written in logical language typed at the command line. Run

```bash
python proof_check.py
```

then enter the proof you wish to check. An example is

```bash
$ python proof_check.py
Write your proof here
--------------------------------
1. show: p -> --(--p)
2.   p :AS
3.   show: --(--p)
4.     --p :AS
5.   :ID 2 4
6. :CD 3
Done checking proof
Proof is correct. Well Done!
You proved: T |- (p -> (--(--p)))
```

Lines are automatically numbered, so all you have to do is type your proof. Capitalization and whitespace are ignored, and line justifications can be in any order.

## Logical Language

### Formulas

The standard propositional logical symbols are understood. Specifically, the allowed symbols and their representations are

* &not; is ```--``` (negation)
* &and; is ```/\``` (conjunction/and)
* &or; is ```\/``` (disjunction/or)
* &rarr; is ```->``` (implication)

### Justification

Each line of a proof consists of a formula written with variables and the symbols above and a justification. The justification is separated by  ```:``` and consists of numbers, referencing the lines that justify the current formula. The possible justifications are

* ```PR``` premise, no justification needed.
* ```AS``` assumption, no justification needed. Used in conditional and indirect derivations.
* ```MP``` modus ponens, justified by two previous lines. Relative to the following, one of the listed lines should contain &phi; &rarr; &psi; and the other &phi;.
  > &phi; &rarr; &psi;, &phi; &vdash; &psi;
* ```MT``` modus tollens, justified by two previous lines. Relative to the following, one of the listed lines should contain &phi; &rarr; &psi; and the other &not; &psi;.
  > &phi; &rarr; &psi;, &not; &psi; &vdash; &psi;
* ```DNE``` double negation elimination, justified by one previous line. Relative to the following, the listed line should contain &not;(&not; &phi;).
  > &not;(&not; &phi;) &vdash; &phi;
* ```DNI``` double negation introduction, justified by one previous line. Relative to the following, the list line should contain &phi;.
  > &phi; &vdash; &not;(&not; &phi;)
* ```ADJ``` adjunction, justified by two previous lines. Relative to the following, one of the listed lines should contain &phi; and the other &psi;.
  > &phi;, &psi; &vdash; &phi; &and; &psi;
* ```S``` simplification, justified by one previous line. Relative to the following, the listed line should contain &phi; &and; &psi;.
  > &phi; &and; &psi; &vdash; &phi;
* ```ADD``` addition, justified by one previous line. Relative to the following, the listed line should contain &phi;.
  > &phi; &vdash; &phi; &or; &psi;
* ```MTP``` modus tollendo ponens (also called disjunctive syllogism), justified by two previous lines. Relative to the following, one of the other listed lines should contain &phi; &or; &psi; and the other &not; &phi;.
  > &phi; &or; &psi;, &not; &phi; &vdash; &psi;

### Writing Proofs

Proofs are started with a *show* line, which consists of ```show``` followed by the formula to be proved. The following lines are formulas with justifications, until the *QED* line.

### Proof Techniques

There are three styles of proofs that are allowed: direct derivations, conditional derivations, and indirect derivations. They are identified by their *QED* lines.

* Direct derivations prove any formula and have no assumptions. They begin with a *show* line and proceed directly from the *show* line to the *QED* line, which is ```:DD``` followed by the line number on which the formula specified in the *show* line was achieved.
* Conditional derivations prove formulas of the form &phi; &rarr; &psi; and have one assumption, namely &phi;. They begin with assuming &phi; and proceed to achieve &psi;. They conclude with the *QED* line, which is ```:CD``` followed by the line number on which &psi; was achieved.
* Indirect derivations prove formulas of the from &not; &phi; and have one assumption, namely &phi;. They begin with assuming &phi; and proceeds to achieve a contradiction, which is having &psi; and &not; &psi; on separate lines for any formula &psi;. They conclude with the *QED* line, which is ```:ID``` followed by the line numbers on which &psi; and &not; &psi; were achieved.

Note that proofs can be nested using *show* and *QED* lines as usual.

### Examples of Proofs

Law of Excluded Middle: ```T |- (p \/ --p)```

```bash
1.  show: (p \/ --p)
2.    show: ----(p \/ --p)
3.      --(p \/ --p) :AS
4.      show: --p
5.        p :AS
6.        p \/ --p :ADD 5
7.      :ID 3 6
8.      p \/ --p :ADD 4
9.    :ID 3 8
10.   p \/ --p :DNE 2
11. :DD 10
```

One version of DeMorgan's Law: ```--(P /\ Q) |- --P \/ --Q```

```bash
1.  show: --P \/ --Q
2.    --(P /\ Q) :PR
3.    show: ----(--P \/ --Q)
4.      --(--P \/ --Q) :AS
5.      show: ----P
6.        --P :AS
7.        --P \/ --Q :ADD 6
8.      :ID 4 7
9.      P :DNE 5
10.     show: ----Q
11.       --Q :AS
12.       --P \/ --Q :ADD 11
13.     :ID 4 12
14.     Q :DNE 10
15.     P /\ Q :ADJ 9 14
16.   :ID 2 15
17.   --P \/ --Q :DNE 3
18. :DD 17
```

Many more examples can be found in the ```test``` function in ```proof_check.py```.
