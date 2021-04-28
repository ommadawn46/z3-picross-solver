import z3


def build_blocks_list(problem, var_char):
    """
    問題から各ブロックを表すz3変数のリストを生成
    """
    blocks_list = []
    for var_num, numbers in enumerate(problem):
        blocks = []
        for n_i, n in enumerate(numbers):
            left = z3.Int(f"{var_char}{var_num}_{n_i}")
            right = left + n
            blocks.append((left, right))
        blocks_list.append(blocks)
    return blocks_list


def add_blocks_constraint(solver, blocks_list, right_max):
    """
    各ブロックの制約をソルバーに追加
    """
    for blocks in blocks_list:
        left_min = 0
        for left, right in blocks:
            # 左端が下限値以上
            solver.add(left_min <= left)
            # 次のブロックとの間に1マス空く
            left_min = right + 1
        # 右端が上限値以下
        solver.add(right <= right_max)


def generate_cell_constraint(i, blocks, cell):
    """
    マス目の制約を生成
    """
    # マス目がいずれかのブロックに含まれる⇒黒, 含まれない⇒白
    consts = [z3.And(left <= i, i < right) for left, right in blocks]
    return cell == z3.Or(consts)


def add_cells_constraint(solver, cells, v_blocks_list, h_blocks_list):
    """
    各マス目の制約をソルバーに追加
    """
    for x in range(len(v_blocks_list)):
        for y in range(len(h_blocks_list)):
            solver.add(
                generate_cell_constraint(y, blocks=v_blocks_list[x], cell=cells[x][y]),
                generate_cell_constraint(x, blocks=h_blocks_list[y], cell=cells[x][y]),
            )


def solve_problem(v_problem, h_problem):
    """
    ピクロスの問題を解く
    """
    solver = z3.Solver()
    width, height = len(v_problem), len(h_problem)

    # 各マス目のz3変数を生成
    cells = [[z3.Bool(f"c_{x}_{y}") for y in range(height)] for x in range(width)]

    # 問題から各ブロックを表すz3変数のリストを作成
    v_blocks_list = build_blocks_list(problem=v_problem, var_char="v")
    h_blocks_list = build_blocks_list(problem=h_problem, var_char="h")

    # 各ブロックに制約を追加
    add_blocks_constraint(solver=solver, blocks_list=v_blocks_list, right_max=height)
    add_blocks_constraint(solver=solver, blocks_list=h_blocks_list, right_max=width)

    # 各マス目に制約を追加
    add_cells_constraint(
        solver=solver,
        cells=cells,
        v_blocks_list=v_blocks_list,
        h_blocks_list=h_blocks_list,
    )

    # 問題が解けるかチェック
    if solver.check() != z3.sat:
        return None

    model = solver.model()
    return [[bool(model[cells[x][y]]) for y in range(height)] for x in range(width)]


def generate_pretty_str(solution, v_problem, h_problem, margin):
    """
    解法からピクロス盤面を表す文字列を生成
    """
    sp = lambda m: " " * m

    v_max = max(map(len, v_problem))
    h_max = max(map(len, h_problem))

    result = ""
    for i in range(v_max):
        result += sp(margin + 1) * h_max
        for v_numbers in v_problem:
            n_len = len(v_numbers)
            v_number_str = (
                str(v_numbers[i + n_len - v_max]) if i >= v_max - n_len else ""
            )
            result += v_number_str + sp(margin - len(v_number_str) + 1)
        result += "\n"

    for y in range(len(h_problem)):
        h_numbers = h_problem[y]
        result += sp(margin + 1) * (h_max - len(h_numbers))
        for h_number in h_numbers:
            h_number_str = str(h_number)
            result += h_number_str + sp(margin - len(h_number_str) + 1)

        for x in range(len(v_problem)):
            result += ("■" if solution[x][y] else "□") + sp(margin)
        result += "\n"

    return result


def main():
    import argparse
    import yaml

    parser = argparse.ArgumentParser()
    parser.add_argument("problem_file", help="Path to a problem file", type=str)
    parser.add_argument(
        "--margin",
        help="Size of margin between each cell",
        default=1,
        type=int,
    )
    args = parser.parse_args()

    # ピクロス問題をロード
    with open(args.problem_file, "r") as f:
        problem = yaml.safe_load(f)

    # ピクロスを解く
    v_problem, h_problem = problem["vertical"], problem["horizontal"]
    solution = solve_problem(v_problem=v_problem, h_problem=h_problem)

    # 解法を表示
    if solution:
        print("[+] Successfully solved the problem.")
        result = generate_pretty_str(
            solution=solution,
            v_problem=v_problem,
            h_problem=h_problem,
            margin=args.margin,
        )
        print(result)
    else:
        print("[!] Failed to solve the problem.")


if __name__ == "__main__":
    main()
