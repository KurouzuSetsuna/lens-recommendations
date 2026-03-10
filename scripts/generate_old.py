#!/usr/bin/env python3
"""
50mmレンズおすすめサイト HTML生成スクリプト
"""

import json
import os
from datetime import datetime
from pathlib import Path


def load_lenses(json_path):
    """lenses.jsonを読み込む"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_amazon_link(asin, associate_id=None):
    """Amazonアフィリエイトリンクを生成"""
    base_url = f"https://www.amazon.co.jp/dp/{asin}/"

    if associate_id:
        return f"{base_url}?tag={associate_id}"
    else:
        return base_url


def render_lens_card(lens, amazon_link):
    """個別のレンズカードHTMLを生成"""
    html = f"""
        <div class="lens">
            <h2>{lens['name']}</h2>

            <div class="lens-specs">
                <p><strong>ブランド:</strong> {lens['brand']}</p>
                <p><strong>マウント:</strong> {lens['mount']}</p>
                <p><strong>絞り:</strong> {lens['aperture']}</p>
                <p><strong>重量:</strong> {lens['weight']}g</p>
            </div>

            <p class="description">{lens['description']}</p>

            <a href="{amazon_link}" class="amazon-link" target="_blank" rel="noopener noreferrer">
                Amazonで見る
            </a>
        </div>
    """
    return html.strip()


def generate_html(lenses, template_path, output_path, associate_id=None):
    """HTMLページを生成"""

    # レンズカードを生成
    lens_cards = []
    for lens in lenses:
        amazon_link = create_amazon_link(lens['amazon_asin'], associate_id)
        card_html = render_lens_card(lens, amazon_link)
        lens_cards.append(card_html)

    # カードを結合
    lens_list_html = '\n'.join(lens_cards)

    # テンプレートを読み込み
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # 現在の日付を取得
    update_date = datetime.now().strftime('%Y年%m月%d日')

    # テンプレートに埋め込み
    html = template.replace('{{LENS_LIST}}', lens_list_html)
    html = html.replace('{{UPDATE_DATE}}', update_date)

    # 出力ディレクトリを作成
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # HTMLを出力
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"[SUCCESS] HTMLを生成しました: {output_path}")
    print(f"[INFO] {len(lenses)}個のレンズを掲載")


def main():
    """メイン処理"""
    # プロジェクトルートディレクトリを取得
    project_root = Path(__file__).parent.parent

    # パスを設定
    data_path = project_root / 'data' / 'lenses.json'
    template_path = project_root / 'templates' / 'index.html'
    output_path = project_root / 'site' / 'index.html'

    # 環境変数からアフィリエイトIDを取得（オプション）
    associate_id = os.environ.get('AMAZON_ASSOCIATE_ID')

    if associate_id:
        print(f"[INFO] Amazonアソシエイト ID: {associate_id}")
    else:
        print("[WARNING] AMAZON_ASSOCIATE_ID が設定されていません。通常のAmazonリンクを使用します。")

    # レンズデータを読み込み
    lenses = load_lenses(data_path)
    print(f"[INFO] {len(lenses)}個のレンズデータを読み込みました")

    # HTMLを生成
    generate_html(lenses, template_path, output_path, associate_id)

    print("\n[SUCCESS] 生成完了!")


if __name__ == '__main__':
    main()
