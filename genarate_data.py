# ==================================================
# デジタル広告効果分析用サンプルデータ生成スクリプト
# ファイル名: generate_sample_data.py
# 単一フォルダ・日付ファイル名版
# ==================================================

import json
import csv
from datetime import datetime, timedelta
import random
import uuid
import os

# 乱数シードを固定（再現性のため）
random.seed(42)

# ==================================================
# 基本設定
# ==================================================

# 出力ディレクトリ
OUTPUT_DIR = "./sample_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/items", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/digital_ads", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/transactions", exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/ad_clicks", exist_ok=True)

# 期間設定（過去3ヶ月）
end_date = datetime.now()
start_date = end_date - timedelta(days=90)

print(f"データ生成期間: {start_date.date()} ～ {end_date.date()}")
print(f"出力先: {OUTPUT_DIR}")

# ==================================================
# マスタデータ定義
# ==================================================

# キャンペーン情報
campaigns = [
    {"campaign_id": "C001", "name": "春夏新作_ドレス", "target_category": "ドレス", "budget_daily": 50000},
    {"campaign_id": "C002", "name": "セール_アウター", "target_category": "アウター", "budget_daily": 70000},
    {"campaign_id": "C003", "name": "トレンド_トップス", "target_category": "トップス", "budget_daily": 40000},
    {"campaign_id": "C004", "name": "新作_バッグ", "target_category": "バッグ", "budget_daily": 60000},
    {"campaign_id": "C005", "name": "シューズ_プロモ", "target_category": "シューズ", "budget_daily": 45000},
    {"campaign_id": "C006", "name": "アクセサリー_キャンペーン", "target_category": "アクセサリー", "budget_daily": 30000},
    {"campaign_id": "C007", "name": "デニム_特集", "target_category": "ボトムス", "budget_daily": 35000},
    {"campaign_id": "C008", "name": "ワンピース_セール", "target_category": "ドレス", "budget_daily": 55000},
]

# 広告プラットフォーム
platforms = [
    {"name": "google", "avg_cpc": 80, "avg_ctr": 2.5},
    {"name": "facebook", "avg_cpc": 60, "avg_ctr": 3.0},
    {"name": "instagram", "avg_cpc": 70, "avg_ctr": 3.5},
    {"name": "youtube", "avg_cpc": 100, "avg_ctr": 2.0},
    {"name": "twitter", "avg_cpc": 50, "avg_ctr": 2.2},
]

# 広告フォーマット
ad_formats = ["video", "image", "carousel", "story", "banner"]

# 商品カテゴリ構造
categories = [
    {"l1": "レディース", "l2": "ドレス", "l3": "ワンピース"},
    {"l1": "レディース", "l2": "ドレス", "l3": "パーティードレス"},
    {"l1": "レディース", "l2": "トップス", "l3": "ブラウス"},
    {"l1": "レディース", "l2": "トップス", "l3": "Tシャツ"},
    {"l1": "レディース", "l2": "トップス", "l3": "ニット"},
    {"l1": "レディース", "l2": "アウター", "l3": "ジャケット"},
    {"l1": "レディース", "l2": "アウター", "l3": "コート"},
    {"l1": "レディース", "l2": "ボトムス", "l3": "パンツ"},
    {"l1": "レディース", "l2": "ボトムス", "l3": "スカート"},
    {"l1": "レディース", "l2": "ボトムス", "l3": "デニム"},
    {"l1": "アクセサリー", "l2": "バッグ", "l3": "ハンドバッグ"},
    {"l1": "アクセサリー", "l2": "バッグ", "l3": "トートバッグ"},
    {"l1": "アクセサリー", "l2": "シューズ", "l3": "パンプス"},
    {"l1": "アクセサリー", "l2": "シューズ", "l3": "スニーカー"},
    {"l1": "アクセサリー", "l2": "アクセサリー", "l3": "ネックレス"},
    {"l1": "アクセサリー", "l2": "アクセサリー", "l3": "ピアス"},
]

# ブランド
brands = ["ZARA", "H&M", "UNIQLO", "GU", "Forever21", "SHEIN", "Private Brand"]

# 色
colors = ["ブラック", "ホワイト", "ネイビー", "グレー", "ベージュ", "ピンク", "レッド", "ブルー"]

