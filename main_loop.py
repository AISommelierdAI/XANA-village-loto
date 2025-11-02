#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import json
import csv
from datetime import datetime
from typing import List, Dict, Tuple
from features import TotoFeatures
from predict_adaptive import TotoPredictorAdaptive
from evaluate import TotoEvaluator
from learn import TotoLearner

class TotoLearningSystem:
    def __init__(self, csv_file='totomaru.csv'):
        """
        自己学習型Totoシステムの初期化
        """
        self.csv_file = csv_file
        self.predictor = TotoPredictorAdaptive(csv_file)
        self.evaluator = TotoEvaluator()
        self.learner = TotoLearner()
        self.processed_dates = self.load_processed_dates()
        
    def load_processed_dates(self) -> set:
        """
        既に処理済みの日付を読み込み
        """
        try:
            with open('processed_dates.json', 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except FileNotFoundError:
            return set()
        except Exception as e:
            print(f"処理済み日付読み込みエラー: {e}")
            return set()
    
    def save_processed_dates(self):
        """
        処理済み日付を保存
        """
        try:
            with open('processed_dates.json', 'w', encoding='utf-8') as f:
                json.dump(list(self.processed_dates), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"処理済み日付保存エラー: {e}")
    
    def get_unprocessed_draws(self) -> List[Dict]:
        """
        未処理の抽選データを取得
        """
        try:
            df = pd.read_csv(self.csv_file)
            unprocessed = []
            
            for _, row in df.iterrows():
                draw_date = row['DrawDate']
                if draw_date not in self.processed_dates:
                    # 実際の結果を取得
                    actual_result = [
                        row['Number1'], row['Number2'], row['Number3'],
                        row['Number4'], row['Number5'], row['Number6']
                    ]
                    unprocessed.append({
                        'date': draw_date,
                        'actual_result': actual_result
                    })
            
            return unprocessed
        except Exception as e:
            print(f"未処理抽選データ取得エラー: {e}")
            return []
    
    def process_single_draw(self, draw_info: Dict) -> bool:
        """
        単一の抽選を処理
        
        Args:
            draw_info: 抽選情報 {'date': str, 'actual_result': List[int]}
            
        Returns:
            処理成功フラグ
        """
        draw_date = draw_info['date']
        actual_result = draw_info['actual_result']
        
        print(f"\n🔄 {draw_date} の処理開始")
        print("=" * 60)
        
        try:
            # 1. 特徴量抽出
            print("📊 特徴量抽出中...")
            features = self.predictor.all_features
            
            # 2. 予測（現在の重みを使用）
            print("🎯 予測生成中...")
            predictions = self.predictor.predict_numbers(num_candidates=20, num_predictions=6)
            
            # 予測結果を表示
            print(f"\n📋 {draw_date} の予測結果:")
            for i, (numbers, score) in enumerate(predictions, 1):
                confidence = self.predictor.calculate_confidence_score(numbers, score)
                sorted_numbers = sorted(numbers)
                print(f"  パターン{i}: {sorted_numbers} (信頼度: {confidence:.1f}%)")
            
            # 3. 評価
            print(f"\n📈 評価実行中...")
            evaluation = self.evaluator.evaluate_predictions(
                draw_date, predictions, actual_result
            )
            self.evaluator.print_evaluation_summary(evaluation)
            
            # 4. 学習
            print(f"\n🧠 学習実行中...")
            self.learner.learn_from_evaluation(draw_date, features)
            
            # 5. 重みを再読み込み（学習後の重みを反映）
            self.predictor.weights = self.learner.weights
            
            # 処理済みとして記録
            self.processed_dates.add(draw_date)
            self.save_processed_dates()
            
            print(f"✅ {draw_date} の処理完了")
            return True
            
        except Exception as e:
            print(f"❌ {draw_date} の処理エラー: {e}")
            return False
    
    def run_learning_loop(self, max_draws=None):
        """
        学習ループを実行
        
        Args:
            max_draws: 最大処理回数（Noneの場合は全件処理）
        """
        print("🚀 自己学習型ToTo〇くん 開始")
        print("=" * 60)
        
        # 現在の重み情報を表示
        self.predictor.print_weight_info()
        
        # 未処理の抽選を取得
        unprocessed = self.get_unprocessed_draws()
        
        if not unprocessed:
            print("✅ 処理済みの抽選はありません")
            return
        
        print(f"📋 未処理抽選数: {len(unprocessed)}件")
        
        # 最大処理回数の制限
        if max_draws:
            unprocessed = unprocessed[:max_draws]
            print(f"📋 今回処理予定: {len(unprocessed)}件")
        
        # 各抽選を順次処理
        success_count = 0
        for i, draw_info in enumerate(unprocessed, 1):
            print(f"\n🔄 進捗: {i}/{len(unprocessed)}")
            
            if self.process_single_draw(draw_info):
                success_count += 1
            else:
                print(f"⚠️ {draw_info['date']} の処理をスキップしました")
        
        # 最終結果を表示
        print(f"\n🎉 学習ループ完了")
        print("=" * 60)
        print(f"処理成功: {success_count}/{len(unprocessed)}件")
        
        # 最終的な重み情報を表示
        print("\n⚖️ 学習後の重み設定:")
        self.predictor.print_weight_info()
        
        # パフォーマンス推移を表示
        self.evaluator.print_performance_trends()
        
        # 評価結果をCSVにエクスポート
        self.evaluator.export_evaluation_csv()
        
        print("=" * 60)
    
    def predict_next_draw(self, draw_date: str = None):
        """
        次回抽選の予測を実行
        """
        if not draw_date:
            draw_date = "次回抽選"
        
        print(f"\n🎯 {draw_date} の予測")
        print("=" * 60)
        
        # 現在の重み情報を表示
        self.predictor.print_weight_info()
        
        # 予測実行
        predictions = self.predictor.predict_numbers(num_candidates=25, num_predictions=6)
        
        print(f"\n📋 予測結果:")
        for i, (numbers, score) in enumerate(predictions, 1):
            confidence = self.predictor.calculate_confidence_score(numbers, score)
            sorted_numbers = sorted(numbers)
            print(f"  パターン{i}: {sorted_numbers} (信頼度: {confidence:.1f}%)")
            
            # 予測理由を表示
            reasons = self.predictor.get_prediction_reasons(numbers)
            print(f"    理由: {'; '.join(reasons[:3])}")  # 上位3つの理由のみ表示
        
        print("=" * 60)
        return predictions
    
    def add_actual_result(self, draw_date: str, actual_result: List[int]):
        """
        実際の結果を追加
        
        Args:
            draw_date: 抽選日
            actual_result: 実際の結果（6個の数字）
        """
        try:
            # CSVファイルに追加
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([draw_date, '金'] + actual_result)
            
            print(f"✅ {draw_date} の実際の結果を追加しました: {actual_result}")
            
            # 即座に学習処理を実行
            draw_info = {'date': draw_date, 'actual_result': actual_result}
            self.process_single_draw(draw_info)
            
        except Exception as e:
            print(f"❌ 実際の結果追加エラー: {e}")
    
    def get_system_status(self) -> Dict:
        """
        システムの現在の状態を取得
        """
        status = {
            'total_processed': len(self.processed_dates),
            'current_weights': self.predictor.weights,
            'performance_trends': self.evaluator.get_performance_trends(),
            'last_processed_date': max(self.processed_dates) if self.processed_dates else None
        }
        return status
    
    def print_system_status(self):
        """
        システムの現在の状態を表示
        """
        status = self.get_system_status()
        
        print("\n📊 システム状態")
        print("=" * 60)
        print(f"処理済み抽選数: {status['total_processed']}件")
        
        if status['last_processed_date']:
            print(f"最終処理日: {status['last_processed_date']}")
        
        trends = status['performance_trends']
        if trends:
            print(f"平均最高一致数: {trends['average_best_hits']:.2f}/6")
            print(f"平均一致数: {trends['average_average_hits']:.2f}/6")
        
        print("\n現在の重み設定:")
        sorted_weights = sorted(status['current_weights'].items(), key=lambda x: x[1], reverse=True)
        for feature_name, weight in sorted_weights[:5]:  # 上位5つのみ表示
            print(f"  {feature_name}: {weight:.3f}")
        
        print("=" * 60)

def main():
    """
    メイン実行関数
    """
    system = TotoLearningSystem()

    print("🤖 自己学習型ToTo〇くん v2.0")
    print("=" * 60)
    
    while True:
        print("\n📋 メニュー:")
        print("1. 学習ループ実行（全未処理抽選）")
        print("2. 学習ループ実行（指定回数）")
        print("3. 次回抽選予測")
        print("4. 実際の結果を追加")
        print("5. システム状態表示")
        print("6. 終了")
        
        choice = input("\n選択してください (1-6): ").strip()
        
        if choice == '1':
            system.run_learning_loop()
        elif choice == '2':
            try:
                max_draws = int(input("処理回数を入力してください: "))
                system.run_learning_loop(max_draws)
            except ValueError:
                print("❌ 無効な入力です")
        elif choice == '3':
            system.predict_next_draw()
        elif choice == '4':
            try:
                draw_date = input("抽選日を入力してください (YYYY-MM-DD): ")
                numbers_input = input("6個の数字をカンマ区切りで入力してください: ")
                numbers = [int(x.strip()) for x in numbers_input.split(',')]
                if len(numbers) == 6:
                    system.add_actual_result(draw_date, numbers)
                else:
                    print("❌ 6個の数字を入力してください")
            except (ValueError, IndexError):
                print("❌ 無効な入力です")
        elif choice == '5':
            system.print_system_status()
        elif choice == '6':
            print("👋 自己学習型ToTo〇くんを終了します")
            break
        else:
            print("❌ 無効な選択です")

if __name__ == "__main__":
    main() 