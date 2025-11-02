import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Animated,
  Dimensions,
  Alert,
  ImageBackground,
  Platform,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

const { width, height } = Dimensions.get('window');
const isWeb = Platform.OS === 'web';

// 画像をコンポーネントの外で定義（エラー回避のためtry-catchで包む）
let backgroundImage;
try {
  backgroundImage = require('./background.png');
} catch (error) {
  console.warn('Background image not found:', error);
  backgroundImage = null;
}

export default function App() {
  const [gameState, setGameState] = useState({
    currentStep: 1,
    selectedNumbers: [],
    availableNumbers: [1, 2, 3, 4, 5, 6],
    isComplete: false,
    isAutoMode: false,
  });

  const [slotAnimations] = useState([
    new Animated.Value(0),
    new Animated.Value(0),
    new Animated.Value(0),
  ]);

  const [slotValues] = useState([
    new Animated.Value(0),
    new Animated.Value(0),
    new Animated.Value(0),
  ]);

  const [diceRotations] = useState([
    new Animated.Value(0),
    new Animated.Value(0),
    new Animated.Value(0),
  ]);

  const [showResult, setShowResult] = useState(false);
  const [result, setResult] = useState(null);

  // サイコロアニメーション（桃鉄風コロコロ回転）
  const animateDice = (diceIndex, targetNumber) => {
    // 高速回転フェーズ（サイコロがコロコロ回転）
    const fastRotation = Animated.loop(
      Animated.sequence([
        Animated.timing(diceRotations[diceIndex], {
          toValue: 1,
          duration: 60,
          useNativeDriver: true,
        }),
        Animated.timing(diceRotations[diceIndex], {
          toValue: 0,
          duration: 60,
          useNativeDriver: true,
        }),
      ]),
      { iterations: 30 } // 3.6秒間の高速回転
    );

    // 減速フェーズ
    const slowRotation = Animated.loop(
      Animated.sequence([
        Animated.timing(diceRotations[diceIndex], {
          toValue: 1,
          duration: 120,
          useNativeDriver: true,
        }),
        Animated.timing(diceRotations[diceIndex], {
          toValue: 0,
          duration: 120,
          useNativeDriver: true,
        }),
      ]),
      { iterations: 5 } // 1.2秒間の減速
    );

    // 最終停止フェーズ
    const finalStop = Animated.timing(diceRotations[diceIndex], {
      toValue: 0,
      duration: 200,
      useNativeDriver: true,
    });

    // アニメーションシーケンス（回転のみ、数字は別途制御）
    Animated.sequence([fastRotation, slowRotation, finalStop]).start();
  };

  // 自動選択機能
  const autoSelectNumbers = () => {
    // 現在のステップに応じて次のリールを回転
    const currentStep = gameState.currentStep;
    
    if (currentStep > 3) {
      // 全てのリールが完了した場合、結果を表示
      const finalResult = getFinalResult(gameState.selectedNumbers);
      setResult(finalResult);
      setShowResult(true);
      return;
    }

    // 自動モードを開始
    setGameState(prev => ({
      ...prev,
      isAutoMode: true,
    }));

    // XETAベースの乱数生成（$XETAの特性を活用）
    const generateXETARandom = () => {
      const now = Date.now();
      
      // $XETAの特性を活用した複数の要素
      const xetaElements = {
        // 現在時刻（ミリ秒）
        timestamp: now,
        // 時刻の秒部分
        seconds: Math.floor(now / 1000),
        // 時刻の分部分
        minutes: Math.floor(now / 60000),
        // 時刻の時間部分
        hours: Math.floor(now / 3600000),
        // 日付の日部分
        day: new Date(now).getDate(),
        // 日付の月部分
        month: new Date(now).getMonth() + 1,
        // 日付の年部分
        year: new Date(now).getFullYear(),
        // タイムスタンプの下6桁
        timestampTail: now % 1000000,
        // タイムスタンプの上6桁
        timestampHead: Math.floor(now / 1000000),
        // ランダム要素
        random: Math.random() * 1000000,
      };
      
      // 各要素を文字列化して結合
      const combinedString = Object.values(xetaElements).join('');
      
      // ハッシュ値を計算
      let hash = 0;
      for (let i = 0; i < combinedString.length; i++) {
        hash = ((hash << 5) - hash + combinedString.charCodeAt(i)) & 0xffffffff;
      }
      
      // 絶対値にして1-6の範囲に変換
      return Math.abs(hash) % 6 + 1;
    };

    // XETAベースの乱数で数字を選択（重複なし）
    const availableNumbers = [1, 2, 3, 4, 5, 6].filter(num => 
      !gameState.selectedNumbers.includes(num)
    );
    
    let selectedNumber;
    let attempts = 0;
    do {
      selectedNumber = generateXETARandom();
      attempts++;
    } while (!availableNumbers.includes(selectedNumber) && attempts < 100);
    
    // フォールバック（万が一の場合）
    if (!availableNumbers.includes(selectedNumber)) {
      const randomIndex = Math.floor(Math.random() * availableNumbers.length);
      selectedNumber = availableNumbers[randomIndex];
    }

    // 現在のステップのリールを回転
    const reelIndex = currentStep - 1;
    animateDice(reelIndex, selectedNumber);
    
    // アニメーション完了後に結果を表示
    setTimeout(() => {
      setGameState(prev => ({
        ...prev,
        selectedNumbers: [...prev.selectedNumbers, selectedNumber],
        currentStep: prev.currentStep + 1,
        isAutoMode: false, // アニメーション完了後に自動モードを解除
      }));
    }, 5000); // 5秒のアニメーション完了後に結果を表示
  };

  // 数字選択
  const selectNumber = (number) => {
    if (gameState.isAutoMode) return; // 自動モード中は手動選択を無効化

    if (gameState.selectedNumbers.includes(number)) {
      Alert.alert('エラー', 'この数字は既に選択されています');
      return;
    }

    if (gameState.currentStep > 3) {
      Alert.alert('エラー', '既に3つの数字が選択されています');
      return;
    }

    const newSelectedNumbers = [...gameState.selectedNumbers, number];
    const newCurrentStep = gameState.currentStep + 1;
    const newAvailableNumbers = gameState.availableNumbers.filter(n => n !== number);

    // サイコロアニメーション
    animateDice(gameState.currentStep - 1, number);

    setGameState({
      currentStep: newCurrentStep,
      selectedNumbers: newSelectedNumbers,
      availableNumbers: newAvailableNumbers,
      isComplete: newCurrentStep > 3,
      isAutoMode: false,
    });

    if (newCurrentStep > 3) {
      setTimeout(() => {
        const finalResult = getFinalResult(newSelectedNumbers);
        setResult(finalResult);
        setShowResult(true);
      }, 2000);
    }
  };

  // 最終結果の計算
  const getFinalResult = (numbers) => {
    const total = numbers.reduce((sum, num) => sum + num, 0);
    const sortedNumbers = [...numbers].sort((a, b) => a - b);
    
    let pattern = '';
    if (sortedNumbers[1] === sortedNumbers[0] + 1 && sortedNumbers[2] === sortedNumbers[1] + 1) {
      pattern = '連続数字';
    } else {
      const oddCount = numbers.filter(n => n % 2 === 1).length;
      if (oddCount === 0) pattern = '全偶数';
      else if (oddCount === 3) pattern = '全奇数';
      else if (oddCount === 1) pattern = '奇数1個';
      else pattern = '奇数2個';
    }

    return {
      numbers,
      total,
      pattern,
    };
  };

  // ゲームリセット
  const resetGame = () => {
    setGameState({
      currentStep: 1,
      selectedNumbers: [],
      availableNumbers: [1, 2, 3, 4, 5, 6],
      isComplete: false,
      isAutoMode: false,
    });
    setShowResult(false);
    setResult(null);
    slotAnimations.forEach(anim => anim.setValue(0));
    slotValues.forEach(anim => anim.setValue(0));
    diceRotations.forEach(anim => anim.setValue(0));
  };

  // サイコロ表示コンポーネント（桃鉄風コロコロ回転）
  const DiceDisplay = React.memo(({ diceIndex, number, isAnimating }) => {
    const [currentDisplayNumber, setCurrentDisplayNumber] = useState(number ? String(number) : '?');
    const [isRolling, setIsRolling] = useState(false);
    const [finalNumber, setFinalNumber] = useState(null);
    const [hasCompleted, setHasCompleted] = useState(false);

    // アニメーション値を監視して表示数字を更新
    useEffect(() => {
      // 完了したリールは何もしない
      if (hasCompleted) {
        return;
      }

      if (isAnimating) {
        setIsRolling(true);
        setFinalNumber(null);
        // 回転中は1～6の数字がくるくる回転（桃鉄風）
        const diceFaces = ['1', '2', '3', '4', '5', '6'];
        let rotationIndex = 0;
        let speed = 50; // 高速回転開始
        let rotationInterval;
        
        const startRotation = () => {
          rotationInterval = setInterval(() => {
            setCurrentDisplayNumber(diceFaces[rotationIndex]);
            rotationIndex = (rotationIndex + 1) % 6;
          }, speed);
        };

        startRotation();

        // 段階的に減速（最後まで変化させる）
        const speedUpdater = setInterval(() => {
          speed = Math.min(speed + 3, 200); // より緩やかに減速
          clearInterval(rotationInterval);
          startRotation();
        }, 300); // より頻繁に速度を更新

        // アニメーション終了直前まで回転を続ける
        const finalRotation = setTimeout(() => {
          clearInterval(rotationInterval);
          clearInterval(speedUpdater);
          // 最後の瞬間までランダムな数字を表示（目標とは違う数字）
          const wrongNumbers = diceFaces.filter((_, index) => index !== (number - 1));
          const finalRandomIndex = Math.floor(Math.random() * wrongNumbers.length);
          setCurrentDisplayNumber(wrongNumbers[finalRandomIndex]);
        }, 4800); // 約4.8秒アニメーション終了の200ms前まで回転

        return () => {
          clearInterval(rotationInterval);
          clearInterval(speedUpdater);
          clearTimeout(finalRotation);
        };
      } else {
        setIsRolling(false);
        if (number && !hasCompleted) {
          const diceFaces = ['1', '2', '3', '4', '5', '6'];
          // アニメーション完了時に最終結果を表示
          setTimeout(() => {
            setFinalNumber(diceFaces[number - 1]);
            setCurrentDisplayNumber(diceFaces[number - 1]);
            setHasCompleted(true);
          }, 100); // 少し遅延させて最終結果を表示
        } else if (!number && !hasCompleted) {
          setCurrentDisplayNumber('?');
          setHasCompleted(false);
        }
      }
    }, [diceIndex, isAnimating, hasCompleted]);

    // 完了したリールの表示を即座に更新
    useEffect(() => {
      if (hasCompleted && finalNumber) {
        setCurrentDisplayNumber(finalNumber);
      }
    }, [hasCompleted, finalNumber]);

    // 完了したリールは中央に固定
    const shouldShowFinalNumber = hasCompleted && finalNumber;
    
    // 完了したリールは一切変化させない
    if (hasCompleted && finalNumber) {
      return (
        <View style={styles.diceItem}>
          <View style={[styles.dice, { transform: [{ translateY: 0 }] }]}>
            <Text style={styles.diceNumber}>
              {finalNumber}
            </Text>
          </View>
        </View>
      );
    }

    return (
      <View style={styles.diceItem}>
        <View style={[styles.dice, { transform: [{ translateY: 0 }] }]}>
          <Text style={styles.diceNumber}>
            {currentDisplayNumber}
          </Text>
        </View>
      </View>
    );
  });

  // 結果表示モーダル
  const ResultModal = () => {
    if (!showResult || !result) return null;

    const ModalContent = isWeb ? View : LinearGradient;
    const gradientProps = isWeb ? { style: { backgroundColor: '#667eea' } } : { colors: ['#667eea', '#764ba2'] };

    return (
      <View style={styles.modalOverlay}>
        <View style={styles.modalContent}>
          <ModalContent
            {...gradientProps}
            style={styles.modalGradient}
          >
            <Text style={styles.modalTitle}>🎉 ゲーム完了！</Text>
            <Text style={styles.resultText}>
              選択した数字: {result.numbers.join(', ')}
            </Text>
            <Text style={styles.resultText}>
              合計: {result.total}
            </Text>
            <Text style={styles.resultText}>
              パターン: {result.pattern}
            </Text>
            <TouchableOpacity style={styles.resetButton} onPress={resetGame}>
              <Text style={styles.resetButtonText}>もう一度プレイ</Text>
            </TouchableOpacity>
          </ModalContent>
        </View>
      </View>
    );
  };

  const ViewContainer = backgroundImage ? ImageBackground : View;
  const containerProps = backgroundImage ? {
    source: backgroundImage,
    resizeMode: 'cover',
    imageStyle: { 
      top: 0,
      left: 0,
      height: height * 2,
      width: width * 2,
    }
  } : {};

  return (
    <ViewContainer
      {...containerProps}
      style={styles.container}
    >

      <View style={styles.gameArea}>
        {/* サイコロ表示 */}
        <View style={styles.diceContainer}>
          <DiceDisplay
            diceIndex={0}
            number={gameState.selectedNumbers[0]}
            isAnimating={gameState.currentStep === 1 && gameState.isAutoMode}
          />
          <DiceDisplay
            diceIndex={1}
            number={gameState.selectedNumbers[1]}
            isAnimating={gameState.currentStep === 2 && gameState.isAutoMode}
          />
          <DiceDisplay
            diceIndex={2}
            number={gameState.selectedNumbers[2]}
            isAnimating={gameState.currentStep === 3 && gameState.isAutoMode}
          />
        </View>

        {/* Let's XAMA! ボタン */}
        <View style={styles.autoButtonContainer}>
          <TouchableOpacity
            style={[styles.autoButton, (gameState.currentStep > 3 || gameState.isAutoMode) && styles.disabledButton]}
            onPress={autoSelectNumbers}
            disabled={gameState.currentStep > 3 || gameState.isAutoMode}
          >
            <Text style={styles.autoButtonText}>
              {gameState.currentStep > 3 ? 'もう一回挑戦する？' : 
               gameState.currentStep === 1 ? '🌱 マギスロに挑戦！' :
               gameState.currentStep === 2 ? '🌲 次は何かな？' :
               '🌳 がんばって～！'}
            </Text>
          </TouchableOpacity>
        </View>



      </View>

      {/* リセットボタン */}
      <View style={styles.bottomArea}>
        <View style={styles.resetButtonContainer}>
          <TouchableOpacity
            style={styles.resetButton}
            onPress={resetGame}
          >
            <Text style={styles.resetButtonText}>やりなおす</Text>
          </TouchableOpacity>
        </View>
      </View>

      <ResultModal />
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 0,
    width: '100%',
    height: '100%',
    justifyContent: 'flex-start',
  },
  header: {
    alignItems: 'center',
    marginBottom: 30,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.8)',
    textAlign: 'center',
    marginTop: 5,
  },
  gameArea: {
    flex: 1,
    paddingHorizontal: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 0,
  },
  bottomArea: {
    paddingHorizontal: 20,
    paddingBottom: 20,
  },
  stepText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
    textAlign: 'center',
    marginBottom: 30,
  },
  diceContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginBottom: 40,
    marginTop: 0,
  },
  diceItem: {
    marginHorizontal: 10,
    height: 120,
    width: 120,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 0, // 枠を削除
    borderRadius: 25,
    overflow: 'hidden', // スロット効果のため
    position: 'relative', // リール効果のため
    backgroundColor: 'rgba(255, 255, 255, 0.9)', // 回転背景を白に
  },
  dice: {
    height: 120,
    width: 120,
    backgroundColor: 'transparent', // 背景を透明に
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 0, // 枠のボーダーを削除
    shadowColor: 'transparent', // 影も削除
    shadowOffset: {
      width: 0,
      height: 0,
    },
    shadowOpacity: 0,
    shadowRadius: 0,
    elevation: 0,
    position: 'absolute', // リール効果のため
    top: 0,
    left: 0,
  },
  diceNumber: {
    fontSize: 60,
    fontWeight: 'bold',
    color: '#333',
    textShadowColor: 'rgba(0, 0, 0, 0.5)',
    textShadowOffset: { width: 3, height: 3 },
    textShadowRadius: 4,
  },
  autoButtonContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  resetButtonContainer: {
    alignItems: 'center',
  },
  autoButton: {
    backgroundColor: 'rgba(255, 215, 0, 0.9)',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 25,
    borderWidth: 2,
    borderColor: 'rgba(255, 255, 255, 0.3)',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  disabledButton: {
    backgroundColor: 'rgba(128, 128, 128, 0.5)',
    borderColor: 'rgba(128, 128, 128, 0.3)',
    shadowOpacity: 0.1,
    elevation: 2,
  },
  autoButtonText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    textAlign: 'center',
  },
  resetButton: {
    backgroundColor: '#6c757d',
    paddingHorizontal: 25,
    paddingVertical: 12,
    borderRadius: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 3,
    },
    shadowOpacity: 0.2,
    shadowRadius: 3,
    elevation: 6,
  },
  resetButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  numberGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    marginBottom: 30,
  },
  numberButton: {
    width: 60,
    height: 60,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    margin: 10,
    borderWidth: 2,
    borderColor: 'rgba(255, 255, 255, 0.3)',
  },
  disabledButton: {
    backgroundColor: 'rgba(255, 255, 255, 0.3)',
    borderColor: 'rgba(255, 255, 255, 0.1)',
  },
  numberButtonText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  selectedContainer: {
    alignItems: 'center',
  },
  selectedText: {
    fontSize: 16,
    color: 'white',
    fontWeight: 'bold',
  },
  modalOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    width: width * 0.8,
    borderRadius: 20,
    overflow: 'hidden',
  },
  modalGradient: {
    padding: 30,
    alignItems: 'center',
    backgroundColor: '#667eea', // Web用のフォールバック
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 20,
  },
  resultText: {
    fontSize: 18,
    color: 'white',
    marginBottom: 10,
    textAlign: 'center',
  },
  resetButton: {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 25,
    marginTop: 20,
  },
  resetButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
