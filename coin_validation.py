# -*- coding: utf-8 -*-
"""
【模块功能】输入校验与边界异常处理
在调用硬币算法之前检查参数合法性，拦截非法输入并给出清晰的中文报错：
- 金额：必须为非负整数（拒绝负数、小数、字符串、布尔值、None 等）
- 面额：列表必须非空、元素均为正整数、不允许重复
- 可解性预判：若金额不能被所有面额的最大公约数整除，则必定无解，提前拦截

注意：可解性预判只是必要条件（能拦截"必定无解"），不是充分条件；
例如面额 [5, 11] 凑 3 通过预判但实际无解，这种情况由 DP 算法本身抛出异常。
"""

from math import gcd
from functools import reduce


def validate_amount(amount):
    """校验目标金额，非法时抛出 TypeError / ValueError"""
    # 注意：Python 中 bool 是 int 的子类，必须先排除 True/False
    if isinstance(amount, bool) or not isinstance(amount, int):
        raise TypeError(f"金额必须是整数，收到：{amount!r}（类型 {type(amount).__name__}）")
    if amount < 0:
        raise ValueError(f"金额不能为负数，收到：{amount}")
    return amount


def validate_coins(coins):
    """校验面额列表，非法时抛出 TypeError / ValueError"""
    if not isinstance(coins, (list, tuple)):
        raise TypeError(f"面额必须是列表或元组，收到类型：{type(coins).__name__}")
    if len(coins) == 0:
        raise ValueError("面额列表不能为空")
    for c in coins:
        if isinstance(c, bool) or not isinstance(c, int):
            raise TypeError(f"面额必须是整数，收到：{c!r}")
        if c <= 0:
            raise ValueError(f"面额必须为正整数，收到：{c}")
    if len(set(coins)) != len(coins):
        raise ValueError(f"面额存在重复：{sorted(coins)}")
    return list(coins)


def check_solvable(coins, amount):
    """
    可解性预判（必要条件）：amount 必须能被所有面额的最大公约数整除。
    返回 True 表示"可能有解"，False 表示"必定无解"。
    """
    g = reduce(gcd, coins)          # 所有面额的最大公约数
    return amount % g == 0


def validate_all(coins, amount):
    """一站式校验：金额 + 面额 + 可解性预判。全部通过则返回 (面额列表, 金额)"""
    validate_amount(amount)
    validate_coins(coins)
    if amount > 0 and not check_solvable(coins, amount):
        g = reduce(gcd, coins)
        raise ValueError(
            f"必定无解：面额 {sorted(coins)} 的最大公约数为 {g}，无法整除金额 {amount}"
        )
    return list(coins), amount


def main():
    """演示：各种非法 / 边界输入会被逐一拦截并打印中文提示"""
    bad_cases = [
        ([1, 5, 11], -3),      # 负数金额
        ([1, 5, 11], 3.5),     # 小数金额
        ([1, 5, 11], "15"),    # 字符串金额
        ([1, 5, 11], None),    # None
        ([], 15),              # 空面额列表
        ([1, 0, 5], 15),       # 面额含 0
        ([1, -5, 11], 15),     # 面额含负数
        ([1, 5, 5], 15),       # 面额重复
        ([2, 4], 7),           # gcd=2 不整除 7，必定无解
        ([1, 5, 11], 15),      # 合法输入（对照组，应通过）
    ]
    print("【输入校验演示】")
    for coins, amount in bad_cases:
        try:
            validate_all(coins, amount)
            print(f"  {str(coins):<14} 凑 {str(amount):>6} -> 校验通过")
        except (TypeError, ValueError) as e:
            print(f"  {str(coins):<14} 凑 {str(amount):>6} -> 拦截：{e}")


if __name__ == "__main__":
    main()
