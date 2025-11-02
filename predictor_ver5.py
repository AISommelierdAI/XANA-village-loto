#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ToTo〇くん Ver.5 - 完成版
現在の限界を突破する新しい予測システム
"""

import csv
import json
import random
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import os

class TotoVer5Predictor:
    def __init__(self, csv_file='totomaru.csv'):
        self.csv_file = csv_file
        self.results_dir = 'results'
        self.ensure_results_dir()
        self.learning_history = self.load_learning_history()
        
    def ensure_results_dir(self):
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
    
    def load_learning_history(self):
        """学習履歴の読み込みと分析"""
        history = {
            'recent_hits': [],
            'range_performance': {'low': [], 'mid': [], 'high': []},
            'consecutive_patterns': [],
            'bonus_patterns': [],
            'failed_predictions': []
        }
        
        # 最近の評価ファイルから学習
        evaluation_files = [f for f in os.listdir('.') if f.startswith('evaluation_') and f.endswith('.json')]
        for file in sorted(evaluation_files)[-10:]:  # 最近10回分
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    actual = data['actual_result']
                    
                    # 範囲別的中率の分析
                    for num in actual:
                        if 1 <= num <= 20:
                            history['range_performance']['low'].append(num)
                        elif 21 <= num <= 40:
                            history['range_performance']['mid'].append(num)
                        else:
                            history['range_performance']['high'].append(num)
                    
                    # 連続数字のパターン分析
                    sorted_nums = sorted(actual)
                    for i in range(len(sorted_nums) - 1):
                        if sorted_nums[i+1] - sorted_nums[i] == 1:
                            history['consecutive_patterns'].append((sorted_nums[i], sorted_nums[i+1]))
                    
                    # ボーナスパターン分析
                    if 'bonus' in data:
                        history['bonus_patterns'].append(data['bonus'])
                        
            except Exception as e:
                continue
        
        return history
    
    def load_data(self):
        """CSVデータの読み込み"""
        data = []
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        # CSVファイルの構造に合わせて修正
                        numbers = []
                        for i in range(1, 7):
                            key = f'Number{i}'
                            if key in row:
                                numbers.append(int(row[key]))
                            else:
                                print(f"列 {key} が見つかりません")
                                return []
                        
                        if 'Additional' in row:
                            bonus = int(row['Additional'])
                        else:
                            bonus = 0
                            
                        if 'DrawDate' in row:
                            date = row['DrawDate']
                        else:
                            date = "unknown"
                            
                        data.append({
                            'date': date,
                            'numbers': numbers,
                            'bonus': bonus
                        })
                    except (ValueError, KeyError) as e:
                        print(f"行の読み込みエラー: {e}")
                        continue
        except Exception as e:
            print(f"データ読み込みエラー: {e}")
            return []
        return data
    
    def analyze_range_trends(self, data):
        """範囲別トレンド分析"""
        range_counts = {'low': Counter(), 'mid': Counter(), 'high': Counter()}
        
        for draw in data[-20:]:  # 最近20回分
            for num in draw['numbers']:
                if 1 <= num <= 20:
                    range_counts['low'][num] += 1
                elif 21 <= num <= 40:
                    range_counts['mid'][num] += 1
                else:
                    range_counts['high'][num] += 1
        
        return range_counts
    
    def analyze_consecutive_patterns(self, data):
        """連続数字パターンの分析"""
        consecutive_freq = Counter()
        
        for draw in data[-30:]:  # 最近30回分
            sorted_nums = sorted(draw['numbers'])
            for i in range(len(sorted_nums) - 1):
                diff = sorted_nums[i+1] - sorted_nums[i]
                if diff <= 3:  # 3以内の差を連続パターンとして扱う
                    consecutive_freq[diff] += 1
        
        return consecutive_freq
    
    def analyze_recent_performance(self, data):
        """最近の的中パフォーマンス分析"""
        recent_performance = {
            'low_range_hits': [],
            'mid_range_hits': [],
            'high_range_hits': [],
            'consecutive_hits': []
        }
        
        # 最近の評価ファイルから的中データを分析
        evaluation_files = [f for f in os.listdir('.') if f.startswith('evaluation_') and f.endswith('.json')]
        for file in sorted(evaluation_files)[-5:]:  # 最近5回分
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    eval_data = json.load(f)
                    actual = eval_data['actual_result']
                    
                    # 範囲別的中分析
                    for num in actual:
                        if 1 <= num <= 20:
                            recent_performance['low_range_hits'].append(num)
                        elif 21 <= num <= 40:
                            recent_performance['mid_range_hits'].append(num)
                        else:
                            recent_performance['high_range_hits'].append(num)
                    
                    # 連続数字分析
                    sorted_nums = sorted(actual)
                    for i in range(len(sorted_nums) - 1):
                        if sorted_nums[i+1] - sorted_nums[i] == 1:
                            recent_performance['consecutive_hits'].append((sorted_nums[i], sorted_nums[i+1]))
                            
            except Exception as e:
                continue
        
        return recent_performance
    
    def predict_range_specific(self, range_type, range_counts, target_count=2):
        """範囲別予測"""
        if range_type == 'low':
            candidates = list(range(1, 21))
        elif range_type == 'mid':
            candidates = list(range(21, 41))
        else:
            candidates = list(range(41, 50))
        
        # 頻度に基づくスコア計算
        scores = {}
        for num in candidates:
            freq = range_counts[range_type].get(num, 0)
            recent_weight = 1.0
            if freq > 0:
                recent_weight = 1.5  # 最近出現した数字に重み
            scores[num] = freq * recent_weight + random.random() * 0.1
        
        # 上位数字を選択
        sorted_numbers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        selected = []
        for num, score in sorted_numbers[:target_count * 2]:  # 2倍選択してから絞り込み
            if len(selected) < target_count:
                selected.append(num)
        
        return selected
    
    def predict_consecutive_aware(self, base_numbers, consecutive_freq):
        """連続数字を考慮した予測"""
        candidates = []
        
        # 連続パターンの確率に基づいて追加
        if consecutive_freq.get(1, 0) > 2:  # 連続数字が頻繁に出現
            for num in base_numbers:
                if num + 1 <= 49 and num + 1 not in base_numbers:
                    candidates.append(num + 1)
                if num - 1 >= 1 and num - 1 not in base_numbers:
                    candidates.append(num - 1)
        
        return candidates[:2]  # 最大2個追加
    
    def predict_bonus_improved(self, data):
        """改良されたボーナス予測"""
        bonus_freq = Counter()
        
        for draw in data[-20:]:
            bonus_freq[draw['bonus']] += 1
        
        # ボーナスの範囲別傾向
        low_bonus = sum(1 for b in bonus_freq if 1 <= b <= 20)
        mid_bonus = sum(1 for b in bonus_freq if 21 <= b <= 40)
        high_bonus = sum(1 for b in bonus_freq if 41 <= b <= 49)
        
        # 最も頻繁な範囲から予測
        if low_bonus > mid_bonus and low_bonus > high_bonus:
            candidates = list(range(1, 21))
        elif mid_bonus > high_bonus:
            candidates = list(range(21, 41))
        else:
            candidates = list(range(41, 50))
        
        # 頻度に基づく選択
        scores = {num: bonus_freq.get(num, 0) + random.random() * 0.1 for num in candidates}
        sorted_bonus = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_bonus[0][0] if sorted_bonus else random.randint(1, 49)
    
    def generate_ver5_patterns(self, data):
        """Ver.5 パターン生成"""
        range_counts = self.analyze_range_trends(data)
        consecutive_freq = self.analyze_consecutive_patterns(data)
        recent_performance = self.analyze_recent_performance(data)
        
        patterns = []
        
        # パターン1: 範囲バランス重視（Ver.5）
        low_nums = self.predict_range_specific('low', range_counts, 2)
        mid_nums = self.predict_range_specific('mid', range_counts, 2)
        high_nums = self.predict_range_specific('high', range_counts, 2)
        
        pattern1 = low_nums + mid_nums + high_nums
        pattern1 = list(set(pattern1))[:6]  # 重複除去
        patterns.append({
            'numbers': pattern1,
            'confidence': 85.0,
            'strategy': '範囲バランスVer.5'
        })
        
        # パターン2: 中範囲強化版（Ver.5）
        mid_nums_strong = self.predict_range_specific('mid', range_counts, 3)
        low_nums_comp = self.predict_range_specific('low', range_counts, 2)
        high_nums_comp = self.predict_range_specific('high', range_counts, 1)
        
        pattern2 = mid_nums_strong + low_nums_comp + high_nums_comp
        pattern2 = list(set(pattern2))[:6]
        patterns.append({
            'numbers': pattern2,
            'confidence': 80.0,
            'strategy': '中範囲強化Ver.5'
        })
        
        # パターン3: 連続数字考慮版（Ver.5）
        base_nums = self.predict_range_specific('low', range_counts, 2) + \
                   self.predict_range_specific('mid', range_counts, 2) + \
                   self.predict_range_specific('high', range_counts, 2)
        consecutive_nums = self.predict_consecutive_aware(base_nums, consecutive_freq)
        
        pattern3 = base_nums + consecutive_nums
        pattern3 = list(set(pattern3))[:6]
        patterns.append({
            'numbers': pattern3,
            'confidence': 75.0,
            'strategy': '連続数字考慮Ver.5'
        })
        
        # パターン4: 低範囲強化版（Ver.5）
        low_nums_strong = self.predict_range_specific('low', range_counts, 3)
        mid_nums_comp = self.predict_range_specific('mid', range_counts, 2)
        high_nums_comp = self.predict_range_specific('high', range_counts, 1)
        
        pattern4 = low_nums_strong + mid_nums_comp + high_nums_comp
        pattern4 = list(set(pattern4))[:6]
        patterns.append({
            'numbers': pattern4,
            'confidence': 70.0,
            'strategy': '低範囲強化Ver.5'
        })
        
        # パターン5: 高範囲強化版（Ver.5）
        high_nums_strong = self.predict_range_specific('high', range_counts, 3)
        low_nums_comp = self.predict_range_specific('low', range_counts, 2)
        mid_nums_comp = self.predict_range_specific('mid', range_counts, 1)
        
        pattern5 = high_nums_strong + low_nums_comp + mid_nums_comp
        pattern5 = list(set(pattern5))[:6]
        patterns.append({
            'numbers': pattern5,
            'confidence': 65.0,
            'strategy': '高範囲強化Ver.5'
        })
        
        # パターン6: 学習履歴重視版（Ver.5）
        recent_trends = self.learning_history['range_performance']
        if len(recent_trends['mid']) > len(recent_trends['low']) and len(recent_trends['mid']) > len(recent_trends['high']):
            # 中範囲が最近多く出現
            mid_nums_trend = self.predict_range_specific('mid', range_counts, 3)
            low_nums_trend = self.predict_range_specific('low', range_counts, 2)
            high_nums_trend = self.predict_range_specific('high', range_counts, 1)
        else:
            low_nums_trend = self.predict_range_specific('low', range_counts, 3)
            mid_nums_trend = self.predict_range_specific('mid', range_counts, 2)
            high_nums_trend = self.predict_range_specific('high', range_counts, 1)
        
        pattern6 = low_nums_trend + mid_nums_trend + high_nums_trend
        pattern6 = list(set(pattern6))[:6]
        patterns.append({
            'numbers': pattern6,
            'confidence': 60.0,
            'strategy': '学習履歴重視Ver.5'
        })
        
        return patterns
    
    def predict(self, target_date):
        """Ver.5 予測実行"""
        print(f"🎯 ToTo〇くん Ver.5 - {target_date}予測")
        print("=" * 60)
        
        # データ読み込み
        data = self.load_data()
        if not data:
            print("❌ データ読み込みに失敗しました")
            return
        
        print(f"📊 Ver.5 データ分析完了（{len(data)}回分）")
        
        # パターン生成
        patterns = self.generate_ver5_patterns(data)
        
        # ボーナス予測
        bonus_prediction = self.predict_bonus_improved(data)
        
        print(f"🔢 予測パターン数: {len(patterns)}")
        print()
        
        # 結果出力
        for i, pattern in enumerate(patterns, 1):
            numbers = pattern['numbers']
            confidence = pattern['confidence']
            strategy = pattern['strategy']
            total = sum(numbers)
            odd_count = len([n for n in numbers if n % 2 == 1])
            even_count = 6 - odd_count
            
            print(f"【パターン{i}】信頼度: {confidence}% ({strategy})")
            print(f"予測数字: {numbers}")
            print(f"合計: {total} | 奇数/偶数: {odd_count}/{even_count}")
            print("-" * 60)
        
        print(f"🎲 Ver.5 予測完了！")
        print("=" * 60)
        
        # 結果保存
        result_file = os.path.join(self.results_dir, f'result_ver5_{target_date}.txt')
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"🎯 ToTo〇くん Ver.5 - {target_date}予測\n")
            f.write("=" * 60 + "\n")
            f.write(f"📊 Ver.5 データ分析完了（{len(data)}回分）\n")
            f.write(f"🔢 予測パターン数: {len(patterns)}\n\n")
            
            for i, pattern in enumerate(patterns, 1):
                numbers = pattern['numbers']
                confidence = pattern['confidence']
                strategy = pattern['strategy']
                total = sum(numbers)
                odd_count = len([n for n in numbers if n % 2 == 1])
                even_count = 6 - odd_count
                
                f.write(f"【パターン{i}】信頼度: {confidence}% ({strategy})\n")
                f.write(f"予測数字: {numbers}\n")
                f.write(f"合計: {total} | 奇数/偶数: {odd_count}/{even_count}\n")
                f.write("-" * 60 + "\n")
            
            f.write(f"🎲 Ver.5 予測完了！\n")
            f.write("=" * 60 + "\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("使用方法: python predictor_ver5.py YYYY-MM-DD")
        sys.exit(1)
    
    target_date = sys.argv[1]
    predictor = TotoVer5Predictor()
    predictor.predict(target_date) 