"""ゲーム終了確認ダイアログの表示機能を提供するモジュール。

ユーザーがゲーム終了を試みた際に、確認ダイアログを表示して処理を分岐させる。
Pyxel 側でウィンドウを生成しているため ``tkinter`` とは直接連携せず、
一時的に ``Tk()`` を生成してメッセージボックスのみ利用する。
"""

import pyxel
import tkinter as tk
from tkinter import messagebox

from firstshot.constants import EXIT_DIALOG_TITLE, EXIT_DIALOG_MESSAGE


# ゲーム終了確認のダイアログを表示
def display_exit_dialog(game):
    """終了確認ダイアログを表示してゲーム終了処理を行う。

    Args:
        game: ゲーム全体の状態を保持する ``Game`` オブジェクト。 ``game.data``
            から終了フラグを更新する。

    Returns:
        None
    """

    # ── 1. ルートウィンドウを作ってすぐに隠す ──
    root = tk.Tk()
    root.withdraw()
    try:
        # ── 2. 確認ダイアログを出す ──
        #   askyesno は True/False を返す
        result = messagebox.askyesno(
            title=EXIT_DIALOG_TITLE,
            message=EXIT_DIALOG_MESSAGE,
            parent=root,
        )
    finally:
        # ── 3. ダイアログが閉じたら root を完全に破棄 ──
        root.destroy()

    # ── 4. 結果に応じて処理 ──
    if  result:
        # 「はい」を押された → Pyxel を終了
        pyxel.quit()
    else:
        # 「いいえ」を押された → 確認モードを解除してゲームに戻る
        game.data.is_exit_mode = False