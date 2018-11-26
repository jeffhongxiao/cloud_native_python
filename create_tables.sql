
---- apirelease ----
CREATE TABLE apirelease(
    buildtime date,
    version varchar(30) primary key,
    links varchar2(30),
    methods varchar2(30)
);

INSERT INTO apirelease values(
    "2017-01-01 10:00:00",
    "v1",
    "/api/v1/users/",
    "get, post, put, delete"
);


---- users ----
CREATE TABLE users(
    username varchar2(30),
    email varchar2(30),
    password varchar2(30),
    full_name varchar(30),
    id integer primary key autoincrement
);

INSERT INTO users values(
    'hong',
    'hong@example.com',
    '123456',
    'Hong Xiao',
    1
)
