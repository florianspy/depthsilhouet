#include <typeinfo>
#include <iostream>
#include <fstream>
#include "ros/ros.h"
#include <opencv2/core/core.hpp>
#include <opencv2/rgbd.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "cv_bridge/cv_bridge.h"
#include <sensor_msgs/image_encodings.h>
#include "image_transport/image_transport.h"

#include "message_filters/subscriber.h"
#include "message_filters/synchronizer.h"
#include "message_filters/time_synchronizer.h"
#include "message_filters/sync_policies/exact_time.h"
#include <message_filters/sync_policies/approximate_time.h>

using namespace std;
using namespace cv;
using namespace sensor_msgs;
using namespace message_filters;

class SubscribeFillPublish
{
    private:
        ros::NodeHandle n;
        ros::Publisher image_pub;
        message_filters::Subscriber<Image> image_sub;
        message_filters::Subscriber<Image> depth_sub;
        typedef sync_policies::ApproximateTime<Image, Image> MySyncPolicy;
        Synchronizer<MySyncPolicy> sync;
        Mat depth, color;
        Scalar edge_color = Scalar(255,0,255);
        vector<vector<Point>> contours;
        vector<Vec4i> hierarchy;
        int contours_size = 3;
        std::ofstream myfile;
        string filename= string(getenv("HOME")).append("/dataNumbers.csv");;        
        double raw_taken,time_taken;
        int width = 0;
        int height = 0;
    public:
    //  Constructor
        SubscribeFillPublish():sync(MySyncPolicy(50), image_sub, depth_sub){
            cout<<"SubscribeFillPublish object will be created"<<endl;
            image_sub.subscribe(n, "/camera/rgb/image_color/", 1);
            depth_sub.subscribe(n, "camera/depth_registered/hw_registered/image_rect", 1);
            sync.registerCallback(boost::bind(&SubscribeFillPublish::callback,this, _1, _2));    
            image_pub = n.advertise<Image>("depth_edges", 50);
        }

    void callback(const sensor_msgs::ImageConstPtr& msg_color,const sensor_msgs::ImageConstPtr& msg_depth){
        // callback
        clock_t start, end,startr;
        start = clock(); 
        // Get the ROS messages
        color = cv_bridge::toCvShare(msg_color)->image;
        depth = cv_bridge::toCvShare(msg_depth)->image;
        // color = imread("/home/LG/Pictures/DatasetLab/Labor4/01486rgb.jpg", CV_LOAD_IMAGE_COLOR);
        // depth = imread("/home/LG/Desktop/RGB_Dataset/Labor4Tag/01486depth.png", CV_LOAD_IMAGE_ANYDEPTH);        
        //cout << depth << endl;
        depth.convertTo(depth, CV_16UC1);

        // Resize picture (x,y,width,height)
        //const Rect myROI(12, 42, 570, 430);
        //depth = depth(myROI);
        //color = color(myROI);

        int z = 1;
        width = depth.cols;
        height = depth.rows;
        // Hole Filler

        // setNumThreads(12);
        // parallel_for_(Range(0, depth.rows*depth.cols), [&](const Range& range){
        // for (int r = range.start; r < range.end; r++)
        // {
        //     int i = r / depth.cols; 
        //     int j = r % depth.cols;

        //     if(depth.at<ushort>(i,j) == 0){
        //         z = 1;
        //         while( ((j+z)<(width-1)) and (depth.at<ushort>(i,j+z)==0) ){
        //             z++;
        //         }
        //         if (j==0){
        //             depth.at<ushort>(i,j) = depth.at<ushort>(i,j+z);
        //         }
        //         if ((j>0) and (j<(width-1))){
        //             depth.at<ushort>(i,j) = max(depth.at<ushort>(i,j-1), depth.at<ushort>(i,j+z));
        //         }
        //         if (j==(width-1)){
        //             depth.at<ushort>(i,j) = depth.at<ushort>(i,j-1);
        //         }
        //     }
        // }
        // });
        startr = clock(); 
        for (int y = 0; y < height; y++){

            for (int x = 0; x < width; x++){

                if (depth.at<ushort>(y,x) == 0){
                    z = 1;
                    while( ((x+z)<(width-1)) and (depth.at<ushort>(y,x+z)==0) ){
                        z++;
                    }
                    if (x==0){
                        depth.at<ushort>(y,x) = depth.at<ushort>(y,x+z);
                    }
                    if ((x>0) and (x<(width-1))){
                        depth.at<ushort>(y,x) = max(depth.at<ushort>(y,x-1), depth.at<ushort>(y,x+z));
                    }
                    if (x==(width-1)){
                        depth.at<ushort>(y,x) = depth.at<ushort>(y,x-1);
                    }
                }
            }
        }

        // Normalize 
        depth.at<ushort>(0,0) = 10000;
        normalize(depth, depth, 0, 255, NORM_MINMAX, CV_8UC1);
        //depth.convertTo(depth, CV_8UC1);

        // MedianFilter to smoothing the edges
        medianBlur(depth, depth,5);
        // Canny
        Canny(depth, depth, 30, 100, 3);
        // Create Contours
        findContours(depth, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE);
        drawContours(color, contours, -1, edge_color, contours_size, 8, hierarchy);
        end = clock(); 
        raw_taken = double(end - startr) / double(CLOCKS_PER_SEC);
        // Publish the images in ROS

        end = clock(); 
        time_taken = double(end - start) / double(CLOCKS_PER_SEC);
        cout << "Time taken by program is : " << fixed << time_taken << setprecision(5) << " sec " << endl;  
        //https://stackoverflow.com/questions/25201131/writing-csv-files-from-c
        myfile.open (filename);
        myfile<< raw_taken << setprecision(5) << ", sec ,"<<time_taken << setprecision(5) << ", sec " << endl;  
        myfile.close();
        //Time taken by program is : 0.01300 sec
        //Time taken by program is : 0.01240 sec
        // ros::Rate loop_rate(2);
        // loop_rate.sleep();
    }

};

int main(int argc, char **argv){
    ros::init(argc, argv,  "talker");
    cout<<"ROS init"<<endl;
    SubscribeFillPublish fill;
    cout<<"ROS init vorbei"<<endl;
    ros::spin();
}