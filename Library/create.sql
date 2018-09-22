create database library;
use library;
create table member(
	name varchar(20) not null,
	realname varchar(20) not null,
	password varchar(20),
	level varchar(20),
	email varchar(100),
	readbook int,
	donatebool int,
	primary key(name)
);
create table book(
	isbn varchar(20),
	name varchar(20),
	
);