drop table if exists candidates;
drop table if exists users;

create table users(
       id serial primary key,
       email text unique not null,
       voted boolean not null default false
);

create table candidates(
       id serial primary key,
       roll_number text unique not null,
       candidate_name text not null,
       post text not null,
       personal_caption text,
       DP_src text,
       votes int default 0
);