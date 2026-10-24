# -*- coding: utf-8 -*-
"""
【模块功能】测试用例套件
覆盖多种面额组合与边界场景，自动断言并汇总通过情况：

正常用例（断言 DP 枚数 + 校验输出 + 判断贪心是否也最优）：
  - 课堂案例：面额 [1,5,11] 凑 15，贪心失效（5 枚 vs 3 枚）—— 课堂检查点
  - 经典反例：面额 [1,3,4] 凑 6，贪心失效（3 枚 vs 2 枚）
  - 美国面额 [1,5,10,25]：贪心恰好也是最优
  - 边界：金额 0、金额等于最大面额、单种面额、较大金额 800（作业预算）

异常用例（断言必须抛出指定异常）：
  - 有解性预判之外的真正无解：面额 [5,11] 凑 3
  - 必定无解被校验模块提前拦截：面额 [2,4] 凑 7
  - 非法输入：负金额、小数金额、空面额、重复面额

依赖：coin_loader / coin_validation / coin_verify
"""

from coin_loader import coin_greedy, coin_dp
from coin_validation import validate_all
from coin_verify import verify_result, verify_dp_optimal

# 正常用例：(说明, 面额, 金额, 期望DP枚数, 贪心是否同样最优)
NORMAL_CASES = [
    ("课堂案例：贪心失效",   [1, 5, 11],     15,  3,  False),
    ("经典反例[1,3,4]凑6",   [1, 3, 4],      6,   2,  False),
    ("美国面额：贪心有效",   [1, 5, 10, 25], 63,  6,  True),
    ("小面额体系[1,2,5]",    [1, 2, 5],      11,  3,  True),
    ("边界：金额 0",         [1, 5, 11],     0,   0,  True),
    ("边界：金额=最大面额",  [1, 5, 11],     11,  1,  True),
    ("边界：单种面额",       [7],            49,  7,  True),
    ("较大金额（预算800）",  [1, 5, 11],     800, 76, True),
]

# 异常用例：(说明, 面额, 金额, 期望抛出的异常类型, 测试目标)
ERROR_CASES = [
    ("真正无解[5,11]凑3", [5, 11], 3,  ValueError, "dp"),       # 由 DP 抛出
    ("必定无解[2,4]凑7",  [2, 4],  7,  ValueError, "validate"), # 被校验提前拦截
    ("负数金额",          [1, 5],  -5, ValueError, "validate"),
    ("小数金额",          [1, 5],  2.5, TypeError,  "validate"),
    ("空面额列表",        [],      10, ValueError, "validate"),
    ("重复面额",          [1, 1],  10, ValueError, "validate"),
]


def run_normal_cases():
    """跑正常用例，返回 (通过数, 总数)"""
    passed = 0
    for name, coins, amount, expect_dp, greedy_optimal in NORMAL_CASES:
        # 先过输入校验，再跑两种算法
        validate_all(coins, amount)
        g_count, g_combo = coin_greedy(amount, coins)
        d_count, d_combo = coin_dp(amount, coins)

        # 输出合法性校验
        verify_result(coins, amount, g_count, g_combo)
        verify_result(coins, amount, d_count, d_combo)

        # 断言 1：DP 枚数符合预期
        assert d_count == expect_dp, f"期望 DP {expect_dp} 枚，实际 {d_count} 枚"
        # 断言 2：贪心是否最优与预期一致（验证"贪心失效/有效"的判断）
        assert (g_count == d_count) == greedy_optimal, \
            f"贪心 {g_count} 枚 vs DP {d_count} 枚，与预期（贪心最优={greedy_optimal}）不符"
        # 断言 3：小金额交叉验证 DP 全局最优
        verify_dp_optimal(coins, amount)

        tag = "贪心同样最优" if greedy_optimal else f"贪心失效（多花 {g_count - d_count} 枚）"
        print(f"  [通过] {name}：DP={d_count} 枚，贪心={g_count} 枚，{tag}")
        passed += 1
    return passed, len(NORMAL_CASES)


def run_error_cases():
    """跑异常用例，返回 (通过数, 总数)"""
    passed = 0
    for name, coins, amount, expect_exc, target in ERROR_CASES:
        try:
            if target == "validate":
                validate_all(coins, amount)
            else:
                coin_dp(amount, coins)
        except expect_exc as e:
            print(f"  [通过] {name}：按预期抛出 {type(e).__name__}（{e}）")
            passed += 1
        else:
            raise AssertionError(f"{name}：本应抛出 {expect_exc.__name__} 却没有抛出")
    return passed, len(ERROR_CASES)


def main():
    print("【测试用例套件】")
    print("-- 正常用例 --")
    p1, t1 = run_normal_cases()
    print("-- 异常用例 --")
    p2, t2 = run_error_cases()
    print(f"\n汇总：正常 {p1}/{t1} 通过，异常 {p2}/{t2} 通过，全部 {'通过' if p1 + p2 == t1 + t2 else '未通过'}")


if __name__ == "__main__":
    main()
