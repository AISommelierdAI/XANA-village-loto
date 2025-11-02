#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改良版学習システム - 的中率改善
より詳細な分析と重み調整
"""

import json
import statistics
from collections import defaultdict

class ImprovedLearningSystem:
    def __init__(self):
        self.weights = self.load_weights()
        self.evaluation_data = self.load_evaluation_data()
        
    def load_weights(self):
        """重み設定を読み込み"""
        try:
            with open('weights.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
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
    
    def load_evaluation_data(self):
        """評価データを読み込み"""
        data = {}
        
        # evaluation_results.jsonから読み込み
        try:
            with open('evaluation_results.json', 'r', encoding='utf-8') as file:
                data.update(json.load(file))
        except FileNotFoundError:
            pass
        
        # 個別の評価ファイルから読み込み
        import glob
        for filename in glob.glob('evaluation_*.json'):
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    eval_data = json.load(file)
                    if 'date' in eval_data:
                        data[eval_data['date']] = eval_data
            except:
                continue
        
        return data
    
    def analyze_pattern_performance(self):
        """パターン別性能分析"""
        pattern_stats = defaultdict(lambda: {
            'total_predictions': 0,
            'total_hits': 0,
            'hit_rates': [],
            'confidence_scores': []
        })
        
        for date, result in self.evaluation_data.items():
            if 'predictions' in result:
                for pred in result['predictions']:
                    pattern_num = pred.get('pattern', 1)
                    hits = pred.get('hits', pred.get('hit_count', 0))
                    confidence = pred.get('confidence', 50)
                    
                    stats = pattern_stats[pattern_num]
                    stats['total_predictions'] += 1
                    stats['total_hits'] += hits
                    stats['hit_rates'].append(hits / 6.0)  # 6個中何個当たったか
                    stats['confidence_scores'].append(confidence)
        
        # 統計計算
        for pattern_num, stats in pattern_stats.items():
            if stats['total_predictions'] > 0:
                stats['average_hit_rate'] = statistics.mean(stats['hit_rates'])
                stats['average_confidence'] = statistics.mean(stats['confidence_scores'])
                stats['overall_hit_rate'] = stats['total_hits'] / (stats['total_predictions'] * 6)
                stats['confidence_accuracy'] = self.calculate_confidence_accuracy(
                    stats['confidence_scores'], stats['hit_rates']
                )
        
        return pattern_stats
    
    def calculate_confidence_accuracy(self, confidences, hit_rates):
        """信頼度と的中率の相関を計算"""
        if len(confidences) < 2:
            return 0.0
        
        # 信頼度と的中率の相関係数
        try:
            correlation = statistics.correlation(confidences, hit_rates)
            return max(0, correlation)  # 負の相関は0として扱う
        except:
            return 0.0
    
    def analyze_feature_effectiveness(self):
        """特徴量の有効性分析"""
        feature_stats = defaultdict(lambda: {
            'high_confidence_hits': 0,
            'high_confidence_total': 0,
            'low_confidence_hits': 0,
            'low_confidence_total': 0
        })
        
        for date, result in self.evaluation_data.items():
            if 'predictions' in result:
                for pred in result['predictions']:
                    confidence = pred.get('confidence', 50)
                    hits = pred.get('hits', pred.get('hit_count', 0))
                    
                    # 高信頼度(80%以上)と低信頼度(80%未満)に分類
                    if confidence >= 80:
                        feature_stats['high_confidence']['high_confidence_hits'] += hits
                        feature_stats['high_confidence']['high_confidence_total'] += 1
                    else:
                        feature_stats['low_confidence']['low_confidence_hits'] += hits
                        feature_stats['low_confidence']['low_confidence_total'] += 1
        
        return feature_stats
    
    def calculate_weight_adjustments(self):
        """重み調整計算"""
        pattern_stats = self.analyze_pattern_performance()
        feature_stats = self.analyze_feature_effectiveness()
        
        # パターン1-3の性能を分析（通常最も信頼度が高い）
        top_patterns = [1, 2, 3]
        top_pattern_performance = []
        
        for pattern_num in top_patterns:
            if pattern_num in pattern_stats:
                stats = pattern_stats[pattern_num]
                if stats['total_predictions'] > 0:
                    top_pattern_performance.append(stats['average_hit_rate'])
        
        # 全体の平均的中率
        overall_hit_rate = statistics.mean(top_pattern_performance) if top_pattern_performance else 0.5
        
        # 重み調整の方向性を決定
        adjustments = {}
        
        if overall_hit_rate >= 0.25:  # 25%以上の的中率
            # 現在の重みを維持または微調整
            adjustments = {
                "total_appearances": 0.0,
                "recent_appearances": 0.0,
                "missing_intervals": 0.0,
                "hot_cold": 0.0,
                "periodicity": 0.0,
                "regression_trend": 0.0,
                "moving_average": 0.0,
                "attraction_effect": 0.0,
                "distribution": 0.0,
                "adjacent_correlation": 0.0
            }
        elif overall_hit_rate >= 0.15:  # 15-25%の的中率
            # 中程度の調整
            adjustments = {
                "total_appearances": -0.005,
                "recent_appearances": -0.005,
                "missing_intervals": +0.010,
                "hot_cold": +0.005,
                "periodicity": +0.005,
                "regression_trend": +0.005,
                "moving_average": +0.005,
                "attraction_effect": +0.005,
                "distribution": +0.005,
                "adjacent_correlation": +0.005
            }
        else:  # 15%未満の的中率
            # 大幅な調整
            adjustments = {
                "total_appearances": -0.010,
                "recent_appearances": -0.010,
                "missing_intervals": +0.020,
                "hot_cold": +0.010,
                "periodicity": +0.010,
                "regression_trend": +0.010,
                "moving_average": +0.010,
                "attraction_effect": +0.010,
                "distribution": +0.010,
                "adjacent_correlation": +0.010
            }
        
        # パターン別性能に基づく微調整
        if 1 in pattern_stats and pattern_stats[1]['total_predictions'] > 0:
            pattern1_performance = pattern_stats[1]['average_hit_rate']
            if pattern1_performance < 0.15:
                # パターン1の性能が悪い場合、基本特徴量を強化
                adjustments["total_appearances"] += 0.005
                adjustments["recent_appearances"] += 0.005
        
        return adjustments, overall_hit_rate
    
    def apply_weight_adjustments(self, adjustments):
        """重み調整を適用"""
        print("🧠 改良版Toto丸くん 学習システム")
        print("\n" + "=" * 40)
        
        # 現在の重みを表示
        print("📊 調整前の重み設定:")
        print("-" * 40)
        for feature, weight in self.weights.items():
            print(f"  {feature}: {weight:.3f}")
        
        # 調整を適用
        print(f"\n📈 重み調整:")
        print("-" * 40)
        for feature, adjustment in adjustments.items():
            old_weight = self.weights[feature]
            new_weight = max(0.01, old_weight + adjustment)  # 最小0.01を保証
            self.weights[feature] = new_weight
            
            change = "+" if adjustment >= 0 else ""
            print(f"  {feature}: {old_weight:.3f} → {new_weight:.3f} ({change}{adjustment:.3f})")
        
        # 重みの正規化
        total_weight = sum(self.weights.values())
        for feature in self.weights:
            self.weights[feature] /= total_weight
        
        print(f"\n⚖️ 調整後の重み設定:")
        print("-" * 40)
        for feature, weight in self.weights.items():
            print(f"  {feature}: {weight:.3f}")
        
        # 重みを保存
        with open('weights.json', 'w', encoding='utf-8') as file:
            json.dump(self.weights, file, indent=2, ensure_ascii=False)
        
        print(f"\n✅ 重み調整完了")
        print("=" * 40)
    
    def generate_learning_report(self):
        """学習レポート生成"""
        pattern_stats = self.analyze_pattern_performance()
        adjustments, overall_hit_rate = self.calculate_weight_adjustments()
        
        print(f"\n📊 学習レポート")
        print("=" * 40)
        print(f"🎯 全体平均的中率: {overall_hit_rate:.1%}")
        
        print(f"\n📈 パターン別性能:")
        print("-" * 40)
        for pattern_num in sorted(pattern_stats.keys()):
            stats = pattern_stats[pattern_num]
            if stats['total_predictions'] > 0:
                print(f"  パターン{pattern_num}: {stats['average_hit_rate']:.1%} "
                      f"({stats['total_predictions']}回)")
        
        print(f"\n🔧 推奨調整:")
        print("-" * 40)
        for feature, adjustment in adjustments.items():
            if adjustment != 0:
                direction = "強化" if adjustment > 0 else "弱化"
                print(f"  {feature}: {direction} ({adjustment:+.3f})")
        
        return {
            'overall_hit_rate': overall_hit_rate,
            'pattern_stats': pattern_stats,
            'adjustments': adjustments
        }
    
    def learn(self):
        """学習実行"""
        print("🧠 改良版Toto丸くん 学習システム")
        print("=" * 50)
        
        if not self.evaluation_data:
            print("⚠️ 評価データが見つかりません")
            return
        
        print(f"📊 分析対象: {len(self.evaluation_data)}回分のデータ")
        
        # 学習レポート生成
        report = self.generate_learning_report()
        
        # 重み調整
        adjustments, overall_hit_rate = self.calculate_weight_adjustments()
        self.apply_weight_adjustments(adjustments)
        
        # 改善提案
        print(f"\n💡 改善提案:")
        print("-" * 40)
        
        if overall_hit_rate < 0.15:
            print("  🔴 的中率が低いため、大幅な調整を行いました")
            print("  📝 推奨: より多くの統計特徴量の追加を検討")
        elif overall_hit_rate < 0.25:
            print("  🟡 的中率が中程度のため、中程度の調整を行いました")
            print("  📝 推奨: パターン生成アルゴリズムの改善を検討")
        else:
            print("  🟢 的中率が良好なため、微調整のみ行いました")
            print("  📝 推奨: 現在の設定を維持")
        
        print(f"\n🎯 学習完了！次回の予測から改善された重みが適用されます。")
        print("=" * 50)

if __name__ == "__main__":
    learner = ImprovedLearningSystem()
    learner.learn() 