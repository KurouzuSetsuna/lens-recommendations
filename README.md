# 50mmレンズおすすめサイト

50mm単焦点レンズのおすすめを紹介する静的サイト生成システムです。GitHub Pagesで公開し、Amazonアフィリエイトリンクを設置しています。

## 特徴

- 📦 JSONデータからHTML自動生成
- 🚀 GitHub Actionsによる自動デプロイ
- 📱 レスポンシブデザイン
- 🔗 Amazonアフィリエイトリンク対応
- ⚡ 軽量で高速な静的サイト

## プロジェクト構造

```
lens-recommendations/
├─ data/
│   └─ lenses.json          # レンズデータ
├─ scripts/
│   └─ generate.py          # HTML生成スクリプト
├─ templates/
│   └─ index.html           # HTMLテンプレート
├─ site/
│   └─ index.html           # 生成されたHTML
├─ .github/workflows/
│   └─ build.yml            # GitHub Actionsワークフロー
└─ README.md
```

## セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/your-username/lens-recommendations.git
cd lens-recommendations
```

### 2. Amazonアソシエイト IDを設定

GitHub Secretsに `AMAZON_ASSOCIATE_ID` を登録してください。

1. GitHubリポジトリの Settings → Secrets and variables → Actions
2. New repository secret をクリック
3. Name: `AMAZON_ASSOCIATE_ID`
4. Value: あなたのAmazonアソシエイトID（例: `yourtag-22`）

### 3. GitHub Pagesを有効化

1. GitHubリポジトリの Settings → Pages
2. Source: `Deploy from a branch`
3. Branch: `gh-pages` / `/ (root)`
4. Save

## ローカルでの実行

### HTMLを生成

```bash
python scripts/generate.py
```

生成されたHTMLは `site/index.html` に出力されます。

### 環境変数を設定して実行

```bash
# Windows
set AMAZON_ASSOCIATE_ID=yourtag-22
python scripts/generate.py

# Linux/Mac
export AMAZON_ASSOCIATE_ID=yourtag-22
python scripts/generate.py
```

## レンズデータの追加

`data/lenses.json` にレンズ情報を追加してください。

```json
{
  "name": "レンズ名",
  "brand": "メーカー名",
  "mount": "マウント名",
  "aperture": "F値",
  "weight": 重量（グラム）,
  "amazon_asin": "AmazonのASINコード",
  "description": "レンズの説明"
}
```

データを追加したら、GitHubにpushすると自動的にサイトが更新されます。

## 自動更新

GitHub Actionsにより、以下のタイミングで自動的にサイトが更新されます。

- 毎日午前3時（UTC）
- mainブランチへのpush時
- 手動実行（workflow_dispatch）

## SEO対策

以下の要素を含めています。

- タイトルタグの最適化
- メタディスクリプション
- 適切な見出しタグ（h1, h2）
- レスポンシブデザイン
- 高速読み込み

## Amazonアフィリエイト規約の遵守

本サイトは以下のAmazonアソシエイトプログラムの規約を遵守しています。

- 価格の固定表示なし
- アフィリエイトリンクであることの明示
- 適切な免責事項の記載

## ライセンス

MIT License

## 今後の拡張予定

- 35mm、85mmレンズのページ追加
- フィルター機能（マウント別、価格帯別）
- レビュー・評価機能
- 比較表の追加
- 画像ギャラリー機能

## 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずissueを開いて変更内容を議論してください。

## お問い合わせ

質問や提案がある場合は、GitHubのIssuesでお知らせください。
