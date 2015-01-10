CREATE TABLE IF NOT EXISTS  `logs`(
	`id` int(11) NOT NULL auto_increment,
	`method` varchar(255) NOT NULL default 'GET',
	`status_code` varchar(255) NOT NULL default '200',
	`useragent` varchar(255),
	`filename` varchar(255),
	`rule` varchar(255),
	`url` text,
	`uri` text,
	`raw_data` MEDIUMBLOB,
	PRIMARY KEY  (`id`)
)ENGINE=MyISAM DEFAULT CHARACTER SET utf8