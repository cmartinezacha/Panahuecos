drop table if exists news;

create table news (
  id integer primary key autoincrement,
  type text not null,
  text text not null,
  time text,

);