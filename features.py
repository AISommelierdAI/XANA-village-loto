import pandas as pd
import numpy as np
from collections import defaultdict, Counter
from scipy import stats
from scipy.stats import chi2_contingency
import math

class TotoFeatures:
    def __init__(self, csv_file='T-maru.csv'):
        """
        Toto特徴量計算クラスの初期化
        """
        self.csv_file = csv_file
        self.data = None
        self.all_numbers = None
        self.load_data()
        
    def load_data(self):
        """
        CSVファイルからデータを読み込み
        """
        try:
            self.data = pd.read_csv(self.csv_file)
            # 当選番号の列を抽出（ボーナス数字は除外）
            number_columns = ['Number1', 'Number2', 'Number3', 'Number4', 'Number5', 'Number6']
            self.all_numbers = self.data[number_columns].values.flatten()
            print(f"データ読み込み完了: {len(self.data)}回分のデータ")
        except FileNotFoundError:
            print(f"エラー: {self.csv_file} が見つかりません")
            raise
        except Exception as e:
            print(f"データ読み込みエラー: {e}")
            raise
    
    def get_total_appearances(self):
        """
        各数字の総出現回数を計算
        """
        return Counter(self.all_numbers)
    
    def get_recent_appearances(self, recent_count=10):
        """
        直近N回での出現回数を計算
        """
        recent_numbers = self.all_numbers[-recent_count*6:]
        return Counter(recent_numbers)
    
    def get_missing_intervals(self):
        """
        各数字の未出間隔を計算
        """
        missing_intervals = {}
        number_columns = ['Number1', 'Number2', 'Number3', 'Number4', 'Number5', 'Number6']
        
        for num in range(1, 50):
            last_appearance = -1
            for i, row in self.data.iterrows():
                if num in row[number_columns].values:
                    last_appearance = i
                    break
            
            if last_appearance == -1:
                missing_intervals[num] = len(self.data)
            else:
                missing_intervals[num] = len(self.data) - 1 - last_appearance
        
        return missing_intervals
    
    def get_consecutive_pairs_frequency(self):
        """
        連番・ペアの出現頻度を計算
        """
        consecutive_count = 0
        pair_count = 0
        total_draws = len(self.data)
        
        for _, row in self.data.iterrows():
            numbers = sorted([row['Number1'], row['Number2'], row['Number3'], 
                            row['Number4'], row['Number5'], row['Number6']])
            
            # 連番チェック
            for i in range(len(numbers)-1):
                if numbers[i+1] - numbers[i] == 1:
                    consecutive_count += 1
            
            # ペアチェック（差が2以内）
            for i in range(len(numbers)-1):
                for j in range(i+1, len(numbers)):
                    if abs(numbers[j] - numbers[i]) <= 2:
                        pair_count += 1
        
        return {
            'consecutive_rate': consecutive_count / total_draws,
            'pair_rate': pair_count / (total_draws * 15)  # 6C2 = 15
        }
    
    def get_odd_even_ratio(self):
        """
        奇数・偶数の比率を計算
        """
        odd_count = sum(1 for num in self.all_numbers if num % 2 == 1)
        even_count = len(self.all_numbers) - odd_count
        return odd_count / len(self.all_numbers)
    
    def get_number_statistics(self):
        """
        数字の合計、中央値、分散を計算
        """
        number_columns = ['Number1', 'Number2', 'Number3', 'Number4', 'Number5', 'Number6']
        sums = []
        medians = []
        variances = []
        
        for _, row in self.data.iterrows():
            numbers = [row[col] for col in number_columns]
            sums.append(sum(numbers))
            medians.append(np.median(numbers))
            variances.append(np.var(numbers))
        
        return {
            'avg_sum': np.mean(sums),
            'avg_median': np.mean(medians),
            'avg_variance': np.mean(variances),
            'sum_std': np.std(sums),
            'median_std': np.std(medians),
            'variance_std': np.std(variances)
        }
    
    def get_prime_square_ratio(self):
        """
        素数、平方数の比率を計算
        """
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    return False
            return True
        
        def is_square(n):
            root = int(math.sqrt(n))
            return root * root == n
        
        prime_count = sum(1 for num in self.all_numbers if is_prime(num))
        square_count = sum(1 for num in self.all_numbers if is_square(num))
        
        return {
            'prime_ratio': prime_count / len(self.all_numbers),
            'square_ratio': square_count / len(self.all_numbers)
        }
    
    def get_hot_cold_numbers(self, threshold=0.7):
        """
        ホット数字・コールド数字の判定
        """
        total_appearances = self.get_total_appearances()
        recent_appearances = self.get_recent_appearances(10)
        
        hot_numbers = []
        cold_numbers = []
        
        for num in range(1, 50):
            total_freq = total_appearances.get(num, 0) / len(self.data)
            recent_freq = recent_appearances.get(num, 0) / 10
            
            if recent_freq > total_freq * threshold:
                hot_numbers.append(num)
            elif recent_freq < total_freq * (1 - threshold):
                cold_numbers.append(num)
        
        return {'hot': hot_numbers, 'cold': cold_numbers}
    
    def get_distribution_patterns(self):
        """
        数字の分布パターン（区間別出現率）
        """
        intervals = {
            '1-10': (1, 10),
            '11-20': (11, 20),
            '21-30': (21, 30),
            '31-40': (31, 40),
            '41-49': (41, 49)
        }
        
        distribution = {}
        for name, (start, end) in intervals.items():
            count = sum(1 for num in self.all_numbers if start <= num <= end)
            distribution[name] = count / len(self.all_numbers)
        
        return distribution
    
    def get_adjacent_correlation(self):
        """
        隣接数字の相関（前回出た数字の±1, ±2の出現傾向）
        """
        adjacent_counts = defaultdict(int)
        total_adjacent_opportunities = 0
        
        for i in range(1, len(self.data)):
            prev_numbers = [self.data.iloc[i-1][f'Number{j}'] for j in range(1, 7)]
            curr_numbers = [self.data.iloc[i][f'Number{j}'] for j in range(1, 7)]
            
            for prev_num in prev_numbers:
                for curr_num in curr_numbers:
                    diff = abs(curr_num - prev_num)
                    if 1 <= diff <= 2:
                        adjacent_counts[diff] += 1
                    total_adjacent_opportunities += 1
        
        return {k: v/total_adjacent_opportunities for k, v in adjacent_counts.items()}
    
    def get_periodicity_analysis(self):
        """
        周期性分析（特定の数字が何回おきに出現するか）
        """
        periodicity = {}
        
        for num in range(1, 50):
            appearances = []
            for i, row in self.data.iterrows():
                if num in [row['Number1'], row['Number2'], row['Number3'], 
                          row['Number4'], row['Number5'], row['Number6']]:
                    appearances.append(i)
            
            if len(appearances) > 1:
                intervals = [appearances[i+1] - appearances[i] for i in range(len(appearances)-1)]
                periodicity[num] = {
                    'avg_interval': np.mean(intervals),
                    'std_interval': np.std(intervals),
                    'last_appearance': appearances[-1] if appearances else -1
                }
            else:
                periodicity[num] = {
                    'avg_interval': float('inf'),
                    'std_interval': 0,
                    'last_appearance': appearances[0] if appearances else -1
                }
        
        return periodicity
    
    def get_combination_frequency(self):
        """
        数字間の同時出現頻度（組み合わせ分析）
        """
        combinations = defaultdict(int)
        total_draws = len(self.data)
        
        for _, row in self.data.iterrows():
            numbers = sorted([row['Number1'], row['Number2'], row['Number3'], 
                            row['Number4'], row['Number5'], row['Number6']])
            
            for i in range(len(numbers)):
                for j in range(i+1, len(numbers)):
                    combinations[(numbers[i], numbers[j])] += 1
        
        # 上位10の組み合わせを返す
        top_combinations = sorted(combinations.items(), key=lambda x: x[1], reverse=True)[:10]
        return {combo: freq/total_draws for combo, freq in top_combinations}
    
    def get_regression_trend(self):
        """
        回帰分析による出現トレンド
        """
        trends = {}
        
        for num in range(1, 50):
            appearances = []
            for i, row in self.data.iterrows():
                if num in [row['Number1'], row['Number2'], row['Number3'], 
                          row['Number4'], row['Number5'], row['Number6']]:
                    appearances.append(i)
            
            if len(appearances) > 5:
                x = np.array(appearances)
                y = np.arange(len(appearances))
                
                # 線形回帰
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                trends[num] = {
                    'slope': slope,
                    'r_squared': r_value**2,
                    'p_value': p_value
                }
            else:
                trends[num] = {
                    'slope': 0,
                    'r_squared': 0,
                    'p_value': 1
                }
        
        return trends
    
    def get_chi_square_bias(self):
        """
        カイ二乗検定による偏りの検出
        """
        observed = [self.all_numbers.count(i) for i in range(1, 50)]
        expected = [len(self.all_numbers) / 49] * 49
        
        chi2, p_value = stats.chisquare(observed, expected)
        
        return {
            'chi2_statistic': chi2,
            'p_value': p_value,
            'is_biased': p_value < 0.05
        }
    
    def get_moving_average_trend(self, window=5):
        """
        移動平均による出現トレンド
        """
        trends = {}
        
        for num in range(1, 50):
            appearances = []
            for i, row in self.data.iterrows():
                if num in [row['Number1'], row['Number2'], row['Number3'], 
                          row['Number4'], row['Number5'], row['Number6']]:
                    appearances.append(1)
                else:
                    appearances.append(0)
            
            if len(appearances) >= window:
                moving_avg = pd.Series(appearances).rolling(window=window).mean()
                trends[num] = {
                    'current_trend': moving_avg.iloc[-1] if not pd.isna(moving_avg.iloc[-1]) else 0,
                    'trend_direction': 'up' if moving_avg.iloc[-1] > moving_avg.iloc[-window] else 'down'
                }
            else:
                trends[num] = {
                    'current_trend': 0,
                    'trend_direction': 'stable'
                }
        
        return trends
    
    def get_repeat_patterns(self):
        """
        前回との数字重複パターン
        """
        repeat_counts = []
        
        for i in range(1, len(self.data)):
            prev_numbers = set([self.data.iloc[i-1][f'Number{j}'] for j in range(1, 7)])
            curr_numbers = set([self.data.iloc[i][f'Number{j}'] for j in range(1, 7)])
            
            repeat_count = len(prev_numbers.intersection(curr_numbers))
            repeat_counts.append(repeat_count)
        
        return {
            'avg_repeats': np.mean(repeat_counts),
            'repeat_distribution': Counter(repeat_counts)
        }
    
    def get_attraction_effect(self):
        """
        数字の「引き寄せ効果」（特定数字が出ると次に出やすい数字）
        """
        attraction = defaultdict(lambda: defaultdict(int))
        
        for i in range(len(self.data) - 1):
            prev_numbers = [self.data.iloc[i][f'Number{j}'] for j in range(1, 7)]
            next_numbers = [self.data.iloc[i+1][f'Number{j}'] for j in range(1, 7)]
            
            for prev_num in prev_numbers:
                for next_num in next_numbers:
                    attraction[prev_num][next_num] += 1
        
        # 各数字について最も引き寄せ効果の強い数字を返す
        attraction_effects = {}
        for num in range(1, 50):
            if num in attraction:
                max_attracted = max(attraction[num].items(), key=lambda x: x[1])
                attraction_effects[num] = {
                    'most_attracted': max_attracted[0],
                    'attraction_strength': max_attracted[1]
                }
            else:
                attraction_effects[num] = {
                    'most_attracted': None,
                    'attraction_strength': 0
                }
        
        return attraction_effects
    
    def calculate_all_features(self):
        """
        全ての特徴量を計算して辞書で返す
        """
        return {
            'total_appearances': self.get_total_appearances(),
            'recent_appearances': self.get_recent_appearances(),
            'missing_intervals': self.get_missing_intervals(),
            'consecutive_pairs': self.get_consecutive_pairs_frequency(),
            'odd_even_ratio': self.get_odd_even_ratio(),
            'number_stats': self.get_number_statistics(),
            'prime_square': self.get_prime_square_ratio(),
            'hot_cold': self.get_hot_cold_numbers(),
            'distribution': self.get_distribution_patterns(),
            'adjacent_correlation': self.get_adjacent_correlation(),
            'periodicity': self.get_periodicity_analysis(),
            'combinations': self.get_combination_frequency(),
            'regression_trend': self.get_regression_trend(),
            'chi_square': self.get_chi_square_bias(),
            'moving_average': self.get_moving_average_trend(),
            'repeat_patterns': self.get_repeat_patterns(),
            'attraction_effect': self.get_attraction_effect()
        } 