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

* $\lnot = $ ```--``` (negation)
* $\land = $ ```/\``` (conjunction/and)
* $\lor = $ ```\/``` (disjunction/or)
* $\rightarrow = $ ```->``` (implication)

### Justification

Each line of a proof consists of a formula written with variables and the symbols above and a justification. The justification is separated by  ```:``` and consists of numbers, referencing the lines that justify the current formula. The possible justifications are

* ```PR``` premise, no justification needed.
* ```AS``` assumption, no justification needed. Used in conditional and indirect derivations.
* ```MP``` modus ponens, justified by two previous lines. Relative to the following, one of the listed lines should contain $\varphi \rightarrow \psi$ and the other $\varphi$.

$$ \varphi \rightarrow \psi, \varphi \vdash \psi $$

* ```MT``` modus tollens, justified by two previous lines. Relative to the following, one of the listed lines should contain $\varphi \rightarrow \psi$ and the other $\lnot \psi$.

$$ \varphi \rightarrow \psi, \lnot \psi \vdash \psi $$

* ```DNE``` double negation elimination, justified by one previous line. Relative to the following, the listed line should contain $\lnot(\lnot \varphi)$.

$$ \lnot(\lnot \varphi) \vdash \varphi $$

* ```DNI``` double negation introduction, justified by one previous line. Relative to the following, the list line should contain $\varphi$.

$$ \varphi \vdash \lnot(\lnot \varphi) $$

* ```ADJ``` adjunction, justified by two previous lines. Relative to the following, one of the listed lines should contain $\varphi$ and the other $\psi$.

$$ \varphi, \psi \vdash \varphi \land \psi $$

* ```S``` simplification, justified by one previous line. Relative to the following, the listed line should contain $\varphi \land \psi$.

$$ \varphi \land \psi \vdash \varphi $$

* ```ADD``` addition, justified by one previous line. Relative to the following, the listed line should contain $\varphi$.

$$ \varphi \vdash \varphi \lor \psi $$

* ```MTP``` modus tollendo ponens (also called disjunctive syllogism), justified by two previous lines. Relative to the following, one oft he other listed lines should contain $\varphi \lor \psi$ and the other $\lnot \varphi$.

$$ \varphi \lor \psi, \lnot \varphi \vdash \psi $$

### Writing Proofs

Proofs are started with a *show* line, which consists of ```show``` followed by the formula to be proved. The following lines are formulas with justifications, until the *QED* line.

### Proof Techniques

There are three styles of proofs that are allowed: direct derivations, conditional derivations, and indirect derivations. They are identified by their *QED* lines.

* Direct derivations prove any formula and have no assumptions. They begin with a *show* line and proceed directly from the *show* line to the *QED* line, which is ```:DD``` followed by the line number on which the formula specified in the *show* line was achieved.

* Conditional derivations prove formulas of the form $\varphi \rightarrow \psi$ and have one assumption, namely $\varphi$. They begin with assuming $\varphi$ and proceed to achieve $\psi$. They conclude with the *QED* line, which is ```:CD``` followed by the line number on which $\psi$ was achieved.

* Indirect derivations prove formulas of the from $\lnot \varphi$ and have one assumption, namely $\varphi$. They begin with assuming $\varphi$ and proceeds to achieve a contradiction, which is having $\psi$ and $\lnot \psi$ on separate lines for any formula $\psi$. They conclude with the *QED* line, which is ```:ID``` followed by the line numbers on which $\psi$ and $\lnot \psi$ were achieved.

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
