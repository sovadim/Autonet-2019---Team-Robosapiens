; Auto-generated. Do not edit!


(cl:in-package vision_info_msg-msg)


;//! \htmlinclude vision_info_msg.msg.html

(cl:defclass <vision_info_msg> (roslisp-msg-protocol:ros-message)
  ((light
    :reader light
    :initarg :light
    :type cl:boolean
    :initform cl:nil)
   (sign
    :reader sign
    :initarg :sign
    :type cl:integer
    :initform 0)
   (blocked
    :reader blocked
    :initarg :blocked
    :type cl:boolean
    :initform cl:nil)
   (pos
    :reader pos
    :initarg :pos
    :type cl:integer
    :initform 0)
   (shift
    :reader shift
    :initarg :shift
    :type cl:integer
    :initform 0))
)

(cl:defclass vision_info_msg (<vision_info_msg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <vision_info_msg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'vision_info_msg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name vision_info_msg-msg:<vision_info_msg> is deprecated: use vision_info_msg-msg:vision_info_msg instead.")))

(cl:ensure-generic-function 'light-val :lambda-list '(m))
(cl:defmethod light-val ((m <vision_info_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader vision_info_msg-msg:light-val is deprecated.  Use vision_info_msg-msg:light instead.")
  (light m))

(cl:ensure-generic-function 'sign-val :lambda-list '(m))
(cl:defmethod sign-val ((m <vision_info_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader vision_info_msg-msg:sign-val is deprecated.  Use vision_info_msg-msg:sign instead.")
  (sign m))

(cl:ensure-generic-function 'blocked-val :lambda-list '(m))
(cl:defmethod blocked-val ((m <vision_info_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader vision_info_msg-msg:blocked-val is deprecated.  Use vision_info_msg-msg:blocked instead.")
  (blocked m))

(cl:ensure-generic-function 'pos-val :lambda-list '(m))
(cl:defmethod pos-val ((m <vision_info_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader vision_info_msg-msg:pos-val is deprecated.  Use vision_info_msg-msg:pos instead.")
  (pos m))

(cl:ensure-generic-function 'shift-val :lambda-list '(m))
(cl:defmethod shift-val ((m <vision_info_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader vision_info_msg-msg:shift-val is deprecated.  Use vision_info_msg-msg:shift instead.")
  (shift m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <vision_info_msg>) ostream)
  "Serializes a message object of type '<vision_info_msg>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'light) 1 0)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'sign)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'blocked) 1 0)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'pos)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'shift)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <vision_info_msg>) istream)
  "Deserializes a message object of type '<vision_info_msg>"
    (cl:setf (cl:slot-value msg 'light) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'sign) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:setf (cl:slot-value msg 'blocked) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'pos) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'shift) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<vision_info_msg>)))
  "Returns string type for a message object of type '<vision_info_msg>"
  "vision_info_msg/vision_info_msg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'vision_info_msg)))
  "Returns string type for a message object of type 'vision_info_msg"
  "vision_info_msg/vision_info_msg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<vision_info_msg>)))
  "Returns md5sum for a message object of type '<vision_info_msg>"
  "2e53e466b1aaabe8828aeec7ac1dc68b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'vision_info_msg)))
  "Returns md5sum for a message object of type 'vision_info_msg"
  "2e53e466b1aaabe8828aeec7ac1dc68b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<vision_info_msg>)))
  "Returns full string definition for message of type '<vision_info_msg>"
  (cl:format cl:nil "bool light~%int32 sign~%bool blocked~%int32 pos~%int32 shift~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'vision_info_msg)))
  "Returns full string definition for message of type 'vision_info_msg"
  (cl:format cl:nil "bool light~%int32 sign~%bool blocked~%int32 pos~%int32 shift~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <vision_info_msg>))
  (cl:+ 0
     1
     4
     1
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <vision_info_msg>))
  "Converts a ROS message object to a list"
  (cl:list 'vision_info_msg
    (cl:cons ':light (light msg))
    (cl:cons ':sign (sign msg))
    (cl:cons ':blocked (blocked msg))
    (cl:cons ':pos (pos msg))
    (cl:cons ':shift (shift msg))
))
