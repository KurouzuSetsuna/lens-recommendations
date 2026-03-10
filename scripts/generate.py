#!/usr/bin/env python3
"""
Photo Gear Guide - サイト生成メインスクリプト
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import markdown
import re

# プロジェクトルート
PROJECT_ROOT = Path(__file__).parent.parent

# パス設定
DATA_DIR = PROJECT_ROOT / 'data'
CONTENT_DIR = PROJECT_ROOT / 'content'
TEMPLATES_DIR = PROJECT_ROOT / 'templates'
ASSETS_DIR = PROJECT_ROOT / 'assets'
SITE_DIR = PROJECT_ROOT / 'site'


class SiteGenerator:
    """サイト生成クラス"""

    def __init__(self):
        self.lenses = []
        self.genres = []
        self.cameras = []
        self.associate_id = os.environ.get('AMAZON_ASSOCIATE_ID')

        # Jinja2環境を初期化
        self.jinja_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

        # Markdownパーサーを初期化
        self.md = markdown.Markdown(extensions=['meta', 'fenced_code', 'tables'])

    def load_data(self):
        """JSONデータを読み込み"""
        print('[INFO] データ読み込み中...')

        with open(DATA_DIR / 'lenses.json', 'r', encoding='utf-8') as f:
            self.lenses = json.load(f)

        with open(DATA_DIR / 'genres.json', 'r', encoding='utf-8') as f:
            self.genres = json.load(f)

        with open(DATA_DIR / 'cameras.json', 'r', encoding='utf-8') as f:
            self.cameras = json.load(f)

        print(f'[INFO] レンズ: {len(self.lenses)}件')
        print(f'[INFO] ジャンル: {len(self.genres)}件')
        print(f'[INFO] カメラ: {len(self.cameras)}件')

    def create_amazon_link(self, asin):
        """Amazonアフィリエイトリンクを生成"""
        base_url = f"https://www.amazon.co.jp/dp/{asin}/"
        if self.associate_id:
            return f"{base_url}?tag={self.associate_id}"
        return base_url

    def prepare_site_dir(self):
        """siteディレクトリを準備"""
        print('[INFO] siteディレクトリを準備中...')

        # siteディレクトリをクリア
        if SITE_DIR.exists():
            shutil.rmtree(SITE_DIR)

        # ディレクトリ構造を作成
        (SITE_DIR / 'lenses').mkdir(parents=True, exist_ok=True)
        (SITE_DIR / 'genres').mkdir(parents=True, exist_ok=True)
        (SITE_DIR / 'learn').mkdir(parents=True, exist_ok=True)
        (SITE_DIR / 'samples').mkdir(parents=True, exist_ok=True)

        # assetsをコピー
        shutil.copytree(ASSETS_DIR, SITE_DIR / 'assets')

        print('[INFO] ディレクトリ準備完了')

    def build_index(self):
        """トップページを生成"""
        print('[INFO] トップページ生成中...')

        template = self.jinja_env.get_template('index_page.html')

        html = template.render(
            current_page='home',
            popular_lenses=self.lenses[:6],  # 人気レンズ6件
            genres=self.genres,
            recent_articles=[
                {'title': '50mmレンズとは？', 'url': '/learn/what-is-50mm/', 'description': '標準単焦点レンズの魅力を徹底解説'}
            ]
        )

        with open(SITE_DIR / 'index.html', 'w', encoding='utf-8') as f:
            f.write(html)

        print('[SUCCESS] トップページ生成完了')

    def build_lens_pages(self):
        """レンズページを生成"""
        print('[INFO] レンズページ生成中...')

        template = self.jinja_env.get_template('lens.html')

        for lens in self.lenses:
            # レンズ詳細ページ
            lens_dir = SITE_DIR / 'lenses' / lens['id']
            lens_dir.mkdir(parents=True, exist_ok=True)

            # 同じマウントの関連レンズを取得
            related_lenses = [
                l for l in self.lenses
                if l['mount'] == lens['mount'] and l['id'] != lens['id']
            ][:3]

            amazon_url = self.create_amazon_link(lens['asin'])

            html = template.render(
                current_page='lenses',
                lens=lens,
                amazon_url=amazon_url,
                related_lenses=related_lenses
            )

            with open(lens_dir / 'index.html', 'w', encoding='utf-8') as f:
                f.write(html)

        # レンズ一覧ページ
        self.build_lens_list()

        print(f'[SUCCESS] {len(self.lenses)}件のレンズページ生成完了')

    def build_lens_list(self):
        """レンズ一覧ページを生成"""
        template = self.jinja_env.get_template('index_page.html')

        html = template.render(
            current_page='lenses',
            popular_lenses=self.lenses,
            genres=[],
            recent_articles=[]
        )

        with open(SITE_DIR / 'lenses' / 'index.html', 'w', encoding='utf-8') as f:
            f.write(html)

    def build_genre_pages(self):
        """ジャンルページを生成"""
        print('[INFO] ジャンルページ生成中...')

        template = self.jinja_env.get_template('genre.html')

        for genre in self.genres:
            genre_dir = SITE_DIR / 'genres' / genre['slug']
            genre_dir.mkdir(parents=True, exist_ok=True)

            # ジャンルのMarkdownファイルを読み込み
            md_path = CONTENT_DIR / 'genres' / f"{genre['slug']}.md"
            content_html = ''

            if md_path.exists():
                with open(md_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    content_html = self.md.convert(content)
                    self.md.reset()

            # おすすめレンズを取得
            recommended_lenses = [
                lens for lens in self.lenses
                if lens['id'] in genre.get('recommended_lenses', [])
            ]

            # 関連ジャンル
            related_genres = [g for g in self.genres if g['id'] != genre['id']][:2]

            html = template.render(
                current_page='genres',
                genre=genre,
                content=content_html,
                recommended_lenses=recommended_lenses,
                related_genres=related_genres
            )

            with open(genre_dir / 'index.html', 'w', encoding='utf-8') as f:
                f.write(html)

        print(f'[SUCCESS] {len(self.genres)}件のジャンルページ生成完了')

    def build_learn_pages(self):
        """学習記事ページを生成"""
        print('[INFO] 学習記事ページ生成中...')

        template = self.jinja_env.get_template('article.html')
        learn_dir = CONTENT_DIR / 'learn'

        if not learn_dir.exists():
            print('[WARNING] learn ディレクトリが存在しません')
            return

        article_count = 0
        for md_file in learn_dir.glob('*.md'):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # メタデータを抽出
            html_content = self.md.convert(content)
            meta = self.md.Meta if hasattr(self.md, 'Meta') else {}
            self.md.reset()

            title = meta.get('title', [md_file.stem])[0]
            description = meta.get('description', [''])[0]
            date = meta.get('date', [''])[0]

            # 出力ディレクトリを作成
            article_dir = SITE_DIR / 'learn' / md_file.stem
            article_dir.mkdir(parents=True, exist_ok=True)

            html = template.render(
                current_page='learn',
                title=title,
                description=description,
                date=date,
                content=html_content,
                related_articles=[]
            )

            with open(article_dir / 'index.html', 'w', encoding='utf-8') as f:
                f.write(html)

            article_count += 1

        print(f'[SUCCESS] {article_count}件の学習記事生成完了')

    def build_sitemap(self):
        """サイトマップを生成"""
        print('[INFO] サイトマップ生成中...')

        base_url = 'https://your-username.github.io/lens-recommendations'
        urls = []

        # トップページ
        urls.append(f"{base_url}/")

        # レンズページ
        for lens in self.lenses:
            urls.append(f"{base_url}/lenses/{lens['id']}/")

        # ジャンルページ
        for genre in self.genres:
            urls.append(f"{base_url}/genres/{genre['slug']}/")

        # 学習記事
        learn_dir = CONTENT_DIR / 'learn'
        if learn_dir.exists():
            for md_file in learn_dir.glob('*.md'):
                urls.append(f"{base_url}/learn/{md_file.stem}/")

        # sitemap.xmlを生成
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

        for url in urls:
            sitemap += '  <url>\n'
            sitemap += f'    <loc>{url}</loc>\n'
            sitemap += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
            sitemap += '  </url>\n'

        sitemap += '</urlset>'

        with open(SITE_DIR / 'sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(sitemap)

        print('[SUCCESS] サイトマップ生成完了')

    def build_robots_txt(self):
        """robots.txtを生成"""
        print('[INFO] robots.txt生成中...')

        robots = """User-agent: *
Allow: /

Sitemap: https://your-username.github.io/lens-recommendations/sitemap.xml
"""

        with open(SITE_DIR / 'robots.txt', 'w', encoding='utf-8') as f:
            f.write(robots)

        print('[SUCCESS] robots.txt生成完了')

    def generate(self):
        """サイト全体を生成"""
        print('\n=== Photo Gear Guide サイト生成開始 ===\n')

        if self.associate_id:
            print(f'[INFO] Amazon Associate ID: {self.associate_id}')
        else:
            print('[WARNING] AMAZON_ASSOCIATE_ID が設定されていません')

        self.load_data()
        self.prepare_site_dir()
        self.build_index()
        self.build_lens_pages()
        self.build_genre_pages()
        self.build_learn_pages()
        self.build_sitemap()
        self.build_robots_txt()

        print('\n=== サイト生成完了 ===\n')
        print(f'[INFO] 出力先: {SITE_DIR}')


def main():
    generator = SiteGenerator()
    generator.generate()


if __name__ == '__main__':
    main()
