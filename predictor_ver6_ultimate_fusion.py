import csv
import json
import random
import math
from collections import Counter, defaultdict
from datetime import datetime
import os

class TotoVer6UltimateFusion:
    """ToTo〇くん Ver.6 Ultimate Fusion - 全機能統合次世代システム"""
    
    def __init__(self, csv_file='totomaru.csv'):
        self.csv_file = csv_file
        self.ai_weights = self.initialize_ai_weights()
        self.learning_history = self.load_learning_history()
        self.ensure_results_dir()
    
    def ensure_results_dir(self):
        """結果ディレクトリの確保"""
        if not os.path.exists('results'):
            os.makedirs('results')
    
    def initialize_ai_weights(self):
        """AI重みの初期化（全機能統合版）"""
        return {
            'range_balance': 0.15,
            'consecutive_pattern': 0.12,
            'frequency_analysis': 0.12,
            'temporal_trend': 0.10,
            'statistical_optimization': 0.12,
            'learning_adaptation': 0.08,
            'monte_carlo': 0.10,
            'markov_chain': 0.08,
            'time_series': 0.08,
            'fourier_analysis': 0.05
        }
    
    def load_learning_history(self):
        """学習履歴の読み込み"""
        try:
            with open('learning_history.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'success_patterns': [],
                'failure_patterns': [],
                'accuracy_trends': [],
                'weight_adjustments': []
            }
    
    def save_learning_history(self):
        """学習履歴の保存"""
        with open('learning_history.json', 'w', encoding='utf-8') as f:
            json.dump(self.learning_history, f, ensure_ascii=False, indent=2)
    
    def load_data(self):
        """CSVデータの読み込み（キャッシュ最適化版）"""
        try:
            data = []
            with open(self.csv_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        # BOMを除去してキーを正規化
                        normalized_row = {}
                        for key, value in row.items():
                            normalized_key = key.replace('\ufeff', '')
                            normalized_row[normalized_key] = value
                        
                        if normalized_row['DrawDate'] and normalized_row['Number1'] and normalized_row['Number1'].strip():
                            numbers = [
                                int(normalized_row['Number1']), int(normalized_row['Number2']), int(normalized_row['Number3']),
                                int(normalized_row['Number4']), int(normalized_row['Number5']), int(normalized_row['Number6'])
                            ]
                            data.append({
                                'date': normalized_row['DrawDate'],
                                'numbers': numbers,
                                'additional': int(normalized_row['Additional']) if normalized_row['Additional'] and normalized_row['Additional'].strip() else 0
                            })
                    except (ValueError, KeyError) as e:
                        continue
            return data
        except Exception as e:
            print(f"❌ データ読み込みエラー: {e}")
            return []
    
    def analyze_all_functions(self, data):
        """全機能統合分析"""
        analysis = {}
        
        # 基本分析
        analysis['range_analysis'] = self.analyze_range_distribution(data)
        analysis['consecutive_analysis'] = self.analyze_consecutive_patterns(data)
        analysis['frequency_analysis'] = self.analyze_frequency_patterns(data)
        analysis['temporal_analysis'] = self.analyze_temporal_patterns(data)
        
        # 高度な数学的分析
        analysis['statistical_tests'] = self.perform_statistical_tests(data)
        analysis['fourier_analysis'] = self.analyze_fourier_patterns(data)
        analysis['bayesian_analysis'] = self.analyze_bayesian_probabilities(data)
        analysis['theoretical_analysis'] = self.analyze_theoretical_probability(data)
        
        # 新分析手法
        analysis['monte_carlo_simulation'] = self.perform_monte_carlo_simulation(data)
        analysis['markov_chain_analysis'] = self.analyze_markov_chains(data)
        analysis['enhanced_time_series'] = self.enhanced_time_series_analysis(data)
        
        # 学習履歴分析
        analysis['learning_analysis'] = self.analyze_learning_patterns()
        
        return analysis
    
    def analyze_range_distribution(self, data):
        """範囲分布分析"""
        ranges = {'low': [], 'mid': [], 'high': []}
        for draw in data[-30:]:
            for num in draw['numbers']:
                if 1 <= num <= 16:
                    ranges['low'].append(num)
                elif 17 <= num <= 32:
                    ranges['mid'].append(num)
                else:
                    ranges['high'].append(num)
        
        return {
            'low_freq': Counter(ranges['low']),
            'mid_freq': Counter(ranges['mid']),
            'high_freq': Counter(ranges['high']),
            'range_balance': {
                'low_ratio': len(ranges['low']) / (len(ranges['low']) + len(ranges['mid']) + len(ranges['high'])),
                'mid_ratio': len(ranges['mid']) / (len(ranges['low']) + len(ranges['mid']) + len(ranges['high'])),
                'high_ratio': len(ranges['high']) / (len(ranges['low']) + len(ranges['mid']) + len(ranges['high']))
            }
        }
    
    def analyze_consecutive_patterns(self, data):
        """連続数字パターン分析"""
        consecutive_stats = {'pairs': Counter(), 'triples': Counter(), 'frequency': 0}
        
        for draw in data[-30:]:
            sorted_nums = sorted(draw['numbers'])
            consecutive_count = 0
            
            for i in range(len(sorted_nums) - 1):
                if sorted_nums[i+1] - sorted_nums[i] == 1:
                    consecutive_count += 1
                    pair = (sorted_nums[i], sorted_nums[i+1])
                    consecutive_stats['pairs'][pair] += 1
            
            if consecutive_count >= 2:
                consecutive_stats['frequency'] += 1
        
        consecutive_stats['frequency'] /= len(data[-30:])
        return consecutive_stats
    
    def analyze_frequency_patterns(self, data):
        """頻度パターン分析"""
        all_numbers = []
        for draw in data[-50:]:
            all_numbers.extend(draw['numbers'])
        
        freq_counter = Counter(all_numbers)
        most_frequent = freq_counter.most_common(15)
        least_frequent = freq_counter.most_common()[:-16:-1]
        
        return {
            'most_frequent': most_frequent,
            'least_frequent': least_frequent,
            'frequency_distribution': dict(freq_counter)
        }
    
    def analyze_temporal_patterns(self, data):
        """時間的パターン分析"""
        temporal_cycles = defaultdict(list)
        
        for draw in data[-30:]:
            try:
                date_obj = datetime.strptime(draw['date'], '%Y-%m-%d')
                weekday = date_obj.weekday()
                temporal_cycles[weekday].extend(draw['numbers'])
            except:
                continue
        
        return dict(temporal_cycles)
    
    def perform_statistical_tests(self, data):
        """統計的検定"""
        observed_freq = Counter()
        for draw in data[-30:]:
            for num in draw['numbers']:
                observed_freq[num] += 1
        
        expected_freq = (6 * 30) / 49
        chi_square = sum(((observed_freq.get(num, 0) - expected_freq) ** 2) / expected_freq for num in range(1, 50))
        
        return {
            'chi_square_test': {
                'chi_square_statistic': chi_square,
                'degrees_of_freedom': 48,
                'p_value_estimate': self.estimate_p_value(chi_square, 48)
            }
        }
    
    def analyze_fourier_patterns(self, data):
        """フーリエ変換分析"""
        try:
            import numpy as np
            
            time_series = {}
            for num in range(1, 50):
                time_series[num] = []
                for draw in data[-50:]:
                    time_series[num].append(1 if num in draw['numbers'] else 0)
            
            fourier_results = {}
            for num, series in time_series.items():
                if len(series) > 1:
                    fft = np.fft.fft(series)
                    power_spectrum = np.abs(fft) ** 2
                    dominant_freq = np.argmax(power_spectrum[1:len(power_spectrum)//2]) + 1
                    fourier_results[num] = {
                        'dominant_frequency': dominant_freq,
                        'power': np.max(power_spectrum),
                        'periodicity_score': np.sum(power_spectrum[1:]) / len(power_spectrum)
                    }
            
            return fourier_results
        except ImportError:
            return {}
    
    def analyze_bayesian_probabilities(self, data):
        """ベイズ統計分析"""
        bayesian_results = {}
        prior_prob = 1/49
        
        for num in range(1, 50):
            appearances = sum(1 for draw in data[-20:] if num in draw['numbers'])
            total_draws = len(data[-20:])
            
            if total_draws > 0:
                likelihood = appearances / total_draws
                posterior_prob = (likelihood * prior_prob) / (likelihood * prior_prob + (1-likelihood) * (1-prior_prob))
                bayesian_results[num] = {
                    'posterior_probability': posterior_prob,
                    'appearances': appearances
                }
        
        return bayesian_results
    
    def analyze_theoretical_probability(self, data):
        """理論的確率分析"""
        total_draws = len(data)
        expected_freq = (6 * total_draws) / 49
        
        actual_freq = Counter()
        for draw in data:
            for num in draw['numbers']:
                actual_freq[num] += 1
        
        deviation_analysis = {}
        for num in range(1, 50):
            actual = actual_freq.get(num, 0)
            deviation = (actual - expected_freq) / expected_freq
            deviation_analysis[num] = {
                'actual': actual,
                'expected': expected_freq,
                'deviation': deviation
            }
        
        return {'deviation_analysis': deviation_analysis}
    
    def perform_monte_carlo_simulation(self, data):
        """モンテカルロシミュレーション"""
        # 最近の出現頻度に基づく確率分布
        recent_freq = Counter()
        for draw in data[-20:]:
            for num in draw['numbers']:
                recent_freq[num] += 1
        
        # 確率分布の正規化
        total_appearances = sum(recent_freq.values())
        probability_distribution = {}
        for num in range(1, 50):
            probability_distribution[num] = recent_freq.get(num, 0) / total_appearances if total_appearances > 0 else 1/49
        
        # シミュレーション実行
        simulations = []
        for _ in range(1000):
            sim_numbers = []
            for _ in range(6):
                weights = [probability_distribution[i] for i in range(1, 50)]
                chosen = random.choices(range(1, 50), weights=weights)[0]
                if chosen not in sim_numbers:
                    sim_numbers.append(chosen)
            if len(sim_numbers) == 6:
                simulations.append(tuple(sorted(sim_numbers)))
        
        sim_counter = Counter(simulations)
        top_patterns = sim_counter.most_common(10)
        
        return {
            'probability_distribution': probability_distribution,
            'top_patterns': top_patterns
        }
    
    def analyze_markov_chains(self, data):
        """マルコフ連鎖分析"""
        # 数字の遷移確率を計算
        transitions = defaultdict(Counter)
        number_sequences = []
        
        for draw in data[-30:]:
            sorted_nums = sorted(draw['numbers'])
            number_sequences.append(sorted_nums)
            
            for i in range(len(sorted_nums) - 1):
                current = sorted_nums[i]
                next_num = sorted_nums[i + 1]
                transitions[current][next_num] += 1
        
        # 遷移確率の計算
        transition_probabilities = {}
        for current, next_counts in transitions.items():
            total = sum(next_counts.values())
            transition_probabilities[current] = {next_num: count/total for next_num, count in next_counts.items()}
        
        # 定常状態確率の簡易計算
        steady_state = {}
        for num in range(1, 50):
            steady_state[num] = sum(1 for seq in number_sequences if num in seq) / len(number_sequences)
        
        return {
            'transition_probabilities': dict(transition_probabilities),
            'steady_state_probabilities': steady_state
        }
    
    def enhanced_time_series_analysis(self, data):
        """強化時系列分析"""
        # トレンド分析
        trend_analysis = {}
        for num in range(1, 50):
            appearances = []
            for i, draw in enumerate(data[-20:]):
                appearances.append(1 if num in draw['numbers'] else 0)
            
            if sum(appearances) > 0:
                # 単純なトレンド計算
                recent_trend = sum(appearances[-5:]) - sum(appearances[:5])
                trend_analysis[num] = {
                    'trend': recent_trend,
                    'recent_frequency': sum(appearances[-5:]) / 5,
                    'overall_frequency': sum(appearances) / len(appearances)
                }
        
        # モメンタム指標
        momentum_indicators = {}
        for num in range(1, 50):
            recent_appearances = sum(1 for draw in data[-5:] if num in draw['numbers'])
            previous_appearances = sum(1 for draw in data[-10:-5] if num in draw['numbers'])
            
            momentum = recent_appearances - previous_appearances
            momentum_indicators[num] = {
                'momentum_strength': abs(momentum),
                'momentum_direction': 'positive' if momentum > 0 else 'negative' if momentum < 0 else 'neutral'
            }
        
        return {
            'trend_analysis': trend_analysis,
            'momentum_indicators': momentum_indicators
        }
    
    def analyze_learning_patterns(self):
        """学習パターン分析"""
        if not self.learning_history['success_patterns']:
            return {}
        
        # 成功パターンから学習
        successful_numbers = []
        for success in self.learning_history['success_patterns'][-5:]:
            successful_numbers.extend(success['numbers'])
        
        success_freq = Counter(successful_numbers)
        
        return {
            'successful_numbers': dict(success_freq),
            'success_patterns': self.learning_history['success_patterns'][-3:]
        }
    
    def estimate_p_value(self, chi_square, df):
        """p値推定"""
        if chi_square < df:
            return 0.5
        elif chi_square < df * 1.5:
            return 0.1
        elif chi_square < df * 2:
            return 0.05
        else:
            return 0.01
    
    def calculate_unified_confidence(self, pattern, all_analysis):
        """統合信頼度計算"""
        confidence = 50.0  # ベース信頼度
        
        # 範囲バランス評価
        range_analysis = all_analysis['range_analysis']
        low_count = len([n for n in pattern if 1 <= n <= 16])
        mid_count = len([n for n in pattern if 17 <= n <= 32])
        high_count = len([n for n in pattern if 33 <= n <= 49])
        
        balance_score = 1 - abs(low_count - mid_count) / 6 - abs(mid_count - high_count) / 6
        confidence += balance_score * 10
        
        # 頻度分析評価
        freq_analysis = all_analysis['frequency_analysis']
        freq_score = 0
        for num in pattern:
            if num in freq_analysis['frequency_distribution']:
                freq_score += freq_analysis['frequency_distribution'][num]
        confidence += (freq_score / len(pattern)) * 5
        
        # ベイズ確率評価
        bayesian_analysis = all_analysis['bayesian_analysis']
        bayesian_score = 0
        for num in pattern:
            if num in bayesian_analysis:
                bayesian_score += bayesian_analysis[num]['posterior_probability']
        confidence += (bayesian_score / len(pattern)) * 10
        
        # モンテカルロ確率評価
        monte_carlo = all_analysis['monte_carlo_simulation']
        monte_score = 0
        for num in pattern:
            if num in monte_carlo['probability_distribution']:
                monte_score += monte_carlo['probability_distribution'][num]
        confidence += (monte_score / len(pattern)) * 8
        
        # 時系列モメンタム評価
        time_series = all_analysis['enhanced_time_series']
        momentum_score = 0
        for num in pattern:
            if num in time_series['momentum_indicators']:
                momentum_score += time_series['momentum_indicators'][num]['momentum_strength']
        confidence += (momentum_score / len(pattern)) * 5
        
        return min(95.0, max(5.0, confidence))
    
    def generate_fusion_patterns(self, data):
        """全機能統合パターン生成"""
        all_analysis = self.analyze_all_functions(data)
        patterns = []
        
        # パターン1: 統計的最適化アプローチ
        pattern1 = self.generate_statistical_optimization_pattern(all_analysis)
        confidence1 = self.calculate_unified_confidence(pattern1, all_analysis)
        patterns.append({
            'numbers': pattern1,
            'confidence': confidence1,
            'strategy': '統計的最適化アプローチ（全機能統合）'
        })
        
        # パターン2: 機械学習アプローチ
        pattern2 = self.generate_machine_learning_pattern(all_analysis)
        confidence2 = self.calculate_unified_confidence(pattern2, all_analysis)
        patterns.append({
            'numbers': pattern2,
            'confidence': confidence2,
            'strategy': '機械学習アプローチ（全機能統合）'
        })
        
        # パターン3: 確率論アプローチ
        pattern3 = self.generate_probabilistic_pattern(all_analysis)
        confidence3 = self.calculate_unified_confidence(pattern3, all_analysis)
        patterns.append({
            'numbers': pattern3,
            'confidence': confidence3,
            'strategy': '確率論アプローチ（全機能統合）'
        })
        
        # パターン4: 時系列分析アプローチ
        pattern4 = self.generate_time_series_pattern(all_analysis)
        confidence4 = self.calculate_unified_confidence(pattern4, all_analysis)
        patterns.append({
            'numbers': pattern4,
            'confidence': confidence4,
            'strategy': '時系列分析アプローチ（全機能統合）'
        })
        
        # パターン5: パターン認識アプローチ
        pattern5 = self.generate_pattern_recognition_pattern(all_analysis)
        confidence5 = self.calculate_unified_confidence(pattern5, all_analysis)
        patterns.append({
            'numbers': pattern5,
            'confidence': confidence5,
            'strategy': 'パターン認識アプローチ（全機能統合）'
        })
        
        # パターン6: 統合最適化アプローチ
        pattern6 = self.generate_integrated_optimization_pattern(all_analysis, patterns[:5])
        confidence6 = self.calculate_unified_confidence(pattern6, all_analysis)
        patterns.append({
            'numbers': pattern6,
            'confidence': confidence6,
            'strategy': '統合最適化アプローチ（全機能統合）'
        })
        
        return patterns
    
    def generate_statistical_optimization_pattern(self, all_analysis):
        """統計的最適化パターン生成"""
        candidates = []
        
        # 統計的検定で有意な数字
        statistical_tests = all_analysis['statistical_tests']
        if 'chi_square_test' in statistical_tests:
            chi_sq = statistical_tests['chi_square_test']
            if chi_sq.get('p_value_estimate', 1) > 0.05:
                # ランダム性が確認された場合、理論値に近い数字を選択
                theoretical = all_analysis['theoretical_analysis']['deviation_analysis']
                sorted_theoretical = sorted(theoretical.items(), key=lambda x: abs(x[1]['deviation']))
                candidates.extend([num for num, _ in sorted_theoretical[:20]])
        
        # ベイズ確率の高い数字
        bayesian = all_analysis['bayesian_analysis']
        sorted_bayesian = sorted(bayesian.items(), key=lambda x: x[1]['posterior_probability'], reverse=True)
        candidates.extend([num for num, _ in sorted_bayesian[:15]])
        
        # 重複除去して6個選択
        unique_candidates = list(dict.fromkeys(candidates))
        if len(unique_candidates) >= 6:
            return random.sample(unique_candidates, 6)
        else:
            # 不足分を補完
            remaining = [i for i in range(1, 50) if i not in unique_candidates]
            return unique_candidates + random.sample(remaining, 6 - len(unique_candidates))
    
    def generate_machine_learning_pattern(self, all_analysis):
        """機械学習パターン生成"""
        candidates = []
        
        # 学習履歴から成功パターンを学習
        learning = all_analysis['learning_analysis']
        if 'successful_numbers' in learning:
            sorted_learning = sorted(learning['successful_numbers'].items(), key=lambda x: x[1], reverse=True)
            candidates.extend([num for num, _ in sorted_learning[:10]])
        
        # 頻度分析で安定した数字
        frequency = all_analysis['frequency_analysis']
        sorted_frequency = sorted(frequency['frequency_distribution'].items(), key=lambda x: x[1], reverse=True)
        candidates.extend([num for num, _ in sorted_frequency[:15]])
        
        # 時系列トレンドで上昇中の数字
        time_series = all_analysis['enhanced_time_series']
        positive_trend = [num for num, data in time_series['trend_analysis'].items() if data['trend'] > 0]
        candidates.extend(positive_trend[:10])
        
        # 重複除去して6個選択
        unique_candidates = list(dict.fromkeys(candidates))
        if len(unique_candidates) >= 6:
            return random.sample(unique_candidates, 6)
        else:
            remaining = [i for i in range(1, 50) if i not in unique_candidates]
            return unique_candidates + random.sample(remaining, 6 - len(unique_candidates))
    
    def generate_probabilistic_pattern(self, all_analysis):
        """確率論パターン生成"""
        candidates = []
        
        # モンテカルロシミュレーションの高確率パターン
        monte_carlo = all_analysis['monte_carlo_simulation']
        if 'top_patterns' in monte_carlo and monte_carlo['top_patterns']:
            top_pattern, _ = monte_carlo['top_patterns'][0]
            candidates.extend(list(top_pattern))
        
        # マルコフ連鎖の定常状態確率
        markov = all_analysis['markov_chain_analysis']
        if 'steady_state_probabilities' in markov:
            sorted_markov = sorted(markov['steady_state_probabilities'].items(), key=lambda x: x[1], reverse=True)
            candidates.extend([num for num, _ in sorted_markov[:12]])
        
        # 確率分布の高い数字
        probability_dist = monte_carlo['probability_distribution']
        sorted_prob = sorted(probability_dist.items(), key=lambda x: x[1], reverse=True)
        candidates.extend([num for num, _ in sorted_prob[:15]])
        
        # 重複除去して6個選択
        unique_candidates = list(dict.fromkeys(candidates))
        if len(unique_candidates) >= 6:
            return random.sample(unique_candidates, 6)
        else:
            remaining = [i for i in range(1, 50) if i not in unique_candidates]
            return unique_candidates + random.sample(remaining, 6 - len(unique_candidates))
    
    def generate_time_series_pattern(self, all_analysis):
        """時系列分析パターン生成"""
        candidates = []
        
        # 時系列モメンタムの強い数字
        time_series = all_analysis['enhanced_time_series']
        momentum = time_series['momentum_indicators']
        positive_momentum = [num for num, data in momentum.items() if data['momentum_direction'] == 'positive']
        candidates.extend(positive_momentum[:10])
        
        # トレンド分析で上昇中の数字
        trend = time_series['trend_analysis']
        rising_trend = [num for num, data in trend.items() if data['trend'] > 0 and data['recent_frequency'] > data['overall_frequency']]
        candidates.extend(rising_trend[:10])
        
        # フーリエ分析で周期性の強い数字
        fourier = all_analysis['fourier_analysis']
        if fourier:
            sorted_fourier = sorted(fourier.items(), key=lambda x: x[1]['periodicity_score'], reverse=True)
            candidates.extend([num for num, _ in sorted_fourier[:10]])
        
        # 重複除去して6個選択
        unique_candidates = list(dict.fromkeys(candidates))
        if len(unique_candidates) >= 6:
            return random.sample(unique_candidates, 6)
        else:
            remaining = [i for i in range(1, 50) if i not in unique_candidates]
            return unique_candidates + random.sample(remaining, 6 - len(unique_candidates))
    
    def generate_pattern_recognition_pattern(self, all_analysis):
        """パターン認識パターン生成"""
        candidates = []
        
        # 連続パターンの分析
        consecutive = all_analysis['consecutive_analysis']
        if 'pairs' in consecutive and consecutive['pairs']:
            top_pairs = consecutive['pairs'].most_common(5)
            for pair, _ in top_pairs:
                candidates.extend(pair)
        
        # 時間的サイクルパターン
        temporal = all_analysis['temporal_analysis']
        for weekday, numbers in temporal.items():
            if numbers:
                candidates.extend(numbers[:3])
        
        # 範囲バランスパターン
        range_analysis = all_analysis['range_analysis']
        for range_type in ['low_freq', 'mid_freq', 'high_freq']:
            if range_type in range_analysis:
                top_range = range_analysis[range_type].most_common(3)
                candidates.extend([num for num, _ in top_range])
        
        # 重複除去して6個選択
        unique_candidates = list(dict.fromkeys(candidates))
        if len(unique_candidates) >= 6:
            return random.sample(unique_candidates, 6)
        else:
            remaining = [i for i in range(1, 50) if i not in unique_candidates]
            return unique_candidates + random.sample(remaining, 6 - len(unique_candidates))
    
    def generate_integrated_optimization_pattern(self, all_analysis, previous_patterns):
        """統合最適化パターン生成"""
        # 前の5パターンから最適な数字を選択
        all_numbers = []
        for pattern in previous_patterns:
            all_numbers.extend(pattern['numbers'])
        
        number_freq = Counter(all_numbers)
        top_numbers = [num for num, freq in number_freq.most_common(12)]
        
        # 全分析手法による重み付け
        weighted_scores = {}
        for num in top_numbers:
            score = number_freq[num] * 10  # 基本スコア
            
            # 各分析手法からのスコア加算
            if num in all_analysis['bayesian_analysis']:
                score += all_analysis['bayesian_analysis'][num]['posterior_probability'] * 100
            
            if num in all_analysis['monte_carlo_simulation']['probability_distribution']:
                score += all_analysis['monte_carlo_simulation']['probability_distribution'][num] * 1000
            
            if num in all_analysis['enhanced_time_series']['momentum_indicators']:
                score += all_analysis['enhanced_time_series']['momentum_indicators'][num]['momentum_strength'] * 50
            
            weighted_scores[num] = score
        
        # スコア順にソートして上位6個選択
        sorted_numbers = sorted(weighted_scores.items(), key=lambda x: x[1], reverse=True)
        return [num for num, _ in sorted_numbers[:6]]
    
    def predict_bonus(self, data, all_analysis):
        """ボーナス数字予測"""
        # 最近のボーナス数字の傾向
        recent_bonuses = [draw['additional'] for draw in data[-10:]]
        bonus_freq = Counter(recent_bonuses)
        
        # 最も頻出のボーナス数字
        if bonus_freq:
            most_common_bonus = bonus_freq.most_common(1)[0][0]
            return most_common_bonus
        
        return random.randint(1, 49)
    
    def predict(self, target_date):
        """Ver.6 Ultimate Fusion 予測実行"""
        print(f"🚀 ToTo〇くん Ver.6 Ultimate Fusion - {target_date}予測")
        print("=" * 70)
        
        # データ読み込み
        data = self.load_data()
        if not data:
            print("❌ データ読み込みに失敗しました")
            return
        
        print(f"🤖 全機能統合分析完了（{len(data)}回分）")
        print(f"🧠 AI重み: {self.ai_weights}")
        
        # 全機能統合分析
        all_analysis = self.analyze_all_functions(data)
        
        # パターン生成
        patterns = self.generate_fusion_patterns(data)
        
        # ボーナス予測
        bonus_prediction = self.predict_bonus(data, all_analysis)
        
        # 分析結果表示
        print("🔬 全機能統合分析結果:")
        if 'statistical_tests' in all_analysis:
            stats = all_analysis['statistical_tests']
            if 'chi_square_test' in stats:
                chi_sq = stats['chi_square_test']
                print(f"   📊 カイ二乗検定: χ²={chi_sq.get('chi_square_statistic', 0):.2f}, p値≈{chi_sq.get('p_value_estimate', 0):.3f}")
        
        if 'monte_carlo_simulation' in all_analysis:
            monte = all_analysis['monte_carlo_simulation']
            if 'top_patterns' in monte and monte['top_patterns']:
                top_pattern, prob = monte['top_patterns'][0]
                print(f"   🎯 モンテカルロ最適パターン: {list(top_pattern)} (確率: {prob/1000:.3f})")
        
        if 'markov_chain_analysis' in all_analysis:
            markov = all_analysis['markov_chain_analysis']
            if 'steady_state_probabilities' in markov:
                steady_state = markov['steady_state_probabilities']
                top_steady = sorted(steady_state.items(), key=lambda x: x[1], reverse=True)[:3]
                print(f"   🔄 マルコフ定常状態上位: {[num for num, _ in top_steady]}")
        
        if 'enhanced_time_series' in all_analysis:
            time_series = all_analysis['enhanced_time_series']
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
            numbers = sorted(pattern['numbers'])
            confidence = pattern['confidence']
            strategy = pattern['strategy']
            total = sum(numbers)
            odd_count = len([n for n in numbers if n % 2 == 1])
            even_count = 6 - odd_count
            
            print(f"【パターン{i}】信頼度: {confidence:.1f}% ({strategy})")
            print(f"予測数字: {numbers}")
            print(f"合計: {total} | 奇数/偶数: {odd_count}/{even_count}")
            print("-" * 70)
        
        print("🎯 Ver.6 Ultimate Fusion 予測完了！")
        print("=" * 70)
        
        # 結果保存
        result_file = f"results/result_ver6_ultimate_fusion_{target_date}.txt"
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"🚀 ToTo〇くん Ver.6 Ultimate Fusion - {target_date}予測\n")
            f.write("=" * 70 + "\n")
            f.write(f"🤖 全機能統合分析完了（{len(data)}回分）\n")
            f.write(f"🧠 AI重み: {self.ai_weights}\n")
            f.write("🔬 全機能統合分析結果:\n")
            
            if 'statistical_tests' in all_analysis:
                stats = all_analysis['statistical_tests']
                if 'chi_square_test' in stats:
                    chi_sq = stats['chi_square_test']
                    f.write(f"   📊 カイ二乗検定: χ²={chi_sq.get('chi_square_statistic', 0):.2f}, p値≈{chi_sq.get('p_value_estimate', 0):.3f}\n")
            
            if 'monte_carlo_simulation' in all_analysis:
                monte = all_analysis['monte_carlo_simulation']
                if 'top_patterns' in monte and monte['top_patterns']:
                    top_pattern, prob = monte['top_patterns'][0]
                    f.write(f"   🎯 モンテカルロ最適パターン: {list(top_pattern)} (確率: {prob/1000:.3f})\n")
            
            if 'markov_chain_analysis' in all_analysis:
                markov = all_analysis['markov_chain_analysis']
                if 'steady_state_probabilities' in markov:
                    steady_state = markov['steady_state_probabilities']
                    top_steady = sorted(steady_state.items(), key=lambda x: x[1], reverse=True)[:3]
                    f.write(f"   🔄 マルコフ定常状態上位: {[num for num, _ in top_steady]}\n")
            
            if 'enhanced_time_series' in all_analysis:
                time_series = all_analysis['enhanced_time_series']
                if 'momentum_indicators' in time_series:
                    momentum_data = time_series['momentum_indicators']
                    positive_momentum = [num for num, data in momentum_data.items() if data['momentum_direction'] == 'positive']
                    if positive_momentum:
                        f.write(f"   📈 時系列モメンタム上位: {positive_momentum[:5]}\n")
            
            f.write(f"🔢 予測パターン数: {len(patterns)}\n")
            f.write(f"🎲 ボーナス予測: {bonus_prediction}\n\n")
            
            for i, pattern in enumerate(patterns, 1):
                numbers = sorted(pattern['numbers'])
                confidence = pattern['confidence']
                strategy = pattern['strategy']
                total = sum(numbers)
                odd_count = len([n for n in numbers if n % 2 == 1])
                even_count = 6 - odd_count
                
                f.write(f"【パターン{i}】信頼度: {confidence:.1f}% ({strategy})\n")
                f.write(f"予測数字: {numbers}\n")
                f.write(f"合計: {total} | 奇数/偶数: {odd_count}/{even_count}\n")
                f.write("-" * 70 + "\n")
            
            f.write("🎯 Ver.6 Ultimate Fusion 予測完了！\n")
            f.write("=" * 70 + "\n")
        
        print(f"💾 結果を {result_file} に保存しました")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("使用方法: python predictor_ver6_ultimate_fusion.py YYYY-MM-DD")
        sys.exit(1)
    
    target_date = sys.argv[1]
    predictor = TotoVer6UltimateFusion()
    predictor.predict(target_date) 