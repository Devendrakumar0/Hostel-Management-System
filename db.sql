/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.4.28-MariaDB : Database - hostel
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`hostel` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;

USE `hostel`;

/*Table structure for table `allocations` */

DROP TABLE IF EXISTS `allocations`;

CREATE TABLE `allocations` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `Rollno` varchar(200) DEFAULT NULL,
  `studentname` varchar(200) DEFAULT NULL,
  `studentemail` varchar(200) DEFAULT NULL,
  `Year` varchar(200) DEFAULT NULL,
  `branch` varchar(200) DEFAULT NULL,
  `roomnumber` varchar(200) DEFAULT NULL,
  `blockname` varchar(200) DEFAULT NULL,
  `wordenname` varchar(200) DEFAULT NULL,
  `room_type` varchar(200) DEFAULT NULL,
  `hostel_type` varchar(200) DEFAULT NULL,
  `course` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `allocations` */
/*Table structure for table `blocks` */

DROP TABLE IF EXISTS `blocks`;

CREATE TABLE `blocks` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `hostel_type` varchar(200) DEFAULT NULL,
  `roomnumber` varchar(200) DEFAULT NULL,
  `blockname` varchar(200) DEFAULT NULL,
  `wordenname` varchar(200) DEFAULT NULL,
  `wordernumber` varchar(200) DEFAULT NULL,
  `wordenemail` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;


/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `email` varchar(200) DEFAULT NULL,
  `feedback` varchar(200) DEFAULT NULL,
  `reason` varchar(200) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Time` time DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `feedback` */

DROP TABLE IF EXISTS `complaints`;

CREATE TABLE `complaints` (
  `complaint_id` int(20) NOT NULL AUTO_INCREMENT,
  `email` varchar(200) DEFAULT NULL,
  `complaint` varchar(200) DEFAULT NULL,
  `roomnumber` varchar(200) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `image` varchar(200) DEFAULT NULL,
  `action_taken` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`complaint_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Table structure for table `foodtypes` */

DROP TABLE IF EXISTS `foodtypes`;

CREATE TABLE `foodtypes` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `Foodid` varchar(200) DEFAULT NULL,
  `FoodType` varchar(200) DEFAULT NULL,
  `Foodname` varchar(200) DEFAULT NULL,
  `AboutFood` varchar(200) DEFAULT NULL,
  `FoodImage` varchar(200) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `ingredients` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT 'pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `foodtypes` */


/*Table structure for table `outpass` */

DROP TABLE IF EXISTS `outpass`;

CREATE TABLE `outpass` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `studentemail` varchar(200) DEFAULT NULL,
  `outdate` varchar(200) DEFAULT NULL,
  `outtime` varchar(200) DEFAULT NULL,
  `reason` varchar(200) DEFAULT NULL,
  `pcontact` varchar(200) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `status` varchar(200) DEFAULT 'pending',
  `destination` varchar(200) DEFAULT NULL,
  `roomnumber` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `outpass` */

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `Rollno` varchar(200) DEFAULT NULL,
  `studentname` varchar(200) DEFAULT NULL,
  `stuemail` varchar(200) DEFAULT NULL,
  `totalamount` varchar(200) DEFAULT NULL,
  `Cardname` varchar(200) DEFAULT NULL,
  `Cardnumber` varchar(200) DEFAULT NULL,
  `expmonth` varchar(200) DEFAULT NULL,
  `cvv` varchar(200) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `hostelfee` varchar(200) DEFAULT NULL,
  `currentbill` varchar(200) DEFAULT NULL,
  status varchar(200) default 'pending';
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `payment` */

/*Table structure for table `paypayment` */

DROP TABLE IF EXISTS `paypayment`;

CREATE TABLE `paypayment` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `Rollno` varchar(200) DEFAULT NULL,
  `studentname` varchar(200) DEFAULT NULL,
  `studentemail` varchar(200) DEFAULT NULL,
  `hostelfee` varchar(200) DEFAULT NULL,
  `currentbill` varchar(200) DEFAULT NULL,
  `total_amount` varchar(200) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  status varchar(200) default 'pending';
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

DROP TABLE IF EXISTS `events`;

CREATE TABLE `events` (
  `event_id` int(20) NOT NULL AUTO_INCREMENT,
  `eventname` varchar(200) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*Data for the table `paypayment` */

/*Table structure for table `students` */

DROP TABLE IF EXISTS `students`;

CREATE TABLE `students` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `studentname` varchar(200) DEFAULT NULL,
  `studentemail` varchar(200) DEFAULT NULL,
  `Rollno` varchar(200) DEFAULT NULL,
  `year` varchar(200) DEFAULT NULL,
  `sem` varchar(200) DEFAULT NULL,
  `branch` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `contact` varchar(200) DEFAULT NULL,
  `pcontact` varchar(200) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `wifiname` varchar(200) DEFAULT NULL,
  `wifipassword` varchar(200) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `profile` varchar(200) DEFAULT NULL,
  `profilename` varchar(200) DEFAULT NULL,
  `room_type` varchar(200) DEFAULT NULL,
  `hostel_type` varchar(200) DEFAULT NULL,
  `reset_token` varchar(200) DEFAULT NULL,
  `course` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `students` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
