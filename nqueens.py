from typing import Tuple, List, Optional, Union

from optilog.formulas import CNF  # type: ignore
from optilog.modelling import Bool, Not
from optilog.solvers.sat import Glucose41


from utils import main, queen_at  # noqa: F401


Literal = Union[Bool, Not]

# ################################################
# #            Your solution here                #
# ################################################
def at_least_one(literals: List[Literal]) -> List[List[Literal]]:
    """
    Generate the At Least One constraint
    for a list of literals.

    Returns a list of clauses.
    """
    clausula=[]
    for i in literals :
        clausula.append(i)
    clausulas = [clausula]
    return clausulas
    


def at_most_one(literals: List[Literal]) -> List[List[Literal]]:
    """
    Generate the At Most One constraint
    for a list of literals.

    Returns a list of clauses
    """
    clausulas = [[]]
    for i in range(len(literals)):
        for a in range(i + 1, len(literals)):
            clausulas.append([~literals[i], ~literals[a]])
    return clausulas


def exactly_one(literals: List[Literal]) -> List[List[Literal]]:
    """
    Generate the Exactly One constraint
    for a list of literals.

    Returns a list of clauses
    """
    clausulas=[]
    clausulas.append(at_least_one(literals))
    clausulas.append(at_most_one(literals))
    return clausulas
    """
    clausulas.append(literals)#assegurem que al menys un ha de ser cert
    for i in range(len(literals)):#assegurem que com a molt haurà una de certa
        for a in range(i + 1, len(literals)):
            clausulas.append([~literals[i], ~literals[a]])
            
    raise NotImplementedError"""


def encode(n: int, placed_queens: List[Tuple[int, int]]) -> CNF:
    """
    Given a size of a chess board (`n` x `n`), encodes
    the N-queens problem.
    The list `placed_queens` contains the cells where a queen MUST be placed.

    Returns a CNF object, with the constraints required for the problem.
    """
    cnf = CNF()
    
    # --------------
    # Your code here
    # --------------
    diagonal=[]
    fila=[]
    cont=[]
    for i in range(n):#files
        cont.clear()
        for j in range(n):
            cont.append(Bool(j))#fem servir array per a gruardar cada una 
        cnf.add_clause(exactly_one(cont))

    for j in range(n):#columnes
        cont.clear()
        for j in range(n):
            cont.append(Bool(j))#fem servir array per a gruardar cada una 
        cnf.add_clause(exactly_one(cont))
    i=0
    while i < n:
        cont.clear()
        

    return cnf


def solve(formula: CNF, seed: Optional[int]) -> Tuple[bool, Optional[List[int]]]:
    """
    Given a CNF formula, calls a SAT solver to check its
    satisfiability.

    If seed is not None, it is used to set the solver seed
    to have reproducible results.

    Returns a tuple, composed by:
    - a boolean that indicates if it is satisfiable.
    - the model if it is satisfiable, otherwise None.
    """

    solver=Glucose41()
    solver.add_clauses(formula.clauses)

    return solver.solve(), solver.model()


# ################################################
# #              Provided methods                #
# ################################################


if __name__ == "__main__":
    main(encode, solve)