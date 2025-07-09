# excerpt-allpages-info
指定したWebサイトにある各種サブページの`title`,`当該ページのURLパス`を抽出する機能です。<br>
`utils/main.py`にある`website_scraping`の引数を調整することで任意のWebサイトから上記情報を抽出できます。<br>
- `website_scraping`の引数
  - 第一引数：`対象サイトのURL`<br>
  ※指定URLページ内にある`a`タグの`href`属性を基準に検出するのでTOPページを指定するのが無難
  - 第二引数（任意）：`検出対象ページ数`（デフォルト = 100件）
  - 第三引数（任意）：`検出対象は同一オリジン限定か他のドメインも含めるか`（デフォルト = `True` -> 同一オリジン限定）

```py
website_scraping_result = website_scraping("https://example-company.co.jp", 5)
```

> [!NOTE]
> Webスクレイピングするので実施サイトの選定には十分注意してください<br>
> 自身が管理または関係するサイト以外でのスクレイピング実施は迷惑行為であり犯罪行為に抵触する可能性もあります。

## ユースケース
- Web解析やリニューアル検討時に、対象サイトのページリストが欲しい場合
- 入力キーワードでフィルターされた（キーワードを含んだ）対象サイトのページリストが欲しい場合
- 対象サイトにおいて、外部リンクも網羅した全体のリンク経路を知りたい場合

## 使い方
### 仮想環境を構築（初回のみ）
ターミナル／コマンドプロンプトを開いてルート（ファイルの最上階層）にいる状態で以下フローを実行
```bash
mkdir venv # venv ディレクトリ（仮想環境ディレクトリ）を作成
cd venv    # 作成した仮想環境ディレクトリ（`venv`）へ移動

# 新しい仮想環境を作成してアクティベート
# WindowsOS の場合: python -m venv env
python3 -m venv env # env{は仮想環境名}

# WindowsOS の場合: env\Scripts\activate
source env/bin/activate

# 仮想環境をアクティベートした状態で、パス指定して`requirements.txt`から各種ライブラリをインストール
# `../requirements.txt`なのは`requirements.txt`がルート直下にあるため
pip install -r ../requirements.txt
```

> [!NOTE]
> インポートしたライブラリを`requirements.txt`に保存する場合は以下コマンドを実行
```bash
# 一階層前にある requirements.txt にライブラリ情報を保存
python -m pip freeze > ../requirements.txt
```

### 仮想環境を立ち上げる（初回以降）
```bash
# 1. 仮想環境を格納しているディレクトリへ移動（存在しない場合は上記を参照に新規作成）
cd venv

# 2. 仮想環境をアクティベート
# WindowsOS の場合: env\Scripts\activate
source env/bin/activate
```

### `utils`ディレクトリへ移動
必ず仮想環境をアクティベートした状態で以下フローを実行
```bash
# ※必要に応じて以下コマンドを実行
# 仮想環境をアクティベートした直後だと`venv`ディレクトリへいるためルートに移動する
cd ../

# `utils`ディレクトリへ移動
cd utils

# WindowsOS の場合:
# python main.py

python3 main.py
```
