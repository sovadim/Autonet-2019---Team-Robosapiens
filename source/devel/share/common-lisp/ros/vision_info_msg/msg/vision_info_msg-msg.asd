
(cl:in-package :asdf)

(defsystem "vision_info_msg-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "vision_info_msg" :depends-on ("_package_vision_info_msg"))
    (:file "_package_vision_info_msg" :depends-on ("_package"))
  ))