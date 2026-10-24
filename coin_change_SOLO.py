# -*- coding: utf-8 -*-
"""
硬币找零问题：贪心算法 vs 动态规划
面额为 1、5、11，目标金额 15
- coin_greedy：贪心策略，每步取不超过余额的最大面额
- coin_dp：动态规划，求最少硬币枚数
两者均返回 (枚数, 具体组合)
"""


def coin_greedy(coins, amount):
    """
    贪心算法：每次从大到小选取不超过当前余额的最大面额。
    返回 (硬币枚数, 硬币组合列表)。
    """
    coins_sorted = sorted(coins, reverse=True)  # 面额从大到小排序
    remaining = amount       # 剩余待凑金额
    combination = []         # 记录已选硬币

    for coin in coins_sorted:
        # 当前面额不超过余额时，尽量多地选取
        while remaining >= coin:
            combination.append(coin)
            remaining -= coin

    return len(combination), combination


def coin_dp(coins, amount):
    """
    动态规划：求凑出 amount 所需的最少硬币枚数及具体组合。
    dp[i] 表示凑出金额 i 所需的最少硬币数；
    choice[i] 记录凑出金额 i 时最后选的那枚硬币，用于回溯组合。
    返回 (硬币枚数, 硬币组合列表)。
    """
    INF = float('inf')
    dp = [INF] * (amount + 1)      # 初始化为无穷大，表示暂时不可达
    choice = [-1] * (amount + 1)   # 记录每个金额最后选用的硬币面额
    dp[0] = 0                      # 金额 0 不需要任何硬币

    # 自底向上：依次计算金额 1 到 amount 的最优解
    for i in range(1, amount + 1):
        for coin in coins:
            # 若可以使用面额 coin，且使用后更优，则更新
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                choice[i] = coin

    # 回溯 choice 数组，还原具体组合
    combination = []
    i = amount
    while i > 0:
        coin = choice[i]
        if coin == -1:             # 理论上不会发生（面额含 1 必然有解）
            break
        combination.append(coin)
        i -= coin

    return dp[amount], combination


if __name__ == "__main__":
    coins = [1, 5, 11]
    amount = 15

    # 贪心算法结果
    greedy_count, greedy_comb = coin_greedy(coins, amount)
    print("【贪心算法】")
    print(f"  硬币枚数：{greedy_count}")
    print(f"  具体组合：{greedy_comb}  ->  {' + '.join(map(str, greedy_comb))} = {sum(greedy_comb)}")

    # 动态规划结果
    dp_count, dp_comb = coin_dp(coins, amount)
    print("【动态规划】")
    print(f"  硬币枚数：{dp_count}")
    print(f"  具体组合：{sorted(dp_comb, reverse=True)}  ->  {' + '.join(map(str, sorted(dp_comb, reverse=True)))} = {sum(dp_comb)}")

    # 对比结论
    print("【对比结论】")
    if dp_count < greedy_count:
        print(f"  贪心得到 {greedy_count} 枚，动态规划仅需 {dp_count} 枚。")
        print("  说明贪心算法在该面额体系下不一定得到全局最优解，动态规划才能保证最少枚数。")
    else:
        print("  两种方法结果一致。")
