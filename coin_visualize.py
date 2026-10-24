# -*- coding: utf-8 -*-
"""
【模块功能】复杂度对比可视化（纯文本 ASCII 版，无需第三方库）
调用性能模块采集的数据，用文本柱状图展示：
1. 耗时随金额增长趋势（贪心 vs DP）
2. 峰值内存随金额增长趋势（贪心 vs DP）

可直观看到：贪心耗时/内存基本平坦（只与枚数有关），
DP 则随金额近似线性增长（dp 数组长度 = 金额 + 1）。

依赖：coin_performance
"""

from coin_performance import collect


def ascii_bar(value, max_value, width=40):
    """按比例生成一根文本柱子，宽度上限 width 个字符"""
    if max_value <= 0:
        return ""
    filled = round(value / max_value * width)
    if value > 0:
        filled = max(1, filled)   # 非零值至少画一格，避免"看不见"
    return "█" * filled


def plot(records, key_g, key_d, title, unit):
    """画一组贪心 vs DP 的对比柱状图"""
    max_v = max(max(r[key_g], r[key_d]) for r in records)
    print(f"\n【{title}】单位：{unit}（柱子按比例缩放，本组最大值 {max_v:.3f}）")
    for r in records:
        print(f"  金额 {r['amount']:>6}")
        print(f"    贪心 |{ascii_bar(r[key_g], max_v)} {r[key_g]:.3f}")
        print(f"    DP   |{ascii_bar(r[key_d], max_v)} {r[key_d]:.3f}")


def main():
    COINS = [1, 5, 11]
    AMOUNTS = [100, 200, 400, 800, 1600, 3200]
    records = collect(AMOUNTS, COINS)
    plot(records, "greedy_ms", "dp_ms", "耗时对比", "毫秒")
    plot(records, "greedy_kb", "dp_kb", "峰值内存对比", "KB")
    print("\n读图结论：DP 耗时/内存随金额线性增长（O(n×k) / O(n)），"
          "贪心基本平坦（只取决于枚数）——这就是 DP 用空间换最优性的代价。")


if __name__ == "__main__":
    main()
