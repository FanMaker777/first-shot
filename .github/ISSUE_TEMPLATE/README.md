# First Shot

Python製の縦スクロールシューティングゲームです。Pyxel と pygame を使って実装されており、数種類のシーンや敵キャラクター、プレイヤー育成要素を備えています。`firstshot/main.py` を実行するとゲームが起動します。

## ディレクトリ構成

- `firstshot/` – ゲーム本体のソースコード
  - `assets/` – 背景画像やBGMなどのリソース
  - `entities/` – プレイヤー・弾・敵などのエンティティクラス
  - `game_data/` – ゲーム設定や状態を管理するデータクラス
  - `logic/` – 衝突判定などのロジック
  - `scenes/` – タイトル画面やステージなど各シーンの処理
  - `main.py` – ゲーム起動用エントリポイント
- `tests/` – pytest 用のテストコード

## 実行方法

```bash
python firstshot/main.py
```

Pyxel・pygame などの依存ライブラリが必要です。詳細な実行環境は `requirements.txt` などを参照してください。

