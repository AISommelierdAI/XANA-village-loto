#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
import sys
from datetime import datetime, timedelta
from collections import Counter
import statistics

class AdvancedTotoPredictor:
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
    
    def analyze_number_ranges(self, data):
        """数字の範囲分布を分析"""
        ranges = {
            'low': (1, 16),      # 1-16
            'mid': (17, 32),     # 17-32  
            'high': (33, 49)     # 33-49
        }
        
        range_counts = {'low': 0, 'mid': 0, 'high': 0}
        range_numbers = {'low': [], 'mid': [], 'high': []}
        
        for draw in data:
            for num in draw:
                if ranges['low'][0] <= num <= ranges['low'][1]:
                    range_counts['low'] += 1
                    range_numbers['low'].append(num)
                elif ranges['mid'][0] <= num <= ranges['mid'][1]:
                    range_counts['mid'] += 1
                    range_numbers['mid'].append(num)
                elif ranges['high'][0] <= num <= ranges['high'][1]:
                    range_counts['high'] += 1
                    range_numbers['high'].append(num)
        
        # 各範囲の出現頻度を計算
        total_numbers = sum(range_counts.values())
        range_frequencies = {}
        for range_name, count in range_counts.items():
            range_frequencies[range_name] = count / total_numbers
        
        return range_frequencies, range_numbers
    
    def analyze_sum_patterns(self, data):
        """合計値の傾向を分析"""
        sums = []
        for draw in data:
            sums.append(sum(draw))
        
        avg_sum = statistics.mean(sums)
        median_sum = statistics.median(sums)
        std_sum = statistics.stdev(sums) if len(sums) > 1 else 0
        
        # 合計値の分布を分析
        sum_ranges = {
            'low': (0, avg_sum - std_sum),
            'mid': (avg_sum - std_sum, avg_sum + std_sum),
            'high': (avg_sum + std_sum, 300)
        }
        
        return {
            'average': avg_sum,
            'median': median_sum,
            'std': std_sum,
            'ranges': sum_ranges,
            'all_sums': sums
        }
    
    def analyze_number_gaps(self, data):
        """隣接数字の間隔を分析"""
        all_gaps = []
        gap_patterns = []
        
        for draw in data:
            sorted_draw = sorted(draw)
            gaps = []
            for i in range(len(sorted_draw) - 1):
                gap = sorted_draw[i+1] - sorted_draw[i]
                gaps.append(gap)
                all_gaps.append(gap)
            gap_patterns.append(gaps)
        
        avg_gap = statistics.mean(all_gaps)
        common_gaps = Counter(all_gaps).most_common(5)
        
        return {
            'average_gap': avg_gap,
            'common_gaps': common_gaps,
            'all_gaps': all_gaps,
            'gap_patterns': gap_patterns
        }
    
    def analyze_temporal_patterns(self, data):
        """時間的なパターンを分析"""
        # 簡略化版：最近のデータを重視
        recent_data = data[-10:] if len(data) >= 10 else data
        recent_numbers = []
        for draw in recent_data:
            recent_numbers.extend(draw)
        
        recent_counts = Counter(recent_numbers)
        return recent_counts
    
    def calculate_advanced_scores(self, data):
        """高度なスコア計算"""
        all_numbers = []
        for draw in data:
            all_numbers.extend(draw)
        number_counts = Counter(all_numbers)
        
        # 範囲分析
        range_frequencies, range_numbers = self.analyze_number_ranges(data)
        
        # 合計値分析
        sum_analysis = self.analyze_sum_patterns(data)
        
        # 間隔分析
        gap_analysis = self.analyze_number_gaps(data)
        
        # 時間的パターン
        temporal_counts = self.analyze_temporal_patterns(data)
        
        scores = {}
        for num in range(1, 50):
            score = 0
            
            # 基本的な出現頻度
            total_count = number_counts.get(num, 0)
            score += total_count * 2
            
            # 最近の出現頻度
            recent_count = temporal_counts.get(num, 0)
            score += recent_count * 8
            
            # 範囲バランス
            if 1 <= num <= 16:
                score += range_frequencies['low'] * 100
            elif 17 <= num <= 32:
                score += range_frequencies['mid'] * 100
            else:
                score += range_frequencies['high'] * 100
            
            # 間隔分析
            if num in gap_analysis['common_gaps']:
                score += 10
            
            # 合計値制御（小さな数字を少し重視）
            if num <= 20:
                score += 5
            
            scores[num] = score
        
        return scores, {
            'range_frequencies': range_frequencies,
            'sum_analysis': sum_analysis,
            'gap_analysis': gap_analysis,
            'temporal_counts': temporal_counts
        }
    
    def generate_balanced_range_pattern(self, scores, analysis_data):
        """範囲バランスを重視したパターン生成"""
        pattern = []
        
        # 各範囲から2個ずつ選択
        ranges = [(1, 16), (17, 32), (33, 49)]
        
        for start, end in ranges:
            range_numbers = [(num, scores[num]) for num in range(start, end+1)]
            range_numbers.sort(key=lambda x: x[1], reverse=True)
            
            # 各範囲から上位2個を選択
            for num, _ in range_numbers[:2]:
                if len(pattern) < 6:
                    pattern.append(num)
        
        pattern.sort()
        return pattern
    
    def control_sum_value(self, numbers, target_sum=140):
        """合計値を制御する機能"""
        current_sum = sum(numbers)
        if 130 <= current_sum <= 150:
            return numbers  # 適切な範囲内
        
        # 合計値を調整
        if current_sum > 150:
            # 大きな数字を小さな数字に置き換え
            for i, num in enumerate(numbers):
                if num > 30 and len(numbers) == 6:
                    for replacement in range(1, 21):
                        if replacement not in numbers:
                            new_numbers = numbers.copy()
                            new_numbers[i] = replacement
                            if 130 <= sum(new_numbers) <= 150:
                                return sorted(new_numbers)
        
        return numbers
    
    def generate_advanced_patterns(self, scores, analysis_data):
        """高度なパターン生成"""
        patterns = []
        used_combinations = set()
        
        # パターン1: 範囲バランス重視
        pattern1 = self.generate_balanced_range_pattern(scores, analysis_data)
        pattern1 = self.control_sum_value(pattern1)
        if tuple(pattern1) not in used_combinations:
            used_combinations.add(tuple(pattern1))
            confidence = self.calculate_confidence(pattern1, scores)
            patterns.append((pattern1, confidence, "範囲バランス重視"))
        
        # パターン2: 合計値制御重視
        pattern2 = []
        target_sum = 140
        sorted_numbers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        for num, _ in sorted_numbers[:20]:
            if len(pattern2) < 6 and num not in pattern2:
                current_sum = sum(pattern2) + num
                if len(pattern2) < 5 or abs(current_sum - target_sum) <= 20:
                    pattern2.append(num)
        
        pattern2.sort()
        if tuple(pattern2) not in used_combinations:
            used_combinations.add(tuple(pattern2))
            confidence = self.calculate_confidence(pattern2, scores)
            patterns.append((pattern2, confidence, "合計値制御重視"))
        
        # パターン3: 間隔分析重視
        gap_analysis = analysis_data['gap_analysis']
        common_gaps = [gap for gap, _ in gap_analysis['common_gaps'][:3]]
        
        pattern3 = []
        if common_gaps:
            # よくある間隔を使ってパターン生成
            start_num = 1
            pattern3.append(start_num)
            for gap in common_gaps:
                if len(pattern3) < 6:
                    next_num = start_num + gap
                    if 1 <= next_num <= 49 and next_num not in pattern3:
                        pattern3.append(next_num)
                        start_num = next_num
        
        # 残りを高スコアで補充
        for num, _ in sorted_numbers:
            if len(pattern3) < 6 and num not in pattern3:
                pattern3.append(num)
        
        pattern3.sort()
        if tuple(pattern3) not in used_combinations:
            used_combinations.add(tuple(pattern3))
            confidence = self.calculate_confidence(pattern3, scores)
            patterns.append((pattern3, confidence, "間隔分析重視"))
        
        # パターン4: 時間的パターン重視
        temporal_counts = analysis_data['temporal_counts']
        recent_favored = sorted(temporal_counts.items(), key=lambda x: x[1], reverse=True)
        
        pattern4 = []
        for num, _ in recent_favored[:15]:
            if len(pattern4) < 6 and num not in pattern4:
                pattern4.append(num)
        
        pattern4.sort()
        if tuple(pattern4) not in used_combinations:
            used_combinations.add(tuple(pattern4))
            confidence = self.calculate_confidence(pattern4, scores)
            patterns.append((pattern4, confidence, "時間的パターン重視"))
        
        # パターン5: 高スコア重視（従来）
        pattern5 = []
        for num, _ in sorted_numbers[:15]:
            if len(pattern5) < 6 and num not in pattern5:
                pattern5.append(num)
        pattern5.sort()
        if tuple(pattern5) not in used_combinations:
            used_combinations.add(tuple(pattern5))
            confidence = self.calculate_confidence(pattern5, scores)
            patterns.append((pattern5, confidence, "高スコア重視"))
        
        # パターン6: 低範囲重視
        pattern6 = []
        low_range_numbers = [(num, scores[num]) for num in range(1, 21)]
        low_range_numbers.sort(key=lambda x: x[1], reverse=True)
        
        for num, _ in low_range_numbers[:8]:
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
            patterns.append((pattern6, confidence, "低範囲重視"))
        
        # パターン7: 高範囲重視
        pattern7 = []
        high_range_numbers = [(num, scores[num]) for num in range(30, 50)]
        high_range_numbers.sort(key=lambda x: x[1], reverse=True)
        
        for num, _ in high_range_numbers[:8]:
            if len(pattern7) < 6 and num not in pattern7:
                pattern7.append(num)
        
        # 残りを高スコアで補充
        for num, _ in sorted_numbers:
            if len(pattern7) < 6 and num not in pattern7:
                pattern7.append(num)
        
        pattern7.sort()
        if tuple(pattern7) not in used_combinations:
            used_combinations.add(tuple(pattern7))
            confidence = self.calculate_confidence(pattern7, scores)
            patterns.append((pattern7, confidence, "高範囲重視"))
        
        # 信頼度順にソート
        patterns.sort(key=lambda x: x[1], reverse=True)
        
        # 確実に6パターンを返す
        if len(patterns) < 6:
            # 不足している場合は追加パターンを生成
            while len(patterns) < 6:
                # ランダムなパターンを生成
                remaining_pattern = []
                for num, _ in sorted_numbers:
                    if len(remaining_pattern) < 6 and num not in remaining_pattern:
                        remaining_pattern.append(num)
                
                remaining_pattern.sort()
                if tuple(remaining_pattern) not in used_combinations:
                    used_combinations.add(tuple(remaining_pattern))
                    confidence = self.calculate_confidence(remaining_pattern, scores)
                    patterns.append((remaining_pattern, confidence, f"補完パターン{len(patterns)+1}"))
        
        return patterns[:6]
    
    def calculate_confidence(self, numbers, scores):
        """信頼度を計算"""
        individual_score = sum(scores[num] for num in numbers)
        
        combo_score = 0
        
        # 範囲バランス
        ranges = [(1,16), (17,32), (33,49)]
        range_counts = [0] * 3
        for num in numbers:
            for i, (start, end) in enumerate(ranges):
                if start <= num <= end:
                    range_counts[i] += 1
                    break
        
        # 各範囲に2個ずつあると高評価
        for count in range_counts:
            if count == 2:
                combo_score += 20
            elif count == 1:
                combo_score += 10
            elif count == 3:
                combo_score += 5
            else:
                combo_score -= 5
        
        # 合計値
        total_sum = sum(numbers)
        if 130 <= total_sum <= 150:
            combo_score += 30
        elif 120 <= total_sum <= 160:
            combo_score += 15
        
        # 間隔バランス
        gaps = []
        sorted_numbers = sorted(numbers)
        for i in range(len(sorted_numbers) - 1):
            gaps.append(sorted_numbers[i+1] - sorted_numbers[i])
        
        avg_gap = statistics.mean(gaps) if gaps else 0
        if 5 <= avg_gap <= 15:
            combo_score += 20
        elif 3 <= avg_gap <= 20:
            combo_score += 10
        
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
        
        print(f"🎯 高度なToto丸くん - {target_date}予測")
        print("=" * 60)
        
        # データ読み込み
        data = self.load_data()
        if not data:
            return
        
        # 高度なスコア計算
        scores, analysis_data = self.calculate_advanced_scores(data)
        
        # 高度なパターン生成
        patterns = self.generate_advanced_patterns(scores, analysis_data)
        
        # 分析結果表示
        print(f"📊 高度なデータ分析完了（{len(data)}回分）")
        print(f"🔢 予測パターン数: {len(patterns)}")
        
        # 範囲分析結果
        range_freq = analysis_data['range_frequencies']
        print(f"📈 範囲分布: 低(1-16): {range_freq['low']:.1%}, 中(17-32): {range_freq['mid']:.1%}, 高(33-49): {range_freq['high']:.1%}")
        
        # 合計値分析結果
        sum_analysis = analysis_data['sum_analysis']
        print(f"💰 平均合計値: {sum_analysis['average']:.1f} ± {sum_analysis['std']:.1f}")
        
        print()
        
        result_lines = []
        result_lines.append(f"🎯 高度なToto丸くん - {target_date}予測")
        result_lines.append("=" * 60)
        result_lines.append(f"📊 高度なデータ分析完了（{len(data)}回分）")
        result_lines.append(f"🔢 予測パターン数: {len(patterns)}")
        result_lines.append(f"📈 範囲分布: 低(1-16): {range_freq['low']:.1%}, 中(17-32): {range_freq['mid']:.1%}, 高(33-49): {range_freq['high']:.1%}")
        result_lines.append(f"💰 平均合計値: {sum_analysis['average']:.1f} ± {sum_analysis['std']:.1f}")
        result_lines.append("")
        
        for i, (numbers, confidence, strategy) in enumerate(patterns, 1):
            total_sum = sum(numbers)
            odd_count = sum(1 for num in numbers if num % 2 == 1)
            even_count = 6 - odd_count
            
            # 範囲分析
            ranges = [(1,16), (17,32), (33,49)]
            range_counts = [0] * 3
            for num in numbers:
                for j, (start, end) in enumerate(ranges):
                    if start <= num <= end:
                        range_counts[j] += 1
                        break
            
            print(f"【パターン{i}】信頼度: {confidence:.1f}% ({strategy})")
            print(f"予測数字: {numbers}")
            print(f"合計: {total_sum} | 奇数/偶数: {odd_count}/{even_count}")
            print(f"範囲分布: 低{range_counts[0]}個, 中{range_counts[1]}個, 高{range_counts[2]}個")
            print("-" * 60)
            
            result_lines.append(f"【パターン{i}】信頼度: {confidence:.1f}% ({strategy})")
            result_lines.append(f"予測数字: {numbers}")
            result_lines.append(f"合計: {total_sum} | 奇数/偶数: {odd_count}/{even_count}")
            result_lines.append(f"範囲分布: 低{range_counts[0]}個, 中{range_counts[1]}個, 高{range_counts[2]}個")
            result_lines.append("-" * 60)
        
        print("🎲 高度な予測完了！")
        print("=" * 60)
        
        result_lines.append("🎲 高度な予測完了！")
        result_lines.append("=" * 60)
        
        # 結果をファイルに保存
        result_file = os.path.join(self.results_dir, f"result_advanced_{target_date}.txt")
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(result_lines))
        
        print(f"💾 結果を {result_file} に保存しました")
        return patterns

def main():
    predictor = AdvancedTotoPredictor()
    
    if len(sys.argv) > 1:
        target_date = sys.argv[1]
        predictor.predict(target_date)
    else:
        # デフォルトで明日の予測を実行
        predictor.predict()

if __name__ == "__main__":
    main() 