# サイズ
sizes = ["XS", "S", "M", "L", "XL", "FREE"]

# シーズン
seasons = ["春夏", "秋冬", "通年"]

# デバイスタイプ
device_types = ["mobile", "desktop", "tablet"]

# ==================================================
# 1. 商品マスタデータ生成（500商品）
# ==================================================

def generate_items(num_items=500):
    print("\n[1/4] 商品マスタデータ生成中...")
    items_data = []
    
    for i in range(num_items):
        item_id = f"P{10000 + i}"
        category = random.choice(categories)
        brand = random.choice(brands)
        
        # 価格設定（カテゴリによって変動）
        if category["l2"] == "ドレス":
            base_price = random.randint(8000, 25000)
        elif category["l2"] == "アウター":
            base_price = random.randint(12000, 35000)
        elif category["l2"] == "トップス":
            base_price = random.randint(3000, 12000)
        elif category["l2"] == "ボトムス":
            base_price = random.randint(5000, 15000)
        elif category["l2"] == "バッグ":
            base_price = random.randint(8000, 30000)
        elif category["l2"] == "シューズ":
            base_price = random.randint(6000, 18000)
        else:  # アクセサリー
            base_price = random.randint(2000, 10000)
        
        # 原価は価格の40-60%
        cost = int(base_price * random.uniform(0.4, 0.6))
        
        # 商品名生成
        item_name = f"{brand} {category['l3']}"
        
        # 発売日（過去1年以内）
        launch_date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        
        items_data.append({
            "item_id": item_id,
            "item_name": item_name,
            "category_l1": category["l1"],
            "category_l2": category["l2"],
            "category_l3": category["l3"],
            "brand": brand,
            "price": base_price,
            "cost": cost,
            "color": random.choice(colors),
            "size": random.choice(sizes),
            "season": random.choice(seasons),
            "launch_date": launch_date,
            "is_active": True
        })
    
    # 日付ごとにJSONファイルを生成
    # ファイル名: YYYYMMDD-items.json
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y%m%d')
        file_path = f"{OUTPUT_DIR}/items/{date_str}-items.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(items_data, f, ensure_ascii=False, indent=2)
        
        current_date += timedelta(days=1)
    
    print(f"✓ 商品データ生成完了: {len(items_data)}件 × {(end_date - start_date).days + 1}日分")
    print(f"  ファイル形式: YYYYMMDD-items.json")
    return items_data

# ==================================================
# 2. デジタル広告データ生成（日次CSV）
# ==================================================

def generate_digital_ads():
    print("\n[2/4] デジタル広告データ生成中...")
    
    total_ads = 0
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y%m%d')
        daily_ads = []
        
        # 各キャンペーンについて
        for campaign in campaigns:
            # 各プラットフォームで広告を出稿（ランダムに選択）
            num_platforms = random.randint(2, 4)
            selected_platforms = random.sample(platforms, num_platforms)
            
            for platform in selected_platforms:
                ad_id = f"AD{campaign['campaign_id']}_{platform['name']}_{date_str}"
                
                # 日次予算を配分
                daily_budget = campaign["budget_daily"] / len(selected_platforms)
                
                # 曜日による変動（土日は1.2倍、平日は0.9-1.1倍）
                day_of_week = current_date.weekday()
                if day_of_week >= 5:  # 土日
                    budget_multiplier = random.uniform(1.1, 1.3)
                else:
                    budget_multiplier = random.uniform(0.85, 1.05)
                
                adjusted_budget = daily_budget * budget_multiplier
                
                # CPC（クリック単価）のランダムな変動
                cpc = platform["avg_cpc"] * random.uniform(0.8, 1.2)
                
                # クリック数を計算
                clicks = int(adjusted_budget / cpc)
                
                # CTR（クリック率）のランダムな変動
                ctr = platform["avg_ctr"] * random.uniform(0.85, 1.15)
                
                # インプレッション数を逆算
                impressions = int(clicks / (ctr / 100))
                
                # 実際のコスト
                actual_cost = round(clicks * cpc, 2)
                
                # UTMパラメータ
                utm_campaign = f"{campaign['name'].lower().replace('_', '-')}"
                
                daily_ads.append({
                    "campaign_id": campaign["campaign_id"],
                    "campaign_name": campaign["name"],
                    "ad_id": ad_id,
                    "ad_platform": platform["name"],
                    "ad_format": random.choice(ad_formats),
                    "target_url": f"https://ec.example.com/products?campaign={campaign['campaign_id']}",
                    "impressions": impressions,
                    "clicks": clicks,
                    "cost": actual_cost,
                    "date": current_date.strftime('%Y-%m-%d'),
                    "utm_source": platform["name"],
                    "utm_medium": "cpc",
                    "utm_campaign": utm_campaign,
                    "target_category": campaign["target_category"]
                })
        
        # 日次CSVファイルとして保存
        # ファイル名: YYYYMMDD-ads.csv
        csv_path = f"{OUTPUT_DIR}/digital_ads/{date_str}-ads.csv"
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            if daily_ads:
                writer = csv.DictWriter(f, fieldnames=daily_ads[0].keys())
                writer.writeheader()
                writer.writerows(daily_ads)
        
        total_ads += len(daily_ads)
        current_date += timedelta(days=1)
    
    print(f"✓ 広告データ生成完了: {total_ads}件")
    print(f"  ファイル形式: YYYYMMDD-ads.csv")
    return total_ads

