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


def add_cells_constraint(solver, cells, v_blocks_list, h_blocks_list):
    """
    マス目の制約をソルバーに追加
    """
    for x in range(len(v_blocks_list)):
        for y in range(len(h_blocks_list)):
            cell = cells[x][y]
            v_blocks, h_blocks = v_blocks_list[x], h_blocks_list[y]

            v_consts = []
            for y_left, y_right in v_blocks:
                # マス目が縦ブロックに含まれるか？
                v_consts.append(z3.And(y_left <= y, y < y_right))
            # マス目がいずれかの縦ブロックに含まれる⇒黒, 含まれない⇒白
            solver.add(cell == z3.Or(v_consts))

            h_consts = []
            for x_left, x_right in h_blocks:
                # マス目が横ブロックに含まれるか？
                h_consts.append(z3.And(x_left <= x, x < x_right))
            # マス目がいずれかの横ブロックに含まれる⇒黒, 含まれない⇒白
            solver.add(cell == z3.Or(h_consts))


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
        print("[!] Failed to solve the problem.")
        return None

    print("[+] Successfully solved the problem.")
    model = solver.model()
    return [[bool(model[cells[x][y]]) for y in range(height)] for x in range(width)]


def generate_pretty_str(solution, v_problem, h_problem, margin):
    """
    解法からピクロス盤面を表す文字列を生成
    """
    sp = " " * margin

    v_max = max(map(len, v_problem))
    h_max = max(map(len, h_problem))

    result = ""
    for i in range(v_max):
        result += (" " + sp) * h_max
        for v_numbers in v_problem:
            n_len = len(v_numbers)
            if i + n_len >= v_max:
                result += f"{v_numbers[i + n_len - v_max]}" + sp
            else:
                result += " " + sp
        result += "\n"

    for y in range(len(h_problem)):
        h_numbers = h_problem[y]
        result += (" " + sp) * (h_max - len(h_numbers))
        for h_number in h_numbers:
            result += f"{h_number}" + sp

        for x in range(len(v_problem)):
            result += ("■" if solution[x][y] else "□") + sp
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
        result = generate_pretty_str(
            solution=solution,
            v_problem=v_problem,
            h_problem=h_problem,
            margin=args.margin,
        )
        print(result)


if __name__ == "__main__":
    main()
