#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from typing import List, Tuple

class SimpleNumberGame:
    """
    1～6の数字から3つを順次選択するシンプルなゲーム
    """
    
    def __init__(self):
        self.available_numbers = list(range(1, 7))  # 1～6
        self.selected_numbers = []
        self.current_step = 1  # 1: 1桁目, 2: 2桁目, 3: 3桁目
    
    def get_available_numbers(self) -> List[int]:
        """
        現在選択可能な数字のリストを返す
        """
        return [num for num in self.available_numbers if num not in self.selected_numbers]
    
    def select_number(self, number: int) -> Tuple[bool, str]:
        """
        数字を選択する
        
        Args:
            number: 選択する数字（1～6）
            
        Returns:
            (成功フラグ, メッセージ)
        """
        if number not in self.available_numbers:
            return False, f"Error: {number} is invalid (select from 1-6)"
        
        if number in self.selected_numbers:
            return False, f"Error: {number} is already selected"
        
        if self.current_step > 3:
            return False, "Error: Already selected 3 numbers"
        
        # Select number
        self.selected_numbers.append(number)
        
        # Move to next step
        self.current_step += 1
        
        if self.current_step <= 3:
            available = self.get_available_numbers()
            return True, f"Selected {number}! Next choose from {available}"
        else:
            return True, f"Selected {number}! Game complete!"
    
    def get_game_status(self) -> dict:
        """
        ゲームの現在の状態を取得
        """
        return {
            'current_step': self.current_step,
            'selected_numbers': self.selected_numbers.copy(),
            'available_numbers': self.get_available_numbers(),
            'is_complete': len(self.selected_numbers) == 3
        }
    
    def reset_game(self):
        """
        ゲームをリセット
        """
        self.selected_numbers = []
        self.current_step = 1
    
    def get_random_suggestion(self) -> int:
        """
        ランダムな数字を提案（AI的な提案）
        """
        available = self.get_available_numbers()
        if not available:
            return None
        return random.choice(available)
    
    def get_smart_suggestion(self) -> int:
        """
        スマートな数字を提案（戦略的な提案）
        """
        available = self.get_available_numbers()
        if not available:
            return None
        
        # 戦略的な提案ロジック
        if len(self.selected_numbers) == 0:
            # 1桁目: 中央値付近を提案
            return 3 if 3 in available else random.choice(available)
        elif len(self.selected_numbers) == 1:
            # 2桁目: 1桁目とバランスを取る
            first = self.selected_numbers[0]
            if first <= 3:
                # 1桁目が小さい場合、大きい数字を提案
                candidates = [num for num in available if num > 3]
                return random.choice(candidates) if candidates else random.choice(available)
            else:
                # 1桁目が大きい場合、小さい数字を提案
                candidates = [num for num in available if num <= 3]
                return random.choice(candidates) if candidates else random.choice(available)
        else:
            # 3桁目: 残りの数字からランダム
            return random.choice(available)
    
    def get_final_result(self) -> dict:
        """
        最終結果を取得
        """
        if len(self.selected_numbers) != 3:
            return None
        
        return {
            'numbers': self.selected_numbers.copy(),
            'sum': sum(self.selected_numbers),
            'pattern': self._analyze_pattern(),
            'message': self._get_result_message()
        }
    
    def _analyze_pattern(self) -> str:
        """
        Analyze pattern of selected numbers
        """
        numbers = sorted(self.selected_numbers)
        
        # Check consecutive numbers
        if numbers == [1, 2, 3] or numbers == [2, 3, 4] or numbers == [3, 4, 5] or numbers == [4, 5, 6]:
            return "連続数字"
        
        # Odd/even balance
        odd_count = sum(1 for num in numbers if num % 2 == 1)
        if odd_count == 0:
            return "全偶数"
        elif odd_count == 3:
            return "全奇数"
        elif odd_count == 1:
            return "奇数1個"
        elif odd_count == 2:
            return "奇数2個"
        
        # Classification by total
        total = sum(numbers)
        if total <= 6:
            return "小さい合計"
        elif total >= 15:
            return "大きい合計"
        else:
            return "中程度の合計"
    
    def _get_result_message(self) -> str:
        """
        Generate message based on result
        """
        numbers = self.selected_numbers
        total = sum(numbers)
        pattern = self._analyze_pattern()
        
        messages = {
            "連続数字": "Consecutive numbers! Great choice!",
            "全偶数": "All even numbers! Balanced choice!",
            "全奇数": "All odd numbers! Strong choice!",
            "小さい合計": "Small total! Conservative choice!",
            "大きい合計": "Large total! Aggressive choice!",
            "中程度の合計": "Medium total! Balanced choice!"
        }
        
        base_message = messages.get(pattern, "Unique choice!")
        return f"{base_message} Total: {total}"

def main():
    """
    ゲームのメイン実行関数
    """
    game = SimpleNumberGame()
    
    print("Simple Number Game")
    print("=" * 40)
    print("Select 3 numbers from 1-6 in sequence")
    print("Cannot select already chosen numbers")
    print("=" * 40)
    
    while not game.get_game_status()['is_complete']:
        status = game.get_game_status()
        
        print(f"\nStep {status['current_step']}/3")
        print(f"Selected: {status['selected_numbers']}")
        print(f"Available: {status['available_numbers']}")
        
        # AI suggestion
        suggestion = game.get_smart_suggestion()
        print(f"AI suggestion: {suggestion}")
        
        try:
            choice = input("Select a number (1-6): ").strip()
            number = int(choice)
            
            success, message = game.select_number(number)
            print(message)
            
            if not success:
                continue
                
        except ValueError:
            print("Invalid input. Please enter a number 1-6.")
        except KeyboardInterrupt:
            print("\nGame ended")
            return
    
    # Final result display
    result = game.get_final_result()
    print("\nGame Complete!")
    print("=" * 40)
    print(f"Selected numbers: {result['numbers']}")
    print(f"Sum: {result['sum']}")
    print(f"Pattern: {result['pattern']}")
    print(f"Message: {result['message']}")
    print("=" * 40)

if __name__ == "__main__":
    main()
