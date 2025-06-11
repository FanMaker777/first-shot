"""ゲーム起動用エントリーポイント。

このモジュールを ``python main.py`` として実行した場合でも、
プロジェクト直下の ``firstshot`` パッケージを正しくインポートできる
ように ``sys.path`` を調整する。
"""

from __future__ import annotations

import os
import sys


def _setup_module_path() -> None:
    """モジュール探索パスを調整する補助関数。"""

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)


def main() -> None:
    """ゲームを起動する。"""

    _setup_module_path()
    from firstshot.game import Game

    Game()


if __name__ == "__main__":
    main()
