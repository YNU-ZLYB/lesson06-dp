# -*- coding: utf-8 -*-
"""
【模块功能】预算 800 对比（自主实践任务①）
把硬币问题的目标金额从课堂的 15 改成 800，重新对比贪心与动态规划：
  - 贪心：每步取不超过余额的最大面额
  - 动态规划：求最少枚数（全局最优）
并解释"为什么 15 时贪心会失效，而 800 时两种方法结果相同"。

依赖：coin_loader（复用已完成的贪心 / 动规实现，不重复写算法）
"""

from coin_loader import coin_greedy, coin_dp

COINS = [1, 5, 11]


def fmt(combo):
    """把 {面额: 次数} 格式化成 5×3 + 1×2 这样的可读字符串"""
    return " + ".join(f"{v}×{k}" for k, v in sorted(combo.items(), reverse=True))


def compare(amount):
    """对单个金额跑两种算法，返回 (贪心枚数, 贪心组合, 动规枚数, 动规组合)"""
    g_count, g_combo = coin_greedy(amount, COINS)
    d_count, d_combo = coin_dp(amount, COINS)
    return g_count, g_combo, d_count, d_combo


def main():
    print(f"【预算对比】面额 {COINS}")
    results = {}
    for amount in (15, 800):
        g_count, g_combo, d_count, d_combo = compare(amount)
        results[amount] = (g_count, d_count)
        print(f"\n  目标 {amount}：")
        print(f"    贪心：{g_count:>3} 枚   组合 {fmt(g_combo)}")
        print(f"    动规：{d_count:>3} 枚   组合 {fmt(d_combo)}")
        if g_count > d_count:
            print(f"    → 贪心失效：比最优多花 {g_count - d_count} 枚")
        else:
            print("    → 贪心恰好也是最优")

    print("\n【解释】")
    print("  凑 15 时，贪心先拿 11，剩下 4 只能用 4 枚 1 元，共 5 枚；")
    print("  而 5+5+5 只要 3 枚。贪心只看眼前最大面额，不会回头，所以会错过全局最优。")
    print("  凑 800 时，800 = 72×11 + 8，8 = 5 + 3×1，贪心共 76 枚；")
    print("  动规用同样的拆分也是 76 枚。原因是 800 对 11 取余后剩下 8，"
          "恰好能用 5 和 1 凑成最优，贪心这次没有踩到坑。")
    print("  结论：贪心是否失效取决于具体金额，不是面额体系固定失效；"
          "动态规划每次都能保证最优，代价是要算整张 dp 表。")


if __name__ == "__main__":
    main()
