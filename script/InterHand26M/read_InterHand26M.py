#-*-coding:utf-8-*-
# date:2025-03-02
# Author: XIAN
# function: handposeX json 格式读取数据标签

import sys
sys.path.append("./")
import os
import cv2
import json
import numpy as np
import random
from pathlib import Path
import re
'''
function: 绘制二维关键点连线
'''
def draw_joints(img_,hand_,x,y):
    thick = 2
    colors = [(0,215,255),(255,115,55),(5,255,55),(25,15,255),(225,15,55)]
    #
    cv2.line(img_, (int(hand_['0']['x']+x), int(hand_['0']['y']+y)),(int(hand_['1']['x']+x), int(hand_['1']['y']+y)), colors[0], thick)
    cv2.line(img_, (int(hand_['1']['x']+x), int(hand_['1']['y']+y)),(int(hand_['2']['x']+x), int(hand_['2']['y']+y)), colors[0], thick)
    cv2.line(img_, (int(hand_['2']['x']+x), int(hand_['2']['y']+y)),(int(hand_['3']['x']+x), int(hand_['3']['y']+y)), colors[0], thick)
    cv2.line(img_, (int(hand_['3']['x']+x), int(hand_['3']['y']+y)),(int(hand_['4']['x']+x), int(hand_['4']['y']+y)), colors[0], thick)

    cv2.line(img_, (int(hand_['0']['x']+x), int(hand_['0']['y']+y)),(int(hand_['5']['x']+x), int(hand_['5']['y']+y)), colors[1], thick)
    cv2.line(img_, (int(hand_['5']['x']+x), int(hand_['5']['y']+y)),(int(hand_['6']['x']+x), int(hand_['6']['y']+y)), colors[1], thick)
    cv2.line(img_, (int(hand_['6']['x']+x), int(hand_['6']['y']+y)),(int(hand_['7']['x']+x), int(hand_['7']['y']+y)), colors[1], thick)
    cv2.line(img_, (int(hand_['7']['x']+x), int(hand_['7']['y']+y)),(int(hand_['8']['x']+x), int(hand_['8']['y']+y)), colors[1], thick)

    cv2.line(img_, (int(hand_['0']['x']+x), int(hand_['0']['y']+y)),(int(hand_['9']['x']+x), int(hand_['9']['y']+y)), colors[2], thick)
    cv2.line(img_, (int(hand_['9']['x']+x), int(hand_['9']['y']+y)),(int(hand_['10']['x']+x), int(hand_['10']['y']+y)), colors[2], thick)
    cv2.line(img_, (int(hand_['10']['x']+x), int(hand_['10']['y']+y)),(int(hand_['11']['x']+x), int(hand_['11']['y']+y)), colors[2], thick)
    cv2.line(img_, (int(hand_['11']['x']+x), int(hand_['11']['y']+y)),(int(hand_['12']['x']+x), int(hand_['12']['y']+y)), colors[2], thick)

    cv2.line(img_, (int(hand_['0']['x']+x), int(hand_['0']['y']+y)),(int(hand_['13']['x']+x), int(hand_['13']['y']+y)), colors[3], thick)
    cv2.line(img_, (int(hand_['13']['x']+x), int(hand_['13']['y']+y)),(int(hand_['14']['x']+x), int(hand_['14']['y']+y)), colors[3], thick)
    cv2.line(img_, (int(hand_['14']['x']+x), int(hand_['14']['y']+y)),(int(hand_['15']['x']+x), int(hand_['15']['y']+y)), colors[3], thick)
    cv2.line(img_, (int(hand_['15']['x']+x), int(hand_['15']['y']+y)),(int(hand_['16']['x']+x), int(hand_['16']['y']+y)), colors[3], thick)

    cv2.line(img_, (int(hand_['0']['x']+x), int(hand_['0']['y']+y)),(int(hand_['17']['x']+x), int(hand_['17']['y']+y)), colors[4], thick)
    cv2.line(img_, (int(hand_['17']['x']+x), int(hand_['17']['y']+y)),(int(hand_['18']['x']+x), int(hand_['18']['y']+y)), colors[4], thick)
    cv2.line(img_, (int(hand_['18']['x']+x), int(hand_['18']['y']+y)),(int(hand_['19']['x']+x), int(hand_['19']['y']+y)), colors[4], thick)
    cv2.line(img_, (int(hand_['19']['x']+x), int(hand_['19']['y']+y)),(int(hand_['20']['x']+x), int(hand_['20']['y']+y)), colors[4], thick)
'''
function: 21个三维关键点转为二维点，并进行绘制
'''
def Draw_KeyPoints3D(img,Joints_,fx,fy,cx,cy):
    #----------------------------------- 计算 3D到 2D相机的投影
    X = Joints_[:,0]
    Y = Joints_[:,1]
    Z = Joints_[:,2]
    x_p = X / Z
    y_p = Y / Z
    #三维点转为二维点
    x_2d = fx* x_p + cx
    y_2d = fy* y_p + cy
    pts2d_list = {}
    pts2d_ss = []
    for ii in range(x_2d.shape[0]):
        x_,y_ = x_2d[ii],y_2d[ii]
        pts2d_list[str(ii)]={"x":x_,"y":y_}
        cv2.circle(img, (int(x_),int(y_)), 4, (25,155,255), -1)
        cv2.circle(img, (int(x_),int(y_)), 2, (255,0,55), -1)
        pts2d_ss.append((x_,y_))

    draw_joints(img,pts2d_list,0,0)
    pts2d_ss = np.array(pts2d_ss)
    return pts2d_ss
