#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改良版Toto丸くん - 新戦略統合システム
新機能:
1. 低範囲予測強化
2. ボーナス予測システム
3. 履歴学習機能
4. 動的スコア調整
5. パターン多様化
"""

import csv
import json
import statistics
import random
import numpy as np
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import os

class AdvancedTotoPredictor:
    def __init__(self, csv_file='totomaru.csv'):
        self.csv_file = csv_file
        self.results_dir = 'results'
        self.ensure_results_dir()
        self.learning_history = self.load_learning_history()
        
    def ensure_results_dir(self):
        """結果ディレクトリの作成"""
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
    
    def load_learning_history(self):
        """学習履歴の読み込み"""
        history = {
            'recent_performance': [],
            'strategy_weights': {
                'バランス重視': 1.0,
                '高スコア重視': 1.0,
                '範囲分散': 1.0,
                '合計値制御': 1.0,
                '連続回避': 1.0,
                '統計最適化': 1.0,
                '低範囲強化': 1.0,
                'ボーナス予測': 1.0,
                '履歴学習': 1.0,
                '動的調整': 1.0
            },
            'range_performance': {'low': 1.0, 'mid': 1.0, 'high': 1.0},
            'bonus_performance': 1.0
        }
        
        # 評価ファイルから学習履歴を読み込み
        evaluation_files = [f for f in os.listdir('.') if f.startswith('evaluation_') and f.endswith('.json')]
        for file in sorted(evaluation_files)[-5:]:  # 最近5回分
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    history['recent_performance'].append(data['analysis']['average_hit_rate'])
                    
                    # 戦略別的中率の更新
                    for pattern_name, pattern_data in data['predictions'].items():
                        strategy = pattern_data['strategy']
                        hit_rate = pattern_data['hit_rate']
                        if strategy in history['strategy_weights']:
                            history['strategy_weights'][strategy] = (history['strategy_weights'][strategy] + hit_rate) / 2
                    
                    # ボーナス的中の更新
                    if data['analysis']['bonus_hit']:
                        history['bonus_performance'] = (history['bonus_performance'] + 1.0) / 2
            except:
                continue
        
        return history
    
    def load_data(self):
        """CSVデータを読み込み"""
        data = []
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    numbers = [int(row[f'Number{i}']) for i in range(1, 7)]
                    data.append(numbers)
        except FileNotFoundError:
            print(f"⚠️ {self.csv_file}が見つかりません")
            return []
        return data
    
    def calculate_advanced_scores(self, data):
        """改良版スコア計算"""
        if not data:
            return {}
        
        # 基本統計
        all_numbers = []
        recent_numbers = []
        very_recent_numbers = []
        
        for i, draw in enumerate(data):
            all_numbers.extend(draw)
            # 最近10回分
            if len(recent_numbers) < 60:
                recent_numbers.extend(draw)
            # 最近5回分
            if len(very_recent_numbers) < 30:
                very_recent_numbers.extend(draw)
        
        # 出現回数
        total_counts = Counter(all_numbers)
        recent_counts = Counter(recent_numbers)
        very_recent_counts = Counter(very_recent_numbers)
        
        # 欠損間隔
        missing_intervals = {}
        current_draw = len(data)
        
        for num in range(1, 50):
            last_appearance = None
            for i, draw in enumerate(reversed(data)):
                if num in draw:
                    last_appearance = current_draw - i
                    break
            
            if last_appearance is None:
                missing_intervals[num] = current_draw
            else:
                missing_intervals[num] = current_draw - last_appearance
        
        # 範囲別パフォーマンス調整
        range_weights = self.learning_history['range_performance']
        
        # 改良版スコア計算
        scores = {}
        for num in range(1, 50):
            # 基本スコア
            base_score = (
                total_counts[num] * 0.15 * 10 +
                recent_counts[num] * 0.20 * 15 +
                very_recent_counts[num] * 0.25 * 20 +
                missing_intervals.get(num, 0) * 0.20 * 25
            )
            
            # 範囲別調整
            if 1 <= num <= 16:
                range_multiplier = range_weights['low']
            elif 17 <= num <= 32:
                range_multiplier = range_weights['mid']
            else:
                range_multiplier = range_weights['high']
            
            # 履歴学習調整
            recent_performance = np.mean(self.learning_history['recent_performance']) if self.learning_history['recent_performance'] else 0.167
            performance_multiplier = 1.0 + (recent_performance - 0.167) * 2  # 的中率に応じて調整
            
            # 最終スコア
            final_score = base_score * range_multiplier * performance_multiplier + random.uniform(0, 15)
            scores[num] = max(0, final_score)
        
        return scores
    
    def generate_advanced_patterns(self, scores):
        """改良版パターン生成"""
        if not scores:
            return []
        
        # 上位スコアの数字を取得
        top_numbers = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:30]
        top_numbers = [num for num, score in top_numbers]
        
        patterns = []
        strategies = [
            "バランス重視",
            "高スコア重視", 
            "範囲分散",
            "合計値制御",
            "連続回避",
            "統計最適化",
            "低範囲強化",
            "ボーナス予測",
            "履歴学習",
            "動的調整"
        ]
        
        # 戦略の重み付け選択
        strategy_weights = self.learning_history['strategy_weights']
        weighted_strategies = [(s, strategy_weights.get(s, 1.0)) for s in strategies]
        weighted_strategies.sort(key=lambda x: x[1], reverse=True)
        
        selected_strategies = [s[0] for s in weighted_strategies[:6]]
        
        for i, strategy in enumerate(selected_strategies):
            numbers = self.generate_advanced_strategy_pattern(top_numbers, strategy, i)
            if numbers:
                confidence = 85 - i * 5 + (strategy_weights.get(strategy, 1.0) - 1.0) * 20
                confidence = max(50, min(95, confidence))
                
                patterns.append({
                    'pattern': i + 1,
                    'numbers': numbers,
                    'strategy': strategy,
                    'confidence': confidence
                })
        
        return patterns[:6]
    
    def generate_advanced_strategy_pattern(self, top_numbers, strategy, pattern_num):
        """改良版戦略別パターン生成"""
        if strategy == "バランス重視":
            return self.generate_balanced_pattern(top_numbers)
        elif strategy == "高スコア重視":
            return self.generate_high_score_pattern(top_numbers)
        elif strategy == "範囲分散":
            return self.generate_range_distributed_pattern(top_numbers)
        elif strategy == "合計値制御":
            return self.generate_sum_controlled_pattern(top_numbers)
        elif strategy == "連続回避":
            return self.generate_non_consecutive_pattern(top_numbers)
        elif strategy == "統計最適化":
            return self.generate_statistical_pattern(top_numbers)
        elif strategy == "低範囲強化":
            return self.generate_low_range_enhanced_pattern(top_numbers)
        elif strategy == "ボーナス予測":
            return self.generate_bonus_prediction_pattern(top_numbers)
        elif strategy == "履歴学習":
            return self.generate_history_learning_pattern(top_numbers)
        elif strategy == "動的調整":
            return self.generate_dynamic_adjustment_pattern(top_numbers)
        
        return sorted(random.sample(top_numbers, 6))
    
    def generate_low_range_enhanced_pattern(self, top_numbers):
        """低範囲強化パターン（新戦略）"""
        low_range = [n for n in top_numbers if 1 <= n <= 20]
        mid_range = [n for n in top_numbers if 21 <= n <= 35]
        high_range = [n for n in top_numbers if 36 <= n <= 49]
        
        pattern = []
        # 低範囲を重視（3個）
        pattern.extend(random.sample(low_range, min(3, len(low_range))))
        # 中範囲（2個）
        pattern.extend(random.sample(mid_range, min(2, len(mid_range))))
        # 高範囲（1個）
        pattern.extend(random.sample(high_range, min(1, len(high_range))))
        
        # 6個に調整
        while len(pattern) < 6:
            remaining = [n for n in top_numbers if n not in pattern]
            if remaining:
                pattern.append(random.choice(remaining))
        
        return sorted(pattern[:6])
    
    def generate_bonus_prediction_pattern(self, top_numbers):
        """ボーナス予測パターン（新戦略）"""
        # ボーナス数字の特徴を分析
        bonus_candidates = []
        
        # 最近のボーナス数字を分析
        data = self.load_data()
        recent_bonuses = []
        for draw in data[-10:]:  # 最近10回分
            if len(draw) > 6:
                recent_bonuses.append(draw[6])
        
        if recent_bonuses:
            bonus_counts = Counter(recent_bonuses)
            # ボーナス候補を選定
            for num in range(1, 50):
                if num in bonus_counts:
                    bonus_candidates.append(num)
        
        # ボーナス候補がない場合は通常の選択
        if not bonus_candidates:
            bonus_candidates = top_numbers[:10]
        
        # 通常の数字5個 + ボーナス候補1個
        normal_numbers = random.sample(top_numbers, 5)
        bonus_number = random.choice(bonus_candidates)
        
        pattern = normal_numbers + [bonus_number]
        return sorted(pattern)
    
    def generate_history_learning_pattern(self, top_numbers):
        """履歴学習パターン（新戦略）"""
        # 最近の的中した数字を分析
        recent_hits = []
        evaluation_files = [f for f in os.listdir('.') if f.startswith('evaluation_') and f.endswith('.json')]
        
        for file in sorted(evaluation_files)[-3:]:  # 最近3回分
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for pattern_data in data['predictions'].values():
                        recent_hits.extend(pattern_data.get('hit_numbers', []))
            except:
                continue
        
        # 的中した数字を重視
        hit_counts = Counter(recent_hits)
        enhanced_numbers = []
        
        for num in top_numbers:
            enhancement = hit_counts.get(num, 0) * 0.5
            enhanced_numbers.append((num, enhancement))
        
        # 重み付けで選択
        enhanced_numbers.sort(key=lambda x: x[1], reverse=True)
        selected_numbers = [num for num, _ in enhanced_numbers[:15]]
        
        return sorted(random.sample(selected_numbers, 6))
    
    def generate_dynamic_adjustment_pattern(self, top_numbers):
        """動的調整パターン（新戦略）"""
        # 最近の的中率に基づいて動的に調整
        recent_performance = np.mean(self.learning_history['recent_performance']) if self.learning_history['recent_performance'] else 0.167
        
        if recent_performance < 0.1:  # 的中率が低い場合
            # より多様な範囲から選択
            ranges = [[1, 15], [16, 30], [31, 49]]
            pattern = []
            for start, end in ranges:
                range_numbers = [n for n in top_numbers if start <= n <= end]
                if range_numbers:
                    pattern.extend(random.sample(range_numbers, min(2, len(range_numbers))))
        else:
            # 的中率が高い場合は通常の選択
            pattern = random.sample(top_numbers, 6)
        
        return sorted(pattern[:6])
    
    # 既存のパターン生成メソッド（改良版）
    def generate_balanced_pattern(self, top_numbers):
        """バランス重視パターン（改良版）"""
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
        
        return sorted(pattern[:6])
    
    def generate_high_score_pattern(self, top_numbers):
        """高スコア重視パターン（改良版）"""
        return sorted(random.sample(top_numbers[:15], 6))
    
    def generate_range_distributed_pattern(self, top_numbers):
        """範囲分散パターン（改良版）"""
        ranges = [[1, 16], [17, 32], [33, 49]]
        pattern = []
        
        for start, end in ranges:
            range_numbers = [n for n in top_numbers if start <= n <= end]
            if range_numbers:
                pattern.extend(random.sample(range_numbers, min(2, len(range_numbers))))
        
        while len(pattern) < 6:
            remaining = [n for n in top_numbers if n not in pattern]
            if remaining:
                pattern.append(random.choice(remaining))
        
        return sorted(pattern[:6])
    
    def generate_sum_controlled_pattern(self, top_numbers):
        """合計値制御パターン（改良版）"""
        target_sum = 150
        
        best_pattern = None
        best_diff = float('inf')
        
        for _ in range(50):
            pattern = sorted(random.sample(top_numbers, 6))
            current_sum = sum(pattern)
            diff = abs(current_sum - target_sum)
            
            if diff < best_diff:
                best_diff = diff
                best_pattern = pattern
        
        return best_pattern or sorted(random.sample(top_numbers, 6))
    
    def generate_non_consecutive_pattern(self, top_numbers):
        """連続回避パターン（改良版）"""
        pattern = []
        candidates = top_numbers.copy()
        
        while len(pattern) < 6 and candidates:
            num = random.choice(candidates)
            candidates.remove(num)
            
            is_consecutive = False
            for existing in pattern:
                if abs(num - existing) == 1:
                    is_consecutive = True
                    break
            
            if not is_consecutive:
                pattern.append(num)
        
        while len(pattern) < 6:
            remaining = [n for n in top_numbers if n not in pattern]
            if remaining:
                pattern.append(random.choice(remaining))
        
        return sorted(pattern[:6])
    
    def generate_statistical_pattern(self, top_numbers):
        """統計最適化パターン（改良版）"""
        odd_count = random.randint(2, 4)
        even_count = 6 - odd_count
        
        odd_numbers = [n for n in top_numbers if n % 2 == 1]
        even_numbers = [n for n in top_numbers if n % 2 == 0]
        
        pattern = []
        pattern.extend(random.sample(odd_numbers, min(odd_count, len(odd_numbers))))
        pattern.extend(random.sample(even_numbers, min(even_count, len(even_numbers))))
        
        while len(pattern) < 6:
            remaining = [n for n in top_numbers if n not in pattern]
            if remaining:
                pattern.append(random.choice(remaining))
        
        return sorted(pattern[:6])
    
    def predict(self, target_date):
        """改良版予測実行"""
        print(f"🚀 改良版Toto丸くん - {target_date}予測")
        print("=" * 60)
        
        data = self.load_data()
        if not data:
            print("⚠️ データがありません")
            return
        
        print(f"📊 改良版データ分析完了（{len(data)}回分）")
        print(f"🧠 学習履歴: {len(self.learning_history['recent_performance'])}回分")
        
        # 改良版スコア計算
        scores = self.calculate_advanced_scores(data)
        
        # 改良版パターン生成
        patterns = self.generate_advanced_patterns(scores)
        
        print(f"🔢 予測パターン数: {len(patterns)}")
        
        # 結果をファイルに保存
        result_file = f"results/result_advanced_{target_date}.txt"
        
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"🚀 改良版Toto丸くん - {target_date}予測\n")
            f.write("=" * 60 + "\n")
            f.write(f"📊 改良版データ分析完了（{len(data)}回分）\n")
            f.write(f"🧠 学習履歴: {len(self.learning_history['recent_performance'])}回分\n")
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
            
            f.write("🎲 改良版予測完了！\n")
            f.write("=" * 60 + "\n")
        
        print("🎲 改良版予測完了！")
        print("=" * 60)
        print(f"📄 結果を {result_file} に保存しました")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("使用方法: python predictor_advanced_v2.py YYYY-MM-DD")
        sys.exit(1)
    
    target_date = sys.argv[1]
    predictor = AdvancedTotoPredictor()
    predictor.predict(target_date) 