#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import statistics
from typing import Dict, List, Tuple
from evaluate import TotoEvaluator

class TotoLearner:
    def __init__(self, weights_file='weights.json', learning_rate=0.1):
        """
        Toto学習クラスの初期化
        """
        self.weights_file = weights_file
        self.learning_rate = learning_rate
        self.weights = self.load_weights()
        self.evaluator = TotoEvaluator()
        
    def load_weights(self) -> Dict:
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
    
    def save_weights(self):
        """
        重みを保存
        """
        try:
            with open(self.weights_file, 'w', encoding='utf-8') as f:
                json.dump(self.weights, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"重み保存エラー: {e}")
    
    def analyze_feature_performance(self, draw_date: str, features: Dict) -> Dict:
        """
        各特徴量のパフォーマンスを分析
        
        Args:
            draw_date: 抽選日
            features: 特徴量データ
            
        Returns:
            特徴量パフォーマンス分析結果
        """
        evaluation = self.evaluator.results.get(draw_date)
        if not evaluation:
            return {}
        
        actual_result = evaluation['actual_result']
        predictions = evaluation['predictions']
        
        # 各特徴量の貢献度を分析
        feature_performance = {}
        
        for feature_name in self.weights.keys():
            performance = self.analyze_single_feature(
                feature_name, features, actual_result, predictions
            )
            feature_performance[feature_name] = performance
        
        return feature_performance
    
    def analyze_single_feature(self, feature_name: str, features: Dict, 
                             actual_result: List[int], predictions: List[Dict]) -> Dict:
        """
        単一特徴量のパフォーマンスを分析
        """
        # 実際に当選した数字の特徴量値を取得
        actual_feature_values = {}
        for num in actual_result:
            if feature_name == 'total_appearances':
                actual_feature_values[num] = features.get('total_appearances', {}).get(num, 0)
            elif feature_name == 'recent_appearances':
                actual_feature_values[num] = features.get('recent_appearances', {}).get(num, 0)
            elif feature_name == 'missing_intervals':
                actual_feature_values[num] = features.get('missing_intervals', {}).get(num, 0)
            # 他の特徴量も同様に処理...
        
        # 予測で高スコアだった数字の特徴量値を取得
        predicted_feature_values = {}
        for pred in predictions:
            if pred['hit_count'] >= 2:  # 2個以上当たった予測のみ考慮
                for num in pred['predicted_numbers']:
                    if feature_name == 'total_appearances':
                        predicted_feature_values[num] = features.get('total_appearances', {}).get(num, 0)
                    elif feature_name == 'recent_appearances':
                        predicted_feature_values[num] = features.get('recent_appearances', {}).get(num, 0)
                    elif feature_name == 'missing_intervals':
                        predicted_feature_values[num] = features.get('missing_intervals', {}).get(num, 0)
                    # 他の特徴量も同様に処理...
        
        # パフォーマンス指標を計算
        actual_avg = statistics.mean(list(actual_feature_values.values())) if actual_feature_values else 0
        predicted_avg = statistics.mean(list(predicted_feature_values.values())) if predicted_feature_values else 0
        
        # 特徴量の有効性スコア（実際の値と予測値の相関）
        effectiveness = 1.0 - abs(actual_avg - predicted_avg) / max(actual_avg, predicted_avg, 1)
        
        return {
            'actual_average': actual_avg,
            'predicted_average': predicted_avg,
            'effectiveness': max(0, effectiveness),
            'contribution_score': 0.0  # 後で計算
        }
    
    def calculate_weight_adjustments(self, feature_performance: Dict, 
                                   evaluation: Dict) -> Dict:
        """
        重み調整量を計算
        """
        adjustments = {}
        best_hit_count = evaluation['summary']['best_hit_count']
        avg_hit_count = evaluation['summary']['average_hit_count']
        
        # 全体的なパフォーマンススコア
        overall_performance = (best_hit_count / 6.0) * 0.7 + (avg_hit_count / 6.0) * 0.3
        
        for feature_name, performance in feature_performance.items():
            effectiveness = performance['effectiveness']
            
            # 特徴量の貢献度を計算
            if effectiveness > 0.6:  # 有効な特徴量
                if overall_performance > 0.5:  # 良い予測結果
                    adjustment = self.learning_rate * effectiveness
                else:  # 悪い予測結果
                    adjustment = -self.learning_rate * effectiveness * 0.5
            else:  # 無効な特徴量
                if overall_performance > 0.5:  # 良い予測結果（他の特徴量が効いている）
                    adjustment = -self.learning_rate * (1 - effectiveness) * 0.3
                else:  # 悪い予測結果
                    adjustment = -self.learning_rate * (1 - effectiveness)
            
            adjustments[feature_name] = adjustment
        
        return adjustments
    
    def apply_weight_adjustments(self, adjustments: Dict):
        """
        重み調整を適用
        """
        print("\n🔧 重み調整:")
        print("-" * 40)
        
        for feature_name, adjustment in adjustments.items():
            old_weight = self.weights[feature_name]
            new_weight = max(0.01, min(0.5, old_weight + adjustment))  # 0.01-0.5の範囲に制限
            
            self.weights[feature_name] = new_weight
            
            if abs(adjustment) > 0.001:  # 有意な変更のみ表示
                print(f"{feature_name}: {old_weight:.3f} → {new_weight:.3f} ({adjustment:+.3f})")
        
        # 重みの正規化（合計が1になるように）
        total_weight = sum(self.weights.values())
        for feature_name in self.weights:
            self.weights[feature_name] /= total_weight
        
        print("-" * 40)
        print("✅ 重み調整完了")
    
    def learn_from_evaluation(self, draw_date: str, features: Dict):
        """
        評価結果から学習
        """
        print(f"\n🧠 {draw_date} からの学習開始")
        print("=" * 50)
        
        # 特徴量パフォーマンスを分析
        feature_performance = self.analyze_feature_performance(draw_date, features)
        
        # 評価結果を取得
        evaluation = self.evaluator.results.get(draw_date)
        if not evaluation:
            print("❌ 評価結果が見つかりません")
            return
        
        # 重み調整量を計算
        adjustments = self.calculate_weight_adjustments(feature_performance, evaluation)
        
        # 重み調整を適用
        self.apply_weight_adjustments(adjustments)
        
        # 重みを保存
        self.save_weights()
        
        # 学習結果を表示
        self.print_learning_summary(feature_performance, evaluation)
    
    def print_learning_summary(self, feature_performance: Dict, evaluation: Dict):
        """
        学習結果のサマリーを表示
        """
        print("\n📊 学習サマリー:")
        print("-" * 40)
        print(f"最高一致数: {evaluation['summary']['best_hit_count']}/6")
        print(f"平均一致数: {evaluation['summary']['average_hit_count']:.2f}/6")
        
        print("\n特徴量有効性:")
        for feature_name, performance in feature_performance.items():
            effectiveness = performance['effectiveness']
            if effectiveness > 0.5:
                status = "✅ 有効"
            elif effectiveness > 0.3:
                status = "⚠️  中程度"
            else:
                status = "❌ 低効率"
            
            print(f"  {feature_name}: {effectiveness:.3f} {status}")
        
        print("-" * 40)
    
    def get_learning_history(self) -> Dict:
        """
        学習履歴を取得
        """
        try:
            with open('learning_history.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except Exception as e:
            print(f"学習履歴読み込みエラー: {e}")
            return {}
    
    def save_learning_history(self, draw_date: str, adjustments: Dict, 
                            feature_performance: Dict):
        """
        学習履歴を保存
        """
        history = self.get_learning_history()
        
        history[draw_date] = {
            'timestamp': str(np.datetime64('now')),
            'adjustments': adjustments,
            'feature_performance': feature_performance,
            'weights_after': self.weights.copy()
        }
        
        try:
            with open('learning_history.json', 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"学習履歴保存エラー: {e}")
    
    def print_weight_summary(self):
        """
        現在の重みサマリーを表示
        """
        print("\n⚖️ 現在の重み設定:")
        print("-" * 40)
        
        sorted_weights = sorted(self.weights.items(), key=lambda x: x[1], reverse=True)
        for feature_name, weight in sorted_weights:
            print(f"  {feature_name}: {weight:.3f}")
        
        print(f"  合計: {sum(self.weights.values()):.3f}")
        print("-" * 40) 