def letterbox(img, height=416, augment=False, color=(266,255,255)):
    # Resize a rectangular image to a padded square
    shape = img.shape[:2]  # shape = [height, width]
    ratio = float(height) / max(shape)  # ratio  = old / new
    new_shape = (round(shape[1] * ratio), round(shape[0] * ratio))
    dw = (height - new_shape[0]) / 2  # width padding
    dh = (height - new_shape[1]) / 2  # height padding
    top, bottom = round(dh - 0.1), round(dh + 0.1)
    left, right = round(dw - 0.1), round(dw + 0.1)
    # resize img
    if augment:
        interpolation = np.random.choice([None, cv2.INTER_NEAREST, cv2.INTER_LINEAR,
                                          None, cv2.INTER_NEAREST, cv2.INTER_LINEAR,
                                          cv2.INTER_AREA, cv2.INTER_CUBIC, cv2.INTER_LANCZOS4])
        if interpolation is None:
            img = cv2.resize(img, new_shape)
        else:
            img = cv2.resize(img, new_shape, interpolation=interpolation)
    else:
        img = cv2.resize(img, new_shape, interpolation=cv2.INTER_NEAREST)
    # print("resize time:",time.time()-s1)

    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # padded square
    return img
def Draw_Vertex_KeyPoints(img,img_mesh,Vertex,fx_d,fy_d,cx_d,cy_d,triangles_index,RGB_ = (245, 125, 35)):
    #----------------------------------- 计算 Mano 到 相机的投影
    Xdc = -Vertex[:,0].reshape(-1)
    Ydc = -Vertex[:,1].reshape(-1)
    Zdc = -Vertex[:,2].reshape(-1)

    x_mano_p = Xdc / Zdc
    y_mano_p = Ydc / Zdc
    #点云转为二维图

    x_mano = fx_d* x_mano_p + cx_d
    y_mano = fy_d* y_mano_p + cy_d
    manopts_list = []

    mesh_list = []
    color_rr = (random.randint(100,230),random.randint(120,250),random.randint(100,240))
    for ii in range(triangles_index.shape[0]):
        a,b,c = triangles_index[ii]

        x1_,y1_ = x_mano[a].astype(np.int32),y_mano[a].astype(np.int32)
        x2_,y2_ = x_mano[b].astype(np.int32),y_mano[b].astype(np.int32)
        x3_,y3_ = x_mano[c].astype(np.int32),y_mano[c].astype(np.int32)

        area_ = np.array([[int(x1_), int(y1_)], [int(x2_), int(y2_)], [int(x3_),int(y3_)]])
        color_ = (255, 0, 0)
        # cv2.fillPoly(mask_v, [area_], (255))
        cv2.fillPoly(img_mesh, [area_], color_rr)
        mesh_list.append(area_)
    cv2.fillPoly(img, mesh_list, RGB_)

def find_jpg_files(root_folder):
    root_path = Path(root_folder)
    jpg_files = list(root_path.rglob('*.jpg'))  # rglob递归查找
    return jpg_files
if __name__ == '__main__':

    root_folder = '../../InterHand2.6M_5fps_batch1-20250302-min/'
    jpg_files = find_jpg_files(root_folder)

    path_data = []
    for path in jpg_files:
        path_str = str(path)
        # print(path)
        # print(type(path))
        path_img = path_str.replace("\\","/")
        path_json = re.sub(r"(cam\d+)", r"\1_label", path_img)
        path_json = path_json.replace(".jpg",".json")

        if not os.access(path_json,os.F_OK):
            continue
        # print(path_img)
        # print(path_label)
        path_data.append((path_img,path_json))


    triangles_index = np.load("../../config/triangles_index.npy").reshape(-1,3)

    out_cnt = 0
    hand_cnt = 0

    for (path_img,path_json) in path_data:
        if not os.access(path_json,os.F_OK):
            continue
        try:
            with open(path_json, 'r', encoding='utf-8') as file:
                data_json = json.load(file)
        except:
            print("error ")
            os.remove(path_img)
            os.remove(path_json)
            continue
        hands_json = data_json["hands"]
        cx,cy,fx,fy = data_json["cx"],data_json["cy"],data_json["fx"],data_json["fy"]

        img_ = cv2.imread(path_img)
        img_joint = img_.copy()
        img_mesh = img_.copy()
        img_mask = np.zeros(img_.shape).astype(np.uint8)
        img_mask[:,:,:]=255

        for msg_ in hands_json:

            RGB_ = (245, 55, 133)
            if msg_["label"] == "left":
                RGB_ = (25, 255, 133)
            Joints3D = np.array(msg_["joint3d"])
            Vertex3D = np.array(msg_["vertex3d"])
            pts2d_ss = Draw_KeyPoints3D(img_joint,Joints3D,fx,fy,cx,cy)
            Draw_Vertex_KeyPoints(img_mesh,img_mask,Vertex3D,fx,fy,cx,cy,triangles_index,RGB_ = RGB_)
            hand_cnt += 1

        stk_1 = np.hstack((img_,img_joint))
        stk_2 = np.hstack((img_mesh,img_mask))

        stk_ = np.vstack((stk_1,stk_2))

        cv2.namedWindow("img_stk",0)
        cv2.imshow("img_stk",stk_)
        # cv2.imwrite("example.jpg",stk_)
        out_cnt += 1
        print("---->>> InterHand26M [{}] , hand_num: [{}]".format(out_cnt,hand_cnt))
        key_id = cv2.waitKey(1)
        if key_id == 27:
            break
