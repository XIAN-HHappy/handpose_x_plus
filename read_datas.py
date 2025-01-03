#-*-coding:utf-8-*-
# date:2024-01-24
# Author: DataBall - XIAN
# function: read samples

import os
import cv2
import numpy as np
import copy
from utils import read_obj,read_camera_intrinsics,Draw_KeyPoints3D,Draw_Mesh3D,read_gesture

if __name__ == '__main__':

    path_s = "./handpose_x_plus_datas/"
    ok_cnt = 0
    Flag_check_error = False
    for doc_  in os.listdir(path_s):
        # if "output-enjoy0000153" not in doc_:
        #     continue
        path_root  = path_s + doc_ + "/"
        for f_ in os.listdir(path_root):
            if ".png" not in f_:
                continue
            name_x = f_.replace("_depth.png","")
            path_depth = path_root + f_
            path_mesh = path_root + f_.replace("_depth.png","_Mesh.obj")
            path_joint = path_root + f_.replace("_depth.png","_Joint.obj")
            path_intrinsics = path_root + f_.replace("_depth.png","_intrinsics.txt")
            path_gesture = path_root + f_.replace("_depth.png","_gesture.txt")
            path_img = path_root + f_.replace("_depth.png","_o.jpg")
            path_fusion = path_root + f_.replace("_depth.png","_fusion.jpg")
            path_skl = path_root + f_.replace("_depth.png","_fit2d.jpg")

            fx,fy,cx,cy = read_camera_intrinsics(path_intrinsics)

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

            img_depth = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            img_depth = cv2.cvtColor(img_depth, cv2.COLOR_GRAY2RGB)
            img_depth_jt = img_depth.copy()
            img_jt = img.copy()

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

    print("\n >>>>>>>>>>>>>>>>> ok_cnt:",ok_cnt)
