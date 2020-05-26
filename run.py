from adb import PyADB
from cap import Cap
from PIL import Image
import cv2
import numpy as np
import time
from GameMapping.Board import Board
from GameMapping.Block import Block
from Analysis.TripleAnalyze import TripleAnalyze

# 请根据实际情况修改以下配置项
# ------------------------------------------------------------------------------
ADB_DEVICE_SERIAL = "d82f4a2e"  # adb devices 命令得到的手机序列号
SHOW_MARKED_IMG = False  # 展示标注数据的 RGB 图像
DEBUG = False
# ------------------------------------------------------------------------------

if __name__ == '__main__':

    # 参数定义
    blockSize = (126, 116)
    sampleSize = (100, 100)
    block = Block(
        blockSize,
        (blockSize[0] // 2 - sampleSize[0] // 2, blockSize[1] // 2 -
            sampleSize[1] // 2, sampleSize[0], sampleSize[1]))
    board = Board((7, 7), (698, 137), block, 0.9)

    for round in range(30):
        print(f"round: {round+1}")

        # adb 初始化
        adb = PyADB(ADB_DEVICE_SERIAL)

        if DEBUG:
            # 加载截图
            # img = Image.open("cap.png") # pillow read image file
            img = cv2.imread("cap.png",
                             cv2.IMREAD_COLOR)  # openCV read image file
            print(img.shape)
            # img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR) # 从pillow image转换为cv image
            # img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # 从opencv image转换为pillow image
            # img.show()

        else:
            # 屏幕截图
            cap = Cap()
            img = cap.screencap(adb)
            img = cv2.cvtColor(np.asarray(img),
                               cv2.COLOR_RGB2BGR)  # 从pillow image转换为cv image
            #cv2.imwrite('start.png', img)

        # 冗余操作，用于点击按钮
        adb.short_tap((300, 1455))  # retry
        adb.short_tap((540, 1430))  # begin

        # 刷新面板
        board.Update(img)

        # 分析最佳三连情况
        triple = TripleAnalyze()
        result = triple.Analyze(board.BlockAreaFlags)

        # 执行三连
        if (result[0] is not None):
            swipeFrom = board.GetlocationOfBlockMap(result[0])[::-1]  # x,y 格式
            swipeTo = board.GetlocationOfBlockMap(result[2])[::-1]  # x,y 格式
            swipeFrom = (board.BlockAreaLocation[1] + swipeFrom[0] +
                         board.Block.Size[1] // 2, board.BlockAreaLocation[0] +
                         swipeFrom[1] + board.Block.Size[0] // 2)
            swipeTo = (board.BlockAreaLocation[1] + swipeTo[0] +
                       board.Block.Size[1] // 2, board.BlockAreaLocation[0] +
                       swipeTo[1] + board.Block.Size[0] // 2)
            adb.swipe_tap(swipeFrom, swipeTo)
            time.sleep(0)
