user_control = """CREATE TABLE `auto_test`.`Untitled`  (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(31) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_active` int(2) NOT NULL DEFAULT 0,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`user_id`)
);"""