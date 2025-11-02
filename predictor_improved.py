#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改良版Toto丸くん - 的中率改善システム
信頼度計算の見直しと実用的な予測アルゴリズム
"""

import csv
import json
import statistics
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import random

class ImprovedTotoPredictor:
    def __init__(self, csv_file='totomaru.csv'):
        self.csv_file = csv_file
        self.data = self.load_data()
        self.weights = self.load_weights()
        self.historical_accuracy = self.load_historical_accuracy()
        
    def load_data(self):
        """CSVデータを読み込み"""
        data = []
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    numbers = [int(row[f'Number{i}']) for i in range(1, 7)]
                    data.append({
                        'date': row['DrawDate'],
                        'numbers': numbers,
                        'bonus': int(row['Additional'])
                    })
        except FileNotFoundError:
            print(f"⚠️ {self.csv_file}が見つかりません")
            return []
        return data
    
    def load_weights(self):
        """重み設定を読み込み"""
        try:
            with open('weights.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            # デフォルト重み
            return {
                "total_appearances": 0.15,
                "recent_appearances": 0.20,
                "missing_intervals": 0.20,
                "hot_cold": 0.10,
                "periodicity": 0.10,
                "regression_trend": 0.08,
                "moving_average": 0.08,
                "attraction_effect": 0.05,
                "distribution": 0.02,
                "adjacent_correlation": 0.02
            }
    
    def load_historical_accuracy(self):
        """過去の的中率データを読み込み"""
        try:
            with open('evaluation_results.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
    
    def calculate_realistic_confidence(self, numbers, scores):
        """実用的な信頼度計算（過去の的中率ベース）"""
        # 過去の的中率を分析
        recent_accuracy = self.analyze_recent_accuracy()
        
        # 基本スコア
        base_score = sum(scores) / len(scores)
        
        # 範囲バランススコア
        range_balance = self.calculate_range_balance_score(numbers)
        
        # 合計値スコア
        sum_score = self.calculate_sum_score(numbers)
        
        # 連続数字スコア
        consecutive_score = self.calculate_consecutive_score(numbers)
        
        # 実用的信頼度計算
        realistic_confidence = (
            base_score * 0.4 +
            range_balance * 0.25 +
            sum_score * 0.20 +
            consecutive_score * 0.15
        ) * recent_accuracy['adjustment_factor']
        
        return min(realistic_confidence, 95.0)  # 最大95%に制限
    
    def analyze_recent_accuracy(self):
        """最近の的中率を分析"""
        if not self.historical_accuracy:
            return {'adjustment_factor': 1.0, 'average_hits': 0.5}
        
        recent_results = []
        for date, result in self.historical_accuracy.items():
            if 'summary' in result:
                recent_results.append(result['summary']['average_hit_count'])
        
        if not recent_results:
            return {'adjustment_factor': 1.0, 'average_hits': 0.5}
        
        avg_hits = statistics.mean(recent_results)
        
        # 調整係数（的中率に基づく）
        if avg_hits >= 1.5:
            adjustment_factor = 1.2  # 的中率が高い場合は信頼度を上げる
        elif avg_hits >= 1.0:
            adjustment_factor = 1.0  # 標準
        elif avg_hits >= 0.5:
            adjustment_factor = 0.8  # 的中率が低い場合は信頼度を下げる
        else:
            adjustment_factor = 0.6  # 非常に低い場合は大幅に下げる
        
        return {
            'adjustment_factor': adjustment_factor,
            'average_hits': avg_hits
        }
    
    def calculate_range_balance_score(self, numbers):
        """範囲バランススコア計算"""
        low_count = sum(1 for n in numbers if 1 <= n <= 16)
        mid_count = sum(1 for n in numbers if 17 <= n <= 32)
        high_count = sum(1 for n in numbers if 33 <= n <= 49)
        
        # 理想的な分布: 低2個, 中2個, 高2個
        ideal_distribution = [2, 2, 2]
        actual_distribution = [low_count, mid_count, high_count]
        
        # 分布の類似度を計算
        max_diff = max(abs(ideal - actual) for ideal, actual in zip(ideal_distribution, actual_distribution))
        balance_score = max(0, 100 - max_diff * 20)
        
        return balance_score
    
    def calculate_sum_score(self, numbers):
        """合計値スコア計算"""
        total = sum(numbers)
        
        # 理想的な合計値範囲: 120-180
        if 120 <= total <= 180:
            return 100
        elif 100 <= total <= 200:
            return 80
        elif 80 <= total <= 220:
            return 60
        else:
            return 40
    
    def calculate_consecutive_score(self, numbers):
        """連続数字スコア計算"""
        sorted_numbers = sorted(numbers)
        consecutive_count = 0
        
        for i in range(len(sorted_numbers) - 1):
            if sorted_numbers[i+1] - sorted_numbers[i] == 1:
                consecutive_count += 1
        
        # 連続数字は0-2個が理想的
        if consecutive_count == 0:
            return 100
        elif consecutive_count == 1:
            return 80
        elif consecutive_count == 2:
            return 60
        else:
            return 30
    
    def calculate_improved_scores(self, data):
        """改良されたスコア計算"""
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
        missing_intervals = self.calculate_missing_intervals(data)
        
        # ホット/コールド分析
        hot_cold = self.analyze_hot_cold(data)
        
        # 周期性分析
        periodicity = self.analyze_periodicity(data)
        
        # 回帰トレンド
        regression_trend = self.calculate_regression_trend(data)
        
        # 移動平均
        moving_avg = self.calculate_moving_average(data)
        
        # 引力効果
        attraction_effect = self.calculate_attraction_effect(data)
        
        # 分布分析
        distribution = self.analyze_distribution(data)
        
        # 隣接相関
        adjacent_correlation = self.calculate_adjacent_correlation(data)
        
        # 改良されたスコア計算
        scores = {}
        for num in range(1, 50):
            score = (
                total_counts[num] * self.weights['total_appearances'] * 10 +
                recent_counts[num] * self.weights['recent_appearances'] * 15 +
                missing_intervals.get(num, 0) * self.weights['missing_intervals'] * 20 +
                hot_cold.get(num, 0) * self.weights['hot_cold'] * 10 +
                periodicity.get(num, 0) * self.weights['periodicity'] * 10 +
                regression_trend.get(num, 0) * self.weights['regression_trend'] * 10 +
                moving_avg.get(num, 0) * self.weights['moving_average'] * 10 +
                attraction_effect.get(num, 0) * self.weights['attraction_effect'] * 10 +
                distribution.get(num, 0) * self.weights['distribution'] * 10 +
                adjacent_correlation.get(num, 0) * self.weights['adjacent_correlation'] * 10
            )
            scores[num] = max(0, score)
        
        return scores
    
    def calculate_missing_intervals(self, data):
        """欠損間隔計算（改良版）"""
        if not data:
            return {}
        
        intervals = {}
        current_draw = len(data)
        
        for num in range(1, 50):
            last_appearance = None
            for i, entry in enumerate(reversed(data)):
                if num in entry['numbers']:
                    last_appearance = current_draw - i
                    break
            
            if last_appearance is None:
                intervals[num] = current_draw
            else:
                intervals[num] = current_draw - last_appearance
        
        return intervals
    
    def analyze_hot_cold(self, data):
        """ホット/コールド分析（改良版）"""
        if len(data) < 5:
            return {}
        
        recent_data = data[-5:]  # 最近5回
        older_data = data[-15:-5] if len(data) >= 15 else data[:-5]
        
        recent_counts = Counter()
        older_counts = Counter()
        
        for entry in recent_data:
            recent_counts.update(entry['numbers'])
        
        for entry in older_data:
            older_counts.update(entry['numbers'])
        
        hot_cold = {}
        for num in range(1, 50):
            recent_freq = recent_counts[num]
            older_freq = older_counts[num]
            
            if recent_freq > older_freq:
                hot_cold[num] = 10  # ホット
            elif recent_freq < older_freq:
                hot_cold[num] = 5   # コールド
            else:
                hot_cold[num] = 7   # 中立
        
        return hot_cold
    
    def analyze_periodicity(self, data):
        """周期性分析（改良版）"""
        if len(data) < 10:
            return {}
        
        periodicity = {}
        for num in range(1, 50):
            appearances = []
            for i, entry in enumerate(data):
                if num in entry['numbers']:
                    appearances.append(i)
            
            if len(appearances) >= 2:
                intervals = [appearances[i+1] - appearances[i] for i in range(len(appearances)-1)]
                avg_interval = statistics.mean(intervals)
                last_appearance = appearances[-1]
                current_draw = len(data)
                
                # 次の出現予測
                next_predicted = last_appearance + avg_interval
                if current_draw >= next_predicted - 2 and current_draw <= next_predicted + 2:
                    periodicity[num] = 15  # 出現予測時期
                elif current_draw >= next_predicted - 5 and current_draw <= next_predicted + 5:
                    periodicity[num] = 8   # 近い時期
                else:
                    periodicity[num] = 3   # 遠い時期
            else:
                periodicity[num] = 5
        
        return periodicity
    
    def calculate_regression_trend(self, data):
        """回帰トレンド計算（改良版）"""
        if len(data) < 5:
            return {}
        
        trend = {}
        for num in range(1, 50):
            recent_trend = 0
            for i in range(max(0, len(data)-5), len(data)):
                if num in data[i]['numbers']:
                    recent_trend += 1
            
            if recent_trend >= 3:
                trend[num] = 8   # 上昇トレンド
            elif recent_trend >= 1:
                trend[num] = 5   # 安定
            else:
                trend[num] = 3   # 下降トレンド
        
        return trend
    
    def calculate_moving_average(self, data):
        """移動平均計算（改良版）"""
        if len(data) < 3:
            return {}
        
        moving_avg = {}
        for num in range(1, 50):
            recent_avg = 0
            for i in range(max(0, len(data)-3), len(data)):
                if num in data[i]['numbers']:
                    recent_avg += 1
            
            moving_avg[num] = recent_avg * 5
        
        return moving_avg
    
    def calculate_attraction_effect(self, data):
        """引力効果計算（改良版）"""
        if len(data) < 2:
            return {}
        
        attraction = {}
        last_numbers = data[-1]['numbers']
        
        for num in range(1, 50):
            # 前回出た数字の隣接効果
            adjacent_score = 0
            for last_num in last_numbers:
                if abs(num - last_num) <= 2:
                    adjacent_score += 5
            
            attraction[num] = min(adjacent_score, 15)
        
        return attraction
    
    def analyze_distribution(self, data):
        """分布分析（改良版）"""
        if not data:
            return {}
        
        distribution = {}
        for num in range(1, 50):
            if 1 <= num <= 16:
                distribution[num] = 3  # 低範囲
            elif 17 <= num <= 32:
                distribution[num] = 5  # 中範囲
            else:
                distribution[num] = 3  # 高範囲
        
        return distribution
    
    def calculate_adjacent_correlation(self, data):
        """隣接相関計算（改良版）"""
        if len(data) < 3:
            return {}
        
        adjacent = {}
        for num in range(1, 50):
            # 最近の隣接パターンを分析
            adjacent_count = 0
            for i in range(max(0, len(data)-3), len(data)):
                numbers = data[i]['numbers']
                for n in numbers:
                    if abs(num - n) == 1:
                        adjacent_count += 1
            
            adjacent[num] = adjacent_count * 3
        
        return adjacent
    
    def generate_improved_patterns(self, scores, target_date):
        """改良されたパターン生成"""
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
                
            numbers = self.generate_strategy_pattern(top_numbers, strategy, i)
            if numbers:
                patterns.append({
                    'pattern': i + 1,
                    'numbers': numbers,
                    'strategy': strategy,
                    'confidence': 80 + i * 2  # パターン1が最も高い信頼度
                })
        
        # 6パターンに満たない場合は補完
        while len(patterns) < 6:
            pattern = self.generate_random_pattern(top_numbers, len(patterns))
            patterns.append(pattern)
        
        return patterns[:6]  # 確実に6パターン
    
    def generate_strategy_pattern(self, top_numbers, strategy, pattern_num):
        """戦略別パターン生成"""
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
        
        return sorted(random.sample(top_numbers, 6))  # フォールバック
    
    def generate_balanced_pattern(self, top_numbers):
        """バランス重視パターン"""
        low_range = [n for n in top_numbers if 1 <= n <= 16]
        mid_range = [n for n in top_numbers if 17 <= n <= 32]
        high_range = [n for n in top_numbers if 33 <= n <= 49]
        
        pattern = []
        pattern.extend(random.sample(low_range, min(2, len(low_range))))
        pattern.extend(random.sample(mid_range, min(2, len(mid_range))))
        pattern.extend(random.sample(high_range, min(2, len(high_range))))
        
        # 6個に調整
        while len(pattern) < 6:
            remaining = [n for n in top_numbers if n not in pattern]
            if remaining:
                pattern.append(random.choice(remaining))
        
        return sorted(pattern[:6])
    
    def generate_high_score_pattern(self, top_numbers):
        """高スコア重視パターン"""
        return sorted(random.sample(top_numbers[:12], 6))
    
    def generate_range_distributed_pattern(self, top_numbers):
        """範囲分散パターン"""
        ranges = [[1, 16], [17, 32], [33, 49]]
        pattern = []
        
        for start, end in ranges:
            range_numbers = [n for n in top_numbers if start <= n <= end]
            if range_numbers:
                pattern.extend(random.sample(range_numbers, min(2, len(range_numbers))))
        
        # 6個に調整
        while len(pattern) < 6:
            remaining = [n for n in top_numbers if n not in pattern]
            if remaining:
                pattern.append(random.choice(remaining))
        
        return sorted(pattern[:6])
    
    def generate_sum_controlled_pattern(self, top_numbers):
        """合計値制御パターン"""
        target_sum = 150  # 理想的な合計値
        
        best_pattern = None
        best_diff = float('inf')
        
        # 複数の組み合わせを試行
        for _ in range(50):
            pattern = sorted(random.sample(top_numbers, 6))
            current_sum = sum(pattern)
            diff = abs(current_sum - target_sum)
            
            if diff < best_diff:
                best_diff = diff
                best_pattern = pattern
        
        return best_pattern or sorted(random.sample(top_numbers, 6))
    
    def generate_non_consecutive_pattern(self, top_numbers):
        """連続回避パターン"""
        pattern = []
        candidates = top_numbers.copy()
        
        while len(pattern) < 6 and candidates:
            num = random.choice(candidates)
            candidates.remove(num)
            
            # 連続チェック
            is_consecutive = False
            for existing in pattern:
                if abs(num - existing) == 1:
                    is_consecutive = True
                    break
            
            if not is_consecutive:
                pattern.append(num)
        
        # 6個に調整
        while len(pattern) < 6:
            remaining = [n for n in top_numbers if n not in pattern]
            if remaining:
                pattern.append(random.choice(remaining))
        
        return sorted(pattern[:6])
    
    def generate_statistical_pattern(self, top_numbers):
        """統計最適化パターン"""
        # 奇数の数を調整
        odd_count = random.randint(2, 4)
        even_count = 6 - odd_count
        
        odd_numbers = [n for n in top_numbers if n % 2 == 1]
        even_numbers = [n for n in top_numbers if n % 2 == 0]
        
        pattern = []
        pattern.extend(random.sample(odd_numbers, min(odd_count, len(odd_numbers))))
        pattern.extend(random.sample(even_numbers, min(even_count, len(even_numbers))))
        
        # 6個に調整
        while len(pattern) < 6:
            remaining = [n for n in top_numbers if n not in pattern]
            if remaining:
                pattern.append(random.choice(remaining))
        
        return sorted(pattern[:6])
    
    def generate_random_pattern(self, top_numbers, pattern_num):
        """ランダムパターン生成（補完用）"""
        strategy_names = ["ランダム1", "ランダム2", "ランダム3", "ランダム4"]
        strategy = strategy_names[pattern_num % len(strategy_names)]
        
        pattern = sorted(random.sample(top_numbers, 6))
        return {
            'pattern': pattern_num + 1,
            'numbers': pattern,
            'strategy': strategy,
            'confidence': random.randint(50, 80)
        }
    
    def predict(self, target_date):
        """改良された予測実行"""
        print(f"🎯 改良版Toto丸くん - {target_date}予測")
        print("=" * 60)
        
        if not self.data:
            print("⚠️ データがありません")
            return
        
        print(f"📊 改良されたデータ分析完了（{len(self.data)}回分）")
        
        # 改良されたスコア計算
        scores = self.calculate_improved_scores(self.data)
        
        # 最近の的中率分析
        accuracy_analysis = self.analyze_recent_accuracy()
        print(f"📈 最近の平均当選数: {accuracy_analysis['average_hits']:.1f}個")
        print(f"⚖️ 調整係数: {accuracy_analysis['adjustment_factor']:.2f}")
        
        # 改良されたパターン生成
        patterns = self.generate_improved_patterns(scores, target_date)
        
        print(f"🔢 予測パターン数: {len(patterns)}")
        
        # 結果をファイルに保存
        result_file = f"results/result_improved_{target_date}.txt"
        
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"🎯 改良版Toto丸くん - {target_date}予測\n")
            f.write("=" * 60 + "\n")
            f.write(f"📊 改良されたデータ分析完了（{len(self.data)}回分）\n")
            f.write(f"📈 最近の平均当選数: {accuracy_analysis['average_hits']:.1f}個\n")
            f.write(f"⚖️ 調整係数: {accuracy_analysis['adjustment_factor']:.2f}\n")
            f.write(f"🔢 予測パターン数: {len(patterns)}\n\n")
            
            for i, pattern in enumerate(patterns, 1):
                numbers = pattern['numbers']
                strategy = pattern['strategy']
                confidence = pattern['confidence']
                
                # 改良された信頼度計算
                realistic_confidence = self.calculate_realistic_confidence(numbers, [scores.get(n, 0) for n in numbers])
                
                total = sum(numbers)
                odd_count = sum(1 for n in numbers if n % 2 == 1)
                even_count = 6 - odd_count
                
                low_count = sum(1 for n in numbers if 1 <= n <= 16)
                mid_count = sum(1 for n in numbers if 17 <= n <= 32)
                high_count = sum(1 for n in numbers if 33 <= n <= 49)
                
                f.write(f"【パターン{i}】信頼度: {realistic_confidence:.1f}% ({strategy})\n")
                f.write(f"予測数字: {numbers}\n")
                f.write(f"合計: {total} | 奇数/偶数: {odd_count}/{even_count}\n")
                f.write(f"範囲分布: 低{low_count}個, 中{mid_count}個, 高{high_count}個\n")
                f.write("-" * 60 + "\n")
                
                print(f"【パターン{i}】信頼度: {realistic_confidence:.1f}% ({strategy})")
                print(f"予測数字: {numbers}")
                print(f"合計: {total} | 奇数/偶数: {odd_count}/{even_count}")
                print(f"範囲分布: 低{low_count}個, 中{mid_count}個, 高{high_count}個")
                print("-" * 60)
            
            f.write("🎲 改良された予測完了！\n")
            f.write("=" * 60 + "\n")
        
        print("🎲 改良された予測完了！")
        print("=" * 60)
        print(f"📄 結果を {result_file} に保存しました")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("使用方法: python predictor_improved.py YYYY-MM-DD")
        sys.exit(1)
    
    target_date = sys.argv[1]
    predictor = ImprovedTotoPredictor()
    predictor.predict(target_date) 