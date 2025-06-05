import pyxel

from firstshot.constants import EXIT_DIALOG_TITLE, EXIT_DIALOG_MESSAGE


# ゲーム終了確認のダイアログを表示
def display_exit_dialog(game):
    """
    Eキーを押したときに呼ばれるメソッド。
    Tkinterで「本当に終了しますか？」ダイアログを出し、
    はいなら pyxel.quit()、いいえなら self.confirming を False に戻す。
    """
    # ── 1. 必要なときだけ Tkinter をインポート ──
    import tkinter as tk
    from tkinter import messagebox

    # ── 2. ルートウィンドウを作ってすぐに隠す ──
    root = tk.Tk()
    root.withdraw()

    # ── 3. 確認ダイアログを出す ──
    #   askyesno は True/False を返す
    result = messagebox.askyesno(
        title=EXIT_DIALOG_TITLE,
        message=EXIT_DIALOG_MESSAGE
    )

    # ── 4. ダイアログが閉じたら root を完全に破棄 ──
    root.destroy()

    # ── 5. 結果に応じて処理 ──
    if  result:
        # 「はい」を押された → Pyxel を終了
        pyxel.quit()
    else:
        # 「いいえ」を押された → 確認モードを解除してゲームに戻る
        game.is_exit_dialog = False