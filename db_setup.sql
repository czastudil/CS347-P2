DROP DATABASE IF EXISTS ta;
DROP USER IF EXISTS ta_user;

CREATE USER ta_user PASSWORD 'password';
CREATE DATABASE ta OWNER ta_user;
