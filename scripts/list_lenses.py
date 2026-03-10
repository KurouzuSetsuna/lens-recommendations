#!/usr/bin/env python3
"""
既存のレンズ一覧を表示するスクリプト
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / 'data' / 'lenses.json'


def load_lenses():
    """既存のレンズデータを読み込み"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def list_lenses():
    """レンズ一覧を表示"""
    lenses = load_lenses()

    print("="*80)
    print(f"登録レンズ一覧 - 全{len(lenses)}件")
    print("="*80)

    for i, lens in enumerate(lenses, 1):
        print(f"\n{i}. {lens['name']}")
        print(f"   ID: {lens['id']}")
        print(f"   メーカー: {lens['brand']} | マウント: {lens['mount']}")
        print(f"   焦点距離: {lens['focal_length']} | 絞り: {lens['aperture']} | 重量: {lens['weight']}g")
        print(f"   ASIN: {lens['asin']}")
        print(f"   説明: {lens['description'][:60]}...")
        if lens.get('features'):
            print(f"   特徴: {', '.join(lens['features'][:3])}")
        if lens.get('suitable_for'):
            print(f"   適用: {', '.join(lens['suitable_for'][:5])}")

    print("\n" + "="*80)


def main():
    try:
        list_lenses()
    except Exception as e:
        print(f"[ERROR] エラーが発生しました: {e}")


if __name__ == '__main__':
    main()
