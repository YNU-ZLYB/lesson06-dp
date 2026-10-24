# -*- coding: utf-8 -*-
"""
【模块功能】0/1 背包：登山背包问题
数据来自课堂 PPT《问题三：登山背包》：
    背包限重 1000 克，共 5 件东西
    帐篷 300g / 重要度 90
    炉具 200g / 重要度 60
    睡袋 350g / 重要度 115
    食物 400g / 重要度 120
    水具 250g / 重要度 80
规则：每件东西要么带、要么不带（这就是 0-1），总重量不能超过 1000 克。

变体说明（任务书特别提醒）：
  本模块统一采用"至多装满"变体 —— dst 容量可以不花完，dp 初值全为 0。
  另一种"恰好装满"变体要求 dp[0]=0、其余为 -∞，两者答案可能不同，本课不采用。

状态定义：
  dp[i][w] = 只考虑前 i 件东西、限重为 w 时的最大重要度
转移方程：
  dp[i][w] = max( dp[i-1][w],                       # 不带第 i 件
                  dp[i-1][w-weight] + value )       # 带第 i 件（放得下时）
"""

# 货物表：每项为 (名称, 重量/克, 重要度)
ITEMS = [
    ("帐篷", 300, 90),
    ("炉具", 200, 60),
    ("睡袋", 350, 115),
    ("食物", 400, 120),
    ("水具", 250, 80),
]

CAPACITY = 1000  # 背包限重（克）


def build_dp_table(items, capacity):
    """
    构造二维 dp 表。
    返回 (dp, items)：dp 是 (n+1) x (capacity+1) 的列表，第 0 行为全 0。
    """
    n = len(items)
    # 至多装满变体：整张表初值为 0，表示"什么都不带"也是合法解
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name, weight, value = items[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]              # 先假设不带第 i 件
            if w >= weight:                      # 放得下才考虑带
                take = dp[i - 1][w - weight] + value
                if take > dp[i][w]:              # 带了更优则更新
                    dp[i][w] = take
    return dp


def backtrack(dp, items, capacity):
    """
    从 dp 表右下角向左上回溯，还原具体带了哪些东西。
    判断依据：若 dp[i][w] != dp[i-1][w]，说明第 i 件被选中。
    返回按货物表顺序排列的选中物品列表。
    """
    selected = []
    w = capacity
    for i in range(len(items), 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(items[i - 1])
            w -= items[i - 1][1]                 # 扣掉这件物品的重量
    selected.reverse()                           # 回溯是倒序得到的，翻转回来
    return selected


def knapsack(items, capacity):
    """
    求解 0/1 背包。
    返回 (最大重要度, 选中物品列表, 选中物品总重量)。
    """
    dp = build_dp_table(items, capacity)
    selected = backtrack(dp, items, capacity)
    total_weight = sum(it[1] for it in selected)
    return dp[len(items)][capacity], selected, total_weight


def main():
    best, selected, total_weight = knapsack(ITEMS, CAPACITY)
    print("【0/1 背包（至多装满）】")
    print(f"  限重：{CAPACITY} 克，共 {len(ITEMS)} 件东西")
    for name, weight, value in ITEMS:
        print(f"    {name}：{weight} 克 / 重要度 {value}")
    print(f"  最优重要度：{best}")
    print(f"  带的东西：{'、'.join(it[0] for it in selected)}")
    print(f"  总重量：{total_weight} 克（剩余 {CAPACITY - total_weight} 克）")
    for name, weight, value in selected:
        print(f"    {name} {weight} 克 / {value}")


if __name__ == "__main__":
    main()
