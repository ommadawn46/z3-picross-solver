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
    vertical_hints = problem["vertical_hints"]
    horizontal_hints = problem["horizontal_hints"]

    # ピクロスを解く
    solution = solver.solve_picross(
        vertical_hints=vertical_hints,
        horizontal_hints=horizontal_hints,
    )

    # 解法を表示
    if solution:
        print("[+] Successfully solved the problem.")
        pretty_print.pprint(
            solution=solution,
            vertical_hints=vertical_hints,
            horizontal_hints=horizontal_hints,
            margin=args.margin,
        )
    else:
        print("[!] Failed to solve the problem.")


if __name__ == "__main__":
    main()
