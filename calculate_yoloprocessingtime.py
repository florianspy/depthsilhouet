#!/usr/bin/env python3
""" 
python3 yolov3_to_onnx.py --model yolov3-416
python3 onnx_to_tensorrt.py --model yolov3-416 
"""
from darknet_ros_msgs.msg import BoundingBox, BoundingBoxes
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import CompressedImage, Image, CameraInfo
#import pycuda.driver as cuda
import sys
import time
import argparse
import cv2
import numpy as np
import pycuda.autoinit  # This is needed for initializing CUDA driver
from utils.yolov3_classes import get_cls_dict
from utils.yolov3 import TrtYOLOv3
#from utils.camera import add_camera_args, Camera
#from utils.display import open_window, set_display, show_fps
from utils.visualization import BBoxVisualization

# Name of the camera topic
topic_sub_image = '/camera/rgb/image_color'
#topic_sub_image = '/depth_edges'

# Name of the published image topic
topic_pub_image = '/yolov3_image'

# Name of the published boxes info topic
topic_pub_boxes = '/yolov3_boxes'

# YOLO Dimension - default 416
yolo_dimension = 416    

# Confidence threshold  for YOLO
confidence_threshold = 0.5

class YOLOros:

    def __init__(self):
        self.boxes_pub = rospy.Publisher(topic_pub_boxes, BoundingBoxes, queue_size = 10)
        self.image_pub = rospy.Publisher(topic_pub_image, Image, queue_size = 10) 
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber(topic_sub_image, Image, self.image_callback)
        self.yolo_dim = yolo_dimension
        self.trt_yolov3 = TrtYOLOv3('yolov3-416', (self.yolo_dim, self.yolo_dim))
        self.img = np.zeros(shape=[480, 640, 3], dtype=np.uint8); self.boxes = None; self.confs = None; self.clss = None; self.conf_th = confidence_threshold
        self.msg = None
        self.tic = 0; self.toc = 0
        self.out = np.zeros(shape=[480, 640, 3], dtype=np.uint8)
        self.vis = BBoxVisualization(get_cls_dict('coco'))
        self.oldimg = np.zeros(shape=[480, 640, 3], dtype=np.uint8);
        #self.img = cv2.imread('/home/LG/Pictures/dog.jpg', 0); 
        self.path=os.path.expanduser('~/Documents/document.csv')
        if os.path.isfile(self.path):
                os.remove(self.path)
                print(self.path, "File was deleted and a new one will be created.")
    def write_message(self, detection_results, boxes, scores, classes):
        """ populate output message with input header and bounding boxes information """
        if boxes is None:
            return None
        for box, score, category in zip(boxes, scores, classes):
            # Populate darknet message
            left, bottom, right, top = box
            detection_msg = BoundingBox()
            detection_msg.xmin = np.int64(left)
            detection_msg.xmax = np.int64(right)
            detection_msg.ymin = np.int64(bottom)
            detection_msg.ymax = np.int64(top)
            detection_msg.probability = np.float64(score)
            detection_msg.id = np.int16(category)
            category_name = get_cls_dict('coco').get(category, 'CLS{}'.format(category))
            detection_msg.Class = str(category_name)
            detection_results.bounding_boxes.append(detection_msg)
        return detection_results

    def detect(self):
        """ Function to detect objects and publish them """
        # if image is not empty
        same=True
        if self.img.any():
            if np.all(self.oldimg==self.img):
                 same=True
            else:
                 self.oldimg = self.img
                 same=False 
            # Get the boxes, confs, classes from the image                  
            tocy = time.time()     
            self.boxes, self.confs, self.clss = self.trt_yolov3.detect(self.img, self.conf_th)
            ticy = time.time()  

            # Create BoundingBoxes object with header infos
            detection_results = BoundingBoxes()
            #detection_results.header = self.msg.header
            #detection_results.image_header = self.msg.header
            self.msg = None

            #print(detection_results.bounding_boxes[0].probability, 'prob')
            #print(type(detection_results.bounding_boxes[0].probability), 'prob2')

            # Put boxes, confs, classes in BoundingBoxes object
            self.write_message(detection_results, self.boxes, self.confs, self.clss)
            
            # Draw boxes in img and publish them
            try:
                self.out = self.vis.draw_bboxes(self.img, self.boxes, self.confs, self.clss)
                self.image_pub.publish(self.bridge.cv2_to_imgmsg(self.out,"bgr8"))
            except CvBridgeError as e:
                print(e)

            # Publish the Bounding Box infos 
            try:
                rospy.loginfo("pub")
                self.boxes_pub.publish(detection_results)
            except CvBridgeError as e:
                print(e)
            ticy2 = time.time()  
            if same == false: 
                 timeshort = ticy - tocy
                 timelong= ticy2 - tocy
                 with open(self.path,'a') as fd:
                        fd.write(str(timeshort)+',sec,'+str(timelong)+',sec\n')      

    def image_callback(self, data):
        """ Callback function to get the images from the subscriber """
        try:
            self.img = self.bridge.imgmsg_to_cv2(data, "bgr8")
            self.msg = data
        except CvBridgeError as e:
            print(e)            


def main():
    rospy.init_node('YOLO_TRT_ROS', anonymous=True)
    rospy.loginfo('[YOLO_TRT_ROS] starting the node')
    #YOLO_TRT_ROS = YOLOros()
    #cuda.init()
    #cuda_ctx = cuda.Device(0).make_context() # GPU 0

    try:
        YOLO_TRT_ROS = YOLOros()
    except rospy.ROSInterruptException:
        rospy.logerr('It was not able to create YOLOros object.')
        pass

    sleep_time = rospy.Rate(10)
    while not rospy.is_shutdown():
        YOLO_TRT_ROS.detect()
        sleep_time.sleep()

    # try:
    #   rospy.spin()
    # except KeyboardInterrupt:
    #   print("Shutting down")
    #cv2.destroyAllWindows()

if __name__ == '__main__':
    main()