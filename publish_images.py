import numpy as np
from PIL import Image
import glob, os
import cv2
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image,CameraInfo,Imu
from cv_bridge import CvBridge, CvBridgeError

brigde_object = CvBridge()
#where to get the images from
img_path = os.path.expanduser('~/Desktop/DatasetsPink/*rgb.png') 
#are the images in rgb or bgr format
rgbformat=true
def talker():
    '''create Publisher'''
    rospy.init_node('depth_pointcloud', anonymous=True)
    pub = rospy.Publisher('depth_pointcloud', Image, queue_size=10)
    pub2 = rospy.Publisher('rgb_pointcloud', Image, queue_size=10)
    pub3 = rospy.Publisher("camera_info_pointcloud",CameraInfo,queue_size=10)    
    rate = rospy.Rate(1) # 10hz
    
    # https://www.programcreek.com/python/example/99840/sensor_msgs.msg.CameraInfo      
    #this message remains the same so it goes outside of the loop
    camera_info = CameraInfo()      
    camera_info.width = 570
    camera_info.height = 430
    camera_info.distortion_model = 'plumb_bob'
    camera_info.K = [525.0, 0.0, 319.5, 0.0, 525.0, 239.5, 0.0, 0.0, 1.0]
    camera_info.D = [0.0, 0.0, 0.0, 0.0, 0.0]
    camera_info.R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
    camera_info.P = [525.0, 0.0, 319.5, 0.0, 0.0, 525.0, 239.5, 0.0, 0.0, 0.0, 1.0, 0.0]
    
     
           
    for files in glob.glob(img_path):  
            #publish the rgb image
            rgb = cv2.imread(files)
            if rgbformat == False:
               rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
            ms2=brigde_object.cv2_to_imgmsg(rgb, "bgr8")
            ms2.header.frame_id='map'
            pub2.publish(ms2)               
            #depth and rgb files should have same name except that depth files contain depth instead of rgb in there names
            #publish the depth image
            depthfile=files.replace('rgb', 'depth')
            depth = cv2.imread(depthfile,  cv2.IMREAD_UNCHANGED)
            ms=brigde_object.cv2_to_imgmsg(depth, "16UC1")     
            ms.header.frame_id='map'
            pub.publish(ms)                  
            #publish the camera_info
            pub3.publish(camera_info)
            #rest abit so we have time to process
            rate.sleep()
    
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass