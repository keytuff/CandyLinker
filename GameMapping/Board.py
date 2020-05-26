import cv2
import numpy as np
from Analysis.MatchTemplate import MatchTemplate


class Board:
    __debug = False
    Size = (0, 0)  # height,width
    BlockAreaLocation = (0, 0)  # first block location
    Block = None
    BlockAreaImage = None  # block区域的图像
    BlockSamples = None  # block 区域的切割后的每一块采样
    BlockAreaFlags = None  # 识别之后的区域，给每个block已经标记了相同类型的标签
    MatchThreshold = 0.9

    def __init__(self, s, f, b, t):
        self.Size = s
        self.BlockAreaLocation = f
        self.Block = b
        self.BlockSamples = np.zeros(self.Size + self.Block.SampleArea[2:4] +
                                     (3, ),
                                     dtype=np.uint8)
        self.BlockAreaFlags = np.zeros(self.Size, dtype=np.uint8)
        self.MatchThreshold = t

    def Update(self, img):
        # 裁剪获取block区域
        self.BlockAreaImage = img[
            self.BlockAreaLocation[0]:self.BlockAreaLocation[0] +
            self.Block.Size[0] *
            self.Size[0], self.BlockAreaLocation[1]:self.BlockAreaLocation[1] +
            self.Block.Size[1] * self.Size[1]]
        # 根据坐标和尺寸进行数据采样
        for row in range(self.Size[0]):
            for col in range(self.Size[1]):
                sample = self.__getSample(self.BlockAreaImage, (row, col))
                self.BlockSamples[row, col] = sample

        # 模板匹配
        self.BlockAreaFlags = np.zeros(self.Size, dtype=np.uint8)
        matcher = MatchTemplate()  # 匹配器
        blockType = 0
        for row in range(self.Size[0]):
            for col in range(self.Size[1]):
                if self.BlockAreaFlags[row, col] != 0:
                    continue
                # template_gray = cv2.cvtColor(template_rgb, cv2.COLOR_BGR2GRAY)
                # blockAread_gray = cv2.cvtColor(board.BlockArea, cv2.COLOR_BGR2GRAY)
                template_rgb = self.BlockSamples[row, col]
                blockArea_rgb = self.BlockAreaImage.copy()
                matchs = matcher.Match(blockArea_rgb, template_rgb,
                                       self.MatchThreshold)  # 做匹配计算
                h, w = template_rgb.shape[0:2]
                matchPositions = []
                mm = 0
                for pt in matchs:
                    mm += 1
                    pos = self.GetPositionOfBlockMap(
                        pt)  # 根据匹配位置，获取匹配到的多个block位置
                    if pos not in matchPositions:
                        matchPositions.append(pos)
                        '''
                        blockArea_rec = self.BlockAreaImage.copy()
                        cv2.rectangle(blockArea_rec, pt[::-1],
                                      (pt[1] + w, pt[0] + h), (0, 0, 255),
                                      2)  # 左上角(x,y),右下角(x,y),颜色(bgr)，粗细
                        '''
                # 给同类设置标签
                blockType += 1
                for mPos in matchPositions:
                    self.BlockAreaFlags[mPos] = blockType

                print(
                    f"{(row,col)} type:{blockType}, matchs: {len(matchPositions)}, times: {mm}")

                '''
                # 查看每次分类匹配情况
                cv2.imshow("image", blockArea_rgb)  #  显示图片
                cv2.waitKey(0)  # 等待按键
                '''
        if self.__debug:
            # 打标记，查看分类情况
            blockArea_typeImage = self.BlockAreaImage.copy()
            for row in range(self.Size[0]):
                for col in range(self.Size[1]):
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    text = str(self.BlockAreaFlags[row, col])
                    loc = self.GetlocationOfBlockMap((row, col))[::-1]
                    cv2.putText(blockArea_typeImage, text,
                                (loc[0] + 10, loc[1] + 50), font, 2,
                                (255, 255, 255), 4, cv2.LINE_AA)
            # 查看分类匹配情况
            cv2.imshow("image", blockArea_typeImage)  #  显示图片
            #cv2.imwrite('recognized.png', blockArea_typeImage)
            cv2.waitKey(0)  # 等待按键

    def __getSample(self, img, sampleIndex):
        ''' 获取block中的部分图像采样数据'''
        sampleAreaRows = slice(
            sampleIndex[0] * self.Block.Size[0] + self.Block.SampleArea[0],
            sampleIndex[0] * self.Block.Size[0] + self.Block.SampleArea[0] +
            self.Block.SampleArea[2])
        sampleAreaCols = slice(
            sampleIndex[1] * self.Block.Size[1] + self.Block.SampleArea[1],
            sampleIndex[1] * self.Block.Size[1] + self.Block.SampleArea[1] +
            self.Block.SampleArea[3])
        # img[sampleAreaRows, sampleAreaCols] = [255, 255, 255] #标为红色测试
        return img[sampleAreaRows, sampleAreaCols]

    def GetPositionOfBlockMap(self, location):
        ''' 根据BlockArea中的一个(row,col)坐标，计算出在block的Map位置(row,col)'''
        pos = ((location[0] + 1) // self.Block.Size[0],
               (location[1] + 1) // self.Block.Size[1])
        return pos

    def GetlocationOfBlockMap(self, position):
        ''' 根据block的Map位置(row,col)，计算出在BlockArea中的一个(row,col)起始坐标'''
        loc = (
            position[0] * self.Block.Size[0],
            position[1] * self.Block.Size[1],
        )
        return loc