# ==================================================
# 3. トランザクションデータ生成（日次CSV）
# ==================================================

def generate_transactions(items_data):
    print("\n[3/4] トランザクションデータ生成中...")
    
    # 商品データをカテゴリ別に整理
    items_by_category = {}
    for item in items_data:
        cat = item["category_l2"]
        if cat not in items_by_category:
            items_by_category[cat] = []
        items_by_category[cat].append(item)
    
    transaction_counter = 1
    total_transactions = 0
    
    # 日付ごとに処理
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y%m%d')
        daily_transactions = []
        
        # その日の広告データを生成（仮想的に）
        daily_campaigns = []
        for campaign in campaigns:
            num_platforms = random.randint(2, 4)
            selected_platforms = random.sample(platforms, num_platforms)
            
            for platform in selected_platforms:
                # 簡易的な広告情報
                daily_budget = campaign["budget_daily"] / len(selected_platforms)
                day_of_week = current_date.weekday()
                if day_of_week >= 5:
                    budget_multiplier = random.uniform(1.1, 1.3)
                else:
                    budget_multiplier = random.uniform(0.85, 1.05)
                
                adjusted_budget = daily_budget * budget_multiplier
                cpc = platform["avg_cpc"] * random.uniform(0.8, 1.2)
                clicks = int(adjusted_budget / cpc)
                
                utm_campaign = f"{campaign['name'].lower().replace('_', '-')}"
                
                daily_campaigns.append({
                    "campaign_id": campaign["campaign_id"],
                    "platform_name": platform["name"],
                    "clicks": clicks,
                    "utm_campaign": utm_campaign,
                    "utm_source": platform["name"],
                    "utm_medium": "cpc",
                    "target_category": campaign["target_category"],
                    "target_url": f"https://ec.example.com/products?campaign={campaign['campaign_id']}"
                })
        
        # トランザクション生成
        for campaign_info in daily_campaigns:
            # CVR（コンバージョン率）を設定
            base_cvr = {
                "google": 2.5,
                "facebook": 3.0,
                "instagram": 3.5,
                "youtube": 2.0,
                "twitter": 2.2
            }.get(campaign_info["platform_name"], 2.5)
            
            cvr = base_cvr * random.uniform(0.7, 1.3)
            conversions = int(campaign_info["clicks"] * (cvr / 100))
            
            for _ in range(conversions):
                transaction_id = f"TXN{transaction_counter:08d}"
                transaction_counter += 1
                
                # トランザクション時刻（その日のランダムな時刻）
                transaction_timestamp = current_date + \
                                       timedelta(hours=random.randint(0, 23),
                                               minutes=random.randint(0, 59),
                                               seconds=random.randint(0, 59))
                
                # ターゲットカテゴリから商品を選択
                target_category = campaign_info["target_category"]
                if target_category in items_by_category and items_by_category[target_category]:
                    if random.random() < 0.8:
                        item = random.choice(items_by_category[target_category])
                    else:
                        item = random.choice(items_data)
                else:
                    item = random.choice(items_data)
                
                quantity = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
                
                if random.random() < 0.3:
                    user_id = f"U{random.randint(1, 5000):06d}"
                else:
                    user_id = f"U{random.randint(1, 20000):06d}"
                
                user_email = f"user{user_id.replace('U', '')}@example.com"
                device = random.choices(device_types, weights=[60, 30, 10])[0]
                conversion_time = random.randint(5, 2880)
                
                landing_page_url = f"https://ec.example.com/products/{item['item_id']}?utm_campaign={campaign_info['utm_campaign']}"
                
                daily_transactions.append({
                    "transaction_id": transaction_id,
                    "transaction_timestamp": transaction_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    "item_id": item["item_id"],
                    "user_email": user_email,
                    "user_id": user_id,
                    "quantity": quantity,
                    "price": item["price"],
                    "referrer_url": campaign_info["target_url"],
                    "landing_page_url": landing_page_url,
                    "utm_source": campaign_info["utm_source"],
                    "utm_medium": campaign_info["utm_medium"],
                    "utm_campaign": campaign_info["utm_campaign"],
                    "device_type": device,
                    "session_id": str(uuid.uuid4()),
                    "conversion_time_minutes": conversion_time
                })
        
        # オーガニックトランザクション（その日のトランザクションの30%）
        num_organic = int(len(daily_transactions) * 0.3)
        for _ in range(num_organic):
            transaction_id = f"TXN{transaction_counter:08d}"
            transaction_counter += 1
            
            transaction_timestamp = current_date + \
                                   timedelta(hours=random.randint(0, 23),
                                           minutes=random.randint(0, 59),
                                           seconds=random.randint(0, 59))
            
            item = random.choice(items_data)
            quantity = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
            user_id = f"U{random.randint(1, 20000):06d}"
            user_email = f"user{user_id.replace('U', '')}@example.com"
            device = random.choices(device_types, weights=[60, 30, 10])[0]
            
            daily_transactions.append({
                "transaction_id": transaction_id,
                "transaction_timestamp": transaction_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "item_id": item["item_id"],
                "user_email": user_email,
                "user_id": user_id,
                "quantity": quantity,
                "price": item["price"],
                "referrer_url": "https://ec.example.com",
                "landing_page_url": f"https://ec.example.com/products/{item['item_id']}",
                "utm_source": None,
                "utm_medium": None,
                "utm_campaign": None,
                "device_type": device,
                "session_id": str(uuid.uuid4()),
                "conversion_time_minutes": None
            })
        
        # 日次CSVファイルとして保存
        # ファイル名: YYYYMMDD-transactions.csv
        csv_path = f"{OUTPUT_DIR}/transactions/{date_str}-transactions.csv"
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            if daily_transactions:
                writer = csv.DictWriter(f, fieldnames=daily_transactions[0].keys())
                writer.writeheader()
                writer.writerows(daily_transactions)
        
        total_transactions += len(daily_transactions)
        current_date += timedelta(days=1)
    
    print(f"✓ トランザクションデータ生成完了: {total_transactions}件")
    print(f"  ファイル形式: YYYYMMDD-transactions.csv")
    return total_transactions

