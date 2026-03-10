#!/usr/bin/env python3
"""
新しいレンズを追加する対話型スクリプト
"""

import json
import re
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


def generate_id(name):
    """製品名からIDを自動生成"""
    # 小文字に変換、スペースをハイフンに、記号を削除
    id_str = name.lower()
    id_str = re.sub(r'[^\w\s-]', '', id_str)
    id_str = re.sub(r'[\s]+', '-', id_str)
    return id_str


def validate_asin(asin):
    """ASINの形式を検証"""
    # ASINは10文字の英数字
    return bool(re.match(r'^[A-Z0-9]{10}$', asin.upper()))


def input_with_default(prompt, default=None):
    """デフォルト値付きの入力"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()


def select_from_list(prompt, options):
    """リストから選択"""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")

    while True:
        try:
            choice = int(input("番号を選択: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print(f"[ERROR] 1〜{len(options)}の範囲で入力してください")
        except ValueError:
            print("[ERROR] 数字を入力してください")


def input_features():
    """特徴を入力"""
    print("\n特徴を入力（最大5個、空白で終了）:")
    features = []
    for i in range(1, 6):
        feature = input(f"  特徴{i}: ").strip()
        if not feature:
            break
        features.append(feature)
    return features


def input_suitable_for():
    """適した撮影ジャンルを入力"""
    genres = ['street', 'portrait', 'landscape', 'sports', 'wildlife', 'macro', 'beginner', 'professional', 'low-light', 'travel', 'video']

    print("\n適した撮影ジャンルを選択（複数可、0で終了）:")
    for i, genre in enumerate(genres, 1):
        print(f"  {i}. {genre}")

    selected = []
    while True:
        try:
            choice = input("番号を選択（0で終了）: ").strip()
            if choice == '0':
                break
            choice_num = int(choice)
            if 1 <= choice_num <= len(genres):
                genre = genres[choice_num - 1]
                if genre not in selected:
                    selected.append(genre)
                    print(f"[INFO] {genre} を追加")
                else:
                    print(f"[WARNING] {genre} は既に追加されています")
            else:
                print(f"[ERROR] 1〜{len(genres)}の範囲で入力してください")
        except ValueError:
            print("[ERROR] 数字を入力してください")

    return selected


def add_new_lens():
    """新しいレンズを追加"""
    print("\n" + "="*60)
    print("新しいレンズを追加")
    print("="*60)

    # 既存データを読み込み
    lenses = load_lenses()
    existing_ids = [lens['id'] for lens in lenses]

    # 製品情報を入力
    print("\n【基本情報】")
    name = input("製品名（例: Sony FE 50mm F1.8）: ").strip()
    if not name:
        print("[ERROR] 製品名は必須です")
        return

    # IDを自動生成
    suggested_id = generate_id(name)
    lens_id = input_with_default("ID（自動生成）", suggested_id)

    # ID重複チェック
    if lens_id in existing_ids:
        print(f"[ERROR] ID '{lens_id}' は既に存在します")
        lens_id = input("別のIDを入力: ").strip()
        if lens_id in existing_ids:
            print("[ERROR] ID重複のため追加をキャンセルしました")
            return

    # メーカー
    brands = ['Sony', 'Canon', 'Nikon', 'Sigma', 'Tamron', 'Samyang', 'Viltrox', 'その他']
    brand = select_from_list("メーカーを選択", brands)
    if brand == 'その他':
        brand = input("メーカー名を入力: ").strip()

    # マウント
    mounts = ['Sony E', 'Canon RF', 'Canon EF', 'Nikon Z', 'Nikon F', 'Micro Four Thirds', 'Fujifilm X', 'その他']
    mount = select_from_list("マウントを選択", mounts)
    if mount == 'その他':
        mount = input("マウント名を入力: ").strip()

    # 焦点距離
    focal_lengths = ['35mm', '50mm', '85mm', '24mm', '105mm', 'その他']
    focal_length = select_from_list("焦点距離を選択", focal_lengths)
    if focal_length == 'その他':
        focal_length = input("焦点距離を入力（例: 40mm）: ").strip()

    # 開放F値
    aperture = input("開放F値（例: F1.8）: ").strip()
    if not aperture.startswith('F'):
        aperture = f"F{aperture}"

    # 重量
    while True:
        try:
            weight = int(input("重量（グラム、例: 186）: ").strip())
            break
        except ValueError:
            print("[ERROR] 数字を入力してください")

    # ASIN
    print("\n【Amazon情報】")
    print("ASINの確認方法:")
    print("  1. Amazonで商品ページを開く")
    print("  2. URLの /dp/ の後の10文字がASIN")
    print("  例: https://www.amazon.co.jp/dp/B01MZ8S0WJ/ → B01MZ8S0WJ")

    while True:
        asin = input("ASIN（10文字の英数字）: ").strip().upper()
        if validate_asin(asin):
            break
        print("[ERROR] ASINは10文字の英数字である必要があります")

    # 説明文
    print("\n【説明・特徴】")
    description = input("説明文: ").strip()

    # 特徴
    features = input_features()

    # 適したジャンル
    suitable_for = input_suitable_for()

    # 確認
    print("\n" + "="*60)
    print("入力内容の確認")
    print("="*60)
    print(f"ID: {lens_id}")
    print(f"製品名: {name}")
    print(f"メーカー: {brand}")
    print(f"マウント: {mount}")
    print(f"焦点距離: {focal_length}")
    print(f"開放F値: {aperture}")
    print(f"重量: {weight}g")
    print(f"ASIN: {asin}")
    print(f"説明: {description}")
    print(f"特徴: {', '.join(features)}")
    print(f"適したジャンル: {', '.join(suitable_for)}")
    print("="*60)

    confirm = input("\nこの内容で追加しますか？ (y/n): ").strip().lower()
    if confirm != 'y':
        print("[INFO] 追加をキャンセルしました")
        return

    # 新しいレンズオブジェクトを作成
    new_lens = {
        "id": lens_id,
        "name": name,
        "brand": brand,
        "mount": mount,
        "focal_length": focal_length,
        "aperture": aperture,
        "weight": weight,
        "asin": asin,
        "description": description,
        "features": features,
        "suitable_for": suitable_for
    }

    # 追加
    lenses.append(new_lens)
    save_lenses(lenses)

    print(f"\n[SUCCESS] {name} を追加しました！")
    print(f"[INFO] 現在のレンズ数: {len(lenses)}件")
    print("\n次のステップ:")
    print("  1. git add data/lenses.json")
    print(f'  2. git commit -m "Add new lens: {name}"')
    print("  3. git push origin master")


def main():
    print("="*60)
    print("レンズ追加ツール - Photo Gear Guide")
    print("="*60)

    try:
        add_new_lens()
    except KeyboardInterrupt:
        print("\n\n[INFO] 中断されました")
    except Exception as e:
        print(f"\n[ERROR] エラーが発生しました: {e}")


if __name__ == '__main__':
    main()
