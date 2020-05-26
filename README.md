# CandyLinker
Game Candy Crush auto bot
working with adb.exe for android

Main process

Step1: Capture phone screen

![image](https://github.com/keytuff/CandyLinker/blob/master/capture.png)

Step2: Crop game board

Step3: Detect block classes

Step4: Analyze the best swich

![image](https://github.com/keytuff/CandyLinker/blob/master/recognized.png)

已完成：
1. 自动识别，自动交换。
2. 优先底部交换。
3. 优先连续更长的交换（5连，4连）。

Roadmap:
1. 识别非矩阵游戏面板中的无效格子。
2. 识别特殊道具。
3. 识别暂时不可交换的区域。
4. 识别优先需要碰撞的关键部位。（果冻，小熊糖）
