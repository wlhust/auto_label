# -*- coding:utf-8 -*-
'''上一步在frames_all中删除了不合格的图片，删除raw_all, xml_all中不在frames_all里的文件'''

import os

frames_path = './frames_all'
xml_path = './xml_all'
frames_raw_path = './raw_all'
frames_files = list(map(lambda x: x.split('.')[0], os.listdir(frames_path)))
xml_files = list(map(lambda x: x.split('.')[0], os.listdir(xml_path)))
frames_raw_files = list(map(lambda x: x.split('.')[0], os.listdir(frames_raw_path)))
for i in range(len(xml_files)):
    if xml_files[i] not in frames_files:
        os.remove(os.path.join(xml_path, xml_files[i]) + '.xml')
for i in range(len(frames_raw_files)):
    if frames_raw_files[i] not in frames_files:
        os.remove(os.path.join(frames_raw_path, frames_raw_files[i]) + '.jpg')
