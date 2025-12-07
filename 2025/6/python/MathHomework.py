import argparse
from curses.ascii import isspace
import enum
from pathlib import Path
import time
from typing import Optional
import math
from concurrent.futures import ProcessPoolExecutor


class MathProblem:
    MULTIPLICATION_OPERATOR = "*"
    ADDITION_OPERATOR = "+"
    VALID_OPERATORS = [MULTIPLICATION_OPERATOR, ADDITION_OPERATOR]

    def __init__(
        self,
        operator,
        numerals=[],
    ) -> None:
        self.numerals = numerals
        self.operator = operator

    def solve(self):
        if self.operator == "*":
            return math.prod(self.numerals)
        elif self.operator == "+":
            return sum(self.numerals)

    def __repr__(self) -> str:
        return f"{self.operator} {" ".join([str(i) for i in self.numerals])}"

    @staticmethod
    def solve_problem(problem):  # -> Any:
        # print(f"Solving problem {problem}")
        return problem.solve()

    @staticmethod
    def solve_problems(problems: list):
        solution = 0
        with ProcessPoolExecutor() as executor:
            for ans in executor.map(MathProblem.solve_problem, problems):
                solution += ans
        return solution


def get_operator_positions(operator_line: str, operators=MathProblem.VALID_OPERATORS):
    return [i for i in range(len(operator_line)) if operator_line[i] in operators]


def get_problem_chunks(lines: list[str]):
    operator_indexes = get_operator_positions(lines[-1])
    operator_count = len(operator_indexes)
    for i, val in enumerate(operator_indexes):
        if i == operator_count - 1:
            yield [line[val:] for line in lines]
        else:
            next_val = operator_indexes[i + 1]
            yield [line[val:next_val] for line in lines]


def get_problem(problem_chunk: list[str]) -> MathProblem:
    numerals = [int(line.strip()) for line in problem_chunk[0:-1]]
    operator = problem_chunk[-1].strip()
    problem = MathProblem(operator=operator, numerals=numerals)
    return problem


def get_cephalid_problem(problem_chunk: list[str]) -> MathProblem:
    width = len(problem_chunk[0])
    columns = [
        "".join([line[column] for line in problem_chunk[0:-1]])
        for column in range(width)
    ]
    numerals = [int(column.strip()) for column in columns if len(column.strip())]
    operator = problem_chunk[-1].strip()
    problem = MathProblem(operator=operator, numerals=numerals)
    return problem


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Homework solver")

    default_file = Path(__file__).parent.parent / "sample_homework.txt"

    parser.add_argument(
        "-f",
        "--file",
        default=str(default_file),
        help="Path to instruction_file (default: parent directory sample file)",
    )

    args = parser.parse_args()

    part_1_calculation = 0

    problem_count: int = 0
    start = time.perf_counter()

    lines: list = []

    with open(file=args.file, mode="r") as f:
        lines = f.readlines()

    operators_line = lines[-1]
    problems: list[MathProblem] = []
    problems_cepahlid: list[MathProblem] = []
    for problem_chunk in get_problem_chunks(lines):
        problems.append(get_problem(problem_chunk=problem_chunk))
        problems_cepahlid.append(get_cephalid_problem(problem_chunk=problem_chunk))

    end: float = time.perf_counter()
    part_1_calculation: int = MathProblem.solve_problems(problems)
    print(f"part_1_calculation: {part_1_calculation}")
    part_2_calculation: int = MathProblem.solve_problems(problems_cepahlid)
    print(f"part_2_calculation: {part_2_calculation}")
    print(f"Took {end - start:.6f} seconds")
