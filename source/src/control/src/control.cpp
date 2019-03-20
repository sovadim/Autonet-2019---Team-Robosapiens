#include "ros/ros.h"
#include "std_msgs/Bool.h"
#include "std_msgs/Int32.h"
#include "vision_info_msg/vision_info_msg.h"

#define MAXIMUM_SPEED 450
#define COUNTER_WIDTH 100 // TODO:Calculate
#define SLEEP_STEPS 100 // TODO:Calculate

/// TURN LOGIC
int turn_counter;
int sleep_counter;
int rotation;
bool action_active;
bool reverse;

/// MESSAGE VARIABLES
bool red_light;
int sign;
bool blocked;
int pos;
int shift;

/// current_sign is mark of current
/// running road sign
int current_sign = 0;

/// Action: move forward: true
/// Action: turn: false
bool current_action = true;

int correct_direction(int shift) {
  return (shift > 0 ? 2 : (-2));
}

int calculate_rotation(bool right) {
  if (action_active) {
    /// Move to position
    if (sleep_counter < SLEEP_STEPS) {
      sleep_counter++;
      reverse = false;
      return 0;
    }
    /// Rotate
    if (!reverse) {
      turn_counter++;
      if (turn_counter >= COUNTER_WIDTH)
        reverse = true;
    } else {
      turn_counter--;
      if (turn_counter >= COUNTER_WIDTH) {
        reverse = false;
        action_active = false;
        sleep_counter = 0;
        turn_counter = 0;
      }
    }
    int msg = turn_counter/2;
    if (!right) msg *= (-1);
    return msg;

  } else {
    action_active = true;
    sleep_counter++;
    return 0;
  }
}

void getMessage(const vision_info_msg::vision_info_msg &msg) {
  //ROS_INFO("I heard: [%d], [%i], [%d], [%i], [%i]", msg.light, msg.sign, msg.blocked, msg.pos, msg.shift);

  red_light = msg.light;
  sign = msg.sign;
  blocked = msg.blocked;
  pos = msg.pos;
  shift = msg.shift;
}

int main(int argc, char **argv) {

  ros::init(argc, argv, "listener");
  ros::NodeHandle n;
  ros::Publisher pub_move = n.advertise<std_msgs::Bool>("move", 100);
  ros::Publisher pub_rotate = n.advertise<std_msgs::Int32>("rotate", 100);
  ros::Subscriber sub = n.subscribe("vision_info", 100, getMessage);
  ros::Rate loop_rate(100);

  bool red_light = false;
  int sign = 0;
  bool blocked = false;
  int pos = 0;
  int shift = 0;

  turn_counter = 0;
  sleep_counter = 0;
  rotation = 0;
  action_active = false;
  reverse = false;

  while (ros::ok) {

    std_msgs::Bool msg_move;
    std_msgs::Bool msg_rotation;

    if (red_light) {
      return false;
    }

    current_sign = sign;

    if (sign == 0){
      msg_move.data = true;
      pub_move.publish(msg_move);

      msg_rotation.data = 0;
      //pub_rotate.publish(correct_direction(shift));
      pub_rotate.publish(msg_rotation);
      continue;
    }

    switch (sign) {
      case 1: /// left sign
      {
        msg_move.data = true;
        msg_rotation.data = calculate_rotation(false);
        break;
      }
      case 2: /// right sign
      {
        msg_move.data = true;
        msg_rotation.data = calculate_rotation(true);
        break;
      }
      case 3: /// left and forward sign
      {
        /// block sign is forward?
        if (blocked) {
          msg_move.data = true;
          msg_rotation.data = calculate_rotation(false);
        }
        break;
      }
      case 4: /// right and forward sign
      {
        /// block sign is forward?
        if (blocked) {
          msg_move.data = true;
          msg_rotation.data = calculate_rotation(true);
        }
        break;
      }
      case 5: /// block sign
      {
        msg_move.data = false;
        msg_rotation.data = 0;
        break;
      }
    }

    pub_move.publish(msg_move);
    pub_rotate.publish(msg_rotation);
  }

  ros::spin();

  return 0;
}
