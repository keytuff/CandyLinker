import cv2
import numpy as np


class MatchTemplate:
    ''' 模板匹配'''
    __debug = False

    def Match(self, image, template, threshold=0.9):
        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        if self.__debug:
            # 识别部分画图
            w, h = template.shape[0:2][::-1]
            for pt in zip(*loc[0:2][::-1]):
                cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h),
                              (0, 0, 255), 1)
            cv2.imshow("image", image)  #  显示图片
            cv2.waitKey(0)  # 等待按键
        return zip(*loc[0:2])
