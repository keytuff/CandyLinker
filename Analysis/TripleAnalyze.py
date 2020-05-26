import numpy as np


class TripleAnalyze:
    def Analyze(self, blockFlags):
        size = blockFlags.shape
        maxPos = None  # 从哪
        toPos = None  # 去哪
        maxCon = 2  # 至少要3连
        maxDirection = ""
        for row in reversed(range(size[0])):
            for col in reversed(range(size[1])):

                # 与上互换
                flags = blockFlags.copy()
                toRow = row - 1
                if toRow >= 0:
                    orginType = flags[row][col]
                    swapType = flags[toRow][col]
                    temp = flags[toRow][col]
                    flags[toRow][col] = flags[row][col]
                    flags[row][col] = temp
                    con = self.__tripleDetect(flags, (row, col), orginType,
                                              (toRow, col), swapType)
                    if con > maxCon:
                        maxCon = con
                        maxDirection = "up"
                        maxPos = (row, col)
                        toPos = (toRow, col)
                        print(f"{maxPos} {maxDirection} {maxCon}")

                # 与下互换
                flags = blockFlags.copy()
                toRow = row + 1
                if toRow < size[0]:
                    orginType = flags[row][col]
                    swapType = flags[toRow][col]
                    temp = flags[toRow][col]
                    flags[toRow][col] = flags[row][col]
                    flags[row][col] = temp
                    con = self.__tripleDetect(flags, (row, col), orginType,
                                              (toRow, col), swapType)
                    if con > maxCon:
                        maxCon = con
                        maxDirection = "down"
                        maxPos = (row, col)
                        toPos = (toRow, col)
                        print(f"{maxPos} {maxDirection} {maxCon}")

                # 与左互换
                flags = blockFlags.copy()
                toCol = col - 1
                if toCol >= 0:
                    orginType = flags[row][col]
                    swapType = flags[row][toCol]
                    temp = flags[row][toCol]
                    flags[row][toCol] = flags[row][col]
                    flags[row][col] = temp
                    con = self.__tripleDetect(flags, (row, col), orginType,
                                              (row, toCol), swapType)
                    if con > maxCon:
                        maxCon = con
                        maxDirection = "left"
                        maxPos = (row, col)
                        toPos = (row, toCol)
                        print(f"{maxPos} {maxDirection} {maxCon}")

                # 与右互换
                flags = blockFlags.copy()
                toCol = col + 1
                if toCol < size[1]:
                    orginType = flags[row][col]
                    swapType = flags[row][toCol]
                    temp = flags[row][toCol]
                    flags[row][toCol] = flags[row][col]
                    flags[row][col] = temp
                    con = self.__tripleDetect(flags, (row, col), orginType,
                                              (row, toCol), swapType)
                    if con > maxCon:
                        maxCon = con
                        maxDirection = "right"
                        maxPos = (row, col)
                        toPos = (row, toCol)
                        print(f"{maxPos} {maxDirection} {maxCon}")
        print(f"best move: {maxPos} {maxDirection} to {toPos} made {maxCon}")
        return (maxPos, maxDirection, toPos, maxCon)

    def __tripleDetect(self, flags, orginPos, orginType, swapPos, swapType):
        ''' 以一个位置为中心，横竖2个方向上，是否有三连以上的发生。
            返回最长连续数
        '''
        size = flags.shape
        continues = 0
        maxContinues = 0

        #
        ''' 原位置检测 '''
        row = orginPos[0]
        col = orginPos[1]

        # 原位置 原类型 竖向检测
        continues = 0
        for r in range(size[0]):
            if flags[r, col] == orginType:
                continues += 1
            else:
                continues = 0
            if continues > maxContinues:
                maxContinues = continues

        # 原位置 原类型  横向检测
        continues = 0
        for c in range(size[1]):
            if flags[row, c] == orginType:
                continues += 1
            else:
                continues = 0
            if continues > maxContinues:
                maxContinues = continues

        # 原位置 交换类型 竖向检测
        continues = 0
        for r in range(size[0]):
            if flags[r, col] == swapType:
                continues += 1
            else:
                continues = 0
            if continues > maxContinues:
                maxContinues = continues

        # 原位置 交换类型  横向检测
        continues = 0
        for c in range(size[1]):
            if flags[row, c] == swapType:
                continues += 1
            else:
                continues = 0
            if continues > maxContinues:
                maxContinues = continues

        #
        ''' 交换位置类型检测 '''
        row = swapPos[0]
        col = swapPos[1]

        # 交换位置 交换类型  竖向检测
        continues = 0
        for r in range(size[0]):
            if flags[r, col] == swapType:
                continues += 1
            else:
                continues = 0
            if continues > maxContinues:
                maxContinues = continues

        # 交换位置 交换类型  横向检测
        continues = 0
        for c in range(size[1]):
            if flags[row, c] == swapType:
                continues += 1
            else:
                continues = 0
            if continues > maxContinues:
                maxContinues = continues

        # 交换位置 原类型  竖向检测
        continues = 0
        for r in range(size[0]):
            if flags[r, col] == orginType:
                continues += 1
            else:
                continues = 0
            if continues > maxContinues:
                maxContinues = continues

        # 交换位置 原类型  横向检测
        continues = 0
        for c in range(size[1]):
            if flags[row, c] == orginType:
                continues += 1
            else:
                continues = 0
            if continues > maxContinues:
                maxContinues = continues
                
        return maxContinues
