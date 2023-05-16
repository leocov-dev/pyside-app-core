class PixelVal(int):
    def __new__(cls, val: int):
        return super(PixelVal, cls).__new__(cls, val)

    def __str__(self):
        return f"{int(self)}px"
