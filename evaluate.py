#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
from datetime import datetime
from typing import List, Dict, Tuple

class TotoEvaluator:
    def __init__(self, evaluation_file='evaluation_results.json'):
        """
        Toto予測評価クラスの初期化
        """
        self.evaluation_file = evaluation_file
        self.results = self.load_evaluation_results()
        
    def load_evaluation_results(self) -> Dict:
        """
        評価結果を読み込み
        """
        try:
            with open(self.evaluation_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except Exception as e:
            print(f"評価結果読み込みエラー: {e}")
            return {}
    
    def save_evaluation_results(self):
        """
        評価結果を保存
        """
        try:
            with open(self.evaluation_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"評価結果保存エラー: {e}")
    
    def evaluate_predictions(self, draw_date: str, predictions: List[Tuple[List[int], float]], 
                           actual_result: List[int]) -> Dict:
        """
        予測結果を評価
        
        Args:
            draw_date: 抽選日
            predictions: 予測結果のリスト [(numbers, score), ...]
            actual_result: 実際の結果
            
        Returns:
            評価結果の辞書
        """
        actual_sorted = sorted(actual_result)
        evaluation = {
            'draw_date': draw_date,
            'actual_result': actual_sorted,
            'total_predictions': len(predictions),
            'predictions': [],
            'summary': {
                'best_hit_count': 0,
                'best_prediction_index': -1,
                'average_hit_count': 0.0,
                'hit_distribution': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
            }
        }
        
        total_hits = 0
        best_hits = 0
        best_index = -1
        
        for i, (numbers, score) in enumerate(predictions):
            sorted_numbers = sorted(numbers)
            hits = len(set(sorted_numbers) & set(actual_sorted))
            
            prediction_eval = {
                'index': i + 1,
                'predicted_numbers': sorted_numbers,
                'confidence_score': score,
                'hit_count': hits,
                'hit_numbers': list(set(sorted_numbers) & set(actual_sorted)),
                'missed_numbers': list(set(actual_sorted) - set(sorted_numbers)),
                'extra_numbers': list(set(sorted_numbers) - set(actual_sorted))
            }
            
            evaluation['predictions'].append(prediction_eval)
            evaluation['summary']['hit_distribution'][hits] += 1
            total_hits += hits
            
            if hits > best_hits:
                best_hits = hits
                best_index = i
        
        evaluation['summary']['best_hit_count'] = best_hits
        evaluation['summary']['best_prediction_index'] = best_index + 1
        evaluation['summary']['average_hit_count'] = total_hits / len(predictions)
        
        # 結果を保存
        self.results[draw_date] = evaluation
        self.save_evaluation_results()
        
        return evaluation
    
    def print_evaluation_summary(self, evaluation: Dict):
        """
        評価結果のサマリーを表示
        """
        print(f"\n🎯 {evaluation['draw_date']} 評価結果")
        print("=" * 60)
        print(f"実際の結果: {evaluation['actual_result']}")
        print(f"予測パターン数: {evaluation['total_predictions']}")
        print(f"最高一致数: {evaluation['summary']['best_hit_count']}/6")
        print(f"平均一致数: {evaluation['summary']['average_hit_count']:.2f}/6")
        
        if evaluation['summary']['best_prediction_index'] > 0:
            best_pred = evaluation['predictions'][evaluation['summary']['best_prediction_index'] - 1]
            print(f"最高一致予測: パターン{best_pred['index']} - {best_pred['predicted_numbers']}")
            print(f"  信頼度: {best_pred['confidence_score']:.1f}%")
            print(f"  一致数字: {best_pred['hit_numbers']}")
        
        print("\n一致数分布:")
        for hits, count in evaluation['summary']['hit_distribution'].items():
            if count > 0:
                print(f"  {hits}個一致: {count}パターン")
        
        print("=" * 60)
    
    def export_evaluation_csv(self, csv_file='evaluation_summary.csv'):
        """
        評価結果をCSVファイルにエクスポート
        """
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'DrawDate', 'ActualResult', 'BestHitCount', 'BestPredictionIndex',
                    'AverageHitCount', 'TotalPredictions', 'HitDistribution'
                ])
                
                for draw_date, evaluation in self.results.items():
                    writer.writerow([
                        draw_date,
                        str(evaluation['actual_result']),
                        evaluation['summary']['best_hit_count'],
                        evaluation['summary']['best_prediction_index'],
                        f"{evaluation['summary']['average_hit_count']:.2f}",
                        evaluation['total_predictions'],
                        str(evaluation['summary']['hit_distribution'])
                    ])
            
            print(f"✅ 評価結果を {csv_file} にエクスポートしました")
        except Exception as e:
            print(f"❌ CSVエクスポートエラー: {e}")
    
    def get_performance_trends(self) -> Dict:
        """
        パフォーマンスの推移を分析
        """
        if not self.results:
            return {}
        
        trends = {
            'total_draws': len(self.results),
            'average_best_hits': 0.0,
            'average_average_hits': 0.0,
            'hit_improvement': {},
            'best_performance': {'date': '', 'hits': 0},
            'worst_performance': {'date': '', 'hits': 6}
        }
        
        total_best_hits = 0
        total_average_hits = 0
        
        for draw_date, evaluation in self.results.items():
            best_hits = evaluation['summary']['best_hit_count']
            avg_hits = evaluation['summary']['average_hit_count']
            
            total_best_hits += best_hits
            total_average_hits += avg_hits
            
            # 最高・最低パフォーマンスの記録
            if best_hits > trends['best_performance']['hits']:
                trends['best_performance'] = {'date': draw_date, 'hits': best_hits}
            
            if best_hits < trends['worst_performance']['hits']:
                trends['worst_performance'] = {'date': draw_date, 'hits': best_hits}
        
        trends['average_best_hits'] = total_best_hits / len(self.results)
        trends['average_average_hits'] = total_average_hits / len(self.results)
        
        return trends
    
    def print_performance_trends(self):
        """
        パフォーマンス推移を表示
        """
        trends = self.get_performance_trends()
        if not trends:
            print("評価データがありません")
            return
        
        print("\n📊 パフォーマンス推移")
        print("=" * 60)
        print(f"総評価回数: {trends['total_draws']}回")
        print(f"平均最高一致数: {trends['average_best_hits']:.2f}/6")
        print(f"平均一致数: {trends['average_average_hits']:.2f}/6")
        print(f"最高パフォーマンス: {trends['best_performance']['date']} ({trends['best_performance']['hits']}/6)")
        print(f"最低パフォーマンス: {trends['worst_performance']['date']} ({trends['worst_performance']['hits']}/6)")
        print("=" * 60) 