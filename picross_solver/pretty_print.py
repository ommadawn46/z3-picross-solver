def generate_pretty_str(solution, vertical_hints, horizontal_hints, margin):
    """
    解法からピクロス盤面を表す文字列を生成
    """
    sp = lambda m: " " * m

    v_max = max(map(len, vertical_hints))
    h_max = max(map(len, horizontal_hints))

    result = ""
    for i in range(v_max):
        result += sp(margin + 1) * h_max
        for v_numbers in vertical_hints:
            n_len = len(v_numbers)
            v_number_str = (
                str(v_numbers[i + n_len - v_max]) if i >= v_max - n_len else ""
            )
            result += v_number_str + sp(margin - len(v_number_str) + 1)
        result += "\n"

    for y in range(len(horizontal_hints)):
        h_numbers = horizontal_hints[y]
        result += sp(margin + 1) * (h_max - len(h_numbers))
        for h_number in h_numbers:
            h_number_str = str(h_number)
            result += h_number_str + sp(margin - len(h_number_str) + 1)

        for x in range(len(vertical_hints)):
            result += ("■" if solution[x][y] else "□") + sp(margin)
        result += "\n"

    return result.rstrip()


def pprint(solution, vertical_hints, horizontal_hints, margin):
    print(generate_pretty_str(solution, vertical_hints, horizontal_hints, margin))
