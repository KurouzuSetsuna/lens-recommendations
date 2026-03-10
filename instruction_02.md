# ClaudeCode用 完全プロンプト

## フォト系アフィリエイトサイト自動生成（GitHub Pages）

以下の指示に従って、
**GitHub Pagesで公開する静的フォト系アフィリエイトサイト**を構築してください。

目的は **月10万円のアフィリエイト収益を狙うSEOサイト**です。

---

# 要件

以下をすべて実装してください。

* 静的サイト
* GitHub Pages公開
* Pythonでサイト自動生成
* Markdown記事管理
* SEO構造
* Amazonアフィリエイト対応

---

# 技術構成

使用技術

* Python
* Jinja2
* Markdown
* HTML/CSS
* GitHub Actions

---

# ディレクトリ構成

以下の構成でプロジェクトを作成してください。

```
photo-gear-guide
│
├ README.md
├ requirements.txt
│
├ data
│   ├ lenses.json
│   ├ cameras.json
│   └ genres.json
│
├ content
│   ├ lenses
│   ├ genres
│   ├ learn
│   ├ samples
│   └ spots
│
├ templates
│   ├ base.html
│   ├ lens.html
│   ├ genre.html
│   ├ article.html
│   └ sample.html
│
├ assets
│   ├ css
│   │   └ style.css
│   ├ js
│   │   └ main.js
│   └ images
│
├ scripts
│   ├ generate.py
│   ├ build_lens_pages.py
│   ├ build_sample_pages.py
│   └ build_index.py
│
├ site
│
└ .github
    └ workflows
        └ deploy.yml
```

---

# データ構造

## lenses.json

```
[
 {
  "name": "Sony FE 50mm F1.8",
  "brand": "Sony",
  "mount": "Sony E",
  "focal_length": "50mm",
  "aperture": "F1.8",
  "weight": 186,
  "asin": "B01MZ8S0WJ"
 }
]
```

---

# Markdown記事

すべてMarkdownで管理。

例

```
content/lenses/50mm.md
content/genres/street.md
content/samples/50mm-street.md
content/learn/focal-length-guide.md
```

---

# ページ種類

生成するページ

### トップページ

```
/
```

内容

* 人気記事
* 人気レンズ
* 作例リンク

---

### レンズページ

```
/lenses/50mm
/lenses/35mm
/lenses/85mm
```

内容

* レンズ説明
* 作例リンク
* Amazonリンク

---

### ジャンルページ

```
/genres/street
/genres/portrait
/genres/landscape
```

---

### 作例ページ

```
/samples/50mm-street
/samples/50mm-portrait
```

---

### 学習記事

```
/learn/what-is-50mm
/learn/focal-length-guide
```

---

# HTMLテンプレート仕様

テンプレートは **Jinja2** を使用する。

## base.html

共通レイアウト

```
<header>
<nav>
Home
Lenses
Genres
Learn
</nav>
</header>

<main>
{{ content }}
</main>

<footer>
Photo Gear Guide
</footer>
```

---

# Amazonアフィリエイトリンク

リンク形式

```
https://www.amazon.co.jp/dp/{ASIN}/?tag={ASSOCIATE_ID}
```

レンズページでは自動生成する。

---

# Pythonサイト生成

## generate.py

以下の処理を行う。

1 data読み込み
2 markdown読み込み
3 htmlテンプレート適用
4 siteフォルダへ出力

---

# Python仕様

使用ライブラリ

```
jinja2
markdown
```

---

# GitHub Actions

自動デプロイを設定。

```
.github/workflows/deploy.yml
```

処理

1 リポジトリ取得
2 Pythonセットアップ
3 generate.py実行
4 siteフォルダ生成
5 GitHub Pagesへデプロイ

---

# CSS

ミニマルデザイン。

要件

* モバイル対応
* 読みやすいタイポグラフィ
* シンプルUI
* 高速表示

---

# SEO要件

必須

```
titleタグ
meta description
h1 h2構造
内部リンク
```

URL構造

```
/lenses/50mm
/genres/street
/samples/50mm-street
/learn/what-is-50mm
```

---

# 追加機能

実装してください

* サイトマップ生成
* robots.txt
* 内部リンク自動生成
* 関連記事表示

---

# 生成されるサイト

```
site/
 ├ index.html
 ├ lenses/
 ├ genres/
 ├ samples/
 └ learn/
```

---

# サンプル記事も生成する

以下の記事を自動生成してください。

レンズ

```
50mmレンズおすすめ
35mmレンズおすすめ
85mmレンズおすすめ
```

ジャンル

```
ストリートスナップ
ポートレート撮影
風景写真
```

---

# 最終目標

このサイトは以下の流れで収益化する。

```
検索流入
↓
作例記事
↓
レンズ紹介
↓
Amazonアフィリエイト
```

---

# 出力

以下をすべて出力してください。

1 完全なディレクトリ構造
2 Pythonコード
3 HTMLテンプレート
4 CSS
5 GitHub Actions
6 サンプル記事

**すぐにGitHubへPushできる完成状態で生成してください。**

