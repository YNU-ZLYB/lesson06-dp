# -*- coding: utf-8 -*-
"""
【模块功能】打印背包 dp 表与回溯路径（自主实践任务③的素材生成器）
输出三块内容，可直接截图/粘贴进进度报告：
  1. dp 表采样视图：行=前 i 件货物，列=容量（每 50 克取一列，便于阅读）
  2. dp 表最后一行完整数值：容量 0~1000 共 1001 个值，每行 20 个
  3. 回溯路径：从 dp[5][1000] 倒推，逐件判断"带 / 不带"

依赖：knapsack.py（build_dp_table）
"""

from knapsack import ITEMS, CAPACITY, build_dp_table

SAMPLE_STEP = 50   # 采样视图的列间距（克）
ROW_WIDTH = 20     # 最后一行每行打印多少个数值


def print_sampled_table(dp):
    """打印 dp 表采样视图"""
    columns = list(range(0, CAPACITY + 1, SAMPLE_STEP))
    print(f"\n【dp 表·采样视图】（列每 {SAMPLE_STEP} 克取一个，完整数值见下一节）")
    header = "i \\ w".ljust(8) + "".join(f"{c:>6}" for c in columns)
    print(header)
    print("-" * len(header))
    for i in range(len(ITEMS) + 1):
        label = "0(空)" if i == 0 else f"{i}({ITEMS[i - 1][0]})"
        # 中文标签占两格，手工补空格保证列对齐
        pad = 8 - (len(label) * 2 if i > 0 else len(label))
        line = label + " " * max(pad, 0)
        line += "".join(f"{dp[i][c]:>6}" for c in columns)
        print(line)


def print_last_row(dp):
    """打印 dp 表最后一行（全部 1001 个数值）"""
    last = dp[len(ITEMS)]
    print(f"\n【dp 表最后一行·完整】共 {len(last)} 个值（容量 0~{CAPACITY}）")
    for start in range(0, len(last), ROW_WIDTH):
        chunk = last[start:start + ROW_WIDTH]
        header = f"容量 {start:>4}~{start + len(chunk) - 1:>4}："
        print(header + "".join(f"{v:>4}" for v in chunk))


def print_backtrack_path(dp):
    """打印回溯路径：每步判断当前这件东西带不带"""
    print("\n【回溯路径】从 dp[5][1000] 倒推")
    w = CAPACITY
    picked = []
    for i in range(len(ITEMS), 0, -1):
        name, weight, value = ITEMS[i - 1]
        cur, prev = dp[i][w], dp[i - 1][w]
        if cur != prev:
            picked.append(name)
            print(f"  i={i} {name:<2}：dp[{i}][{w}]={cur} ≠ dp[{i - 1}][{w}]={prev}"
                  f"  → 带，w 变为 {w - weight}")
            w -= weight
        else:
            print(f"  i={i} {name:<2}：dp[{i}][{w}]={cur} =  dp[{i - 1}][{w}]={prev}"
                  f"  → 不带，w 保持 {w}")
    picked.reverse()
    print(f"  回溯结束：最优值 {dp[len(ITEMS)][CAPACITY]}，组合 = {'、'.join(picked)}，剩余容量 {w} 克")


def main():
    dp = build_dp_table(ITEMS, CAPACITY)
    print_sampled_table(dp)
    print_last_row(dp)
    print_backtrack_path(dp)


if __name__ == "__main__":
    main()
