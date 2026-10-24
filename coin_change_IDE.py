# -*- coding: utf-8 -*-
"""
找零问题：贪心 vs 动态规划
---------------------------------
给定若干面额 coins 和目标金额 amount，求最少硬币枚数及具体组合。

本模块实现两种经典策略：
  1. coin_greedy  —— 贪心算法：每一步都取"不超过当前余额"的最大面额
  2. coin_dp      —— 动态规划：枚举所有可能，保证得到全局最优解

用面额 [1, 5, 11] 凑 15 元时，贪心会给出 11+1+1+1+1 = 5 枚，
而 DP 能找到 5+5+5 = 3 枚 —— 这正是"贪心不一定最优"的教科书例子。
"""

from collections import Counter


def coin_greedy(amount, coins):
    """
    贪心算法求解最少找零枚数。

    策略：每一步都挑出 ≤ 当前余额的最大面额硬币，扣减后继续，直到余额归零。

    参数：
        amount (int)：需要凑出的目标金额（单位：元/分，必须为非负整数）
        coins  (list)：可用面额列表，如 [1, 5, 11]，顺序不敏感

    返回：
        (total, combo) —— 总枚数，以及各面额使用次数的字典
            例如 (3, {5: 3}) 表示 3 枚 5 元硬币
    """
    # 把面额降序排列，方便每次从"最大面额"开始尝试
    sorted_coins = sorted(coins, reverse=True)

    combo = Counter()      # 记录每种面额用了多少枚
    remaining = amount     # 剩余待凑金额

    while remaining > 0:
        # 找到第一个 ≤ remaining 的最大面额
        chosen = None
        for c in sorted_coins:
            if c <= remaining:
                chosen = c
                break

        if chosen is None:
            # 所有面额都比剩余金额大，说明凑不出来（比如用 [5,11] 凑 3）
            raise ValueError(f"无法用面额 {coins} 凑出 {amount} 元")

        combo[chosen] += 1
        remaining -= chosen

    return sum(combo.values()), dict(combo)


def coin_dp(amount, coins):
    """
    动态规划求解最少找零枚数（保证全局最优）。

    转移方程：
        dp[i] = 凑出金额 i 所需的最少硬币枚数
        dp[i] = min( dp[i - c] + 1 )  对所有满足 i - c ≥ 0 的面额 c
        边界：dp[0] = 0（凑 0 元不需要硬币）

    同时维护 parent[i] —— 在最优解下，凑出金额 i 时最后选的那枚硬币面额，
    这样可以从 amount 倒推，完整还原出具体组合。

    参数：
        amount (int)：需要凑出的目标金额
        coins  (list)：可用面额列表

    返回：
        (total, combo) —— 总枚数，以及各面额使用次数的字典
    """
    # dp[i] 初始化为"无穷大"，表示暂时无法凑出；dp[0] = 0
    INF = float('inf')
    dp = [INF] * (amount + 1)
    dp[0] = 0

    # parent[i] 记录：凑出金额 i 时，最后选的那枚硬币面额
    parent = [None] * (amount + 1)

    for i in range(1, amount + 1):
        for c in coins:
            # 面额 c 必须 ≤ 当前金额 i，且子问题 dp[i - c] 必须有解
            if i - c >= 0 and dp[i - c] + 1 < dp[i]:
                dp[i] = dp[i - c] + 1
                parent[i] = c

    if dp[amount] == INF:
        raise ValueError(f"无法用面额 {coins} 凑出 {amount} 元")

    # ---------- 回溯还原具体组合 ----------
    combo = Counter()
    cur = amount
    while cur > 0:
        c = parent[cur]
        combo[c] += 1
        cur -= c

    return dp[amount], dict(combo)


# ============================================================
# 主程序：用面额 [1, 5, 11] 凑 15 元，对比贪心与 DP 的结果
# ============================================================
if __name__ == "__main__":
    COINS = [1, 5, 11]
    TARGET = 15

    print(f"=== 找零问题对比：面额 {COINS}，目标 {TARGET} 元 ===\n")

    total_g, combo_g = coin_greedy(TARGET, COINS)
    total_d, combo_d = coin_dp(TARGET, COINS)

    # 把组合字典按面额升序整理，打印更直观
    def fmt(combo):
        return " + ".join(f"{v}×{k}" for k, v in sorted(combo.items()))

    print(f"[贪心] 枚数 = {total_g}  组合 = {fmt(combo_g)}")
    print(f"[DP ] 枚数 = {total_d}  组合 = {fmt(combo_d)}")
    print()

    if total_g > total_d:
        print(f"👉 贪心比 DP 多花了 {total_g - total_d} 枚硬币，"
              f"再次说明：贪心策略不一定能得到全局最优解！")
    elif total_g == total_d:
        print("👉 两种策略给出的枚数相同（本次面额组合碰巧没有反例）。")
    else:
        print("👉 出现了意外情况，请检查代码。")
