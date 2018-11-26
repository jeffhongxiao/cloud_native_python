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
