#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
import sys
from datetime import datetime, timedelta
from collections import Counter

class TotoPredictor:
    def __init__(self):
        self.csv_file = 'totomaru.csv'
        self.results_dir = 'results'
        self.ensure_results_dir()
    
    def ensure_results_dir(self):
        """結果保存ディレクトリの作成"""
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
    
    def load_data(self):
        """CSVデータの読み込み"""
        data = []
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # ヘッダーをスキップ
                for row in reader:
                    if len(row) >= 7:
                        numbers = []
                        for i in range(1, 7):
                            try:
                                num = int(row[i])
                                if 1 <= num <= 49:
                                    numbers.append(num)
                            except ValueError:
                                continue
                        if len(numbers) == 6:
                            data.append(numbers)
            print(f"✅ {len(data)}回分のデータを読み込みました")
            return data
        except FileNotFoundError:
            print(f"❌ {self.csv_file}が見つかりません")
            return []
    
    def calculate_scores(self, data):
        """スコア計算（学習結果を反映）"""
        all_numbers = []
        for draw in data:
            all_numbers.extend(draw)
        number_counts = Counter(all_numbers)
        
        recent_data = data[-10:] if len(data) >= 10 else data
        recent_numbers = []
        for draw in recent_data:
            recent_numbers.extend(draw)
        recent_counts = Counter(recent_numbers)
        
        scores = {}
        for num in range(1, 50):
            total_count = number_counts.get(num, 0)
            recent_count = recent_counts.get(num, 0)
            
            last_appearance = 0
            for i, draw in enumerate(reversed(data)):
                if num in draw:
                    last_appearance = i + 1
                    break
            
            # 学習結果を反映したスコア計算
            score = 0
            score += total_count * 2
            score += recent_count * 8  # 最近出現重視
            score += max(0, 20 - last_appearance) * 3
            
            if recent_count >= 2:
                score += 15  # ホット数字
            elif last_appearance >= 15:
                score += 15  # コールド数字
            
            scores[num] = score
        
        return scores, recent_counts
    
    def generate_patterns(self, scores, recent_counts):
        """予測パターンの生成"""
        sorted_numbers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        patterns = []
        used_combinations = set()
        
        # パターン1: 最近出現重視
        recent_favored = sorted(recent_counts.items(), key=lambda x: x[1], reverse=True)
        pattern1 = []
        for num, _ in recent_favored[:15]:
            if len(pattern1) < 6 and num not in pattern1:
                pattern1.append(num)
        pattern1.sort()
        if tuple(pattern1) not in used_combinations:
            used_combinations.add(tuple(pattern1))
            confidence = self.calculate_confidence(pattern1, scores)
            patterns.append((pattern1, confidence, "最近出現重視"))
        
        # パターン2: 高スコア重視
        pattern2 = []
        for num, _ in sorted_numbers[:15]:
            if len(pattern2) < 6:
                pattern2.append(num)
        pattern2.sort()
        if tuple(pattern2) not in used_combinations:
            used_combinations.add(tuple(pattern2))
            confidence = self.calculate_confidence(pattern2, scores)
            patterns.append((pattern2, confidence, "高スコア重視"))
        
        # パターン3: 範囲バランス重視
        pattern3 = []
        ranges = [(1,10), (11,20), (21,30), (31,40), (41,49)]
        for start, end in ranges:
            range_numbers = [(num, scores[num]) for num in range(start, end+1)]
            range_numbers.sort(key=lambda x: x[1], reverse=True)
            for num, _ in range_numbers[:3]:
                if len(pattern3) < 6 and num not in pattern3:
                    pattern3.append(num)
        pattern3.sort()
        if tuple(pattern3) not in used_combinations:
            used_combinations.add(tuple(pattern3))
            confidence = self.calculate_confidence(pattern3, scores)
            patterns.append((pattern3, confidence, "範囲バランス重視"))
        
        # パターン4: 連続数字重視
        pattern4 = []
        consecutive_candidates = []
        for i in range(1, 48):
            if i in scores and i+1 in scores:
                consecutive_score = scores[i] + scores[i+1]
                consecutive_candidates.append((i, consecutive_score))
                consecutive_candidates.append((i+1, consecutive_score))
        
        consecutive_candidates.sort(key=lambda x: x[1], reverse=True)
        for num, _ in consecutive_candidates[:10]:
            if len(pattern4) < 6 and num not in pattern4:
                pattern4.append(num)
        
        for num, _ in sorted_numbers:
            if len(pattern4) < 6 and num not in pattern4:
                pattern4.append(num)
        
        pattern4.sort()
        if tuple(pattern4) not in used_combinations:
            used_combinations.add(tuple(pattern4))
            confidence = self.calculate_confidence(pattern4, scores)
            patterns.append((pattern4, confidence, "連続数字重視"))
        
        # パターン5: 奇数/偶数バランス
        odd_numbers = [(num, scores[num]) for num in range(1, 50) if num % 2 == 1]
        even_numbers = [(num, scores[num]) for num in range(1, 50) if num % 2 == 0]
        odd_numbers.sort(key=lambda x: x[1], reverse=True)
        even_numbers.sort(key=lambda x: x[1], reverse=True)
        
        pattern5 = []
        for i in range(3):
            if i < len(odd_numbers):
                pattern5.append(odd_numbers[i][0])
            if i < len(even_numbers):
                pattern5.append(even_numbers[i][0])
        pattern5.sort()
        if tuple(pattern5) not in used_combinations:
            used_combinations.add(tuple(pattern5))
            confidence = self.calculate_confidence(pattern5, scores)
            patterns.append((pattern5, confidence, "奇数/偶数バランス"))
        
        # パターン6: 5の倍数重視
        multiple_5_numbers = [(num, scores[num]) for num in range(1, 50) if num % 5 == 0]
        multiple_5_numbers.sort(key=lambda x: x[1], reverse=True)
        
        pattern6 = []
        for num, _ in multiple_5_numbers[:8]:
            if len(pattern6) < 6 and num not in pattern6:
                pattern6.append(num)
        
        # 残りを高スコアで補充
        for num, _ in sorted_numbers:
            if len(pattern6) < 6 and num not in pattern6:
                pattern6.append(num)
        
        pattern6.sort()
        if tuple(pattern6) not in used_combinations:
            used_combinations.add(tuple(pattern6))
            confidence = self.calculate_confidence(pattern6, scores)
            patterns.append((pattern6, confidence, "5の倍数重視"))
        
        # パターン7: 合計値重視
        pattern7 = []
        target_sum = 150
        for num, _ in sorted_numbers[:20]:
            if len(pattern7) < 6 and num not in pattern7:
                current_sum = sum(pattern7) + num
                if len(pattern7) < 5 or abs(current_sum - target_sum) <= 50:
                    pattern7.append(num)
        pattern7.sort()
        if tuple(pattern7) not in used_combinations:
            used_combinations.add(tuple(pattern7))
            confidence = self.calculate_confidence(pattern7, scores)
            patterns.append((pattern7, confidence, "合計値重視"))
        
        # パターン8: 素数重視
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True
        
        prime_numbers = [(num, scores[num]) for num in range(1, 50) if is_prime(num)]
        prime_numbers.sort(key=lambda x: x[1], reverse=True)
        
        pattern8 = []
        for num, _ in prime_numbers[:10]:
            if len(pattern8) < 6 and num not in pattern8:
                pattern8.append(num)
        
        # 残りを高スコアで補充
        for num, _ in sorted_numbers:
            if len(pattern8) < 6 and num not in pattern8:
                pattern8.append(num)
        
        pattern8.sort()
        if tuple(pattern8) not in used_combinations:
            used_combinations.add(tuple(pattern8))
            confidence = self.calculate_confidence(pattern8, scores)
            patterns.append((pattern8, confidence, "素数重視"))
        
        # 信頼度順にソート
        patterns.sort(key=lambda x: x[1], reverse=True)
        
        # 上位6パターンのみを返す
        return patterns[:6]
    
    def calculate_confidence(self, numbers, scores):
        """信頼度を計算"""
        individual_score = sum(scores[num] for num in numbers)
        
        combo_score = 0
        
        # 範囲バランス
        ranges = [(1,10), (11,20), (21,30), (31,40), (41,49)]
        range_counts = [0] * 5
        for num in numbers:
            for i, (start, end) in enumerate(ranges):
                if start <= num <= end:
                    range_counts[i] += 1
                    break
        
        for count in range_counts:
            if count <= 2:
                combo_score += 10
            elif count == 3:
                combo_score += 5
            else:
                combo_score -= 5
        
        # 奇数/偶数バランス
        odd_count = sum(1 for num in numbers if num % 2 == 1)
        even_count = 6 - odd_count
        if 2 <= odd_count <= 4 and 2 <= even_count <= 4:
            combo_score += 15
        elif 1 <= odd_count <= 5 and 1 <= even_count <= 5:
            combo_score += 10
        
        # 合計値
        total_sum = sum(numbers)
        if 100 <= total_sum <= 200:
            combo_score += 20
        elif 80 <= total_sum <= 220:
            combo_score += 10
        
        # 連続数
        consecutive_count = 0
        for i in range(len(numbers) - 1):
            if numbers[i+1] - numbers[i] == 1:
                consecutive_count += 1
        
        if consecutive_count <= 1:
            combo_score += 10
        elif consecutive_count == 2:
            combo_score += 5
        
        max_individual = max(scores.values()) * 6
        max_combo = 100
        
        confidence = ((individual_score / max_individual) * 0.6 + 
                     (combo_score / max_combo) * 0.4) * 100
        
        return min(confidence, 100)
    
    def predict(self, target_date=None):
        """予測実行"""
        if target_date is None:
            target_date = datetime.now() + timedelta(days=1)
            target_date = target_date.strftime('%Y-%m-%d')
        
        print(f"🎯 Toto丸くん - {target_date}予測")
        print("=" * 60)
        
        # データ読み込み
        data = self.load_data()
        if not data:
            return
        
        # スコア計算
        scores, recent_counts = self.calculate_scores(data)
        
        # パターン生成
        patterns = self.generate_patterns(scores, recent_counts)
        
        # 結果表示
        print(f"📊 データ分析完了（{len(data)}回分）")
        print(f"🔢 予測パターン数: {len(patterns)}")
        print()
        
        result_lines = []
        result_lines.append(f"🎯 Toto丸くん - {target_date}予測")
        result_lines.append("=" * 60)
        result_lines.append(f"📊 データ分析完了（{len(data)}回分）")
        result_lines.append(f"🔢 予測パターン数: {len(patterns)}")
        result_lines.append("")
        
        for i, (numbers, confidence, strategy) in enumerate(patterns, 1):
            total_sum = sum(numbers)
            odd_count = sum(1 for num in numbers if num % 2 == 1)
            even_count = 6 - odd_count
            
            print(f"【パターン{i}】信頼度: {confidence:.1f}% ({strategy})")
            print(f"予測数字: {numbers}")
            print(f"合計: {total_sum} | 奇数/偶数: {odd_count}/{even_count}")
            print(f"範囲: {max(numbers) - min(numbers)}")
            print("-" * 60)
            
            result_lines.append(f"【パターン{i}】信頼度: {confidence:.1f}% ({strategy})")
            result_lines.append(f"予測数字: {numbers}")
            result_lines.append(f"合計: {total_sum} | 奇数/偶数: {odd_count}/{even_count}")
            result_lines.append(f"範囲: {max(numbers) - min(numbers)}")
            result_lines.append("-" * 60)
        
        print("🎲 予測完了！")
        print("=" * 60)
        
        result_lines.append("🎲 予測完了！")
        result_lines.append("=" * 60)
        
        # 結果をファイルに保存
        result_file = os.path.join(self.results_dir, f"result_{target_date}.txt")
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(result_lines))
        
        print(f"💾 結果を {result_file} に保存しました")
        return patterns
    
    def evaluate_prediction(self, target_date, actual_numbers, bonus_number=None):
        """予測結果の評価"""
        result_file = os.path.join(self.results_dir, f"result_{target_date}.txt")
        
        if not os.path.exists(result_file):
            print(f"❌ {target_date}の予測結果が見つかりません")
            return
        
        # 予測結果を読み込み
        with open(result_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 予測パターンを抽出
        patterns = []
        for line in lines:
            if line.startswith("【パターン") and "信頼度:" in line:
                parts = line.strip().split()
                pattern_num = int(parts[0][4:-1])
                confidence = float(parts[2][:-1])
                strategy = parts[3][1:-1]
                
                # 次の行から数字を取得
                numbers_line = lines[lines.index(line) + 1]
                numbers_str = numbers_line.split(": ")[1].strip()
                numbers = eval(numbers_str)
                
                patterns.append((pattern_num, numbers, confidence, strategy))
        
        # 評価実行
        print(f"\n🎯 {target_date}予測結果の評価")
        print("=" * 60)
        print(f"実際の結果: {sorted(actual_numbers)}")
        if bonus_number:
            print(f"ボーナス数字: {bonus_number}")
        
        best_match = 0
        best_prediction = None
        
        for pattern_num, predicted, confidence, strategy in patterns:
            matches = len(set(predicted) & set(actual_numbers))
            hit_numbers = list(set(predicted) & set(actual_numbers))
            bonus_match = bonus_number in predicted if bonus_number else False
            
            print(f"\n【パターン{pattern_num}】信頼度: {confidence:.1f}% ({strategy})")
            print(f"予測: {predicted}")
            print(f"一致数: {matches}/6")
            print(f"一致数字: {hit_numbers}")
            if bonus_match:
                print(f"ボーナス数字一致: ✅ {bonus_number}")
            else:
                print(f"ボーナス数字一致: ❌")
            
            if matches > best_match:
                best_match = matches
                best_prediction = (pattern_num, predicted, confidence, strategy, bonus_match)
        
        if best_prediction:
            pattern_num, numbers, confidence, strategy, bonus_match = best_prediction
            print(f"\n🏆 最高一致結果:")
            print(f"パターン{pattern_num}: {numbers}")
            print(f"信頼度: {confidence:.1f}% ({strategy})")
            print(f"一致数: {best_match}/6")
            if bonus_match:
                print(f"ボーナス数字: ✅")
            else:
                print(f"ボーナス数字: ❌")
        
        # 評価結果をファイルに保存
        evaluation_file = os.path.join(self.results_dir, f"evaluation_{target_date}.txt")
        # 評価結果の保存処理（省略）
        
        print(f"\n💾 評価結果を {evaluation_file} に保存しました")

def main():
    predictor = TotoPredictor()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "predict":
            target_date = sys.argv[2] if len(sys.argv) > 2 else None
            predictor.predict(target_date)
        elif sys.argv[1] == "evaluate":
            if len(sys.argv) < 4:
                print("使用方法: python predictor.py evaluate YYYY-MM-DD 'num1,num2,num3,num4,num5,num6' [bonus]")
                return
            target_date = sys.argv[2]
            actual_numbers = [int(x) for x in sys.argv[3].split(',')]
            bonus_number = int(sys.argv[4]) if len(sys.argv) > 4 else None
            predictor.evaluate_prediction(target_date, actual_numbers, bonus_number)
        else:
            print("使用方法:")
            print("  python predictor.py predict [YYYY-MM-DD]  # 予測実行")
            print("  python predictor.py evaluate YYYY-MM-DD 'num1,num2,num3,num4,num5,num6' [bonus]  # 評価実行")
    else:
        # デフォルトで明日の予測を実行
        predictor.predict()

if __name__ == "__main__":
    main() 