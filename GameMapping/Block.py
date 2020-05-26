class Block:
    Size = (0, 0)  #height,width
    SampleArea = (0, 0, 0, 0)  # rowIndexOfBlock,ColIndexOfBlock, areaHeight, areaWidth

    def __init__(self, s, a):
        self.Size = s
        self.SampleArea = a