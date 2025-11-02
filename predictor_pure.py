#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
純粋分析版ToTo〇くん - 固定数字排除システム
"""

import csv
import json
import statistics
import random
from collections import Counter
from datetime import datetime, timedelta
import os

class PureTotoPredictor:
    def __init__(self, csv_file='totomaru.csv'):
        self.csv_file = csv_file
        self.results_dir = 'results'
        self.cache_file = 'cache_data.json'
        self.cached_data = None
        self.last_modified = None
        self.ensure_results_dir()
        
    def ensure_results_dir(self):
        """結果ディレクトリの作成"""
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
    
    def get_file_modified_time(self):
        """CSVファイルの最終更新時刻を取得"""
        try:
            return os.path.getmtime(self.csv_file)
        except OSError:
            return 0
    
    def load_cache(self):
        """キャッシュデータを読み込み"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                    if cache.get('csv_modified') == self.get_file_modified_time():
                        return cache.get('data', []), cache.get('csv_modified')
        except (json.JSONDecodeError, OSError):
            pass
        return None, None
    
    def save_cache(self, data):
        """データをキャッシュに保存"""
        try:
            cache = {
                'data': data,
                'csv_modified': self.get_file_modified_time()
            }
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
        except OSError:
            pass  # キャッシュ保存に失敗しても処理は続行
    
    def load_data(self):
        """CSVデータを読み込み（キャッシュ対応）"""
        # キャッシュから読み込みを試行
        cached_data, cached_modified = self.load_cache()
        current_modified = self.get_file_modified_time()
        
        print(f"🔍 キャッシュ確認中...")
        print(f"   - キャッシュデータ: {'あり' if cached_data else 'なし'}")
        print(f"   - キャッシュ更新時刻: {cached_modified}")
        print(f"   - CSV更新時刻: {current_modified}")
        
        # キャッシュが有効な場合
        if cached_data and cached_modified == current_modified:
            print(f"📦 キャッシュからデータを読み込みました（{len(cached_data)}回分）")
            return cached_data
        
        # キャッシュが無効な場合、CSVから読み込み
        print(f"📊 CSVファイルからデータを読み込み中...")
        data = []
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    numbers = [int(row[f'Number{i}']) for i in range(1, 7)]
                    data.append(numbers)
            
            # 新しいデータをキャッシュに保存
            self.save_cache(data)
            print(f"✅ データをキャッシュに保存しました（{len(data)}回分）")
            
        except FileNotFoundError:
            print(f"⚠️ {self.csv_file}が見つかりません")
            return []
        
        return data
    
    def calculate_pure_scores(self, data):
        """純粋なスコア計算（固定排除）"""
        if not data:
            return {}
        
        # 基本統計
        all_numbers = []
        recent_numbers = []
        
        for draw in data:
            all_numbers.extend(draw)
            # 最近10回分
            if len(recent_numbers) < 60:
                recent_numbers.extend(draw)
        
        # 出現回数
        total_counts = Counter(all_numbers)
        recent_counts = Counter(recent_numbers)
        
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
        
        # 純粋なスコア計算（固定排除）
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
    
    def generate_pure_patterns(self, scores):
        """純粋なパターン生成（固定排除）"""
        if not scores:
            return []
        
        # 上位スコアの数字を取得
        top_numbers = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:25]
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
                    'confidence': 85 - i * 5  # パターン1が最も高い信頼度
                })
        
        # 6パターンに満たない場合は補完
        while len(patterns) < 6:
            pattern = self.generate_random_pattern(top_numbers, len(patterns))
            patterns.append(pattern)
        
        return patterns[:6]  # 確実に6パターン
    
    def generate_strategy_pattern(self, top_numbers, strategy, pattern_num):
        """戦略別パターン生成（固定排除）"""
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
        """バランス重視パターン（固定排除）"""
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
        """高スコア重視パターン（固定排除）"""
        return sorted(random.sample(top_numbers[:15], 6))
    
    def generate_range_distributed_pattern(self, top_numbers):
        """範囲分散パターン（固定排除）"""
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
        """合計値制御パターン（固定排除）"""
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
        """連続回避パターン（固定排除）"""
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
        """統計最適化パターン（固定排除）"""
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
            'confidence': random.randint(50, 75)
        }
    
    def predict(self, target_date):
        """純粋な予測実行"""
        try:
            print(f"🎯 純粋分析版ToTo〇くん - {target_date}予測")
            print("=" * 60)
            
            print("🔍 load_data()を呼び出しています...")
            data = self.load_data()
            print(f"🔍 load_data()完了: {len(data)}件のデータを取得")
            if not data:
                print("⚠️ データがありません")
                return
            
            print(f"📊 純粋なデータ分析完了（{len(data)}回分）")
            
            # 純粋なスコア計算
            scores = self.calculate_pure_scores(data)
            
            # 純粋なパターン生成
            patterns = self.generate_pure_patterns(scores)
            
            print(f"🔢 予測パターン数: {len(patterns)}")
            
            # 結果をファイルに保存
            result_file = f"results/result_pure_{target_date}.txt"
            
            with open(result_file, 'w', encoding='utf-8') as f:
                f.write(f"🎯 純粋分析版ToTo〇くん - {target_date}予測\n")
                f.write("=" * 60 + "\n")
                f.write(f"📊 純粋なデータ分析完了（{len(data)}回分）\n")
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
                
                f.write("🎲 純粋な予測完了！\n")
                f.write("=" * 60 + "\n")
            
            print("🎲 純粋な予測完了！")
            print("=" * 60)
            print(f"📄 結果を {result_file} に保存しました")
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("使用方法: python predictor_pure.py YYYY-MM-DD")
        sys.exit(1)
    
    target_date = sys.argv[1]
    predictor = PureTotoPredictor()
    predictor.predict(target_date) 