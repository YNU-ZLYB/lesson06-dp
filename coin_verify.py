# -*- coding: utf-8 -*-
"""
【模块功能】运行结果验证
对已完成的贪心 / 动态规划算法输出做独立校验，防止"算错但没人发现"：
1. 组合中的面额必须全部来自可用面额（来源合法）
2. 组合金额之和必须等于目标金额（凑对了没有）
3. 返回的枚数必须等于组合中硬币的实际总个数（前后一致）
4. 小金额场景下用暴力枚举交叉验证 DP 给出的确实是全局最优枚数

依赖：coin_loader（统一加载已完成的算法）
"""

from itertools import combinations_with_replacement
from coin_loader import coin_greedy, coin_dp

# 暴力枚举只用于小金额（指数级复杂度），超过该阈值自动跳过
BRUTE_FORCE_LIMIT = 120


def verify_result(coins, amount, count, combo):
    """
    校验单次算法输出的合法性。combo 格式：{面额: 使用次数}
    全部通过返回 True，否则抛出 AssertionError 并说明原因。
    """
    # 1. 面额来源合法
    for c in combo:
        assert c in coins, f"组合中出现非法面额 {c}（可用面额：{coins}）"
    # 2. 组合求和必须等于目标金额
    total = sum(c * n for c, n in combo.items())
    assert total == amount, f"组合求和 {total} ≠ 目标金额 {amount}"
    # 3. 返回枚数与实际组合枚数一致
    n_coins = sum(combo.values())
    assert n_coins == count, f"返回枚数 {count} 与组合实际枚数 {n_coins} 不一致"
    return True


def brute_force_min(coins, amount):
    """
    暴力枚举：从 0 枚开始逐枚增加，找到能凑出 amount 的最少枚数。
    仅用于小金额的正确性交叉验证（组合爆炸，大金额勿用）。
    无解时返回 None。
    """
    for k in range(amount + 1):
        # 从所有面额中可重复地取 k 枚，枚举全部组合
        for combo in combinations_with_replacement(coins, k):
            if sum(combo) == amount:
                return k
    return None


def verify_dp_optimal(coins, amount):
    """用暴力枚举交叉验证：DP 给出的枚数确实是全局最优"""
    dp_count, dp_combo = coin_dp(amount, coins)
    verify_result(coins, amount, dp_count, dp_combo)
    if amount > BRUTE_FORCE_LIMIT:
        return "跳过暴力验证（金额过大）"
    bf = brute_force_min(coins, amount)
    assert bf == dp_count, f"DP 给出 {dp_count} 枚，但暴力枚举最优为 {bf} 枚"
    return True


def main():
    """演示：对几组典型用例做完整验证"""
    cases = [([1, 5, 11], 15), ([1, 2, 5], 11), ([1, 5, 10, 25], 63)]
    print("【结果验证演示】")
    for coins, amount in cases:
        g_count, g_combo = coin_greedy(amount, coins)
        d_count, d_combo = coin_dp(amount, coins)
        verify_result(coins, amount, g_count, g_combo)   # 校验贪心输出格式
        verify_result(coins, amount, d_count, d_combo)   # 校验 DP 输出格式
        verify_dp_optimal(coins, amount)                 # 交叉验证 DP 最优性
        print(f"  面额 {coins} 凑 {amount}：输出校验通过，DP 最优性交叉验证通过")


if __name__ == "__main__":
    main()
