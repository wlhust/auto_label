# -*- coding:utf-8 -*-
'''将文件名改成0,1,2,3.......jpg(xml),并将修改xml文件中filename'''

import os
import xml.dom.minidom

i = 0
for file in os.listdir('./frames_all/'): 
    os.rename(os.path.join('./frames_all', file), os.path.join('./frames_all', str(i)+'.jpg'))
    i += 1
i = 0
for file in os.listdir('./xml_all/'): 
    os.rename(os.path.join('./xml_all', file), os.path.join('./xml_all', str(i)+'.xml'))
    i += 1
i = 0 
for file in os.listdir('./raw_all/'):
    os.rename(os.path.join('./raw_all', file), os.path.join('./raw_all', str(i)+'.jpg'))
    i += 1

os.system('mkdir -p xml_new')
for file in os.listdir('./xml_all'):
    if file.split('.')[-1] != 'xml':
        continue
    dom = xml.dom.minidom.parse(os.path.join('xml_all', file))
    root = dom.documentElement
    filename = root.getElementsByTagName('filename')
    filename[0].firstChild.data = file.split('.')[0]
    with open(os.path.join('xml_new', file), 'w') as f:
        dom.writexml(f)