# ==================================================
# 4. 広告クリックログ生成（日次CSV）- オプション
# ==================================================

def generate_ad_clicks():
    print("\n[4/4] 広告クリックログ生成中...")
    
    click_counter = 1
    total_clicks = 0
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y%m%d')
        daily_clicks = []
        
        # その日の各キャンペーン
        for campaign in campaigns:
            num_platforms = random.randint(2, 4)
            selected_platforms = random.sample(platforms, num_platforms)
            
            for platform in selected_platforms:
                ad_id = f"AD{campaign['campaign_id']}_{platform['name']}_{date_str}"
                utm_campaign = f"{campaign['name'].lower().replace('_', '-')}"
                target_url = f"https://ec.example.com/products?campaign={campaign['campaign_id']}"
                
                # 簡易的なクリック数計算
                daily_budget = campaign["budget_daily"] / len(selected_platforms)
                day_of_week = current_date.weekday()
                if day_of_week >= 5:
                    budget_multiplier = random.uniform(1.1, 1.3)
                else:
                    budget_multiplier = random.uniform(0.85, 1.05)
                
                adjusted_budget = daily_budget * budget_multiplier
                cpc = platform["avg_cpc"] * random.uniform(0.8, 1.2)
                num_clicks = int(adjusted_budget / cpc)
                
                # 各クリック（サンプリング：最大50件/広告）
                for _ in range(min(num_clicks, 50)):
                    click_id = f"CLK{click_counter:010d}"
                    click_counter += 1
                    
                    click_timestamp = current_date + \
                                     timedelta(hours=random.randint(0, 23),
                                             minutes=random.randint(0, 59),
                                             seconds=random.randint(0, 59))
                    
                    user_id = f"U{random.randint(1, 20000):06d}"
                    device = random.choices(device_types, weights=[60, 30, 10])[0]
                    
                    daily_clicks.append({
                        "click_id": click_id,
                        "click_timestamp": click_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                        "campaign_id": campaign["campaign_id"],
                        "ad_id": ad_id,
                        "user_id": user_id,
                        "landing_page_url": target_url,
                        "utm_campaign": utm_campaign,
                        "device_type": device,
                        "ip_address": f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}",
                        "user_agent": f"Mozilla/5.0 ({device})"
                    })
        
        # 日次CSVファイルとして保存
        # ファイル名: YYYYMMDD-clicks.csv
        csv_path = f"{OUTPUT_DIR}/ad_clicks/{date_str}-clicks.csv"
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            if daily_clicks:
                writer = csv.DictWriter(f, fieldnames=daily_clicks[0].keys())
                writer.writeheader()
                writer.writerows(daily_clicks)
        
        total_clicks += len(daily_clicks)
        current_date += timedelta(days=1)
    
    print(f"✓ クリックログ生成完了: {total_clicks}件（サンプリング版）")
    print(f"  ファイル形式: YYYYMMDD-clicks.csv")
    return total_clicks

