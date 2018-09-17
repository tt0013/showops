/*
Navicat MySQL Data Transfer

Source Server         : showops
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Records of itom_group
-- ----------------------------
INSERT INTO `itom_group` VALUES ('1', '管理员', '1', '管理员组');
INSERT INTO `itom_group` VALUES ('2', '测试', '1', '测试组');
INSERT INTO `itom_group` VALUES ('3', '操作员', '1', '操作专用组');

-- ----------------------------
-- Records of itom_group_menu
-- ----------------------------
INSERT INTO `itom_group_menu` VALUES ('8', '1', '1');
INSERT INTO `itom_group_menu` VALUES ('9', '1', '2');
INSERT INTO `itom_group_menu` VALUES ('10', '1', '3');
INSERT INTO `itom_group_menu` VALUES ('11', '1', '4');
INSERT INTO `itom_group_menu` VALUES ('12', '1', '5');
INSERT INTO `itom_group_menu` VALUES ('13', '1', '6');
INSERT INTO `itom_group_menu` VALUES ('24', '2', '1');
INSERT INTO `itom_group_menu` VALUES ('14', '3', '1');
INSERT INTO `itom_group_menu` VALUES ('15', '3', '2');
INSERT INTO `itom_group_menu` VALUES ('16', '3', '3');
INSERT INTO `itom_group_menu` VALUES ('17', '3', '4');

-- ----------------------------
-- Records of itom_menu
-- ----------------------------
INSERT INTO `itom_menu` VALUES ('1', '欢迎页', '0', '/itom/home/', '0', '0', '0', 'layui-icon-home', '0');
INSERT INTO `itom_menu` VALUES ('2', '系统设置', '0', '', '0', '0', '0', 'layui-icon-set-fill', '0');
INSERT INTO `itom_menu` VALUES ('3', '菜单管理', '2', '/itom/menu/', '0', '0', '0', '', '0');
INSERT INTO `itom_menu` VALUES ('4', '用户管理', '2', '/itom/user/', '0', '1', '0', '', '0');
INSERT INTO `itom_menu` VALUES ('5', '部门管理', '2', '/itom/org/', '0', '2', '0', '', '0');
INSERT INTO `itom_menu` VALUES ('6', '角色管理', '2', '/itom/group/', '0', '3', '0', '', '0');

-- ----------------------------
-- Records of itom_org
-- ----------------------------
INSERT INTO `itom_org` VALUES ('1', '运维', '运维部门');
INSERT INTO `itom_org` VALUES ('2', '测试', '测试部门');
INSERT INTO `itom_org` VALUES ('3', '研发', '研发部门');

-- ----------------------------
-- Records of itom_user
-- ----------------------------
INSERT INTO `itom_user` VALUES ('1', 'admin', '超级管理员', 'e10adc3949ba59abbe56e057f20f883e', 'lijie@sinashow.com', '2018-08-30 15:25:05.717987', '127.0.0.1', '2018-08-30 18:04:40.741647', '1', '1');

