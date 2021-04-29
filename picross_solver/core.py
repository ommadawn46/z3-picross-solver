import argparse
import yaml
from picross_solver import pretty_print
from picross_solver import solver


def get_args():
    parser = argparse.ArgumentParser(prog="z3-picross-solver")
    parser.add_argument("problem_file", help="Path to a problem file", type=str)
    parser.add_argument(
        "--margin",
        help="Size of margin between each cell",
        default=1,
        type=int,
    )
    return parser.parse_args()


def main():
    args = get_args()

    # ピクロス問題をロード
    with open(args.problem_file, "r") as f:
        problem = yaml.safe_load(f)
    vertical_problem = problem["vertical"]
    horizontal_problem = problem["horizontal"]

    # ピクロスを解く
    solution = solver.solve_problem(
        vertical_problem=vertical_problem,
        horizontal_problem=horizontal_problem,
    )

    # 解法を表示
    if solution:
        print("[+] Successfully solved the problem.")
        pretty_print.pprint(
            solution=solution,
            vertical_problem=vertical_problem,
            horizontal_problem=horizontal_problem,
            margin=args.margin,
        )
    else:
        print("[!] Failed to solve the problem.")


if __name__ == "__main__":
    main()
