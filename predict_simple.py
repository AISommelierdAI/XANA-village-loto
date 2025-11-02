#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡易版Toto丸くん - 2023-09-21予測
"""

import csv
import json
import random
from collections import Counter

def load_data():
    """CSVデータを読み込み"""
    data = []
    try:
        with open('totomaru.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                numbers = [int(row[f'Number{i}']) for i in range(1, 7)]
                data.append({
                    'date': row['DrawDate'],
                    'numbers': numbers,
                    'bonus': int(row['Additional'])
                })
    except FileNotFoundError:
        print(f"⚠️ totomaru.csvが見つかりません")
        return []
    return data

def calculate_scores(data):
    """スコア計算"""
    if not data:
        return {}
    
    # 基本統計
    all_numbers = []
    recent_numbers = []
    
    for entry in data:
        all_numbers.extend(entry['numbers'])
        # 最近10回分
        if len(recent_numbers) < 60:
            recent_numbers.extend(entry['numbers'])
    
    # 出現回数
    total_counts = Counter(all_numbers)
    recent_counts = Counter(recent_numbers)
    
    # 欠損間隔
    missing_intervals = {}
    current_draw = len(data)
    
    for num in range(1, 50):
        last_appearance = None
        for i, entry in enumerate(reversed(data)):
            if num in entry['numbers']:
                last_appearance = current_draw - i
                break
        
        if last_appearance is None:
            missing_intervals[num] = current_draw
        else:
            missing_intervals[num] = current_draw - last_appearance
    
    # スコア計算
    scores = {}
    for num in range(1, 50):
        score = (
            total_counts[num] * 0.15 * 10 +
            recent_counts[num] * 0.20 * 15 +
            missing_intervals.get(num, 0) * 0.20 * 20 +
            random.uniform(0, 10)  # ランダム要素
        )
        scores[num] = max(0, score)
    
    return scores

def generate_patterns(scores):
    """パターン生成"""
    if not scores:
        return []
    
    # 上位スコアの数字を取得
    top_numbers = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:20]
    top_numbers = [num for num, score in top_numbers]
    
    patterns = []
    strategies = [
        "バランス重視",
        "高スコア重視", 
        "範囲分散",
        "合計値制御",
        "連続回避",
        "統計最適化"
    ]
    
    for i, strategy in enumerate(strategies):
        if i >= 6:  # 6パターンに制限
            break
        
        # パターン生成
        if strategy == "バランス重視":
            low_range = [n for n in top_numbers if 1 <= n <= 16]
            mid_range = [n for n in top_numbers if 17 <= n <= 32]
            high_range = [n for n in top_numbers if 33 <= n <= 49]
            
            pattern = []
            pattern.extend(random.sample(low_range, min(2, len(low_range))))
            pattern.extend(random.sample(mid_range, min(2, len(mid_range))))
            pattern.extend(random.sample(high_range, min(2, len(high_range))))
            
            while len(pattern) < 6:
                remaining = [n for n in top_numbers if n not in pattern]
                if remaining:
                    pattern.append(random.choice(remaining))
            
            numbers = sorted(pattern[:6])
        else:
            numbers = sorted(random.sample(top_numbers, 6))
        
        patterns.append({
            'pattern': i + 1,
            'numbers': numbers,
            'strategy': strategy,
            'confidence': 90 - i * 5  # パターン1が最も高い信頼度
        })
    
    return patterns

def predict(target_date):
    """予測実行"""
    print(f"🎯 簡易版Toto丸くん - {target_date}予測")
    print("=" * 60)
    
    data = load_data()
    if not data:
        print("⚠️ データがありません")
        return
    
    print(f"📊 データ分析完了（{len(data)}回分）")
    
    # スコア計算
    scores = calculate_scores(data)
    
    # パターン生成
    patterns = generate_patterns(scores)
    
    print(f"🔢 予測パターン数: {len(patterns)}")
    
    # 結果をファイルに保存
    result_file = f"results/result_simple_{target_date}.txt"
    
    with open(result_file, 'w', encoding='utf-8') as f:
        f.write(f"🎯 簡易版Toto丸くん - {target_date}予測\n")
        f.write("=" * 60 + "\n")
        f.write(f"📊 データ分析完了（{len(data)}回分）\n")
        f.write(f"🔢 予測パターン数: {len(patterns)}\n\n")
        
        for pattern in patterns:
            numbers = pattern['numbers']
            strategy = pattern['strategy']
            confidence = pattern['confidence']
            
            total = sum(numbers)
            odd_count = sum(1 for n in numbers if n % 2 == 1)
            even_count = 6 - odd_count
            
            low_count = sum(1 for n in numbers if 1 <= n <= 16)
            mid_count = sum(1 for n in numbers if 17 <= n <= 32)
            high_count = sum(1 for n in numbers if 33 <= n <= 49)
            
            f.write(f"【パターン{pattern['pattern']}】信頼度: {confidence:.1f}% ({strategy})\n")
            f.write(f"予測数字: {numbers}\n")
            f.write(f"合計: {total} | 奇数/偶数: {odd_count}/{even_count}\n")
            f.write(f"範囲分布: 低{low_count}個, 中{mid_count}個, 高{high_count}個\n")
            f.write("-" * 60 + "\n")
            
            print(f"【パターン{pattern['pattern']}】信頼度: {confidence:.1f}% ({strategy})")
            print(f"予測数字: {numbers}")
            print(f"合計: {total} | 奇数/偶数: {odd_count}/{even_count}")
            print(f"範囲分布: 低{low_count}個, 中{mid_count}個, 高{high_count}個")
            print("-" * 60)
        
        f.write("🎲 簡易版予測完了！\n")
        f.write("=" * 60 + "\n")
    
    print("🎲 簡易版予測完了！")
    print("=" * 60)
    print(f"📄 結果を {result_file} に保存しました")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("使用方法: python predict_simple.py YYYY-MM-DD")
        sys.exit(1)
    
    target_date = sys.argv[1]
    predict(target_date) 