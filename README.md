# rtr_qr_reader
Decode QR-code from image topic and show as OverlayText in rviz
![](./resource/screenshot.png)
## requirements
~~~bash
sudo apt install zbar-tools
pip3 install pyzbar
pip3 install opencv-python
sudo apt install ros-noetic-cv-bridge
sudo apt install ros-noetic-jsk-rviz-plugins
# opencv
~~~
## 使い方
### rtr_qr_reader_node
非推奨
### multi_qr_reader.py
複数の画像トピックからQRコードを読み取り、OverlayTextと画像に表示する．
※同時に複数の画像トピックでQRコードが発見された場合，表示が不安定になるので注意

参考launchファイル
~~~xml
<?xml version="1.0"?>
<launch>
    <node pkg="rtr_qr_reader" type="multi_qr_reader.py" name="multi_qr_reader" output="screen">
        <!-- カンマ区切りでトピックを指定 -->
        <param name="topics" value="/RTRQuadcopter/Camera2/image_raw,/RTRQuadcopter/Camera3/image_raw"/>
    </node>
</launch>
~~~


