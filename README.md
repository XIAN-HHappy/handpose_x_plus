# handpose X plus


* [演示完整视频](https://www.bilibili.com/video/BV1HTYReYEBj/?share_source=copy_web&vd_source=014da96a262b45c24251d22ed2727fba)  

<img src="doc/demo.gif" width="100%" alt="知识星球">

# 一、数据集介绍

## 数据内容包括：

* 1）rgb 图像 （rgb image）
* 2）深度点云图像 (depth image)
* 3）手21三维和二维关键点 (21 3d & 2d joints)
* 4）手三维和二维mesh网格点 (3d & 2d mesh )
* 5）相机内参 (camera Intrinsics : fx, fy, cx, cy)
* 6）静态手势 (gesture)
* 7）手部mask （hand mask）
* 8）室内&室外场景
# 二、数据集解析

```bash
python read_datas.py
```

# 三、数据增强

```bash
python read_datas_augmentation.py
```
#### 数据增强样例

<img src="samples/s1.png" width="50%" alt="知识星球">

# 四、数据集整合
```bash
注意：
1)为了方便使用，按照 handposeX json 自定义格式存储
2)使用常见依赖库进行调用,降低数据集使用难度。
3)部分数据集获取请加入：DataBall-X数据球(free)
4)完整数据集获取请加入：DataBall-X数据球(vip)
```

- [x] [FreiHAND](https://github.com/XIAN-HHappy/handpose_x_plus/script/FreiHAND)
- [ ] [handposeX_3D_rgb_v1]
- [ ] [HO3D]
- [ ] [InterHand26M]

```bash
官方项目：https://github.com/lmb-freiburg/freihand
```

## 4.1 handposeX json 格式示例：
```bash
{
 "author": "XIAN",
 "img_name:": "",
 "cx": 112.0,
 "cy": 112.0,
 "fx": 388.9018310596544,
 "fy": 388.71231836584275,
 "hands": [
  {
   "label": "right",
   "joint3d": [
    [
     29.402047395706177,
     -27.920207008719444,
     587.0807766914368
    ],
    ······
   ],
   "vertex3d": [
    [
     10.056010007858276,
     29.915300235152245,
     -626.9440693855286
    ],
    ······
   ]
  }
 ]
}
```
## 4.2 FreiHAND 数据集示例
<img src="samples/f1.jpg" width="50%" alt="知识星球">


#### 加入 “DataBall - X 数据球” 知识星球,获取数据集

<img src="doc/zsxq.jpg" width="50%" alt="知识星球">

### 即将发布 Coming Soon
### 联系方式 （Contact）  
* E-mails: 305141918@qq.com   
