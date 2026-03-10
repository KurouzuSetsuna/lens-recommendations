#!/usr/bin/env python3
"""
レンズを削除する対話型スクリプト
"""

import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / 'data' / 'lenses.json'


def load_lenses():
    """既存のレンズデータを読み込み"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_lenses(lenses):
    """レンズデータを保存（バックアップも作成）"""
    # バックアップを作成
    backup_file = PROJECT_ROOT / 'data' / f'lenses_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        backup_data = f.read()
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(backup_data)
    print(f'[INFO] バックアップを作成: {backup_file.name}')

    # 保存
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(lenses, f, ensure_ascii=False, indent=2)
    print('[SUCCESS] lenses.jsonを更新しました')


def remove_lens():
    """レンズを削除"""
    print("\n" + "="*60)
    print("レンズ削除")
    print("="*60)

    # 既存データを読み込み
    lenses = load_lenses()

    if not lenses:
        print("[INFO] 削除するレンズがありません")
        return

    # 一覧表示
    print(f"\n現在のレンズ数: {len(lenses)}件\n")
    for i, lens in enumerate(lenses, 1):
        print(f"{i}. {lens['name']}")
        print(f"   ID: {lens['id']} | {lens['brand']} | {lens['mount']}")

    # 削除する番号を選択
    print("\n削除するレンズの番号を入力（0でキャンセル）:")
    while True:
        try:
            choice = int(input("番号: ").strip())
            if choice == 0:
                print("[INFO] キャンセルしました")
                return
            if 1 <= choice <= len(lenses):
                break
            print(f"[ERROR] 1〜{len(lenses)}の範囲で入力してください")
        except ValueError:
            print("[ERROR] 数字を入力してください")

    # 選択されたレンズ
    selected_lens = lenses[choice - 1]

    # 確認
    print("\n" + "="*60)
    print("削除確認")
    print("="*60)
    print(f"製品名: {selected_lens['name']}")
    print(f"ID: {selected_lens['id']}")
    print(f"メーカー: {selected_lens['brand']}")
    print(f"ASIN: {selected_lens['asin']}")
    print("="*60)

    confirm = input("\nこのレンズを削除しますか？ (y/n): ").strip().lower()
    if confirm != 'y':
        print("[INFO] 削除をキャンセルしました")
        return

    # 削除
    removed_lens = lenses.pop(choice - 1)
    save_lenses(lenses)

    print(f"\n[SUCCESS] {removed_lens['name']} を削除しました")
    print(f"[INFO] 残りのレンズ数: {len(lenses)}件")
    print("\n次のステップ:")
    print("  1. git add data/lenses.json")
    print(f"  2. git commit -m \"Remove lens: {removed_lens['name']}\"")
    print("  3. git push origin master")


def main():
    print("="*60)
    print("レンズ削除ツール - Photo Gear Guide")
    print("="*60)

    try:
        remove_lens()
    except KeyboardInterrupt:
        print("\n\n[INFO] 中断されました")
    except Exception as e:
        print(f"\n[ERROR] エラーが発生しました: {e}")


if __name__ == '__main__':
    main()
