create database if not exists Files;
use Files;
drop table if exists FilePath;
create table if not exists FilePath(id int auto_increment, table_file varchar(300), operation varchar(100), start_idx int default -1, end_idx int default -1, primary key (id));
select * from FilePath;
