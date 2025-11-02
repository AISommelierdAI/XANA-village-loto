#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from learn import TotoLearner

def main():
    print("🧠 ToTo〇くん 学習システム")
    print("=" * 50)
    
    # 学習クラスの初期化
    learner = TotoLearner()
    
    # 現在の重み設定を表示
    print("📊 現在の重み設定:")
    learner.print_weight_summary()
    
    # 学習実行（2023-09-07の結果から）
    print("\n🔧 学習による重み調整:")
    print("-" * 40)
    
    # 合計値制御重視の重みを微調整（1個一致したため）
    old_total_weight = learner.weights['total_appearances']
    learner.weights['total_appearances'] = max(0.01, old_total_weight - 0.005)
    print(f"total_appearances: {old_total_weight:.3f} → {learner.weights['total_appearances']:.3f} (-0.005)")
    
    # 時間的パターン重視の重みを微調整（1個一致したため）
    old_recent_weight = learner.weights['recent_appearances']
    learner.weights['recent_appearances'] = max(0.01, old_recent_weight - 0.005)
    print(f"recent_appearances: {old_recent_weight:.3f} → {learner.weights['recent_appearances']:.3f} (-0.005)")
    
    # 間隔分析重視の重みを微調整（1個一致したため）
    old_adjacent_weight = learner.weights['adjacent_correlation']
    learner.weights['adjacent_correlation'] = max(0.01, old_adjacent_weight - 0.005)
    print(f"adjacent_correlation: {old_adjacent_weight:.3f} → {learner.weights['adjacent_correlation']:.3f} (-0.005)")
    
    # 高範囲重視の重みを微調整（1個一致したため）
    old_hot_cold_weight = learner.weights['hot_cold']
    learner.weights['hot_cold'] = max(0.01, old_hot_cold_weight - 0.005)
    print(f"hot_cold: {old_hot_cold_weight:.3f} → {learner.weights['hot_cold']:.3f} (-0.005)")
    
    # 範囲バランス重視の重みを減少（0個一致したため）
    old_distribution_weight = learner.weights['distribution']
    learner.weights['distribution'] = max(0.01, old_distribution_weight - 0.01)
    print(f"distribution: {old_distribution_weight:.3f} → {learner.weights['distribution']:.3f} (-0.010)")
    
    # 低範囲重視の重みを減少（0個一致したため）
    old_periodicity_weight = learner.weights['periodicity']
    learner.weights['periodicity'] = max(0.01, old_periodicity_weight - 0.01)
    print(f"periodicity: {old_periodicity_weight:.3f} → {learner.weights['periodicity']:.3f} (-0.010)")
    
    # 中範囲重視の重みを増加（実際の結果が中範囲中心だったため）
    old_missing_weight = learner.weights['missing_intervals']
    learner.weights['missing_intervals'] = min(0.5, old_missing_weight + 0.02)
    print(f"missing_intervals: {old_missing_weight:.3f} → {learner.weights['missing_intervals']:.3f} (+0.020)")
    
    # 重みの正規化
    total_weight = sum(learner.weights.values())
    for feature_name in learner.weights:
        learner.weights[feature_name] /= total_weight
    
    print("-" * 40)
    print("✅ 重み調整完了")
    
    # 調整後の重みを保存
    learner.save_weights()
    
    print("\n📊 調整後の重み設定:")
    learner.print_weight_summary()
    
    print("\n🎯 学習完了！次回の予測から改善された重みが適用されます。")
    print("📈 中範囲（17-32）の数字が多く出る傾向を学習しました！")

if __name__ == "__main__":
    main() 