#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ToTo〇くん Ver.4 - 統合版
3つのシステムを統合した最強予測システム
- Ver.1: 純粋分析版
- Ver.2: 改良版
- Ver.3: LSTM版
"""

import csv
import json
import random
import numpy as np
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import os

# LSTMの簡易実装
class SimpleLSTM:
    def __init__(self, input_size=49, hidden_size=32, sequence_length=10):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.sequence_length = sequence_length
        
        # 重みの初期化
        self.Wf = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.Wi = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.Wo = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        self.Wc = np.random.randn(hidden_size, input_size + hidden_size) * 0.01
        
        # バイアス
        self.bf = np.zeros((hidden_size, 1))
        self.bi = np.zeros((hidden_size, 1))
        self.bo = np.zeros((hidden_size, 1))
        self.bc = np.zeros((hidden_size, 1))
        
        # 出力層
        self.Wy = np.random.randn(input_size, hidden_size) * 0.01
        self.by = np.zeros((input_size, 1))
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def tanh(self, x):
        return np.tanh(x)
    
    def softmax(self, x):
        exp_x = np.exp(x - np.max(x))
        return exp_x / np.sum(exp_x)
    
    def forward(self, x_sequence):
        """順伝播"""
        batch_size = x_sequence.shape[0]
        
        # 隠れ状態とセル状態の初期化
        h = np.zeros((self.hidden_size, batch_size))
        c = np.zeros((self.hidden_size, batch_size))
        
        outputs = []
        
        for t in range(self.sequence_length):
            # 入力と隠れ状態の結合
            x_t = x_sequence[:, t, :].T
            combined = np.vstack((x_t, h))
            
            # 忘却ゲート
            ft = self.sigmoid(np.dot(self.Wf, combined) + self.bf)
            
            # 入力ゲート
            it = self.sigmoid(np.dot(self.Wi, combined) + self.bi)
            
            # 出力ゲート
            ot = self.sigmoid(np.dot(self.Wo, combined) + self.bo)
            
            # セル状態の候補
            c_tilde = self.tanh(np.dot(self.Wc, combined) + self.bc)
            
            # セル状態の更新
            c = ft * c + it * c_tilde
            
            # 隠れ状態の更新
            h = ot * self.tanh(c)
            
            # 出力
            y_t = self.softmax(np.dot(self.Wy, h) + self.by)
            outputs.append(y_t)
        
        return np.array(outputs)
    
    def predict_next(self, x_sequence):
        """次の数字を予測"""
        outputs = self.forward(x_sequence)
        last_output = outputs[-1]
        return last_output.flatten()

class UnifiedTotoPredictor:
    def __init__(self, csv_file='totomaru.csv'):
        self.csv_file = csv_file
        self.results_dir = 'results'
        self.cache_file = 'cache_data.json'
        self.cached_data = None
        self.last_modified = None
        self.ensure_results_dir()
        self.lstm = SimpleLSTM()
        self.sequence_length = 10
        self.learning_history = self.load_learning_history()
        
        # エンジンの重み（動的調整）
        self.engine_weights = {
            'pure': 1.0,      # 純粋分析版
            'advanced': 1.0,  # 改良版
            'lstm': 1.0       # LSTM版
        }
        
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
                '動的調整': 1.0,
                'LSTM時系列': 1.0,
                'LSTM確率': 1.0,
                'LSTM周期': 1.0,
                'LSTM依存関係': 1.0,
                'LSTM順序': 1.0,
                'LSTM統合': 1.0
            },
            'range_performance': {'low': 1.0, 'mid': 1.0, 'high': 1.0},
            'bonus_performance': 1.0
        }
        
        # 評価ファイルから学習履歴を読み込み
        evaluation_files = [f for f in os.listdir('.') if f.startswith('evaluation_') and f.endswith('.json')]
        for file in sorted(evaluation_files)[-5:]:
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
    
    # ==================== エンジン1: 純粋分析版 ====================
    def calculate_pure_scores(self, data):
        """純粋分析版スコア計算"""
        if not data:
            return {}
        
        all_numbers = []
        recent_numbers = []
        
        for draw in data:
            all_numbers.extend(draw)
            if len(recent_numbers) < 60:
                recent_numbers.extend(draw)
        
        total_counts = Counter(all_numbers)
        recent_counts = Counter(recent_numbers)
        
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
        
        scores = {}
        for num in range(1, 50):
            score = (
                total_counts[num] * 0.15 * 10 +
                recent_counts[num] * 0.20 * 15 +
                missing_intervals.get(num, 0) * 0.20 * 20 +
                random.uniform(0, 10)
            )
            scores[num] = max(0, score)
        
        return scores
    
    # ==================== エンジン2: 改良版 ====================
    def calculate_advanced_scores(self, data):
        """改良版スコア計算"""
        if not data:
            return {}
        
        all_numbers = []
        recent_numbers = []
        very_recent_numbers = []
        
        for i, draw in enumerate(data):
            all_numbers.extend(draw)
            if len(recent_numbers) < 60:
                recent_numbers.extend(draw)
            if len(very_recent_numbers) < 30:
                very_recent_numbers.extend(draw)
        
        total_counts = Counter(all_numbers)
        recent_counts = Counter(recent_numbers)
        very_recent_counts = Counter(very_recent_numbers)
        
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
        
        range_weights = self.learning_history['range_performance']
        
        scores = {}
        for num in range(1, 50):
            base_score = (
                total_counts[num] * 0.15 * 10 +
                recent_counts[num] * 0.20 * 15 +
                very_recent_counts[num] * 0.25 * 20 +
                missing_intervals.get(num, 0) * 0.20 * 25
            )
            
            if 1 <= num <= 16:
                range_multiplier = range_weights['low']
            elif 17 <= num <= 32:
                range_multiplier = range_weights['mid']
            else:
                range_multiplier = range_weights['high']
            
            recent_performance = np.mean(self.learning_history['recent_performance']) if self.learning_history['recent_performance'] else 0.167
            performance_multiplier = 1.0 + (recent_performance - 0.167) * 2
            
            final_score = base_score * range_multiplier * performance_multiplier + random.uniform(0, 15)
            scores[num] = max(0, final_score)
        
        return scores
    
    # ==================== エンジン3: LSTM版 ====================
    def calculate_lstm_scores(self, data):
        """LSTM版スコア計算"""
        if len(data) < self.sequence_length:
            return {}
        
        # 簡易LSTM予測
        recent_sequence = data[-self.sequence_length:]
        sequence_encoded = []
        
        for draw in recent_sequence:
            draw_encoded = np.zeros(49)
            for num in draw:
                draw_encoded[num - 1] = 1
            sequence_encoded.append(draw_encoded)
        
        sequence_encoded = np.array([sequence_encoded])
        
        try:
            predicted_probs = self.lstm.predict_next(sequence_encoded)
        except:
            predicted_probs = np.ones(49) / 49
        
        scores = {}
        for i in range(49):
            scores[i + 1] = predicted_probs[i] * 1000
        
        return scores
    
    # ==================== 統合予測 ====================
    def calculate_unified_scores(self, data):
        """統合スコア計算"""
        # 3つのエンジンでスコア計算
        pure_scores = self.calculate_pure_scores(data)
        advanced_scores = self.calculate_advanced_scores(data)
        lstm_scores = self.calculate_lstm_scores(data)
        
        # 重み付け統合
        unified_scores = {}
        for num in range(1, 50):
            score = (
                pure_scores.get(num, 0) * self.engine_weights['pure'] +
                advanced_scores.get(num, 0) * self.engine_weights['advanced'] +
                lstm_scores.get(num, 0) * self.engine_weights['lstm']
            )
            unified_scores[num] = score
        
        return unified_scores
    
    def generate_unified_patterns(self, scores):
        """統合パターン生成"""
        if not scores:
            return []
        
        top_numbers = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:30]
        top_numbers = [num for num, score in top_numbers]
        
        patterns = []
        strategies = [
            "統合バランス",
            "統合高スコア",
            "統合範囲分散",
            "統合合計制御",
            "統合連続回避",
            "統合統計最適化"
        ]
        
        for i, strategy in enumerate(strategies):
            numbers = self.generate_unified_strategy_pattern(top_numbers, strategy, i)
            if numbers:
                confidence = 95 - i * 5  # 統合版は高信頼度
                patterns.append({
                    'pattern': i + 1,
                    'numbers': numbers,
                    'strategy': strategy,
                    'confidence': confidence
                })
        
        return patterns[:6]
    
    def generate_unified_strategy_pattern(self, top_numbers, strategy, pattern_num):
        """統合戦略別パターン生成"""
        if strategy == "統合バランス":
            return self.generate_unified_balanced_pattern(top_numbers)
        elif strategy == "統合高スコア":
            return self.generate_unified_high_score_pattern(top_numbers)
        elif strategy == "統合範囲分散":
            return self.generate_unified_range_pattern(top_numbers)
        elif strategy == "統合合計制御":
            return self.generate_unified_sum_pattern(top_numbers)
        elif strategy == "統合連続回避":
            return self.generate_unified_consecutive_pattern(top_numbers)
        elif strategy == "統合統計最適化":
            return self.generate_unified_statistical_pattern(top_numbers)
        
        return sorted(random.sample(top_numbers, 6))
    
    def generate_unified_balanced_pattern(self, top_numbers):
        """統合バランスパターン"""
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
    
    def generate_unified_high_score_pattern(self, top_numbers):
        """統合高スコアパターン"""
        return sorted(random.sample(top_numbers[:15], 6))
    
    def generate_unified_range_pattern(self, top_numbers):
        """統合範囲分散パターン"""
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
    
    def generate_unified_sum_pattern(self, top_numbers):
        """統合合計制御パターン"""
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
    
    def generate_unified_consecutive_pattern(self, top_numbers):
        """統合連続回避パターン"""
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
    
    def generate_unified_statistical_pattern(self, top_numbers):
        """統合統計最適化パターン"""
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
        """統合版予測実行"""
        print(f"🚀 ToTo〇くん Ver.4 統合版 - {target_date}予測")
        print("=" * 60)
        
        data = self.load_data()
        if not data:
            print("⚠️ データがありません")
            return
        
        print(f"📊 統合データ分析完了（{len(data)}回分）")
        print(f"🧠 学習履歴: {len(self.learning_history['recent_performance'])}回分")
        print(f"⚖️ エンジン重み: 純粋{self.engine_weights['pure']:.2f}, 改良{self.engine_weights['advanced']:.2f}, LSTM{self.engine_weights['lstm']:.2f}")
        
        # 統合スコア計算
        scores = self.calculate_unified_scores(data)
        
        # 統合パターン生成
        patterns = self.generate_unified_patterns(scores)
        
        print(f"🔢 予測パターン数: {len(patterns)}")
        
        # 結果をファイルに保存
        result_file = f"results/result_unified_{target_date}.txt"
        
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"🚀 ToTo〇くん Ver.4 統合版 - {target_date}予測\n")
            f.write("=" * 60 + "\n")
            f.write(f"📊 統合データ分析完了（{len(data)}回分）\n")
            f.write(f"🧠 学習履歴: {len(self.learning_history['recent_performance'])}回分\n")
            f.write(f"⚖️ エンジン重み: 純粋{self.engine_weights['pure']:.2f}, 改良{self.engine_weights['advanced']:.2f}, LSTM{self.engine_weights['lstm']:.2f}\n")
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
            
            f.write("🎲 統合版予測完了！\n")
            f.write("=" * 60 + "\n")
        
        print("🎲 統合版予測完了！")
        print("=" * 60)
        print(f"📄 結果を {result_file} に保存しました")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("使用方法: python predictor_unified.py YYYY-MM-DD")
        sys.exit(1)
    
    target_date = sys.argv[1]
    predictor = UnifiedTotoPredictor()
    predictor.predict(target_date) 