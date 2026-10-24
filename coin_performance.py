# -*- coding: utf-8 -*-
"""
【模块功能】性能对比分析
用 timeit 测量贪心与 DP 在不同金额下的平均耗时，
用 tracemalloc 测量峰值内存占用，采集成数据记录（供可视化模块使用）。

理论复杂度（n=金额，k=面额种数）：
- 贪心：时间约 O(枚数)，空间 O(枚数) —— 几乎与面额种数无关
- DP  ：时间 O(n × k)，空间 O(n)   —— 随金额线性增长

依赖：coin_loader
"""

import timeit
import tracemalloc
from coin_loader import coin_greedy, coin_dp


def measure_time(func, amount, coins, repeat=5, number=20):
    """
    测量平均单次耗时（毫秒）。
    repeat 轮取最优（减少系统抖动影响），每轮连续执行 number 次。
    """
    timer = timeit.Timer(lambda: func(amount, coins))
    best = min(timer.repeat(repeat=repeat, number=number))
    return best / number * 1000  # 换算成毫秒


def measure_memory(func, amount, coins):
    """测量算法单次执行的峰值内存（KB），用 tracemalloc 跟踪 Python 对象分配"""
    tracemalloc.start()
    func(amount, coins)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak / 1024  # 换算成 KB


def collect(amounts, coins):
    """
    对一组金额逐一采集性能数据。
    返回记录列表，每条记录：{amount, greedy_ms, dp_ms, greedy_kb, dp_kb}
    """
    records = []
    for amount in amounts:
        records.append({
            "amount": amount,
            "greedy_ms": measure_time(coin_greedy, amount, coins),
            "dp_ms": measure_time(coin_dp, amount, coins),
            "greedy_kb": measure_memory(coin_greedy, amount, coins),
            "dp_kb": measure_memory(coin_dp, amount, coins),
        })
    return records


def main():
    """演示：采集数据并打印对比表格"""
    COINS = [1, 5, 11]
    AMOUNTS = [100, 200, 400, 800, 1600, 3200]
    print("【性能对比】面额 [1, 5, 11]")
    print(f"{'金额':>8} | {'贪心(ms)':>10} | {'DP(ms)':>10} | {'贪心(KB)':>10} | {'DP(KB)':>10}")
    print("-" * 60)
    for r in collect(AMOUNTS, COINS):
        print(f"{r['amount']:>8} | {r['greedy_ms']:>10.3f} | {r['dp_ms']:>10.3f} "
              f"| {r['greedy_kb']:>10.2f} | {r['dp_kb']:>10.2f}")


if __name__ == "__main__":
    main()
