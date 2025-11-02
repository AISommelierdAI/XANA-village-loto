#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import json
from features import TotoFeatures
import random

class TotoPredictorAdaptive:
    def __init__(self, csv_file='totomaru.csv', weights_file='weights.json'):
        """
        適応型Toto予測クラスの初期化
        """
        self.features = TotoFeatures(csv_file)
        self.weights_file = weights_file
        self.all_features = None
        self.weights = self.load_weights()
        self.calculate_features()
        
    def load_weights(self):
        """
        重みを読み込み
        """
        default_weights = {
            'total_appearances': 0.15,
            'recent_appearances': 0.20,
            'missing_intervals': 0.15,
            'hot_cold': 0.10,
            'periodicity': 0.10,
            'regression_trend': 0.08,
            'moving_average': 0.08,
            'attraction_effect': 0.05,
            'distribution': 0.05,
            'adjacent_correlation': 0.04
        }
        
        try:
            with open(self.weights_file, 'r', encoding='utf-8') as f:
                loaded_weights = json.load(f)
                # 新しい特徴量が追加された場合の対応
                for key, value in default_weights.items():
                    if key not in loaded_weights:
                        loaded_weights[key] = value
                return loaded_weights
        except FileNotFoundError:
            return default_weights
        except Exception as e:
            print(f"重み読み込みエラー: {e}")
            return default_weights
        
    def calculate_features(self):
        """
        全ての特徴量を計算
        """
        print("特徴量を計算中...")
        self.all_features = self.features.calculate_all_features()
        print("特徴量計算完了")
    
    def calculate_number_score(self, number):
        """
        各数字の総合スコアを計算（重みを動的に適用）
        """
        score = 0.0
        
        # 1. 総出現回数スコア（回帰平均の法則）
        total_appearances = self.all_features['total_appearances'].get(number, 0)
        expected_appearances = len(self.features.data) * 6 / 49  # 理論期待値
        appearance_score = 1.0 - abs(total_appearances - expected_appearances) / expected_appearances
        score += self.weights['total_appearances'] * appearance_score
        
        # 2. 直近出現回数スコア（マルコフ連鎖）
        recent_appearances = self.all_features['recent_appearances'].get(number, 0)
        recent_score = min(recent_appearances / 3.0, 1.0)  # 直近10回で3回以上なら高スコア
        score += self.weights['recent_appearances'] * recent_score
        
        # 3. 未出間隔スコア（回帰平均の法則）
        missing_interval = self.all_features['missing_intervals'].get(number, 0)
        avg_interval = len(self.features.data) * 6 / 49  # 平均間隔
        if missing_interval > avg_interval * 1.5:  # 長期間未出なら高スコア
            interval_score = min(missing_interval / (avg_interval * 2), 1.0)
        else:
            interval_score = 0.3
        score += self.weights['missing_intervals'] * interval_score
        
        # 4. ホット・コールドスコア
        hot_numbers = self.all_features['hot_cold']['hot']
        cold_numbers = self.all_features['hot_cold']['cold']
        if number in hot_numbers:
            hot_cold_score = 0.7  # ホット数字は中程度のスコア
        elif number in cold_numbers:
            hot_cold_score = 0.8  # コールド数字は高スコア（回帰期待）
        else:
            hot_cold_score = 0.5  # 中立
        score += self.weights['hot_cold'] * hot_cold_score
        
        # 5. 周期性スコア
        periodicity = self.all_features['periodicity'].get(number, {})
        if periodicity.get('avg_interval', float('inf')) != float('inf'):
            current_interval = self.all_features['missing_intervals'].get(number, 0)
            expected_interval = periodicity['avg_interval']
            if abs(current_interval - expected_interval) <= periodicity.get('std_interval', 1):
                periodicity_score = 0.9  # 周期性に一致
            else:
                periodicity_score = 0.3
        else:
            periodicity_score = 0.5
        score += self.weights['periodicity'] * periodicity_score
        
        # 6. 回帰トレンドスコア
        trend = self.all_features['regression_trend'].get(number, {})
        if trend.get('r_squared', 0) > 0.3:  # 有意なトレンドがある場合
            if trend.get('slope', 0) > 0:
                trend_score = 0.8  # 上昇トレンド
            else:
                trend_score = 0.6  # 下降トレンド
        else:
            trend_score = 0.5  # トレンドなし
        score += self.weights['regression_trend'] * trend_score
        
        # 7. 移動平均スコア
        moving_avg = self.all_features['moving_average'].get(number, {})
        if moving_avg.get('trend_direction') == 'up':
            ma_score = 0.7
        elif moving_avg.get('trend_direction') == 'down':
            ma_score = 0.8  # 下降トレンドは回帰期待で高スコア
        else:
            ma_score = 0.5
        score += self.weights['moving_average'] * ma_score
        
        # 8. 引き寄せ効果スコア
        attraction = self.all_features['attraction_effect'].get(number, {})
        if attraction.get('attraction_strength', 0) > 2:  # 強い引き寄せ効果
            attraction_score = 0.8
        else:
            attraction_score = 0.5
        score += self.weights['attraction_effect'] * attraction_score
        
        # 9. 分布バランススコア
        distribution = self.all_features['distribution']
        if 1 <= number <= 10:
            interval = '1-10'
        elif 11 <= number <= 20:
            interval = '11-20'
        elif 21 <= number <= 30:
            interval = '21-30'
        elif 31 <= number <= 40:
            interval = '31-40'
        else:
            interval = '41-49'
        
        interval_rate = distribution.get(interval, 0.2)
        if interval_rate < 0.15:  # 低出現区間なら高スコア
            distribution_score = 0.8
        elif interval_rate > 0.25:  # 高出現区間なら低スコア
            distribution_score = 0.3
        else:
            distribution_score = 0.5
        score += self.weights['distribution'] * distribution_score
        
        # 10. 隣接相関スコア
        adjacent_corr = self.all_features['adjacent_correlation']
        if adjacent_corr.get(1, 0) > 0.1 or adjacent_corr.get(2, 0) > 0.1:
            adjacent_score = 0.6
        else:
            adjacent_score = 0.5
        score += self.weights['adjacent_correlation'] * adjacent_score
        
        return score
    
    def calculate_combination_score(self, numbers):
        """
        数字の組み合わせスコアを計算
        """
        if len(numbers) != 6:
            return 0.0
        
        combination_score = 0.0
        
        # 1. 合計値の最適化
        total = sum(numbers)
        optimal_total = 147  # 1-49の平均 * 6
        total_score = 1.0 - abs(total - optimal_total) / optimal_total
        combination_score += 0.2 * total_score
        
        # 2. 奇数・偶数のバランス
        odd_count = sum(1 for num in numbers if num % 2 == 1)
        even_count = 6 - odd_count
        balance_score = 1.0 - abs(odd_count - even_count) / 6.0
        combination_score += 0.15 * balance_score
        
        # 3. 区間分布のバランス
        intervals = [0] * 5
        for num in numbers:
            if 1 <= num <= 10:
                intervals[0] += 1
            elif 11 <= num <= 20:
                intervals[1] += 1
            elif 21 <= num <= 30:
                intervals[2] += 1
            elif 31 <= num <= 40:
                intervals[3] += 1
            else:
                intervals[4] += 1
        
        # 各区間に1-2個の数字があるのが理想的
        distribution_score = 0.0
        for count in intervals:
            if 1 <= count <= 2:
                distribution_score += 1.0
            elif count == 0:
                distribution_score += 0.3
            else:
                distribution_score += 0.5
        distribution_score /= 5.0
        combination_score += 0.15 * distribution_score
        
        # 4. 連番の回避
        sorted_numbers = sorted(numbers)
        consecutive_count = 0
        for i in range(len(sorted_numbers) - 1):
            if sorted_numbers[i+1] - sorted_numbers[i] == 1:
                consecutive_count += 1
        
        consecutive_score = 1.0 - (consecutive_count / 3.0)  # 連番が少ないほど高スコア
        combination_score += 0.1 * consecutive_score
        
        # 5. 素数のバランス
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True
        
        prime_count = sum(1 for num in numbers if is_prime(num))
        prime_score = 1.0 - abs(prime_count - 2) / 6.0  # 素数2個が理想的
        combination_score += 0.1 * prime_score
        
        # 6. 平方数のバランス
        def is_square(n):
            root = int(n**0.5)
            return root * root == n
        
        square_count = sum(1 for num in numbers if is_square(num))
        square_score = 1.0 - abs(square_count - 1) / 6.0  # 平方数1個が理想的
        combination_score += 0.1 * square_score
        
        return combination_score
    
    def predict_numbers(self, num_candidates=20, num_predictions=6):
        """
        数字を予測
        """
        # 各数字のスコアを計算
        number_scores = {}
        for num in range(1, 50):
            number_scores[num] = self.calculate_number_score(num)
        
        # スコアの高い数字から候補を選択
        sorted_numbers = sorted(number_scores.items(), key=lambda x: x[1], reverse=True)
        candidates = [num for num, score in sorted_numbers[:num_candidates]]
        
        # 組み合わせを生成
        predictions = []
        attempts = 0
        max_attempts = num_predictions * 100
        
        while len(predictions) < num_predictions and attempts < max_attempts:
            # 候補から6個をランダムに選択
            selected = random.sample(candidates, 6)
            
            # 組み合わせスコアを計算
            combination_score = self.calculate_combination_score(selected)
            
            # 重複チェック
            is_duplicate = False
            for existing_numbers, _ in predictions:
                if set(selected) == set(existing_numbers):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                predictions.append((selected, combination_score))
            
            attempts += 1
        
        # 組み合わせスコアでソート
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        return predictions[:num_predictions]
    
    def get_prediction_reasons(self, numbers):
        """
        予測の理由を取得
        """
        reasons = []
        
        for num in numbers:
            num_reasons = []
            score = self.calculate_number_score(num)
            
            # 各特徴量の貢献度を分析
            total_appearances = self.all_features['total_appearances'].get(num, 0)
            recent_appearances = self.all_features['recent_appearances'].get(num, 0)
            missing_interval = self.all_features['missing_intervals'].get(num, 0)
            
            if total_appearances > len(self.features.data) * 6 / 49:
                num_reasons.append("出現回数が多い")
            elif total_appearances < len(self.features.data) * 6 / 49 * 0.8:
                num_reasons.append("出現回数が少ない（回帰期待）")
            
            if recent_appearances >= 2:
                num_reasons.append("直近で出現")
            elif missing_interval > len(self.features.data) * 0.3:
                num_reasons.append("長期間未出")
            
            if num in self.all_features['hot_cold']['hot']:
                num_reasons.append("ホット数字")
            elif num in self.all_features['hot_cold']['cold']:
                num_reasons.append("コールド数字（回帰期待）")
            
            reasons.append(f"{num}: {', '.join(num_reasons)}")
        
        return reasons
    
    def calculate_confidence_score(self, numbers, combination_score):
        """
        信頼度スコアを計算
        """
        # 個別スコアの平均
        individual_scores = [self.calculate_number_score(num) for num in numbers]
        avg_individual_score = np.mean(individual_scores)
        
        # 組み合わせスコア
        combo_score = combination_score
        
        # 総合信頼度（個別スコア60%、組み合わせスコア40%）
        confidence = avg_individual_score * 0.6 + combo_score * 0.4
        
        return confidence * 100  # パーセンテージに変換
    
    def print_weight_info(self):
        """
        現在の重み情報を表示
        """
        print("\n⚖️ 現在の重み設定:")
        print("-" * 40)
        
        sorted_weights = sorted(self.weights.items(), key=lambda x: x[1], reverse=True)
        for feature_name, weight in sorted_weights:
            print(f"  {feature_name}: {weight:.3f}")
        
        print(f"  合計: {sum(self.weights.values()):.3f}")
        print("-" * 40) 