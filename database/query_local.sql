-- USE ai_gp3_vnpt_db; 
-- CREATE TABLE `taskmanager` (
-- `ID` int(11) unsigned NOT NULL AUTO_INCREMENT,
-- `TASK_ID` varchar(255) DEFAULT NULL,
-- `TASK_NAME` text DEFAULT NULL,
-- `STREAM_ID` varchar(255) DEFAULT NULL,
-- `DATECREATED` datetime DEFAULT NULL,
-- `DATEUPDATE` datetime DEFAULT NULL,
-- `USER_ID` int(11) unsigned DEFAULT NULL,
-- `THREAD_ID` int(11) unsigned DEFAULT NULL,
-- `STATUS` int(1) unsigned DEFAULT NULL,
-- `SETTING` text DEFAULT NULL,
-- `DV_ID` int(11) unsigned DEFAULT NULL,
-- PRIMARY KEY (`ID`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- 
-- CREATE TABLE `unitmanager` (
-- `ID` int(11) unsigned NOT NULL AUTO_INCREMENT,
-- `UNIT_ID` varchar(255) DEFAULT NULL,
-- `UNIT_NAME` text DEFAULT NULL,
-- `DATECREATED` datetime DEFAULT NULL,
-- `DATEUPDATE` datetime DEFAULT NULL,
-- `STATUS` int(1) unsigned DEFAULT NULL,
-- PRIMARY KEY (`ID`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- 
-- CREATE TABLE `streammanager` (
-- `ID` int(11) unsigned NOT NULL AUTO_INCREMENT,
-- `STREAM_ID` varchar(255) DEFAULT NULL,
-- `STREAM_NAME` text DEFAULT NULL,
-- `STREAM_URL` varchar(255) DEFAULT NULL,
-- `DATECREATED` datetime DEFAULT NULL,
-- `DATEUPDATE` datetime DEFAULT NULL,
-- `THREAD_ID` int(11) unsigned DEFAULT NULL,
-- `STATUS` int(1) unsigned DEFAULT NULL,
-- `SETTING` text DEFAULT NULL,
-- `DV_ID` int(11) unsigned DEFAULT NULL,
-- PRIMARY KEY (`ID`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- 
-- CREATE TABLE `data_people` (
-- `DP_ID` int(11) unsigned NOT NULL AUTO_INCREMENT,
-- `DP_NAME` text DEFAULT NULL,
-- `DP_CB_URL` varchar(255) DEFAULT NULL,
-- `DP_IMAGE_ENCODING` text DEFAULT NULL,
-- `DP_IMAGE_FACE` longtext DEFAULT NULL,
-- `DATECREATED` datetime DEFAULT NULL,
-- `DATEUPDATE` datetime DEFAULT NULL,
-- `DP_ALARM` int(1) unsigned DEFAULT NULL,
-- `STATUS` int(1) unsigned DEFAULT NULL,
-- `DV_ID` int(11) unsigned DEFAULT NULL,
-- PRIMARY KEY (`DP_ID`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- 
-- CREATE TABLE `camera_people` (
-- `ID` int(11) unsigned NOT NULL AUTO_INCREMENT,
-- `STREAM_ID` varchar(255) DEFAULT NULL,
-- `FACES` longtext DEFAULT NULL,
-- `IMAGE` longtext DEFAULT NULL,
-- `FACE_RECTANGLE` text DEFAULT NULL,
-- `AMOUNT_OF_PEOPLE` int(11) unsigned DEFAULT NULL,
-- `NUMBER_OF_IDENTIFYERS` int(11) unsigned DEFAULT NULL,
-- `GENDER` text DEFAULT NULL,
-- `AGE` text DEFAULT NULL,
-- `MASK` text DEFAULT NULL,
-- `CREATEAT` datetime DEFAULT NULL,
-- `CREATEAT_TICKS` datetime DEFAULT NULL,
-- `UPDATEAT` datetime DEFAULT NULL,
-- `STATUS` int(1) unsigned DEFAULT NULL,
-- PRIMARY KEY (`ID`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

select * from camera_people
