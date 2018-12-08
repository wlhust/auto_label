# -*- coding:utf-8 -*-
from shutil import copy
import os
import glob
# -*- coding: utf-8 -*- 
'''将上一步产生的所有文件复制到三个代表不同类型的文件夹中'''

dirs = os.listdir('videos/')
dirs = list(map(lambda x: x.split('.')[0], dirs))
# dirs = ['VID_20181207_220711']
new_frame_dir = './frames_all'
new_xml_dir = './xml_all'
new_raw_dir = './raw_all'
os.system('mkdir -p ' + new_frame_dir)
os.system('mkdir -p ' + new_xml_dir)
os.system('mkdir -p ' + new_raw_dir)

for dir_tmp in dirs:
    frame_path = os.path.join(dir_tmp, 'frames')
    xml_path = os.path.join(dir_tmp, 'xml')
    raw_path = os.path.join(dir_tmp, 'frames_raw')
    for frame in os.listdir(frame_path):
        print('\r' + os.path.join(frame_path, frame), end='', flush=True)
        copy(os.path.join(frame_path, frame), new_frame_dir)
    for xml in os.listdir(xml_path):
        print('\r' + os.path.join(xml_path, xml), end='', flush=True)
        copy(os.path.join(xml_path, xml), new_xml_dir)
    for frame_raw in os.listdir(raw_path):
        print('\r' + os.path.join(raw_path, frame_raw), end='', flush=True)
        copy(os.path.join(raw_path, frame_raw), new_raw_dir)