#include "ros/ros.h"
#include "std_msgs/String.h"

/// current_sign is mark of current
/// running road sign
int current_sign = 0;

/// Action: move forward: true
/// Action: turn: false
bool current_action = true;

/// Default: moving forward
void sendMessage() {
  // TODO: connection with arduino
  // [speed, shift]
}

void sendMessage(int speed, int shift) {
  // TODO: connection with arduino
  // [speed, shift]
}

void correct_direction() {
  // TODO: correction logic
}

void calculate_rotation(bool right) {
  // TODO: rotation logic
}

void run(const std_msgs::String::ConstPtr& msg) {

  ROS_INFO("I heard: [%s]", msg->data.c_str());

  // TODO: read message
  bool red_light = false;
  int sign = 0;
  bool blocked = false;
  int pos = 0;
  int shift = 0;

  if (red_light) {
    // TODO: stop-message
    return;
  }

  current_sign = sign;

  /// 0 is forward sign
  if (sign == 0){
    correct_direction();
    return;
  }

  switch (sign) {
    case 1: /// left sign
    {
      calculate_rotation(false);
      break;
    }
    case 2: /// right sign
    {
      calculate_rotation(true);
      break;
    }
    case 3: /// left and forward sign
    {
      /// block sign is forward?
      if (blocked) {
        calculate_rotation(false);
      }
      break;
    }
    case 4: /// right and forward sign
    {
      /// block sign is forward?
      if (blocked) {
        calculate_rotation(true);
      }
      break;
    }
    case 5: /// block sign
    {
      // TODO: move forward or stop; decide; forward as default
      break;
    }
  }

}

int main(int argc, char **argv) {

  ros::init(argc, argv, "listener");
  ros::NodeHandle n;

  if (true){
    ROS_INFO("TRUE");
  }

  ros::Subscriber sub = n.subscribe("vision_info", 10, run);

  ros::spin();

  return 0;
}
