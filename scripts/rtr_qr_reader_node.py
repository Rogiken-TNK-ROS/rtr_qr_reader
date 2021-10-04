#!/bin/python3
from typing import Text
from pyzbar.pyzbar import decode

import rospy

import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from jsk_rviz_plugins.msg import OverlayText

bridge = CvBridge()

class Node:
    def __init__(self):
        rospy.init_node("rtr_qr_reader_node")
        topic = rospy.get_param("/qr_reader/topic_name", "/usb_cam/image_raw")

        self.img_sub = rospy.Subscriber(
            topic, Image, self.img_callback, queue_size=100)

        self.output_pub = rospy.Publisher("qr_output", OverlayText, queue_size=10)

    def img_callback(self, img_msg):
        img = bridge.imgmsg_to_cv2(img_msg, "bgr8")
        data = decode(img)
        if len(data) == 0:
            return
        print(data[0][0].decode('utf-8', 'ignore'))
        print(data[0][1])
        print(data[0][2])
        print(data[0][3])

        text = OverlayText()
        text.text = data[0][0].decode('utf-8', 'ignore')
        text.width = 500
        text.height = 500
        text.text_size = 12
        text.left = 10
        text.top = 10
        text.font = "Ubuntu Mono Regular"
        text.bg_color.a = 0
        text.fg_color.r = 25 / 255.0
        text.fg_color.g = 1
        text.fg_color.b = 1
        text.fg_color.a = 1
        self.output_pub.publish(text)

if __name__ == '__main__':
    node = Node()
    rospy.spin()
