#!/bin/python3
from typing import Text
from pyzbar.pyzbar import decode

import rclpy
from rclpy.node import Node

import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from jsk_rviz_plugins.msg import OverlayText
from rtr_msgs.srv import QRPosition

bridge = CvBridge()


class QRReaderNode(Node):
    def __init__(self):
        super().__init__('rtr_qr_reader_node')
        topic = self.declare_parameter('topic_name', '/RTRQuadcopter/Camera2/image_raw').get_parameter_value().string_value

        self.qr_position = self.create_client(QRPosition, "/quadcopter/qr_position")
        while not self.qr_position.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')

        self.img_sub = self.create_subscription(
            Image, topic, self.img_callback, 10)

        self.output_pub = self.create_publisher(
            OverlayText, "qr_output", 10)
        self.res = None

    def img_callback(self, img_msg):
        img = bridge.imgmsg_to_cv2(img_msg, "bgr8")
        data = decode(img)
        if len(data) == 0:
            return
        print(data[0][0].decode('utf-8', 'ignore'))
        print(data[0][1])
        print(data[0][2])
        print(data[0][3])
        x = 0
        y = 0
        for p in data[0][3]:
            x += p.x
            y += p.y
        x /= 4
        y /= 4
        x = int(x)
        y = int(y)

        print(x, y)
        req = QRPosition.Request()
        req.x = x
        req.y = y
        future = self.qr_position.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        try:
            self.res = future.result()
        except Exception as e:
            self.get_logger().error('Service call failed %r' % (e,))

        print(self.res)
        text = OverlayText()
        text.text = data[0][0].decode('utf-8', 'ignore') + ': {:.3g}'.format(self.res.qr_global_x) + ", " + '{:.3g}'.format(self.res.qr_global_y) + ", " + '{:.3g}'.format(self.res.qr_global_z)
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


def main(args=None):
    rclpy.init(args=args)
    node = QRReaderNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
