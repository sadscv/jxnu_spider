
import time
import os
from sklearn import svm
from PIL import Image
from numpy import array
from imghandle import *
from sklearn.externals import joblib
clf = None

model = None
lb= None

def get_image_fit_data(dir_name):
    """读取labeled_images文件夹的图片，返回图片的特征矩阵及相应标记"""
    X = []
    Y = []
    name_list = os.listdir(dir_name)
    for name in name_list:
        # if not os.path.isdir(os.path.join(dir_name, name)):
        #     continue
        image_files = os.listdir(os.path.join(dir_name, name))
        for img in image_files:
            i = Image.open(os.path.join(dir_name, name, img))
            X.append(array(i).flatten())
            Y.append(name)
    print(len(X),len(Y))
    return X, Y


def get_classifier_from_learn():
    """学习数据获取分类器"""
    t = time.time()
    global clf
    if not clf:
        clf = svm.SVC(kernel='linear')  #线性准确率高一点
        #clf = svm.SVC()   #默认为rbf
        X, Y = get_image_fit_data("labeled_images")
        clf.fit(X, Y)
        print("学习用了"+str(time.time()-t)+"s")
        print(clf)
    return clf      #学习到的矩阵

def get_code(img):
    img_piece = do_image_crop(img)
    X = img_list_to_array_list(img_piece)
    clf = get_classifier_from_learn()
    y = clf.predict(X)
    return "".join(y)
if __name__ == '__main__':
    # print(get_classifier_from_learn())
    clf = joblib.load("svm.m")
    sourse="images"
    name_list = os.listdir(sourse)
    num=0
    right=0
    for name in name_list:
        num=num+1
        img=Image.open(sourse+"/"+name)
        code = get_validate_code_from_image(img)
        if code==name[:4]:
            right=right+1
            print("right")
        else:
            print("error:"+code+":"+name)
    print("共测试了"+str(num)+"张验证码")
    print("正确率:"+str(right))   #输出准确率
    img = Image.open("img.png")
    code = get_code(img)
    print(code)