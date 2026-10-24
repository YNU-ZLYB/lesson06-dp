# -*- coding: utf-8 -*-
"""
【模块功能】总入口
按顺序一键串联所有功能模块，方便整体检查与课堂演示：
  1. coin_validation  —— 输入校验与边界异常处理演示
  2. coin_test_cases  —— 测试用例套件（含结果验证断言）
  3. coin_verify      —— 结果验证演示
  4. coin_performance —— 性能对比表格
  5. coin_visualize   —— 复杂度 ASCII 可视化

说明：贪心 / DP 算法本体在 coin_change-SOLO.py、coin_change-IDE.py 中已完成，
本入口不重复实现，只负责组织调用各补充模块。
"""

import coin_validation
import coin_test_cases
import coin_verify
import coin_performance
import coin_visualize


def main():
    print("=" * 64)
    print("模块 1/5：输入校验与边界异常处理")
    print("=" * 64)
    coin_validation.main()

    print("\n" + "=" * 64)
    print("模块 2/5：测试用例套件")
    print("=" * 64)
    coin_test_cases.main()

    print("\n" + "=" * 64)
    print("模块 3/5：运行结果验证")
    print("=" * 64)
    coin_verify.main()

    print("\n" + "=" * 64)
    print("模块 4/5：性能对比分析")
    print("=" * 64)
    coin_performance.main()

    print("\n" + "=" * 64)
    print("模块 5/5：复杂度对比可视化")
    print("=" * 64)
    coin_visualize.main()

    print("\n全部模块运行完毕。")


if __name__ == "__main__":
    main()
