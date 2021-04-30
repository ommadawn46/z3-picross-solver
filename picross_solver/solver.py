import z3


def build_blocks_list(hints, var_char):
    """
    問題から各ブロックを表すz3変数のリストを生成
    """
    blocks_list = []
    for var_num, numbers in enumerate(hints):
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
            # 次のブロックとの間に1マス空ける
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
    add_const = lambda x, y: solver.add(
        generate_cell_constraint(i=y, blocks=v_blocks_list[x], cell=cells[x][y]),
        generate_cell_constraint(i=x, blocks=h_blocks_list[y], cell=cells[x][y]),
    )
    for x in range(len(v_blocks_list)):
        for y in range(len(h_blocks_list)):
            add_const(x, y)


def solve_picross(vertical_hints, horizontal_hints):
    """
    ピクロスの問題を解く
    """
    solver = z3.Solver()
    width, height = len(vertical_hints), len(horizontal_hints)

    # 各マス目のz3変数を生成
    cells = [[z3.Bool(f"c_{x}_{y}") for y in range(height)] for x in range(width)]

    # 問題から各ブロックを表すz3変数のリストを作成
    v_blocks_list = build_blocks_list(hints=vertical_hints, var_char="v")
    h_blocks_list = build_blocks_list(hints=horizontal_hints, var_char="h")

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
