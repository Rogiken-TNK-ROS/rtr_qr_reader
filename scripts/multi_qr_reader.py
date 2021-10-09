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
        topics = rospy.get_param("~topics","")
        self.topics = topics.split(",")

        self.image_subscribers = []
        for topic in self.topics:
            self.image_subscribers.append(
                rospy.Subscriber(topic, Image, self.img_callback, queue_size=1)
            )

        self.output_text_pub = rospy.Publisher(
            "qr_output", OverlayText, queue_size=1)

        self.output_image_pub = rospy.Publisher(
            "qr_image",Image,queue_size=1)

    def img_callback(self, img_msg):
        img = bridge.imgmsg_to_cv2(img_msg, "bgr8")
        data = decode(img)
        if len(data) == 0:
            return

        color = (255,0,0)

        all_text = ''
        for d in data:
            text = d[0].decode('utf-8','ignore')
            pts = d[3]
            img = cv2.line(img,pts[0],pts[1],color,5)
            img = cv2.line(img,pts[1],pts[2],color,5)
            img = cv2.line(img,pts[2],pts[3],color,5)
            img = cv2.line(img,pts[3],pts[0],color,5)
            x = 1000
            y = 0
            for p in pts:
                x = min(x,p[0])
                y = max(y,p[1])
            font = cv2.FONT_HERSHEY_SIMPLEX
            (w, h), baseline = cv2.getTextSize(text, font, 1, 2)
            cv2.rectangle(img, (x-5, y - h + 35 ), (x + w + 5, y + baseline + 45), (255, 255, 255), thickness=-1)
            cv2.putText(img,text,(x,y + 40), font, 1,(255,0,0),2,cv2.LINE_AA)
            print(text)
            all_text +=  text + '  '

        cv2.putText(img,str(rospy.get_time()),(10,40), font, 1,(255,0,0),2,cv2.LINE_AA)
        img_msg = bridge.cv2_to_imgmsg(img, "bgr8")
        self.output_image_pub.publish(img_msg)

        text = OverlayText()
        text.text = all_text
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
        self.output_text_pub.publish(text)


if __name__ == '__main__':
    node = Node()
    rospy.spin()
