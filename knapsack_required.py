# -*- coding: utf-8 -*-
"""
【模块功能】0/1 背包 + 必投项目约束（自主实践任务②）
题目：登山背包，限重 1000 克，5 件东西（数据见 knapsack.py）。
新增约束：指定某件东西必须带（必投项目），其余东西仍按 0-1 规则自由选择。

做法：
  1. 先把必投项目直接放进背包，扣掉它的重量和重要度；
  2. 对剩下的东西、在剩余容量上再跑一次标准 0/1 背包；
  3. 两部分合并，就是满足约束的最优解。
这样既不用改 dp 结构，也保证了必投项目一定入选。

依赖：knapsack.py（货物表与通用的 0/1 背包求解）
"""

from knapsack import ITEMS, CAPACITY, knapsack


def knapsack_with_required(items, capacity, required_name):
    """
    带必投项目约束的 0/1 背包。
    返回 (最大重要度, 选中物品列表, 总重量)。
    若不存在该货物或剩余容量为负，抛出 ValueError。
    """
    names = [it[0] for it in items]
    if required_name not in names:
        raise ValueError(f"货物表中没有 {required_name}，现有：{names}")

    required = next(it for it in items if it[0] == required_name)
    rest = [it for it in items if it[0] != required_name]
    remaining_capacity = capacity - required[1]

    if remaining_capacity < 0:
        raise ValueError(f"必投项目 {required_name} 重 {required[1]} 克，已超过限重 {capacity} 克")

    # 剩余容量上对剩余货物做标准 0/1 背包
    best_rest, selected_rest, _ = knapsack(rest, remaining_capacity)

    selected = [required] + selected_rest
    total_weight = sum(it[1] for it in selected)
    return required[2] + best_rest, selected, total_weight


def main():
    required_name = "帐篷"   # 本实验指定帐篷为必投项目

    free_best, free_selected, free_weight = knapsack(ITEMS, CAPACITY)
    must_best, must_selected, must_weight = knapsack_with_required(ITEMS, CAPACITY, required_name)

    print("【必投项目约束】")
    print(f"  限重 {CAPACITY} 克，必投项目：{required_name}")
    print(f"  [无约束] 最优重要度 {free_best}，总重 {free_weight} 克")
    print(f"           组合：{'、'.join(it[0] for it in free_selected)}")
    print(f"  [有约束] 最优重要度 {must_best}，总重 {must_weight} 克")
    print(f"           组合：{'、'.join(it[0] for it in must_selected)}")
    print(f"  结论：强迫带上 {required_name} 后，最优值由 {free_best} 变为 {must_best}，"
          f"少了 {free_best - must_best}；约束降低了可选空间，最优解不会更好，只会持平或变差。")


if __name__ == "__main__":
    main()
