# 50mmレンズおすすめサイト 自動生成システム設計書

## 概要

本プロジェクトは **50mmレンズのおすすめ一覧サイト** を自動生成し、
**GitHub Pages** に公開する静的サイト生成システムである。

商品情報をデータファイルから読み込み、
HTMLページを生成する。

生成されたページには **Amazonアフィリエイトリンク** を設置する。

更新は **GitHub Actions** により自動化する。

---

# システム構成

```
Repository
│
├─ data/
│   └─ lenses.json
│
├─ scripts/
│   └─ generate.py
│
├─ templates/
│   └─ index.html
│
├─ site/
│   └─ (生成されたHTML)
│
├─ .github/workflows/
│   └─ build.yml
│
└─ README.md
```

---

# データ仕様

## lenses.json

50mmレンズ情報を管理する。

```
[
  {
    "name": "Sony FE 50mm F1.8",
    "brand": "Sony",
    "mount": "Sony E",
    "aperture": "F1.8",
    "weight": 186,
    "amazon_asin": "B01MZ8S0WJ",
    "description": "軽量で安価な標準単焦点レンズ"
  },
  {
    "name": "Sigma 50mm F1.4 DG DN Art",
    "brand": "Sigma",
    "mount": "Sony E",
    "aperture": "F1.4",
    "weight": 670,
    "amazon_asin": "B0XXXXXXX",
    "description": "高解像度のArtラインレンズ"
  }
]
```

---

# Amazonアフィリエイトリンク生成

Amazonリンクは以下の形式で生成する。

```
https://www.amazon.co.jp/dp/{ASIN}/?tag={ASSOCIATE_ID}
```

例

```
https://www.amazon.co.jp/dp/B01MZ8S0WJ/?tag=yourtag-22
```

`ASSOCIATE_ID` は環境変数で管理する。

---

# HTMLテンプレート

templates/index.html

```
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>50mmレンズおすすめ</title>
</head>

<body>

<h1>おすすめ50mmレンズ</h1>

{{LENS_LIST}}

</body>
</html>
```

---

# レンズカードHTML

各レンズは以下形式で表示する。

```
<div class="lens">

<h2>{name}</h2>

<p>ブランド: {brand}</p>
<p>マウント: {mount}</p>
<p>絞り: {aperture}</p>
<p>重量: {weight}g</p>

<p>{description}</p>

<a href="{amazon_link}" target="_blank">
Amazonで見る
</a>

</div>
```

---

# HTML生成スクリプト

scripts/generate.py

処理フロー

```
1. lenses.json を読み込む
2. Amazonリンクを生成
3. HTMLカードを生成
4. index.htmlテンプレートに埋め込む
5. site/index.html に出力
```

疑似コード

```
load json

for lens in lenses:

  amazon_link = create_link(lens.asin)

  card = render_html(lens)

append cards

write index.html
```

---

# GitHub Actions

.github/workflows/build.yml

```
name: build

on:
  schedule:
    - cron: "0 3 * * *"

  workflow_dispatch:

jobs:

  build:

    runs-on: ubuntu-latest

    steps:

    - uses: actions/checkout@v3

    - name: setup python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11

    - name: generate site
      run: python scripts/generate.py

    - name: deploy
      uses: peaceiris/actions-gh-pages@v3
      with:
        publish_dir: ./site
        github_token: ${{ secrets.GITHUB_TOKEN }}
```

---

# GitHub Pages設定

GitHub Repository Settings

```
Pages
Source: gh-pages
```

---

# SEO

各ページには以下を含める

```
title
meta description
h1
```

例

```
<title>50mmレンズおすすめ | ストリートスナップ向け単焦点</title>
```

---

# 将来拡張

以下ページを追加可能

```
/35mm
/85mm
/portrait-lens
/street-snap-lens
```

データを増やすだけで自動生成される構造にする。

---

# 目標

このサイトは

```
50mm レンズ おすすめ
50mm 単焦点
標準レンズ おすすめ
```

などの検索流入を狙う。

---

# 完成イメージ

```
タイトル
↓
おすすめレンズ一覧
↓
各レンズ詳細
↓
Amazonリンク
```

---

# 注意

Amazonアフィリエイト規約により以下を遵守する。

・価格は固定表示しない
・画像はAPIまたは公式素材を使用
・アフィリエイトリンクであることを明示する

---

# ライセンス

MIT

