# メインモジュール
# このモジュールを実行することでゲームを起動する
"""ゲーム起動用のエントリーポイント。

このスクリプトは ``python firstshot/main.py`` のように直接実行される
ことを想定している。カレントディレクトリに ``firstshot`` パッケージを
インストールしていない環境でも、親ディレクトリを ``sys.path`` に
追加することでモジュールのインポートエラーを回避する。
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from firstshot.game import Game

if __name__ == "__main__":
    # ゲームを開始する
    Game()
