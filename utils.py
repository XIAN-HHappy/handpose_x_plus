#-*-coding:utf-8-*-
# date:2024-01-24
# Author: XIAN
# function: utils

import os
import numpy as np
import cv2
import copy
import random
'''
 数据增强 crop
'''
def img_agu_crop(img_):
    scale_ = int(min(img_.shape[0],img_.shape[1])/20)
    # scale_ = 5
    x1 = max(0,random.randint(0,scale_))
    y1 = max(0,random.randint(0,scale_))
    x2 = min(img_.shape[1]-1,img_.shape[1] - random.randint(0,scale_))
    y2 = min(img_.shape[0]-1,img_.shape[1] - random.randint(0,scale_))
    # print(img_.shape,'-crop- : ',x1,y1,x2,y2)
    try:
        img_crop_ = img_[y1:y2,x1:x2,:]
    except:
        img_crop_ = img_
        print("img_agu_crop error ")
    return img_crop_

'''
function：读取 obj 信息
'''
def read_obj(objFilePath):
    mesh = {
        "joints":None,
        "faces_index":None,
        }
    print("objFilePath:",objFilePath)
    with open(objFilePath) as file:
        joints = []
        faces_index = []
        while True:
            line = file.readline().strip()
            if not line:
                break
            strs = line.split(" ")
            if strs[0] == "v"and len(strs)==4:
                joints.append((float(strs[1]), float(strs[2]), float(strs[3])))
            if strs[0] == "f" and len(strs)==4:
                faces_index.append((int(strs[1]), int(strs[2]), int(strs[3])))

    # print("joints num : {}".format(len(joints)))
    # print("faces  num : {}".format(len(faces_index)))

    if len(joints)!=0:
        mesh["joints"] = np.array(joints).reshape(-1,3)
    if len(faces_index)!=0:
        mesh["faces_index"] = np.array(faces_index).reshape(-1,3)
    return mesh
'''
function: 读取相机内参
'''
def read_camera_intrinsics(file_):
    with open(file_) as file:
        joints = []
        faces_index = []
        while True:
            line = file.readline().strip()
            if not line:
                break
            strs = line.split(" ")
            print(strs)
            fx,fy,cx,cy = float(strs[0]), float(strs[1]), float(strs[2]),float(strs[3])
    print("fx,fy,cx,cy : {},{},{},{}".format(fx,fy,cx,cy))
    return fx,fy,cx,cy
'''
function : 读取 gesture
'''
def read_gesture(file_):
    Gesture_ = "None"
    with open(file_) as file:
        joints = []
        faces_index = []
        idx = 0
        while True:
            line = file.readline().strip()
            if line is not None:
                Gesture_ = line
            # idx += 1
            # print(idx,"Gesture_:",Gesture_)
            break
            if not line:
                break
    return Gesture_
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
    for ii in range(x_2d.shape[0]):
        x_,y_ = x_2d[ii],y_2d[ii]
        pts2d_list[str(ii)]={"x":x_,"y":y_}
        cv2.circle(img, (int(x_),int(y_)), 4, (25,155,255), -1)
        cv2.circle(img, (int(x_),int(y_)), 2, (255,0,55), -1)

    draw_joints(img,pts2d_list,0,0)
'''
function: Mesh 三维点转为二维点，并进行绘制
'''
def Draw_Mesh3D(img,Mesh,fx,fy,cx,cy,RGB_ = (245, 125, 35)):
    #----------------------------------- 三维点到 二维点相机的投影
    Joints = copy.deepcopy(Mesh["joints"])
    faces_index = copy.deepcopy(Mesh["faces_index"])
    X = Joints[:,0].reshape(-1)
    Y = Joints[:,1].reshape(-1)
    Z = Joints[:,2].reshape(-1)

    x_p = X / Z
    y_p = Y / Z
    #点云转为深度二维图

    x_2d = fx* x_p + cx
    y_2d = fy* y_p + cy

    mesh_list = []
    for ii in range(faces_index.shape[0]):
        a,b,c = faces_index[ii] # 三角网格索引
        a -=1
        b -=1
        c -=1
        x1_,y1_ = x_2d[a].astype(np.int32),y_2d[a].astype(np.int32)
        x2_,y2_ = x_2d[b].astype(np.int32),y_2d[b].astype(np.int32)
        x3_,y3_ = x_2d[c].astype(np.int32),y_2d[c].astype(np.int32)

        area_ = np.array([[int(x1_), int(y1_)], [int(x2_), int(y2_)], [int(x3_),int(y3_)]])
        mesh_list.append(area_)
    # 绘制mesh 二维网格
    cv2.fillPoly(img, mesh_list, RGB_)
