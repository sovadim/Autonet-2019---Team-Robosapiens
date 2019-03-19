;; Auto-generated. Do not edit!


(when (boundp 'vision_info_msg::vision_info_msg)
  (if (not (find-package "VISION_INFO_MSG"))
    (make-package "VISION_INFO_MSG"))
  (shadow 'vision_info_msg (find-package "VISION_INFO_MSG")))
(unless (find-package "VISION_INFO_MSG::VISION_INFO_MSG")
  (make-package "VISION_INFO_MSG::VISION_INFO_MSG"))

(in-package "ROS")
;;//! \htmlinclude vision_info_msg.msg.html


(defclass vision_info_msg::vision_info_msg
  :super ros::object
  :slots (_light _sign _blocked _pos _shift ))

(defmethod vision_info_msg::vision_info_msg
  (:init
   (&key
    ((:light __light) nil)
    ((:sign __sign) 0)
    ((:blocked __blocked) nil)
    ((:pos __pos) 0)
    ((:shift __shift) 0)
    )
   (send-super :init)
   (setq _light __light)
   (setq _sign (round __sign))
   (setq _blocked __blocked)
   (setq _pos (round __pos))
   (setq _shift (round __shift))
   self)
  (:light
   (&optional __light)
   (if __light (setq _light __light)) _light)
  (:sign
   (&optional __sign)
   (if __sign (setq _sign __sign)) _sign)
  (:blocked
   (&optional __blocked)
   (if __blocked (setq _blocked __blocked)) _blocked)
  (:pos
   (&optional __pos)
   (if __pos (setq _pos __pos)) _pos)
  (:shift
   (&optional __shift)
   (if __shift (setq _shift __shift)) _shift)
  (:serialization-length
   ()
   (+
    ;; bool _light
    1
    ;; int32 _sign
    4
    ;; bool _blocked
    1
    ;; int32 _pos
    4
    ;; int32 _shift
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _light
       (if _light (write-byte -1 s) (write-byte 0 s))
     ;; int32 _sign
       (write-long _sign s)
     ;; bool _blocked
       (if _blocked (write-byte -1 s) (write-byte 0 s))
     ;; int32 _pos
       (write-long _pos s)
     ;; int32 _shift
       (write-long _shift s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _light
     (setq _light (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; int32 _sign
     (setq _sign (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; bool _blocked
     (setq _blocked (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; int32 _pos
     (setq _pos (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _shift
     (setq _shift (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get vision_info_msg::vision_info_msg :md5sum-) "2e53e466b1aaabe8828aeec7ac1dc68b")
(setf (get vision_info_msg::vision_info_msg :datatype-) "vision_info_msg/vision_info_msg")
(setf (get vision_info_msg::vision_info_msg :definition-)
      "bool light
int32 sign
bool blocked
int32 pos
int32 shift

")



(provide :vision_info_msg/vision_info_msg "2e53e466b1aaabe8828aeec7ac1dc68b")