# ==================================================
# メイン実行
# ==================================================

def main():
    print("\n" + "="*60)
    print("デジタル広告効果分析用サンプルデータ生成")
    print("単一フォルダ・日付ファイル名版")
    print("="*60)
    
    # データ生成
    items = generate_items(num_items=500)
    ads_count = generate_digital_ads()
    txn_count = generate_transactions(items)
    clicks_count = generate_ad_clicks()
    
    # 統計情報
    print("\n" + "="*60)
    print("データ生成完了！")
    print("="*60)
    
    num_days = (end_date - start_date).days + 1
    
    print(f"\n【生成データサマリ】")
    print(f"期間: {start_date.date()} ～ {end_date.date()} ({num_days}日間)")
    print(f"商品数: {len(items)}件 × {num_days}日分のJSON")
    print(f"広告レコード数: {ads_count:,}件")
    print(f"トランザクション数: {txn_count:,}件")
    print(f"クリック数: {clicks_count:,}件（サンプリング版）")
    
    print(f"\n【ファイル構造】")
    print(f"{OUTPUT_DIR}/")
    print(f"├── items/")
    print(f"│   ├── 20240901-items.json")
    print(f"│   ├── 20240902-items.json")
    print(f"│   └── ...")
    print(f"├── digital_ads/")
    print(f"│   ├── 20240901-ads.csv")
    print(f"│   ├── 20240902-ads.csv")
    print(f"│   └── ...")
    print(f"├── transactions/")
    print(f"│   ├── 20240901-transactions.csv")
    print(f"│   ├── 20240902-transactions.csv")
    print(f"│   └── ...")
    print(f"└── ad_clicks/")
    print(f"    ├── 20240901-clicks.csv")
    print(f"    ├── 20240902-clicks.csv")
    print(f"    └── ...")
    
    print("\n【Databricksでの読み込み例】")
    print("# 商品マスタ（JSON）")
    print("items_df = spark.read.json('/mnt/data/items/*.json')")
    print("\n# 広告データ（CSV）")
    print("ads_df = spark.read.option('header', 'true').csv('/mnt/data/digital_ads/*-ads.csv')")
    print("\n# トランザクション（CSV）")
    print("txn_df = spark.read.option('header', 'true').csv('/mnt/data/transactions/*-transactions.csv')")
    print("\n# 特定月のデータのみ")
    print("ads_sep_df = spark.read.option('header', 'true').csv('/mnt/data/digital_ads/202409*-ads.csv')")

if __name__ == "__main__":
    main()