// Auto-generated. Do not edit!

// (in-package vision_info_msg.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class vision_info_msg {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.light = null;
      this.sign = null;
      this.blocked = null;
      this.pos = null;
      this.shift = null;
    }
    else {
      if (initObj.hasOwnProperty('light')) {
        this.light = initObj.light
      }
      else {
        this.light = false;
      }
      if (initObj.hasOwnProperty('sign')) {
        this.sign = initObj.sign
      }
      else {
        this.sign = 0;
      }
      if (initObj.hasOwnProperty('blocked')) {
        this.blocked = initObj.blocked
      }
      else {
        this.blocked = false;
      }
      if (initObj.hasOwnProperty('pos')) {
        this.pos = initObj.pos
      }
      else {
        this.pos = 0;
      }
      if (initObj.hasOwnProperty('shift')) {
        this.shift = initObj.shift
      }
      else {
        this.shift = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type vision_info_msg
    // Serialize message field [light]
    bufferOffset = _serializer.bool(obj.light, buffer, bufferOffset);
    // Serialize message field [sign]
    bufferOffset = _serializer.int32(obj.sign, buffer, bufferOffset);
    // Serialize message field [blocked]
    bufferOffset = _serializer.bool(obj.blocked, buffer, bufferOffset);
    // Serialize message field [pos]
    bufferOffset = _serializer.int32(obj.pos, buffer, bufferOffset);
    // Serialize message field [shift]
    bufferOffset = _serializer.int32(obj.shift, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type vision_info_msg
    let len;
    let data = new vision_info_msg(null);
    // Deserialize message field [light]
    data.light = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [sign]
    data.sign = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [blocked]
    data.blocked = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [pos]
    data.pos = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [shift]
    data.shift = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 14;
  }

  static datatype() {
    // Returns string type for a message object
    return 'vision_info_msg/vision_info_msg';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '2e53e466b1aaabe8828aeec7ac1dc68b';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool light
    int32 sign
    bool blocked
    int32 pos
    int32 shift
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new vision_info_msg(null);
    if (msg.light !== undefined) {
      resolved.light = msg.light;
    }
    else {
      resolved.light = false
    }

    if (msg.sign !== undefined) {
      resolved.sign = msg.sign;
    }
    else {
      resolved.sign = 0
    }

    if (msg.blocked !== undefined) {
      resolved.blocked = msg.blocked;
    }
    else {
      resolved.blocked = false
    }

    if (msg.pos !== undefined) {
      resolved.pos = msg.pos;
    }
    else {
      resolved.pos = 0
    }

    if (msg.shift !== undefined) {
      resolved.shift = msg.shift;
    }
    else {
      resolved.shift = 0
    }

    return resolved;
    }
};

module.exports = vision_info_msg;
