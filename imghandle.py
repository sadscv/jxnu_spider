from numpy import array
from PIL import Image
from PIL import ImageFilter
def do_image_crop(img):
    """做图片切割，返回块图片列表"""
    start = 10
    width = 15
    top = 0
    height = 24

    img_list = []

    # def init_table(threshold=135):
    #     table = []
    #     for i in range(256):
    #         if i < threshold:
    #             table.append(0)
    #         else:
    #             table.append(1)

    #     return table

    # img = img.convert("L").point(init_table(), '1')
    def init_table(threshold):
        table = []
        for i in range(256):
            if i >= threshold:
                table.append(0)
            else:
                table.append(1)

        return table
    def yuzhi(img):
        colect={}
        width,height=img.size
        for w in range(0, width):  
            for h in range(0, height): 
                pix=img.getpixel((w,h))
                # print(w,h,pix)
                if pix not in colect:
                    colect[pix]=1
                else:
                    colect[pix]+=1
        colect = sorted(colect.items(), key=lambda x: x[1],reverse = True)
        print(colect)
        if colect[0][0]==76 and colect[0][1]+colect[1][1]>5000:
            if colect[0][1]>4500:
                return colect[0][0]
            if colect[1][0]==29:
                return colect[2][0]
            else:
                return colect[1][0]
        else:
            return colect[0][0]
    img=img.convert("L")
    # img.save("g:/pyhuidu.png")
    # img_yuzhi=yuzhi(img)
    # print(img_yuzhi)
    img=img.point(init_table(29),"1")
    for i in range(4):
        new_start = start + width * i
        box = (new_start, top, new_start + width, height)
        piece = img.crop(box)
        # piece.show()
        img_list.append(piece)

    return img_list

def img_list_to_array_list(img_list):
    """PIL Image对象转array_list"""
    array_list = []
    for img in img_list:
        array_list.append(array(img).flatten())
    return array_list
if __name__ == "__main__":
    img=Image.open("images/4W6D.png")
    img=img.convert("L")
    img_list=do_image_crop(img)
    # array_list=img_list_to_array_list(img_list)