#include "ros/ros.h"

int main(int argc, char **argv) {

  ros::init(argc, argv, "listener");
  ros::NodeHandle n;

  ROS_INFO("run");

  ros::spinOnce();

  return 0;
}
