# 管理・メンテナンスガイド

Photo Gear Guide の定期更新とメンテナンス方法を説明します。

## 目次

- [レンズ管理ツール](#レンズ管理ツール)
- [月次メンテナンス](#月次メンテナンス)
- [更新フロー](#更新フロー)
- [トラブルシューティング](#トラブルシューティング)

---

## レンズ管理ツール

プロジェクトには3つの管理用スクリプトがあります。

### 1. レンズ一覧の表示

```bash
python scripts/list_lenses.py
```

**機能:**
- 登録済みレンズの一覧を表示
- ID、メーカー、マウント、ASIN などの情報を確認

**使用タイミング:**
- 新製品追加前に既存データを確認
- 削除対象を選ぶ前に一覧を確認

---

### 2. 新しいレンズの追加

```bash
python scripts/add_lens.py
```

**機能:**
- 対話形式で新しいレンズ情報を入力
- 自動でIDを生成
- ASIN形式の検証
- 入力内容の確認
- 自動バックアップ作成

**入力項目:**
1. 製品名（例: Sony FE 50mm F1.8）
2. ID（自動生成・編集可能）
3. メーカー（選択式）
4. マウント（選択式）
5. 焦点距離（選択式）
6. 開放F値（例: F1.8）
7. 重量（グラム）
8. Amazon ASIN（10文字）
9. 説明文
10. 特徴（最大5個）
11. 適したジャンル（複数選択可）

**ASINの確認方法:**
1. Amazonで商品ページを開く
2. URLの `/dp/` の後の10文字がASIN
3. 例: `https://www.amazon.co.jp/dp/B01MZ8S0WJ/` → `B01MZ8S0WJ`

**実行例:**
```bash
$ python scripts/add_lens.py

============================================================
レンズ追加ツール - Photo Gear Guide
============================================================

【基本情報】
製品名（例: Sony FE 50mm F1.8）: Sony FE 35mm F1.8
ID（自動生成） [sony-fe-35mm-f18]:
...
```

---

### 3. レンズの削除

```bash
python scripts/remove_lens.py
```

**機能:**
- 既存レンズの一覧表示
- 番号を選択して削除
- 削除前の確認
- 自動バックアップ作成

**使用タイミング:**
- 販売終了品の削除
- 在庫切れが長期化している商品の削除
- 誤って追加した商品の削除

---

## 月次メンテナンス

月に1回、以下のチェックを実施することを推奨します。

### チェックリスト

- [ ] **新製品の発売確認**
  - 各メーカーの公式サイトをチェック
  - カメラ系ニュースサイトを確認
  - 発売された製品を追加

- [ ] **在庫状況の確認**
  - Amazonで各商品の在庫をチェック
  - 長期在庫切れの商品を削除検討
  - 販売終了品を削除

- [ ] **価格変動のチェック**
  - 大幅な価格変動があれば説明文を調整
  - 「高価」「安価」などの表現を見直し

- [ ] **ASIN の有効性確認**
  - 商品ページが正しく表示されるか確認
  - 404エラーがあれば削除検討

### 推奨スケジュール

| タイミング | 作業内容 |
|----------|---------|
| **毎月1日** | 新製品発売情報の確認・追加 |
| **毎月15日** | 在庫・価格チェック |
| **四半期ごと** | 全商品の見直し・古い商品の削除 |

---

## 更新フロー

### 新製品を追加する場合

```bash
# 1. 既存のレンズを確認
python scripts/list_lenses.py

# 2. 新しいレンズを追加
python scripts/add_lens.py

# 3. ローカルでサイトを生成してテスト
python scripts/generate.py
cd site
python -m http.server 8000
# ブラウザで http://localhost:8000 を確認

# 4. 問題なければコミット
git add data/lenses.json
git commit -m "Add new lens: Sony FE 35mm F1.8"
git push origin master

# 5. GitHub Actionsが自動的にデプロイ（数分待つ）
```

### 古い製品を削除する場合

```bash
# 1. 既存のレンズを確認
python scripts/list_lenses.py

# 2. レンズを削除
python scripts/remove_lens.py

# 3. ローカルでサイトを生成してテスト
python scripts/generate.py

# 4. 問題なければコミット
git add data/lenses.json
git commit -m "Remove discontinued lens: Old Product Name"
git push origin master
```

### 一度に複数の変更を行う場合

```bash
# 1. 追加と削除を実施
python scripts/add_lens.py
python scripts/add_lens.py  # 複数回実行可能
python scripts/remove_lens.py

# 2. ローカルでテスト
python scripts/generate.py

# 3. まとめてコミット
git add data/lenses.json
git commit -m "Update lens database: add 2 new products, remove 1 discontinued"
git push origin master
```

---

## トラブルシューティング

### Q: スクリプト実行時にエラーが出る

**A:** Python依存関係を確認してください

```bash
pip install -r requirements.txt
```

### Q: バックアップファイルが大量にある

**A:** 古いバックアップを削除できます

```bash
# 30日以上前のバックアップを削除（Linux/Mac）
find data/ -name "lenses_backup_*.json" -mtime +30 -delete

# Windows
# data/フォルダで古いlenses_backup_*.jsonを手動削除
```

### Q: ASINが正しいか確認したい

**A:** ブラウザで以下のURLにアクセスして確認

```
https://www.amazon.co.jp/dp/{ASIN}/
```

商品ページが表示されればOKです。

### Q: 誤って削除してしまった

**A:** バックアップから復元できます

```bash
# data/ フォルダの中のバックアップファイルを確認
ls data/lenses_backup_*.json

# 最新のバックアップを復元
cp data/lenses_backup_20260311_120000.json data/lenses.json
```

### Q: GitHub Actionsがエラーになる

**A:** 以下を確認してください

1. lenses.json のJSON形式が正しいか
   ```bash
   python -m json.tool data/lenses.json
   ```

2. GitHub Secrets の `AMAZON_ASSOCIATE_ID` が設定されているか

3. Actionsタブでエラーログを確認

---

## データの整合性チェック

定期的にデータの整合性を確認することを推奨します。

```bash
# JSON形式の検証
python -m json.tool data/lenses.json > /dev/null && echo "OK" || echo "NG"

# レンズ数の確認
python -c "import json; print(f'Total: {len(json.load(open(\"data/lenses.json\")))}')"

# 重複IDのチェック
python -c "import json; data=json.load(open('data/lenses.json')); ids=[l['id'] for l in data]; print('重複あり' if len(ids)!=len(set(ids)) else 'OK')"
```

---

## ベストプラクティス

1. **定期更新を習慣化する**
   - カレンダーに予定を入れる
   - 月初の作業ルーティンに組み込む

2. **バックアップを確認する**
   - スクリプト実行後、バックアップが作成されているか確認

3. **ローカルテストを忘れずに**
   - `python scripts/generate.py` でサイトを生成
   - ブラウザで確認してからpush

4. **コミットメッセージを明確に**
   - 何を追加・削除したか分かりやすく記載
   - 例: "Add new lens: Sony FE 35mm F1.8"
   - 例: "Remove discontinued lens: Old Model X"

5. **Amazonアソシエイト規約を遵守**
   - 価格を固定表示しない
   - 在庫切れ商品を放置しない
   - アフィリエイトであることを明示（既に実装済み）

---

## 参考リンク

- [Amazonアソシエイト プログラム運営規約](https://affiliate.amazon.co.jp/help/operating/agreement)
- [GitHub Actions ドキュメント](https://docs.github.com/ja/actions)
- [Jinja2 ドキュメント](https://jinja.palletsprojects.com/)

---

質問や問題がある場合は、GitHubのIssuesで報告してください。
