# opencv实现矩形物体的自动化标注并生成xml文件(如纸币)
## 视频规范
1. 初始帧目标呈水平
2. 拍摄过程中保持目标水平且离镜头距离不变，可以上下左右移动
## Testing
`python3 detect.py --video_index 0`
`python3 copyfile.py`
### 在frames_all中删除不合格的图片
`python3 del_xml_file.py`
`python3 rename.py`
