create table if not exists users (
    username text primary key,
    event_type text,
    flags int,
    tsadded datetime default current_timestamp,
    tsmodified datetime default current_timestamp
);

create table if not exists user_records (
    username text,
    event_type text,
    won int,
    lost int,
    played int,
    pct float,
    tsadded datetime default current_timestamp,
    unique (username, event_type, tsadded)
);

create table if not exists twitters (
    username text,
    twitter_id text,
    twitter_name text,   
    tsadded datetime default current_timestamp,
    tsmodified datetime default current_timestamp,
    unique (username, twitter_id) 
);

create table if not exists twitter_mentions (
    mention_id text primary key,
    twitter_id text,
    twitter_name text,
    mention text,
    tsadded datetime default current_timestamp
);

create table if not exists twitter_commands (
    mention_id text primary key,
    username text,
    command text,
    tsadded datetime default current_timestamp
);

create table if not exists events (
    event_id int primary key,
    event_type text,
    name text,
    host text,
    url text,
    time_open text,
    time_close text,
    event_theme text,
    event_rounds text,
    tsadded datetime default current_timestamp
);

create table if not exists event_users (
    event_id int,
    username text,
    won int,
    event_ts datetime,
    record_ts datetime,
    tsadded datetime default current_timestamp,
    unique (event_id, username)
);   
    
