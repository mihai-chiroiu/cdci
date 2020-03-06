drop user if exists 'vulnUser'@'localhost';
create user 'vulnUser'@'localhost' IDENTIFIED BY 'vulnPassword';
create database if not exists vulnSensors;
grant all privileges on vulnSensors.* TO 'vulnUser'@'localhost';
use vulnSensors;
drop table if exists sensors;
create table sensors(id int not null auto_increment, name varchar(100), temperature int, primary key (id));
