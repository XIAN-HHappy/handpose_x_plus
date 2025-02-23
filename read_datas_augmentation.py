#-*-coding:utf-8-*-
# date:2024-01-24
# Author: DataBall - XIAN
# function: read samples & augmentation

import os
import cv2
import numpy as np
import copy
from utils import read_obj,read_camera_intrinsics,Draw_KeyPoints3D,Draw_Mesh3D,read_gesture
from utils import img_agu_crop
import random
if __name__ == '__main__':

    path_s = "./handpose_x_plus_datas/"
    ok_cnt = 0
    Flag_check_error = False
    #-------------------- 数据增强背景图
    path_bkgd = "./bkgt/"
    bkgt_files_list = os.listdir(path_bkgd)

    for f_ in os.listdir(path_bkgd):
        img_ = cv2.imread(path_bkgd + f_)
        img_ = resize_image_by_long_side(img_,640)
        cv2.imwrite(path_bkgd + f_,img_)
    #---------------------
    for doc_  in os.listdir(path_s):

        path_root  = path_s + doc_ + "/"
        for f_ in os.listdir(path_root):
            if ".png" not in f_:
                continue
            name_x = f_.replace("_depth.png","")
            path_depth = path_root + f_
            path_mesh = path_root + f_.replace("_depth.png","_Mesh.obj") # 网格点数据
            path_joint = path_root + f_.replace("_depth.png","_Joint.obj") # 21 关键点数据
            path_intrinsics = path_root + f_.replace("_depth.png","_intrinsics.txt") # 相机内参数据
            path_gesture = path_root + f_.replace("_depth.png","_gesture.txt") # 手势数据
            path_img = path_root + f_.replace("_depth.png","_o.jpg") # RGB 图像数数据
            path_fusion = path_root + f_.replace("_depth.png","_fusion.jpg") # 可视化3d效果渲染数据
            path_skl = path_root + f_.replace("_depth.png","_fit2d.jpg") # 可视化2D效果渲染数据

            fx,fy,cx,cy = read_camera_intrinsics(path_intrinsics)# 相机的内参

            Gesture_ = "NoneNone"
            try:
                Gesture_ = read_gesture(path_gesture)
                print("")
            except:
                continue
                pass

            print("Gesture :",Gesture_)

            Mesh3D = read_obj(path_mesh)
            Joint3D = read_obj(path_joint)

            img = cv2.imread(path_img)
            img_fusion = cv2.imread(path_fusion)

            img_skl = cv2.imread(path_skl)
            depth = cv2.imread(path_depth,-1).astype(np.float32)

            img_fusion.shape
            img.shape
            img_skl.shape
            depth.shape

            fgt_idx = np.where((depth<=1) & (depth<700))
            depth[fgt_idx[0],fgt_idx[1]]=2000
            mask =np.where((0<depth) & (depth<700),255,0).astype(np.uint8)

            #------------------------------------------------------------------- 数据增强
            pf_ = path_bkgd + bkgt_files_list[random.randint(0,len(bkgt_files_list)-1)]

            img_bkgt = cv2.imread(pf_)
            img_bkgt = img_agu_crop(img_bkgt)
            img_bkgt = cv2.resize(img_bkgt, (img.shape[1],img.shape[0])) # interpolation = cv2.INTER_CUBIC


            hand_mask = np.where(mask!=0,1.,0.)
            hand_mask_p = np.zeros((img.shape[0],img.shape[1],3))
            hand_mask_p[:,:,0] = hand_mask
            hand_mask_p[:,:,1] = hand_mask
            hand_mask_p[:,:,2] = hand_mask
            img_agu = img.astype(np.float32)*hand_mask_p + (1.-hand_mask_p)*img_bkgt.astype(np.float32)
            img_agu = img_agu.astype(np.uint8)

            cv2.namedWindow("img_agu",0)
            cv2.imshow("img_agu",img_agu)

            #-------------------------------------------------------------------

            img_depth = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            img_depth = cv2.cvtColor(img_depth, cv2.COLOR_GRAY2RGB)
            img_depth_jt = img_depth.copy()
            img_jt = img.copy()

            # 相机模型公式 应用，3d转为了2d投影点
            Draw_KeyPoints3D(img,Joint3D["joints"],fx,fy,cx,cy)
            Draw_KeyPoints3D(img_depth,Joint3D["joints"],fx,fy,cx,cy)
            Draw_Mesh3D(img_jt,Mesh3D,fx,fy,cx,cy,RGB_ = (245, 55, 133))
            Draw_Mesh3D(img_depth_jt,Mesh3D,fx,fy,cx,cy,RGB_ = (245, 55, 133))

            #------------------------------------------------------------------- 判断 pinch
            def eucliDist(A,B):
                return int(np.linalg.norm(A-B))
                # return np.sqrt(sum(np.power((A - B), 2)))
            Joint3D = Joint3D["joints"]
            Index_dst = eucliDist(Joint3D[4],Joint3D[8])
            Middle_dst = eucliDist(Joint3D[4],Joint3D[12])
            Ring_dst = eucliDist(Joint3D[4],Joint3D[16])
            Pink_dst = eucliDist(Joint3D[4],Joint3D[20])
            RGB_list = [(0,0,255),(0,0,255),(0,0,255),(0,0,255)]
            #-------------------------------------------------------------------

            cv2.putText(img, '{}'.format(doc_), (5,img_fusion.shape[0]-10),cv2.FONT_HERSHEY_COMPLEX, 1.25, (255, 0, 55),2)
            cv2.putText(img, 'IDX:{},{}'.format(ok_cnt,Gesture_), (5,img_fusion.shape[0]-45),cv2.FONT_HERSHEY_COMPLEX, 1.25, (55, 128, 55),2)
            cv2.putText(img,"Index -{}".format(Index_dst),(0,30),0,1.1,RGB_list[0],3)
            cv2.putText(img,"Middle-{}".format(Middle_dst),(0,60),0,1.1,RGB_list[1],3)
            cv2.putText(img,"Ring  -{}".format(Ring_dst),(0,90),0,1.1,RGB_list[2],3)
            cv2.putText(img,"Little-{}".format(Pink_dst),(0,120),0,1.1,RGB_list[3],3)

            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

            cv2.putText(img,"RGB-Joints",(img.shape[1]-230,img.shape[0]-13),0,1.1,(255,100,0),5)
            cv2.putText(img_depth,"Depth-Joints",(img.shape[1]-230,img.shape[0]-13),0,1.1,(255,100,0),5)
            cv2.putText(img_jt,"RGB-Mesh",(img.shape[1]-230,img.shape[0]-13),0,1.1,(255,100,0),5)
            cv2.putText(img_depth_jt,"Depth-Mesh",(img.shape[1]-230,img.shape[0]-13),0,1.1,(255,100,0),5)
            cv2.putText(img_fusion,"RGB-Model",(img.shape[1]-230,img.shape[0]-13),0,1.1,(255,100,0),5)
            cv2.putText(mask,"Mask",(img.shape[1]-130,img.shape[0]-13),0,1.1,(255,100,0),5)

            cv2.putText(img,"RGB-Joints",(img.shape[1]-230,img.shape[0]-13),0,1.1,(0,255,250),2)
            cv2.putText(img_depth,"Depth-Joints",(img.shape[1]-230,img.shape[0]-13),0,1.1,(0,250,250),2)
            cv2.putText(img_jt,"RGB-Mesh",(img.shape[1]-230,img.shape[0]-13),0,1.1,(0,255,250),2)
            cv2.putText(img_depth_jt,"Depth-Mesh",(img.shape[1]-230,img.shape[0]-13),0,1.1,(0,250,250),2)
            cv2.putText(img_fusion,"RGB-Model",(img.shape[1]-230,img.shape[0]-13),0,1.1,(25,100,255),2)
            cv2.putText(mask,"Mask",(img.shape[1]-130,img.shape[0]-13),0,1.1,(0,100,250),2)


            img_m1 = np.hstack((img,img_depth,img_fusion))
            img_m2 = np.hstack((img_jt,img_depth_jt,mask))
            img_m = np.vstack((img_m1,img_m2))

            cv2.namedWindow("img_m",0)
            cv2.imshow("img_m",img_m)
            ok_cnt += 1
            print(" >>>>>>>>> ok_cnt :",ok_cnt)

            if cv2.waitKey(1)==27:
                break

    print("\n -->> ok_cnt:",ok_cnt)
