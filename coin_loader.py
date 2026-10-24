# -*- coding: utf-8 -*-
"""
【模块功能】算法加载器
从项目已有的算法文件中动态加载已完成的贪心 / 动态规划实现，
为其他功能模块（校验、测试、验证、性能、可视化）提供统一调用接口。

说明：
- 算法文件改名为 coin_change_SOLO.py / coin_change_IDE.py 后，
  本模块用 importlib 按文件路径动态加载，避免依赖包导入结构。
- 本模块只做"加载与接口归一化"，不重复实现任何算法逻辑。
- 默认以 coin_change_IDE.py 为准（自带异常处理，组合用 {面额: 次数} 字典表示）。
"""

import importlib.util
from pathlib import Path

# 本文件所在目录，即项目根目录
BASE_DIR = Path(__file__).resolve().parent


def _load_module(file_name, module_name):
    """按文件路径动态加载一个 .py 文件，返回模块对象"""
    path = BASE_DIR / file_name
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# 加载已完成的算法实现（module 级代码只有函数定义，加载无副作用）
_impl = _load_module("coin_change_IDE.py", "coin_change_ide")


def coin_greedy(amount, coins):
    """统一接口 - 贪心算法。返回 (枚数, {面额: 使用次数})"""
    return _impl.coin_greedy(amount, coins)


def coin_dp(amount, coins):
    """统一接口 - 动态规划。返回 (枚数, {面额: 使用次数})"""
    return _impl.coin_dp(amount, coins)


if __name__ == "__main__":
    # 自检：加载后简单调用一次，确认接口可用
    print("加载器自检：", coin_dp(15, [1, 5, 11]))
