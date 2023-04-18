-- drop table if exists
drop table if exists users;
drop table if exists posts;

-- creates table
create table users (
    id integer primary key autoincrement,
    username text unique not null,
    password text not null
);

create table posts (
    id integer primary key autoincrement,
    user_id integer not null references users(id),
    create_ts timestamp not null default current_timestamp,
    title text not null,
    body text not null
);