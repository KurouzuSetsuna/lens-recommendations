# Photo Gear Guide - フォト機材ガイド

カメラレンズと撮影ジャンル別のおすすめ機材を紹介する静的サイト生成システムです。GitHub Pagesで公開し、Amazonアフィリエイトリンクを設置しています。

## 特徴

- 📸 レンズ詳細ページの自動生成
- 🎯 ジャンル別（ストリート、ポートレート、風景）ページ
- 📝 Markdown記事管理
- 🔗 Amazonアフィリエイト対応
- 🚀 GitHub Actionsによる自動デプロイ
- 📱 レスポンシブデザイン
- ⚡ 軽量で高速な静的サイト
- 🔍 SEO最適化（sitemap.xml、robots.txt）

## 技術スタック

- **Python 3.11** - サイト生成エンジン
- **Jinja2** - HTMLテンプレートエンジン
- **Markdown** - 記事管理
- **HTML/CSS/JavaScript** - フロントエンド
- **GitHub Actions** - CI/CD
- **GitHub Pages** - ホスティング

## プロジェクト構造

```
photo-gear-guide/
├── data/                    # JSONデータ
│   ├── lenses.json         # レンズ情報
│   ├── cameras.json        # カメラ情報
│   └── genres.json         # ジャンル情報
├── content/                 # Markdown記事
│   ├── lenses/             # レンズ記事
│   ├── genres/             # ジャンル記事
│   ├── learn/              # 学習記事
│   ├── samples/            # 作例記事
│   └── spots/              # 撮影スポット
├── templates/               # Jinja2テンプレート
│   ├── base.html           # 基本レイアウト
│   ├── lens.html           # レンズページ
│   ├── genre.html          # ジャンルページ
│   ├── article.html        # 記事ページ
│   └── index_page.html     # トップページ
├── assets/                  # 静的ファイル
│   ├── css/style.css       # スタイルシート
│   ├── js/main.js          # JavaScript
│   └── images/             # 画像
├── scripts/                 # 生成スクリプト
│   └── generate.py         # メインスクリプト
├── site/                    # 生成されたサイト
├── .github/workflows/       # GitHub Actions
│   └── deploy.yml          # デプロイワークフロー
└── requirements.txt         # Python依存関係
```

## セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/your-username/lens-recommendations.git
cd lens-recommendations
```

### 2. Python環境を準備

```bash
# 依存関係をインストール
pip install -r requirements.txt
```

### 3. Amazonアソシエイト IDを設定

GitHub Secretsに `AMAZON_ASSOCIATE_ID` を登録してください。

1. GitHubリポジトリの Settings → Secrets and variables → Actions
2. New repository secret をクリック
3. Name: `AMAZON_ASSOCIATE_ID`
4. Value: あなたのAmazonアソシエイトID（例: `yourtag-22`）
5. Add secret をクリック

### 4. GitHub Pagesを有効化

1. GitHubリポジトリの Settings → Pages
2. Source: `Deploy from a branch`
3. Branch: `gh-pages` / `/ (root)`
4. Save

## ローカルでの実行

### サイトを生成

```bash
python scripts/generate.py
```

生成されたHTMLは `site/` ディレクトリに出力されます。

### 環境変数を設定して実行

```bash
# Windows
set AMAZON_ASSOCIATE_ID=yourtag-22
python scripts/generate.py

# Linux/Mac
export AMAZON_ASSOCIATE_ID=yourtag-22
python scripts/generate.py
```

### ローカルサーバーで確認

```bash
cd site
python -m http.server 8000
```

ブラウザで `http://localhost:8000` を開いて確認できます。

## コンテンツの追加

### レンズ情報を追加

`data/lenses.json` にレンズ情報を追加してください。

```json
{
  "id": "lens-id",
  "name": "レンズ名",
  "brand": "メーカー名",
  "mount": "マウント名",
  "focal_length": "50mm",
  "aperture": "F1.8",
  "weight": 186,
  "asin": "AmazonのASINコード",
  "description": "レンズの説明",
  "features": ["特徴1", "特徴2"],
  "suitable_for": ["street", "portrait"]
}
```

### ジャンル記事を追加

`content/genres/` にMarkdownファイルを作成してください。

```markdown
---
title: ジャンル名
description: 説明
genre_id: genre-slug
---

# ジャンル名

本文...
```

### 学習記事を追加

`content/learn/` にMarkdownファイルを作成してください。

```markdown
---
title: 記事タイトル
description: 説明
date: 2026-03-11
---

# 記事タイトル

本文...
```

## 自動デプロイ

GitHub Actionsにより、以下のタイミングで自動的にサイトが更新されます。

- 毎日午前3時（UTC）
- mainブランチへのpush時
- 手動実行（workflow_dispatch）

## SEO対策

以下のSEO対策を実装しています。

- タイトルタグの最適化
- メタディスクリプション
- 適切な見出し構造（h1, h2, h3）
- 内部リンク
- sitemap.xml 自動生成
- robots.txt 自動生成
- レスポンシブデザイン
- 高速読み込み

## ページ種類

生成されるページ：

- **トップページ** (`/`) - 人気レンズ、ジャンル、学習記事の紹介
- **レンズページ** (`/lenses/{id}/`) - 各レンズの詳細情報
- **レンズ一覧** (`/lenses/`) - すべてのレンズ一覧
- **ジャンルページ** (`/genres/{slug}/`) - 撮影ジャンル別おすすめレンズ
- **学習記事** (`/learn/{slug}/`) - レンズや撮影テクニックの解説

## Amazonアフィリエイト規約の遵守

本サイトは以下のAmazonアソシエイトプログラムの規約を遵守しています。

- 価格の固定表示なし
- アフィリエイトリンクであることの明示
- 適切な免責事項の記載

## カスタマイズ

### CSSの編集

`assets/css/style.css` を編集してデザインをカスタマイズできます。

### テンプレートの編集

`templates/` 内のJinja2テンプレートを編集してレイアウトを変更できます。

### サイトURLの変更

`scripts/generate.py` の以下の部分を編集してください。

```python
base_url = 'https://your-username.github.io/lens-recommendations'
```

## トラブルシューティング

### ビルドエラーが発生する

依存関係が正しくインストールされているか確認してください。

```bash
pip install -r requirements.txt
```

### GitHub Pagesで表示されない

1. GitHub Actions のワークフローが正常に完了しているか確認
2. Settings → Pages でgh-pagesブランチが選択されているか確認
3. 数分待ってからアクセス

### Amazonリンクにタグが付かない

GitHub Secretsに `AMAZON_ASSOCIATE_ID` が正しく設定されているか確認してください。

## ライセンス

MIT License

## 今後の拡張予定

- カメラボディ紹介ページ
- 作例ギャラリー
- 撮影スポット紹介
- ユーザーレビュー機能
- 比較表機能
- 検索機能

## 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずissueを開いて変更内容を議論してください。

## お問い合わせ

質問や提案がある場合は、GitHubのIssuesでお知らせください。
