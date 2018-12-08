# -*- coding:utf-8 -*-
'''
在第一帧点两个点，分别是目标左上角和右下角的点，形成一个矩形。
之后每隔15帧截取无检测框和有检测框的图片，同时生成xml文件，分别存在frames，frames_raw, xml文件夹中
每个文件的命名为：视频名_帧序号.jpg(xml)
'''
import cv2
import sys
import os
from lxml_test import gen_txt
import argparse
import pickle
import glob
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--video_index', help='The index of videos in the fold', type=int)
parser.add_argument('--frames_to_cut', default=15, help='Per frames to save image and xml file', type=int)
# parser.add_argument('--video_path')
# parser.add_argument('--xml_path', help='path to save xml files')
args = parser.parse_args()

# Mouse response function
def getPosition(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global x1, y1, x2, y2, clickCount
        if (clickCount == 0):
            x1, y1 = x, y
            clickCount = clickCount + 1
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
            return
        if (clickCount == 1):
            x2, y2 = x, y
            clickCount = clickCount + 1
            return

if __name__ == '__main__':
    video_paths = glob.glob('videos/*.mp4')
    video_path =  video_paths[args.video_index]
    video_name = video_path.split('/')[-1][:-4]
    print(video_name)
    # Set up tracker.
    # Instead of MIL, you can also use
    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']

    # tracker_type = tracker_types[2]
    tracker_type = tracker_types[0]
    tracker = cv2.TrackerBoosting_create()

    # Read video
    print(video_path)
    video = cv2.VideoCapture(video_path)
    # video = cv2.VideoCapture('./videos/test.mp4')

    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()
    xml_path = os.path.join(video_name, 'xml')
    save_img_path = os.path.join(video_name, 'frames')
    save_rawimg_path = os.path.join(video_name, 'frames_raw')
    if not os.path.exists(xml_path):
        os.system('mkdir -p ' + xml_path)
    else:
        shutil.rmtree(xml_path)
        os.mkdir(xml_path)
    if not (os.path.exists(save_img_path)):
        os.mkdir(save_img_path)
    else:
        shutil.rmtree(save_img_path)
        os.mkdir(save_img_path)
    if not (os.path.exists(save_rawimg_path)):
        os.mkdir(save_rawimg_path)
    else:
        shutil.rmtree(save_rawimg_path)
        os.mkdir(save_rawimg_path)
    # init global variable
    clickCount = 0
    x1, y1, x2, y2 = -1, -1, -1, -1

    # show the first frame of the video
    cv2.namedWindow("first frame",0)

    # add mouse response function to window
    cv2.setMouseCallback('first frame', getPosition)

    # resize the window
    cv2.resizeWindow('first frame', 1000, 1000)

    num_frames = 0

    while (clickCount < 2):
        cv2.imshow("first frame", frame)
        cv2.setMouseCallback('first frame', getPosition)
        k = cv2.waitKey(1) & 0xff
        if k == 27: break
    cv2.destroyWindow('first frame')
    # Define an initial bounding box
    bbox = (x1, y1, abs(x2 - x1), abs(y2 - y1))
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)

    # open local file
    # fo = open("./output2/output.txt", "w")
    os.system('mkdir -p ' + video_name)
    fo = open(os.path.join(video_name, 'output.txt'), 'w')

    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
        # Start timer
        timer = cv2.getTickCount()
        # Update tracker
        ok, bbox = tracker.update(frame)
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))  # left-top
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1]))  # right-top
            p3 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))  # right-bottom
            p4 = (int(bbox[0]), int(bbox[1] + bbox[3]))  # left-bottom
            if num_frames % 15 == 0:    
                cv2.imwrite(os.path.join(save_rawimg_path, video_name+'_{}.jpg'.format(num_frames)), frame)
            cv2.rectangle(frame, p1, p3, (255, 0, 0), 2, 1)
            # save the position of the box
            fo.write(
                str(p1[0]) + "," + str(p1[1]) + "\t" + str(p2[0]) + "," + str(p2[1]) + "\t" + str(p3[0]) + "," + str(
                    p3[1]) + "\t" + str(p4[0]) + "," + str(p4[1]) + "\n")
        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # Display result
        cv2.namedWindow('Tracking', 0)
        cv2.resizeWindow('Tracking', 1000, 1000)
        cv2.imshow("Tracking", frame)
        if num_frames % 15 == 0:    
            cv2.imwrite(os.path.join(save_img_path, video_name+'_{}.jpg'.format(num_frames)), frame)
            shape = frame.shape
            gen_txt(os.path.join(xml_path, video_name+'_'+str(num_frames)), shape[0], shape[1], shape[2], p1[0], p2[0], p3[1], p1[1])
            print('\r' + 'num_frames: ' + str(num_frames), end='', flush=True)
        num_frames += 1
        
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            fo.close()
            break

    fo.close()