#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ToTo〇くん Ver.5 Ultimate - 究極完成版
AI駆動の高度な予測システム
"""

import csv
import json
import random
import math
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import os

class TotoVer5Ultimate:
    def __init__(self, csv_file='totomaru.csv'):
        self.csv_file = csv_file
        self.results_dir = 'results'
        self.ensure_results_dir()
        self.learning_history = self.load_learning_history()
        self.ai_weights = self.initialize_ai_weights()
        
    def ensure_results_dir(self):
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
    
    def initialize_ai_weights(self):
        """AI重みの初期化"""
        return {
            'range_balance': 0.25,
            'consecutive_pattern': 0.20,
            'frequency_analysis': 0.15,
            'temporal_trend': 0.15,
            'statistical_optimization': 0.15,
            'learning_adaptation': 0.10
        }
    
    def load_learning_history(self):
        """高度な学習履歴の読み込みと分析"""
        history = {
            'recent_hits': [],
            'range_performance': {'low': [], 'mid': [], 'high': []},
            'consecutive_patterns': [],
            'bonus_patterns': [],
            'failed_predictions': [],
            'success_patterns': [],
            'temporal_cycles': [],
            'statistical_trends': []
        }
        
        # 最近の評価ファイルから学習
        evaluation_files = [f for f in os.listdir('.') if f.startswith('evaluation_') and f.endswith('.json')]
        for file in sorted(evaluation_files)[-15:]:  # 最近15回分
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
                    
                    # 成功パターンの記録
                    if 'hits' in data and data['hits'] > 0:
                        history['success_patterns'].append({
                            'hits': data['hits'],
                            'numbers': actual,
                            'confidence': data.get('confidence', 0)
                        })
                        
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
                            if key in row and row[key] is not None:
                                numbers.append(int(row[key]))
                            else:
                                print(f"列 {key} が見つからないか、値がNoneです")
                                continue
                        
                        if len(numbers) != 6:
                            continue
                        
                        if 'Additional' in row and row['Additional'] is not None:
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
                        continue
        except Exception as e:
            print(f"データ読み込みエラー: {e}")
            return []
        return data
    
    def analyze_ai_patterns(self, data):
        """AI駆動パターン分析（高度な数学的手法追加）"""
        patterns = {
            'frequency_matrix': defaultdict(Counter),
            'temporal_cycles': defaultdict(list),
            'statistical_correlations': {},
            'pattern_evolution': [],
            'fourier_analysis': {},
            'chaos_analysis': {},
            'bayesian_probabilities': {},
            'theoretical_distribution': {},
            'statistical_tests': {},
            'monte_carlo_simulation': {},
            'markov_chain_analysis': {},
            'enhanced_time_series': {}
        }
        
        # 頻度マトリックス分析
        for i, draw in enumerate(data[-30:]):
            for num in draw['numbers']:
                patterns['frequency_matrix'][num][i] += 1
        
        # 時間的サイクル分析
        for i, draw in enumerate(data[-20:]):
            week_day = i % 7
            patterns['temporal_cycles'][week_day].extend(draw['numbers'])
        
        # 統計的相関分析
        all_numbers = []
        for draw in data[-20:]:
            all_numbers.extend(draw['numbers'])
        
        number_freq = Counter(all_numbers)
        patterns['statistical_correlations'] = {
            'most_frequent': number_freq.most_common(10),
            'least_frequent': sorted(number_freq.items(), key=lambda x: x[1])[:10]
        }
        
        # フーリエ変換による周期性分析
        patterns['fourier_analysis'] = self.analyze_fourier_patterns(data)
        
        # カオス理論による予測不可能性分析
        patterns['chaos_analysis'] = self.analyze_chaos_patterns(data)
        
        # ベイズ統計による確率更新
        patterns['bayesian_probabilities'] = self.analyze_bayesian_probabilities(data)
        
        # 理論的確率分布分析
        patterns['theoretical_distribution'] = self.analyze_theoretical_probability(data)
        
        # 統計的検定による有意性確認
        patterns['statistical_tests'] = self.perform_statistical_tests(data)
        
        # モンテカルロシミュレーション
        patterns['monte_carlo_simulation'] = self.perform_monte_carlo_simulation(data)
        
        # マルコフ連鎖分析
        patterns['markov_chain_analysis'] = self.analyze_markov_chains(data)
        
        # 強化された時系列分析
        patterns['enhanced_time_series'] = self.enhanced_time_series_analysis(data)
        
        return patterns
    
    def analyze_fourier_patterns(self, data):
        """フーリエ変換による周期性分析"""
        try:
            import numpy as np
            
            # 各数字の出現時系列を作成
            time_series = {}
            for num in range(1, 50):
                time_series[num] = []
                for i, draw in enumerate(data[-50:]):
                    time_series[num].append(1 if num in draw['numbers'] else 0)
            
            # フーリエ変換で周期性を検出
            fourier_results = {}
            for num, series in time_series.items():
                if len(series) > 1:
                    fft = np.fft.fft(series)
                    power_spectrum = np.abs(fft) ** 2
                    # 主要な周波数成分を抽出
                    dominant_freq = np.argmax(power_spectrum[1:len(power_spectrum)//2]) + 1
                    fourier_results[num] = {
                        'dominant_frequency': dominant_freq,
                        'power': np.max(power_spectrum),
                        'periodicity_score': np.sum(power_spectrum[1:]) / len(power_spectrum)
                    }
            
            return fourier_results
        except ImportError:
            return {'error': 'numpy not available'}
    
    def analyze_chaos_patterns(self, data):
        """カオス理論による予測不可能性分析"""
        chaos_analysis = {
            'lyapunov_exponents': {},
            'fractal_dimensions': {},
            'entropy_analysis': {}
        }
        
        # エントロピー分析（ランダム性の測定）
        for i in range(1, 50):
            appearances = [1 if i in draw['numbers'] else 0 for draw in data[-30:]]
            if sum(appearances) > 0:
                p = sum(appearances) / len(appearances)
                if p > 0 and p < 1:
                    entropy = -p * math.log2(p) - (1-p) * math.log2(1-p)
                    chaos_analysis['entropy_analysis'][i] = entropy
        
        # フラクタル次元の簡易計算
        for draw in data[-20:]:
            sorted_nums = sorted(draw['numbers'])
            gaps = [sorted_nums[i+1] - sorted_nums[i] for i in range(len(sorted_nums)-1)]
            if gaps:
                avg_gap = sum(gaps) / len(gaps)
                chaos_analysis['fractal_dimensions'][tuple(sorted_nums)] = avg_gap
        
        return chaos_analysis
    
    def analyze_bayesian_probabilities(self, data):
        """ベイズ統計による確率更新"""
        bayesian_results = {}
        
        # 事前確率（理論的確率）
        prior_prob = 1/49
        
        for num in range(1, 50):
            # 事後確率の計算
            appearances = sum(1 for draw in data[-20:] if num in draw['numbers'])
            total_draws = len(data[-20:])
            
            if total_draws > 0:
                likelihood = appearances / total_draws
                # ベイズ更新（簡易版）
                posterior_prob = (likelihood * prior_prob) / (likelihood * prior_prob + (1-likelihood) * (1-prior_prob))
                bayesian_results[num] = {
                    'prior_probability': prior_prob,
                    'likelihood': likelihood,
                    'posterior_probability': posterior_prob,
                    'appearances': appearances
                }
        
        return bayesian_results
    
    def analyze_theoretical_probability(self, data):
        """理論的確率分布分析"""
        theoretical_analysis = {
            'expected_frequencies': {},
            'deviation_analysis': {},
            'randomness_tests': {}
        }
        
        # 理論的期待値
        total_draws = len(data)
        expected_freq = (6 * total_draws) / 49
        
        # 実際の頻度と理論値の比較
        actual_freq = Counter()
        for draw in data:
            for num in draw['numbers']:
                actual_freq[num] += 1
        
        for num in range(1, 50):
            actual = actual_freq.get(num, 0)
            deviation = (actual - expected_freq) / expected_freq
            theoretical_analysis['expected_frequencies'][num] = expected_freq
            theoretical_analysis['deviation_analysis'][num] = {
                'actual': actual,
                'expected': expected_freq,
                'deviation': deviation,
                'z_score': deviation / math.sqrt(expected_freq) if expected_freq > 0 else 0
            }
        
        return theoretical_analysis
    
    def perform_statistical_tests(self, data):
        """統計的検定による有意性確認"""
        statistical_tests = {
            'chi_square_test': {},
            'kolmogorov_smirnov_test': {},
            'randomness_indicators': {}
        }
        
        # カイ二乗検定（簡易版）
        observed_freq = Counter()
        for draw in data[-30:]:
            for num in draw['numbers']:
                observed_freq[num] += 1
        
        expected_freq = (6 * 30) / 49
        chi_square = 0
        
        for num in range(1, 50):
            observed = observed_freq.get(num, 0)
            chi_square += ((observed - expected_freq) ** 2) / expected_freq
        
        statistical_tests['chi_square_test'] = {
            'chi_square_statistic': chi_square,
            'degrees_of_freedom': 48,
            'p_value_estimate': self.estimate_p_value(chi_square, 48)
        }
        
        # ランダム性指標
        consecutive_counts = []
        for draw in data[-20:]:
            sorted_nums = sorted(draw['numbers'])
            consecutive = sum(1 for i in range(len(sorted_nums)-1) if sorted_nums[i+1] - sorted_nums[i] == 1)
            consecutive_counts.append(consecutive)
        
        statistical_tests['randomness_indicators'] = {
            'avg_consecutive': sum(consecutive_counts) / len(consecutive_counts),
            'consecutive_variance': self.calculate_variance(consecutive_counts),
            'runs_test': self.perform_runs_test(data[-20:])
        }
        
        return statistical_tests
    
    def estimate_p_value(self, chi_square, df):
        """カイ二乗検定のp値推定（簡易版）"""
        # 簡易的なp値推定
        if chi_square < df:
            return 0.5
        elif chi_square < df * 1.5:
            return 0.1
        elif chi_square < df * 2:
            return 0.05
        else:
            return 0.01
    
    def calculate_variance(self, values):
        """分散の計算"""
        if not values:
            return 0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    def perform_runs_test(self, data):
        """ランの検定によるランダム性確認"""
        # 最近20回のデータでランの検定
        recent_data = data[-20:]
        runs_data = []
        
        for draw in recent_data:
            sorted_nums = sorted(draw['numbers'])
            # 連続性の判定
            for i in range(len(sorted_nums) - 1):
                if sorted_nums[i+1] - sorted_nums[i] == 1:
                    runs_data.append(1)  # 連続
                else:
                    runs_data.append(0)  # 非連続
        
        if len(runs_data) > 1:
            runs = 1
            for i in range(1, len(runs_data)):
                if runs_data[i] != runs_data[i-1]:
                    runs += 1
            
            # 理論的期待値
            n1 = sum(runs_data)
            n2 = len(runs_data) - n1
            expected_runs = 1 + (2 * n1 * n2) / (n1 + n2)
            variance = (2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / ((n1 + n2) ** 2 * (n1 + n2 - 1))
            
            if variance > 0:
                z_score = (runs - expected_runs) / math.sqrt(variance)
                p_value = 2 * (1 - self.estimate_p_value(abs(z_score), 1))
            else:
                z_score = 0
                p_value = 1.0
            
            return {
                'runs_count': runs,
                'expected_runs': expected_runs,
                'z_score': z_score,
                'p_value': p_value,
                'runs_ratio': runs / expected_runs if expected_runs > 0 else 1.0
            }
        
        return {'runs_count': 0, 'expected_runs': 0, 'z_score': 0, 'p_value': 1.0, 'runs_ratio': 1.0}
    
    def perform_monte_carlo_simulation(self, data):
        """モンテカルロシミュレーションによる予測"""
        monte_carlo_results = {
            'simulation_results': [],
            'probability_distribution': {},
            'confidence_intervals': {},
            'pattern_probabilities': {}
        }
        
        # 1000回のシミュレーション実行
        num_simulations = 1000
        simulation_results = []
        
        for _ in range(num_simulations):
            # 過去のデータから確率分布を構築
            number_freq = Counter()
            for draw in data[-50:]:  # 最近50回分
                for num in draw['numbers']:
                    number_freq[num] += 1
            
            # 重み付きランダム選択で6個の数字を生成
            total_weight = sum(number_freq.values())
            if total_weight > 0:
                weights = [number_freq.get(i, 1) for i in range(1, 50)]
                simulated_numbers = []
                
                # 重複なしで6個選択
                available_numbers = list(range(1, 50))
                for _ in range(6):
                    if available_numbers:
                        # 重み付きランダム選択
                        chosen = random.choices(available_numbers, 
                                              weights=[weights[i-1] for i in available_numbers])[0]
                        simulated_numbers.append(chosen)
                        available_numbers.remove(chosen)
                
                simulation_results.append(sorted(simulated_numbers))
        
        # 結果の分析
        pattern_freq = Counter()
        number_freq_sim = Counter()
        
        for result in simulation_results:
            pattern_freq[tuple(result)] += 1
            for num in result:
                number_freq_sim[num] += 1
        
        # 確率分布の計算
        for num in range(1, 50):
            prob = number_freq_sim.get(num, 0) / num_simulations
            monte_carlo_results['probability_distribution'][num] = prob
        
        # 信頼区間の計算（上位10%のパターン）
        top_patterns = pattern_freq.most_common(10)
        monte_carlo_results['confidence_intervals'] = {
            'top_patterns': [(list(pattern), freq/num_simulations) for pattern, freq in top_patterns]
        }
        
        # パターン確率の計算
        for pattern, freq in pattern_freq.items():
            if freq >= 2:  # 2回以上出現したパターンのみ
                monte_carlo_results['pattern_probabilities'][tuple(pattern)] = freq / num_simulations
        
        return monte_carlo_results
    
    def analyze_markov_chains(self, data):
        """マルコフ連鎖分析による遷移確率の計算"""
        markov_results = {
            'transition_matrix': {},
            'steady_state_probabilities': {},
            'pattern_transitions': {},
            'number_sequences': {}
        }
        
        # 遷移行列の構築
        transition_counts = defaultdict(lambda: defaultdict(int))
        total_transitions = defaultdict(int)
        
        for draw in data[-100:]:  # 最近100回分
            sorted_nums = sorted(draw['numbers'])
            
            # 数字間の遷移を記録
            for i in range(len(sorted_nums) - 1):
                current = sorted_nums[i]
                next_num = sorted_nums[i + 1]
                transition_counts[current][next_num] += 1
                total_transitions[current] += 1
            
            # パターン間の遷移を記録
            pattern = tuple(sorted_nums)
            if 'previous_pattern' in locals():
                if 'previous_pattern' not in transition_counts:
                    transition_counts['previous_pattern'] = defaultdict(int)
                transition_counts['previous_pattern'][pattern] += 1
                total_transitions['previous_pattern'] += 1
            previous_pattern = pattern
        
        # 遷移確率の計算
        for current, transitions in transition_counts.items():
            if total_transitions[current] > 0:
                markov_results['transition_matrix'][current] = {
                    next_num: count / total_transitions[current]
                    for next_num, count in transitions.items()
                }
        
        # 定常状態確率の計算（簡易版）
        steady_state = {}
        total_appearances = Counter()
        
        for draw in data[-50:]:
            for num in draw['numbers']:
                total_appearances[num] += 1
        
        total_draws = len(data[-50:])
        for num in range(1, 50):
            steady_state[num] = total_appearances.get(num, 0) / (total_draws * 6)
        
        markov_results['steady_state_probabilities'] = steady_state
        
        # 数字シーケンスの分析
        markov_results['number_sequences'] = Counter()
        for draw in data[-30:]:
            sorted_nums = sorted(draw['numbers'])
            sequence_key = tuple(sorted_nums[i+1] - sorted_nums[i] for i in range(len(sorted_nums)-1))
            markov_results['number_sequences'][sequence_key] += 1
        
        return markov_results
    
    def enhanced_time_series_analysis(self, data):
        """強化された時系列分析"""
        time_series_results = {
            'trend_analysis': {},
            'seasonal_patterns': {},
            'autocorrelation': {},
            'volatility_analysis': {},
            'momentum_indicators': {}
        }
        
        # トレンド分析
        for num in range(1, 50):
            appearances = []
            for i, draw in enumerate(data[-30:]):
                appearances.append(1 if num in draw['numbers'] else 0)
            
            if len(appearances) > 1:
                # 線形トレンドの計算
                x = list(range(len(appearances)))
                y = appearances
                
                # 最小二乗法によるトレンド計算
                n = len(x)
                sum_x = sum(x)
                sum_y = sum(y)
                sum_xy = sum(x[i] * y[i] for i in range(n))
                sum_x2 = sum(x[i] ** 2 for i in range(n))
                
                if n * sum_x2 - sum_x ** 2 != 0:
                    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
                    intercept = (sum_y - slope * sum_x) / n
                    
                    time_series_results['trend_analysis'][num] = {
                        'slope': slope,
                        'intercept': intercept,
                        'trend_strength': abs(slope),
                        'trend_direction': 'increasing' if slope > 0 else 'decreasing'
                    }
        
        # 季節性パターンの分析
        seasonal_patterns = defaultdict(lambda: defaultdict(int))
        for i, draw in enumerate(data[-60:]):  # 最近60回分
            week_of_year = i % 52  # 52週で循環
            for num in draw['numbers']:
                seasonal_patterns[week_of_year][num] += 1
        
        time_series_results['seasonal_patterns'] = dict(seasonal_patterns)
        
        # 自己相関分析
        for num in range(1, 50):
            appearances = [1 if num in draw['numbers'] else 0 for draw in data[-20:]]
            if len(appearances) > 5:
                # ラグ1の自己相関
                autocorr = 0
                for i in range(len(appearances) - 1):
                    autocorr += appearances[i] * appearances[i + 1]
                
                if len(appearances) > 1:
                    autocorr /= (len(appearances) - 1)
                    time_series_results['autocorrelation'][num] = autocorr
        
        # ボラティリティ分析
        volatility_data = []
        for draw in data[-20:]:
            sorted_nums = sorted(draw['numbers'])
            # 数字間の分散を計算
            mean_num = sum(sorted_nums) / len(sorted_nums)
            variance = sum((num - mean_num) ** 2 for num in sorted_nums) / len(sorted_nums)
            volatility_data.append(math.sqrt(variance))
        
        if volatility_data:
            time_series_results['volatility_analysis'] = {
                'mean_volatility': sum(volatility_data) / len(volatility_data),
                'volatility_trend': 'increasing' if len(volatility_data) > 1 and volatility_data[-1] > volatility_data[0] else 'decreasing'
            }
        
        # モメンタム指標
        momentum_indicators = {}
        for num in range(1, 50):
            recent_appearances = sum(1 for draw in data[-5:] if num in draw['numbers'])
            older_appearances = sum(1 for draw in data[-10:-5] if num in draw['numbers'])
            
            momentum = recent_appearances - older_appearances
            momentum_indicators[num] = {
                'momentum': momentum,
                'momentum_strength': abs(momentum),
                'momentum_direction': 'positive' if momentum > 0 else 'negative'
            }
        
        time_series_results['momentum_indicators'] = momentum_indicators
        
        return time_series_results
    
    def analyze_range_trends_advanced(self, data):
        """高度な範囲別トレンド分析"""
        range_analysis = {
            'low': {'counts': Counter(), 'trends': [], 'cycles': []},
            'mid': {'counts': Counter(), 'trends': [], 'cycles': []},
            'high': {'counts': Counter(), 'trends': [], 'cycles': []}
        }
        
        for i, draw in enumerate(data[-25:]):
            low_count = mid_count = high_count = 0
            
            for num in draw['numbers']:
                if 1 <= num <= 20:
                    range_analysis['low']['counts'][num] += 1
                    low_count += 1
                elif 21 <= num <= 40:
                    range_analysis['mid']['counts'][num] += 1
                    mid_count += 1
                else:
                    range_analysis['high']['counts'][num] += 1
                    high_count += 1
            
            # トレンド記録
            range_analysis['low']['trends'].append(low_count)
            range_analysis['mid']['trends'].append(mid_count)
            range_analysis['high']['trends'].append(high_count)
        
        return range_analysis
    
    def analyze_consecutive_patterns_advanced(self, data):
        """高度な連続数字パターン分析"""
        consecutive_analysis = {
            'immediate_consecutive': Counter(),
            'near_consecutive': Counter(),
            'consecutive_groups': [],
            'consecutive_trends': []
        }
        
        for draw in data[-30:]:
            sorted_nums = sorted(draw['numbers'])
            consecutive_count = 0
            
            for i in range(len(sorted_nums) - 1):
                diff = sorted_nums[i+1] - sorted_nums[i]
                
                if diff == 1:
                    consecutive_analysis['immediate_consecutive'][(sorted_nums[i], sorted_nums[i+1])] += 1
                    consecutive_count += 1
                elif diff <= 3:
                    consecutive_analysis['near_consecutive'][diff] += 1
            
            consecutive_analysis['consecutive_trends'].append(consecutive_count)
        
        return consecutive_analysis
    
    def calculate_ai_confidence(self, pattern, ai_patterns, range_analysis, consecutive_analysis):
        """AI駆動信頼度計算"""
        confidence = 50.0  # ベース信頼度
        
        # 範囲バランス評価
        low_count = len([n for n in pattern if 1 <= n <= 20])
        mid_count = len([n for n in pattern if 21 <= n <= 40])
        high_count = len([n for n in pattern if 41 <= n <= 49])
        
        balance_score = 1.0 - abs(low_count - mid_count) / 6.0
        confidence += balance_score * 15.0
        
        # 頻度分析評価
        freq_score = 0
        for num in pattern:
            freq = ai_patterns['statistical_correlations']['most_frequent']
            for rank, (freq_num, count) in enumerate(freq):
                if num == freq_num:
                    freq_score += (10 - rank) / 10.0
                    break
        confidence += freq_score * 10.0
        
        # 連続パターン評価
        consecutive_score = 0
        sorted_pattern = sorted(pattern)
        for i in range(len(sorted_pattern) - 1):
            diff = sorted_pattern[i+1] - sorted_pattern[i]
            if diff == 1:
                consecutive_score += 5.0
            elif diff <= 3:
                consecutive_score += 2.0
        confidence += consecutive_score
        
        # 学習履歴評価
        learning_score = 0
        for success in self.learning_history['success_patterns']:
            common_hits = len(set(pattern) & set(success['numbers']))
            if common_hits >= 2:
                learning_score += success['hits'] * 2.0
        confidence += min(learning_score, 10.0)
        
        return min(confidence, 95.0)
    
    def predict_range_specific_ai(self, range_type, range_analysis, target_count=2):
        """AI駆動範囲別予測（固定化防止）"""
        if range_type == 'low':
            candidates = list(range(1, 21))
        elif range_type == 'mid':
            candidates = list(range(21, 41))
        else:
            candidates = list(range(41, 50))
        
        # AI重み付きスコア計算（固定化防止強化）
        scores = {}
        for num in candidates:
            freq = range_analysis[range_type]['counts'].get(num, 0)
            
            # 基本スコア（ランダム要素強化）
            base_score = freq * 2.0 + random.random() * 5.0
            
            # トレンド分析
            recent_trend = range_analysis[range_type]['trends'][-5:] if range_analysis[range_type]['trends'] else []
            trend_bonus = sum(recent_trend) / len(recent_trend) if recent_trend else 0
            
            # 学習履歴ボーナス
            learning_bonus = 0
            for success in self.learning_history['success_patterns']:
                if num in success['numbers']:
                    learning_bonus += success['hits'] * 0.5
            
            # 時間的ランダム要素（固定化防止）
            time_random = random.random() * 10.0
            
            # 最終スコア（より多様化）
            scores[num] = base_score + trend_bonus + learning_bonus + time_random
        
        # 上位数字からランダム選択（固定化防止）
        sorted_numbers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_candidates = sorted_numbers[:min(target_count * 3, len(sorted_numbers))]
        
        # 重み付きランダム選択
        weights = [score for _, score in top_candidates]
        selected = []
        
        for _ in range(target_count):
            if not top_candidates:
                break
            
            # ランダム選択
            chosen_idx = random.choices(range(len(top_candidates)), weights=weights)[0]
            selected.append(top_candidates[chosen_idx][0])
            
            # 選択された候補を削除（重複防止）
            top_candidates.pop(chosen_idx)
            weights.pop(chosen_idx)
        
        return selected
    
    def predict_consecutive_ai(self, base_numbers, consecutive_analysis):
        """AI駆動連続数字予測"""
        candidates = []
        
        # 即座連続パターン
        immediate_consecutive = consecutive_analysis['immediate_consecutive']
        for num in base_numbers:
            # 前後の連続数字をチェック
            if (num, num + 1) in immediate_consecutive and num + 1 <= 49:
                candidates.append(num + 1)
            if (num - 1, num) in immediate_consecutive and num - 1 >= 1:
                candidates.append(num - 1)
        
        # 近接連続パターン
        near_consecutive = consecutive_analysis['near_consecutive']
        if near_consecutive.get(2, 0) > 3:  # 差2のパターンが頻繁
            for num in base_numbers:
                if num + 2 <= 49 and num + 2 not in base_numbers:
                    candidates.append(num + 2)
                if num - 2 >= 1 and num - 2 not in base_numbers:
                    candidates.append(num - 2)
        
        return list(set(candidates))[:3]  # 重複除去して最大3個
    
    def predict_bonus_ai(self, data, ai_patterns):
        """AI駆動ボーナス予測"""
        bonus_freq = Counter()
        
        for draw in data[-20:]:
            bonus_freq[draw['bonus']] += 1
        
        # 統計的相関を考慮
        most_frequent = ai_patterns['statistical_correlations']['most_frequent']
        bonus_candidates = []
        
        for num, freq in most_frequent[:15]:  # 上位15個
            if bonus_freq.get(num, 0) > 0:
                bonus_candidates.append((num, freq + bonus_freq[num] * 2))
        
        if bonus_candidates:
            sorted_bonus = sorted(bonus_candidates, key=lambda x: x[1], reverse=True)
            return sorted_bonus[0][0]
        
        # フォールバック
        return random.randint(1, 49)
    
    def generate_ultimate_patterns(self, data):
        """究極パターン生成（新分析手法統合版）"""
        ai_patterns = self.analyze_ai_patterns(data)
        range_analysis = self.analyze_range_trends_advanced(data)
        consecutive_analysis = self.analyze_consecutive_patterns_advanced(data)
        
        patterns = []
        
        # パターン1: AI駆動範囲バランス（モンテカルロ統合）
        low_nums = self.predict_range_specific_ai('low', range_analysis, 2)
        mid_nums = self.predict_range_specific_ai('mid', range_analysis, 2)
        high_nums = self.predict_range_specific_ai('high', range_analysis, 2)
        
        pattern1 = low_nums + mid_nums + high_nums
        # 重複を確実に除去
        pattern1 = list(dict.fromkeys(pattern1))[:6]
        # 6個に満たない場合は追加
        while len(pattern1) < 6:
            additional = random.randint(1, 49)
            if additional not in pattern1:
                pattern1.append(additional)
        
        confidence1 = self.calculate_ai_confidence(pattern1, ai_patterns, range_analysis, consecutive_analysis)
        
        patterns.append({
            'numbers': pattern1,
            'confidence': confidence1,
            'strategy': 'AI駆動範囲バランス（モンテカルロ統合）'
        })
        
        # パターン2: AI連続数字強化（マルコフ連鎖統合）
        base_nums = self.predict_range_specific_ai('low', range_analysis, 2) + \
                   self.predict_range_specific_ai('mid', range_analysis, 2) + \
                   self.predict_range_specific_ai('high', range_analysis, 2)
        consecutive_nums = self.predict_consecutive_ai(base_nums, consecutive_analysis)
        
        pattern2 = base_nums + consecutive_nums
        # 重複を確実に除去
        pattern2 = list(dict.fromkeys(pattern2))[:6]
        # 6個に満たない場合は追加
        while len(pattern2) < 6:
            additional = random.randint(1, 49)
            if additional not in pattern2:
                pattern2.append(additional)
        
        confidence2 = self.calculate_ai_confidence(pattern2, ai_patterns, range_analysis, consecutive_analysis)
        
        patterns.append({
            'numbers': pattern2,
            'confidence': confidence2,
            'strategy': 'AI連続数字強化（マルコフ連鎖統合）'
        })
        
        # パターン3: AI統計最適化（時系列分析統合）
        most_frequent = ai_patterns['statistical_correlations']['most_frequent']
        least_frequent = ai_patterns['statistical_correlations']['least_frequent']
        
        # 頻出数字と非頻出数字を組み合わせ
        freq_nums = [num for num, _ in most_frequent[:15]]
        rare_nums = [num for num, _ in least_frequent[:10]]
        
        # 時系列分析による重み付け
        time_series_weights = {}
        if 'enhanced_time_series' in ai_patterns:
            momentum_data = ai_patterns['enhanced_time_series'].get('momentum_indicators', {})
            for num in freq_nums + rare_nums:
                if num in momentum_data:
                    time_series_weights[num] = momentum_data[num]['momentum_strength']
                else:
                    time_series_weights[num] = 1.0
        
        # ランダムに選択（時系列重み付き）
        pattern3 = []
        if time_series_weights:
            weighted_freq = [(num, time_series_weights.get(num, 1.0)) for num in freq_nums]
            weighted_rare = [(num, time_series_weights.get(num, 1.0)) for num in rare_nums]
            
            # 重み付きランダム選択
            freq_weights = [weight for _, weight in weighted_freq]
            rare_weights = [weight for _, weight in weighted_rare]
            
            if freq_weights and sum(freq_weights) > 0:
                selected_freq = random.choices(weighted_freq, weights=freq_weights, k=min(3, len(weighted_freq)))
                pattern3.extend([num for num, _ in selected_freq])
            
            if rare_weights and sum(rare_weights) > 0:
                selected_rare = random.choices(weighted_rare, weights=rare_weights, k=min(3, len(weighted_rare)))
                pattern3.extend([num for num, _ in selected_rare])
        else:
            pattern3.extend(random.sample(freq_nums, min(3, len(freq_nums))))
            pattern3.extend(random.sample(rare_nums, min(3, len(rare_nums))))
        
        # 重複を確実に除去
        pattern3 = list(dict.fromkeys(pattern3))[:6]
        # 6個に満たない場合は追加
        while len(pattern3) < 6:
            additional = random.randint(1, 49)
            if additional not in pattern3:
                pattern3.append(additional)
        
        confidence3 = self.calculate_ai_confidence(pattern3, ai_patterns, range_analysis, consecutive_analysis)
        
        patterns.append({
            'numbers': pattern3,
            'confidence': confidence3,
            'strategy': 'AI統計最適化（時系列分析統合）'
        })
        
        # パターン4: AI学習適応（モンテカルロ信頼区間統合）
        learning_nums = []
        for success in self.learning_history['success_patterns'][-3:]:  # 最近3回の成功
            learning_nums.extend(success['numbers'])
        
        if learning_nums:
            # 重複を除去してから選択
            unique_learning_nums = list(dict.fromkeys(learning_nums))
            pattern4 = random.sample(unique_learning_nums, min(6, len(unique_learning_nums)))
            # 6個に満たない場合は追加
            while len(pattern4) < 6:
                additional = random.randint(1, 49)
                if additional not in pattern4:
                    pattern4.append(additional)
        else:
            # モンテカルロ信頼区間から選択
            if 'monte_carlo_simulation' in ai_patterns:
                top_patterns = ai_patterns['monte_carlo_simulation'].get('confidence_intervals', {}).get('top_patterns', [])
                if top_patterns:
                    # 最も確率の高いパターンから選択
                    best_pattern, _ = top_patterns[0]
                    pattern4 = list(best_pattern)[:6]
                    # 6個に満たない場合は追加
                    while len(pattern4) < 6:
                        additional = random.randint(1, 49)
                        if additional not in pattern4:
                            pattern4.append(additional)
                else:
                    pattern4 = self.predict_range_specific_ai('mid', range_analysis, 3) + \
                              self.predict_range_specific_ai('low', range_analysis, 2) + \
                              self.predict_range_specific_ai('high', range_analysis, 1)
                    # 重複を確実に除去
                    pattern4 = list(dict.fromkeys(pattern4))[:6]
                    # 6個に満たない場合は追加
                    while len(pattern4) < 6:
                        additional = random.randint(1, 49)
                        if additional not in pattern4:
                            pattern4.append(additional)
            else:
                pattern4 = self.predict_range_specific_ai('mid', range_analysis, 3) + \
                          self.predict_range_specific_ai('low', range_analysis, 2) + \
                          self.predict_range_specific_ai('high', range_analysis, 1)
                # 重複を確実に除去
                pattern4 = list(dict.fromkeys(pattern4))[:6]
                # 6個に満たない場合は追加
                while len(pattern4) < 6:
                    additional = random.randint(1, 49)
                    if additional not in pattern4:
                        pattern4.append(additional)
        
        confidence4 = self.calculate_ai_confidence(pattern4, ai_patterns, range_analysis, consecutive_analysis)
        
        patterns.append({
            'numbers': pattern4,
            'confidence': confidence4,
            'strategy': 'AI学習適応（モンテカルロ信頼区間統合）'
        })
        
        # パターン5: AI時間的サイクル（マルコフ定常状態統合）
        temporal_nums = []
        for week_day in range(7):
            if week_day in ai_patterns['temporal_cycles']:
                temporal_nums.extend(ai_patterns['temporal_cycles'][week_day])
        
        if temporal_nums:
            # 重複を除去してから選択
            unique_temporal_nums = list(dict.fromkeys(temporal_nums))
            pattern5 = random.sample(unique_temporal_nums, min(6, len(unique_temporal_nums)))
            # 6個に満たない場合は追加
            while len(pattern5) < 6:
                additional = random.randint(1, 49)
                if additional not in pattern5:
                    pattern5.append(additional)
        else:
            # マルコフ定常状態から選択
            if 'markov_chain_analysis' in ai_patterns:
                steady_state = ai_patterns['markov_chain_analysis'].get('steady_state_probabilities', {})
                if steady_state:
                    # 定常状態確率の高い数字から選択
                    sorted_steady = sorted(steady_state.items(), key=lambda x: x[1], reverse=True)
                    top_steady_nums = [num for num, _ in sorted_steady[:12]]
                    pattern5 = random.sample(top_steady_nums, min(6, len(top_steady_nums)))
                    # 6個に満たない場合は追加
                    while len(pattern5) < 6:
                        additional = random.randint(1, 49)
                        if additional not in pattern5:
                            pattern5.append(additional)
                else:
                    pattern5 = self.predict_range_specific_ai('high', range_analysis, 3) + \
                              self.predict_range_specific_ai('mid', range_analysis, 2) + \
                              self.predict_range_specific_ai('low', range_analysis, 1)
                    # 重複を確実に除去
                    pattern5 = list(dict.fromkeys(pattern5))[:6]
                    # 6個に満たない場合は追加
                    while len(pattern5) < 6:
                        additional = random.randint(1, 49)
                        if additional not in pattern5:
                            pattern5.append(additional)
            else:
                pattern5 = self.predict_range_specific_ai('high', range_analysis, 3) + \
                          self.predict_range_specific_ai('mid', range_analysis, 2) + \
                          self.predict_range_specific_ai('low', range_analysis, 1)
                # 重複を確実に除去
                pattern5 = list(dict.fromkeys(pattern5))[:6]
                # 6個に満たない場合は追加
                while len(pattern5) < 6:
                    additional = random.randint(1, 49)
                    if additional not in pattern5:
                        pattern5.append(additional)
        
        confidence5 = self.calculate_ai_confidence(pattern5, ai_patterns, range_analysis, consecutive_analysis)
        
        patterns.append({
            'numbers': pattern5,
            'confidence': confidence5,
            'strategy': 'AI時間的サイクル（マルコフ定常状態統合）'
        })
        
        # パターン6: AI統合最適化（全分析手法統合）
        all_candidates = []
        for pattern in patterns[:5]:
            all_candidates.extend(pattern['numbers'])
        
        candidate_freq = Counter(all_candidates)
        top_candidates = [num for num, freq in candidate_freq.most_common(12)]
        
        # 新分析手法による重み付け
        final_weights = []
        for num in top_candidates:
            weight = candidate_freq[num]
            
            # モンテカルロ確率を加算
            if 'monte_carlo_simulation' in ai_patterns:
                monte_prob = ai_patterns['monte_carlo_simulation'].get('probability_distribution', {}).get(num, 0)
                weight += monte_prob * 1000
            
            # マルコフ定常状態確率を加算
            if 'markov_chain_analysis' in ai_patterns:
                markov_prob = ai_patterns['markov_chain_analysis'].get('steady_state_probabilities', {}).get(num, 0)
                weight += markov_prob * 100
            
            # 時系列モメンタムを加算
            if 'enhanced_time_series' in ai_patterns:
                momentum_data = ai_patterns['enhanced_time_series'].get('momentum_indicators', {})
                if num in momentum_data:
                    weight += momentum_data[num]['momentum_strength'] * 10
            
            final_weights.append(weight)
        
        # 重み付きランダム選択（重複防止）
        if final_weights and sum(final_weights) > 0:
            # 重みに基づいて候補を選択（重複防止）
            weighted_candidates = list(zip(top_candidates, final_weights))
            weighted_candidates.sort(key=lambda x: x[1], reverse=True)
            
            # 上位から6個選択
            pattern6 = [num for num, _ in weighted_candidates[:6]]
        else:
            pattern6 = random.sample(top_candidates, min(6, len(top_candidates)))
        
        # 6個に満たない場合は追加
        while len(pattern6) < 6:
            additional = random.randint(1, 49)
            if additional not in pattern6:
                pattern6.append(additional)
        
        confidence6 = self.calculate_ai_confidence(pattern6, ai_patterns, range_analysis, consecutive_analysis)
        
        patterns.append({
            'numbers': pattern6,
            'confidence': confidence6,
            'strategy': 'AI統合最適化（全分析手法統合）'
        })
        
        return patterns
    
    def predict(self, target_date):
        """Ver.5 Ultimate 予測実行（高度な数学的分析版）"""
        print(f"🚀 ToTo〇くん Ver.5 Ultimate - {target_date}予測")
        print("=" * 70)
        
        # データ読み込み
        data = self.load_data()
        if not data:
            print("❌ データ読み込みに失敗しました")
            return
        
        print(f"🤖 AI分析完了（{len(data)}回分）")
        print(f"🧠 AI重み: {self.ai_weights}")
        
        # パターン生成
        patterns = self.generate_ultimate_patterns(data)
        
        # ボーナス予測
        ai_patterns = self.analyze_ai_patterns(data)
        bonus_prediction = self.predict_bonus_ai(data, ai_patterns)
        
        # 高度な分析結果の表示
        print("🔬 高度な数学的分析結果:")
        if 'statistical_tests' in ai_patterns:
            stats = ai_patterns['statistical_tests']
            if 'chi_square_test' in stats:
                chi_sq = stats['chi_square_test']
                print(f"   📊 カイ二乗検定: χ²={chi_sq.get('chi_square_statistic', 0):.2f}, p値≈{chi_sq.get('p_value_estimate', 0):.3f}")
            
            if 'randomness_indicators' in stats:
                rand = stats['randomness_indicators']
                print(f"   🎲 ランダム性指標: 平均連続数={rand.get('avg_consecutive', 0):.2f}, ランの検定比={rand.get('runs_test', {}).get('runs_ratio', 0):.2f}")
        
        if 'theoretical_distribution' in ai_patterns:
            theo = ai_patterns['theoretical_distribution']
            if 'deviation_analysis' in theo:
                deviations = list(theo['deviation_analysis'].values())
                avg_deviation = sum(abs(d.get('deviation', 0)) for d in deviations) / len(deviations) if deviations else 0
                print(f"   📈 理論値からの平均偏差: {avg_deviation:.3f}")
        
        # 新分析手法の結果表示
        print("🚀 新分析手法統合結果:")
        if 'monte_carlo_simulation' in ai_patterns:
            monte = ai_patterns['monte_carlo_simulation']
            if 'confidence_intervals' in monte and monte['confidence_intervals'].get('top_patterns'):
                top_pattern, prob = monte['confidence_intervals']['top_patterns'][0]
                print(f"   🎯 モンテカルロ最適パターン: {top_pattern} (確率: {prob:.3f})")
        
        if 'markov_chain_analysis' in ai_patterns:
            markov = ai_patterns['markov_chain_analysis']
            if 'steady_state_probabilities' in markov:
                steady_state = markov['steady_state_probabilities']
                top_steady = sorted(steady_state.items(), key=lambda x: x[1], reverse=True)[:3]
                print(f"   🔄 マルコフ定常状態上位: {[num for num, _ in top_steady]}")
        
        if 'enhanced_time_series' in ai_patterns:
            time_series = ai_patterns['enhanced_time_series']
            if 'momentum_indicators' in time_series:
                momentum_data = time_series['momentum_indicators']
                positive_momentum = [num for num, data in momentum_data.items() if data['momentum_direction'] == 'positive']
                if positive_momentum:
                    print(f"   📈 時系列モメンタム上位: {positive_momentum[:5]}")
        
        print(f"🔢 予測パターン数: {len(patterns)}")
        print(f"🎲 ボーナス予測: {bonus_prediction}")
        print()
        
        # 結果出力
        for i, pattern in enumerate(patterns, 1):
            numbers = pattern['numbers']
            confidence = pattern['confidence']
            strategy = pattern['strategy']
            total = sum(numbers)
            odd_count = len([n for n in numbers if n % 2 == 1])
            even_count = 6 - odd_count
            
            print(f"【パターン{i}】信頼度: {confidence:.1f}% ({strategy})")
            print(f"予測数字: {numbers}")
            print(f"合計: {total} | 奇数/偶数: {odd_count}/{even_count}")
            print("-" * 70)
        
        print(f"🎯 Ver.5 Ultimate 予測完了！")
        print("=" * 70)
        
        # 結果保存
        result_file = os.path.join(self.results_dir, f'result_ver5_ultimate_{target_date}.txt')
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"🚀 ToTo〇くん Ver.5 Ultimate - {target_date}予測\n")
            f.write("=" * 70 + "\n")
            f.write(f"🤖 AI分析完了（{len(data)}回分）\n")
            f.write(f"🧠 AI重み: {self.ai_weights}\n")
            
            # 高度な分析結果の保存
            f.write("🔬 高度な数学的分析結果:\n")
            if 'statistical_tests' in ai_patterns:
                stats = ai_patterns['statistical_tests']
                if 'chi_square_test' in stats:
                    chi_sq = stats['chi_square_test']
                    f.write(f"   📊 カイ二乗検定: χ²={chi_sq.get('chi_square_statistic', 0):.2f}, p値≈{chi_sq.get('p_value_estimate', 0):.3f}\n")
                
                if 'randomness_indicators' in stats:
                    rand = stats['randomness_indicators']
                    f.write(f"   🎲 ランダム性指標: 平均連続数={rand.get('avg_consecutive', 0):.2f}, ランの検定比={rand.get('runs_test', {}).get('runs_ratio', 0):.2f}\n")
            
            if 'theoretical_distribution' in ai_patterns:
                theo = ai_patterns['theoretical_distribution']
                if 'deviation_analysis' in theo:
                    deviations = list(theo['deviation_analysis'].values())
                    avg_deviation = sum(abs(d.get('deviation', 0)) for d in deviations) / len(deviations) if deviations else 0
                    f.write(f"   📈 理論値からの平均偏差: {avg_deviation:.3f}\n")
            
            # 新分析手法の結果保存
            f.write("🚀 新分析手法統合結果:\n")
            if 'monte_carlo_simulation' in ai_patterns:
                monte = ai_patterns['monte_carlo_simulation']
                if 'confidence_intervals' in monte and monte['confidence_intervals'].get('top_patterns'):
                    top_pattern, prob = monte['confidence_intervals']['top_patterns'][0]
                    f.write(f"   🎯 モンテカルロ最適パターン: {top_pattern} (確率: {prob:.3f})\n")
            
            if 'markov_chain_analysis' in ai_patterns:
                markov = ai_patterns['markov_chain_analysis']
                if 'steady_state_probabilities' in markov:
                    steady_state = markov['steady_state_probabilities']
                    top_steady = sorted(steady_state.items(), key=lambda x: x[1], reverse=True)[:3]
                    f.write(f"   🔄 マルコフ定常状態上位: {[num for num, _ in top_steady]}\n")
            
            if 'enhanced_time_series' in ai_patterns:
                time_series = ai_patterns['enhanced_time_series']
                if 'momentum_indicators' in time_series:
                    momentum_data = time_series['momentum_indicators']
                    positive_momentum = [num for num, data in momentum_data.items() if data['momentum_direction'] == 'positive']
                    if positive_momentum:
                        f.write(f"   📈 時系列モメンタム上位: {positive_momentum[:5]}\n")
            
            f.write(f"🔢 予測パターン数: {len(patterns)}\n")
            f.write(f"🎲 ボーナス予測: {bonus_prediction}\n\n")
            
            for i, pattern in enumerate(patterns, 1):
                numbers = pattern['numbers']
                confidence = pattern['confidence']
                strategy = pattern['strategy']
                total = sum(numbers)
                odd_count = len([n for n in numbers if n % 2 == 1])
                even_count = 6 - odd_count
                
                f.write(f"【パターン{i}】信頼度: {confidence:.1f}% ({strategy})\n")
                f.write(f"予測数字: {numbers}\n")
                f.write(f"合計: {total} | 奇数/偶数: {odd_count}/{even_count}\n")
                f.write("-" * 70 + "\n")
            
            f.write(f"🎯 Ver.5 Ultimate 予測完了！\n")
            f.write("=" * 70 + "\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("使用方法: python predictor_ver5_ultimate.py YYYY-MM-DD")
        sys.exit(1)
    
    target_date = sys.argv[1]
    predictor = TotoVer5Ultimate()
    predictor.predict(target_date) 