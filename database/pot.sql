-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 04, 2024 at 11:57 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `pot`
--

-- --------------------------------------------------------

--
-- Table structure for table `post`
--

CREATE TABLE `post` (
  `id` int(50) NOT NULL,
  `product_type` varchar(20) NOT NULL,
  `product` varchar(20) NOT NULL,
  `message` varchar(100) NOT NULL,
  `price` varchar(30) NOT NULL,
  `name` varchar(30) NOT NULL,
  `address` varchar(100) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `post_date` varchar(20) NOT NULL,
  `post_time` varchar(20) NOT NULL,
  `username` varchar(20) NOT NULL,
  `post_id` int(10) NOT NULL,
  `latitude` varchar(30) NOT NULL,
  `longitude` varchar(30) NOT NULL,
  `quantity` int(10) NOT NULL,
  `image` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `post`
--

INSERT INTO `post` (`id`, `product_type`, `product`, `message`, `price`, `name`, `address`, `mobile`, `post_date`, `post_time`, `username`, `post_id`, `latitude`, `longitude`, `quantity`, `image`) VALUES
(1, 'Craft', 'Mud pot', 'Somthinig', '220', 'Porna crafts', '12, new str', 0, 'March 27, 2024', '12:03 PM', 'lo', 0, '76.953484', '11.036302', 120, 'image_7.jpg'),
(2, 'Craft', 'Mud statue', 'Something', '560', 'Porna crafts', '12, new str', 0, 'March 27, 2024', '12:52 PM', 'lo', 0, '76.953484', '11.036302', 20, 'download.jpg'),
(3, 'Craft', 'Mud class', 'Something', '250', 'Porna crafts', '12, new str', 0, 'March 27, 2024', '02:15 PM', 'lo', 0, '76.953484', '11.036302', 120, 'peakpx.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `po_admin`
--

CREATE TABLE `po_admin` (
  `id` int(11) NOT NULL,
  `username` varchar(11) NOT NULL,
  `password` varchar(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `po_admin`
--

INSERT INTO `po_admin` (`id`, `username`, `password`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `po_book`
--

CREATE TABLE `po_book` (
  `id` int(12) NOT NULL,
  `product` varchar(30) NOT NULL,
  `price` varchar(20) NOT NULL,
  `shop` varchar(30) NOT NULL,
  `contact` bigint(20) NOT NULL,
  `pro_username` varchar(20) NOT NULL,
  `name` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `reg_date` varchar(20) NOT NULL,
  `total` int(20) NOT NULL,
  `username` varchar(20) NOT NULL,
  `payment` varchar(20) NOT NULL,
  `status` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `po_book`
--

INSERT INTO `po_book` (`id`, `product`, `price`, `shop`, `contact`, `pro_username`, `name`, `mobile`, `email`, `reg_date`, `total`, `username`, `payment`, `status`) VALUES
(1, 'Mud pot', '220.0', 'Porna crafts', 0, 'lo', 'Raja', 0, 'exsample75@gmail.com', '2024-03-27', 440, 'ram', '', 2),
(2, 'Mud statue', '560.0', 'Porna crafts', 0, 'lo', 'Raja', 0, 'exsample75@gmail.com', '2024-03-27', 1120, 'ram', '', 1),
(3, 'Mud pot', '220.0', 'Porna crafts', 0, 'lo', 'Raja', 0, 'exsample75@gmail.com', '2024-03-27', 440, 'ram', '', 0),
(4, 'Mud pot', '220.0', 'Porna crafts', 0, 'lo', 'Raja', 0, 'exsample75@gmail.com', '2024-03-27', 1100, 'ram', '', 0),
(5, 'Mud class', '250.0', 'Porna crafts', 0, 'lo', 'Raja', 0, 'exsample75@gmail.com', '2024-03-27', 2500, 'ram', '', 0),
(6, 'Mud pot', '220.0', 'Porna crafts', 0, 'lo', 'Raja', 0, 'exsample75@gmail.com', '2024-03-27', 440, 'ram', '', 0),
(7, 'Mud statue', '560.0', 'Porna crafts', 0, 'lo', 'Raja', 0, 'exsample75@gmail.com', '2024-03-27', 1120, 'ram', '', 0),
(8, 'Mud statue', '560.0', 'Porna crafts', 0, 'lo', 'Raja', 0, 'exsample75@gmail.com', '2024-03-27', 2240, 'ram', '', 0),
(9, 'Mud statue', '560.0', 'Porna crafts', 0, 'lo', 'Raja', 0, 'exsample75@gmail.com', '2024-03-27', 1680, 'ram', '', 0),
(10, 'Mud pot', '220.0', 'Porna crafts', 0, 'lo', 'Raja', 0, 'exsample75@gmail.com', '2024-03-27', 1100, 'ram', '', 0),
(11, 'Mud pot', '220.0', 'Porna crafts', 0, 'lo', 'Raja', 0, 'exsample75@gmail.com', '2024-03-27', 440, 'ram', '', 0),
(12, 'Mud pot', '220.0', 'Porna crafts', 0, 'lo', 'Raja', 0, 'exsample75@gmail.com', '2024-03-27', 660, 'ram', '', 0),
(13, 'Mud pot', '220.0', 'Porna crafts', 0, 'lo', 'Raja', 0, 'exsample75@gmail.com', '2024-03-27', 440, 'ram', '', 0),
(14, 'Mud pot', '220.0', 'Porna crafts', 0, 'lo', 'Raja', 0, 'exsample75@gmail.com', '2024-03-27', 660, 'ram', '', 0),
(15, 'Mud statue', '560.0', 'Porna crafts', 0, 'lo', 'Raja', 0, 'exsample75@gmail.com', '2024-03-27', 1120, 'ram', 'COD', 0),
(16, 'Mud statue', '560.0', 'Porna crafts', 0, 'lo', 'Raja', 0, 'exsample75@gmail.com', '2024-03-27', 1120, 'ram', 'COD', 0),
(17, 'Mud pot', '220.0', 'Porna crafts', 0, 'lo', 'farzi', 8148956634, 'huwaidom@gmail.com', '2024-04-11', 440, 'far', 'COD', 0);

-- --------------------------------------------------------

--
-- Table structure for table `po_customer`
--

CREATE TABLE `po_customer` (
  `id` int(50) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(100) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `reg_date` date NOT NULL,
  `action` int(5) NOT NULL,
  `latitude` varchar(30) NOT NULL,
  `longitude` varchar(30) NOT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `po_customer`
--

INSERT INTO `po_customer` (`id`, `name`, `address`, `mobile`, `email`, `username`, `password`, `reg_date`, `action`, `latitude`, `longitude`) VALUES
(1, 'yuvan', '177, Chennai trunk road, Taluk, Srirangam, Thiruvanaikoil', 8148956634, 'huwaidom@gmail.com', 'yu', '1234', '2024-02-02', 1, '10.8155', '78.69651'),
(2, 'sankar', 'No.3354, Shivaram Nagar, Bikshandarkoil, Tamil Nadu', 9098675667, 'huwaidom@gmail.com', 'san', '1234', '2024-02-02', 1, '11.00599003', '77.56089783'),
(3, 'dany', '19, 34, Chandra Nagar St, Periyar Nagar, Tiruchirappalli', 9089675645, 'jai@gmail.com', 'dan', '1234', '2024-02-02', 1, '11.11540985', '77.35456085'),
(4, 'Madhan', 'RP2Q+XM2, Vivek Nagar, Pappakurichi Kattur, Tiruchirappalli', 8148956634, 'huwaidom@gmail.com', 'mad', '1234', '2024-02-02', 1, '11.07750988', '77.88362885'),
(5, 'Harsh', '4/15, Srinivasa Nagar N Ext, Srirangam, Thiruvanaikoil, Tiruchirappalli', 8148956634, 'huwaidom@gmail.com', 'harsh', '1234', '2024-02-08', 1, '10.79426003', '77.71150208'),
(6, 'Muthu', '28, Kuttiambalakaranpatti, Udayanpatti, K K Nagar, Tiruchirappalli', 9589859590, 'hs@gmail.com', 'muthu', '1234', '2024-02-03', 1, '11.10824966', '78.00112915'),
(7, 'the', 'No. 131, Ammamandapam Rd, Srirangam, Tiruchirappalli', 8148956634, 'huwaidom@gmail.com', 'the', '1234', '2024-02-15', 1, '10.73828030', '77.53222656'),
(8, 'run', '28, Kuttiambalakaranpatti, Udayanpatti, K K Nagar, Tiruchirappalli', 9589859590, 'hs@gmail.com', 'ro', '1234', '2024-02-03', 1, '10.95771027', '78.08094788'),
(9, 'was', '4/15, Srinivasa Nagar N Ext, Srirangam, Thiruvanaikoil, Tiruchirappalli', 8148956634, 'huwaidom@gmail.com', 'was', '1234', '2024-02-08', 1, '10.72056961', '77.87950897'),
(10, 'jack', '28, Kuttiambalakaranpatti, Udayanpatti, K K Nagar, Tiruchirappalli', 9589859590, 'hs1@gmail.com', 'jac', '1234', '2024-02-21', 1, '11.05935955', '78.13964844'),
(11, 'farzi', '4/15, Srinivasa Nagar N Ext, Srirangam, Thiruvanaikoil, Tiruchirappalli', 8148956634, 'huwaidom@gmail.com', 'far', '1234', '2024-02-24', 1, '11.15217018', '78.21205139'),
(12, 'io', '28, Kuttiambalakaranpatti, Udayanpatti, K K Nagar, Tiruchirappalli', 8148956634, 'huwaidom@gmail.com', 'io', '1234', '2024-02-24', 1, '11.14671040', '78.28996277'),
(13, 'david', 'Kela Mettu Street, Lakshmi Nagar, No 1 Tollgate, Tiruchirappalli', 8148956634, 'huwaidom@gmail.com', 'dav', '1234', '2024-02-08', 1, '10.45034027', '77.52089691'),
(14, 'little', 'No. 131, Ammamandapam Rd, Srirangam, Tiruchirappalli', 8148956634, 'huwaidom@gmail.com', 'dan', '1234', '2024-02-02', 1, '10.93486977', '78.41251373'),
(15, 'jan', '28, Kuttiambalakaranpatti, Udayanpatti, K K Nagar, Tiruchirappalli', 9589859587, 'iuu@gmail.com', 'pl', '1234', '2024-02-03', 1, '11.12417030', '78.44915771'),
(16, 'art', 'VPH7+F66, 1, Tollgate, Annai Nagar, No 1 Tollgate, Bikshandarkoil, Tiruchirappalli', 9087566778, 'kl@gmail.com', 'war', '1234', '2024-02-24', 1234, '10.60772038', '78.42581940'),
(17, 'pop', '136-2a/2b, Pudukottai Road, Gundur Village, Ramanathapuram Rd, Tiruchirappalli', 8977675690, 'haj@gmail.com', 'kop', '123', '2024-02-29', 1, '11.14968014', '78.59870148'),
(18, 'esaki', '4/15, Srinivasa Nagar N Ext, Srirangam, Thiruvanaikoil, Tiruchirappalli,', 6789095678, 'hgghs@gmail.com', 'uyef@gmail.com', '1234', '2024-02-14', 1, '10.53102016', '77.95018768'),
(19, 'Raja', '12, new str', 0, 'exsample75@gmail.com', 'ram', '1234', '2024-03-27', 0, '11.036302', '76.953484');

-- --------------------------------------------------------

--
-- Table structure for table `po_potter`
--

CREATE TABLE `po_potter` (
  `id` int(50) NOT NULL,
  `shop` varchar(40) NOT NULL,
  `name` varchar(20) NOT NULL,
  `address` varchar(100) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `reg_date` date NOT NULL,
  `action` int(5) NOT NULL,
  `latitude` varchar(30) NOT NULL,
  `longitude` varchar(30) NOT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `po_potter`
--

INSERT INTO `po_potter` (`id`, `shop`, `name`, `address`, `mobile`, `email`, `username`, `password`, `reg_date`, `action`, `latitude`, `longitude`) VALUES
(1, '', 'man', 'No. 131, Ammamandapam Rd, Srirangam, Tiruchirappalli', 8148956634, 'huwaidom@gmail.com', 'klj', '1234', '2024-02-24', 1, '10.8155 ', '78.69651'),
(2, '', 'geo', 'No.3354, Shivaram Nagar, Bikshandarkoil, Tamil Nadu', 8148956634, 'hj@gmail.com', 'geo', '1234', '2024-02-26', 1, '11.00599003', '77.56089783'),
(3, '', 'nani', '4/15, Srinivasa Nagar N Ext, Srirangam, Thiruvanaikoil, Tiruchirappalli', 8148956634, 'huwaidom@gmail.com', 'nani', '1234', '2024-02-24', 1, '10.72056961', '77.87950897'),
(4, '', 'ttt', '28, Kuttiambalakaranpatti, Udayanpatti, K K Nagar, Tiruchirappalli', 8148956634, 'huwaidom@gmail.com', 'huyyt', '1234', '2024-02-24', 1, '10.60772038', '78.42581940'),
(5, '', 'ioioi', 'No.3354, Shivaram Nagar, Bikshandarkoil, Tamil Nadu', 8148956634, 'yyjt@gmail.com', 'yy', '1234', '2024-02-24', 1, '10.10501003', '78.11335754'),
(1, 'Porna crafts', 'ca na ra', '12, new str', 0, 'huwaidom@gmail.com', 'lo', '1234', '2024-03-27', 0, '11.036302', '76.953484');

-- --------------------------------------------------------

--
-- Table structure for table `request`
--

CREATE TABLE `request` (
  `id` int(11) NOT NULL,
  `product` varchar(30) NOT NULL,
  `price` varchar(20) NOT NULL,
  `shop` varchar(40) NOT NULL,
  `contact` bigint(20) NOT NULL,
  `pot_username` varchar(20) NOT NULL,
  `name` varchar(30) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `username` varchar(20) NOT NULL,
  `req_date` varchar(20) NOT NULL,
  `link` varchar(20) NOT NULL,
  `date` varchar(20) NOT NULL,
  `time` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `request`
--

INSERT INTO `request` (`id`, `product`, `price`, `shop`, `contact`, `pot_username`, `name`, `mobile`, `username`, `req_date`, `link`, `date`, `time`) VALUES
(1, 'Mud pot', '220', 'Porna crafts', 0, 'lo', 'Raja', 0, 'ram', 'March 27, 2024', '12', '2024-03-29', '18:33'),
(2, 'Mud pot', '220', 'Porna crafts', 0, 'lo', 'Raja', 0, 'ram', 'March 27, 2024', '123', '2024-03-13', '19:27'),
(3, 'Mud statue', '560', 'Porna crafts', 0, 'lo', 'Raja', 0, 'ram', 'March 27, 2024', '', '', '');
