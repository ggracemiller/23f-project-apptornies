SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `lhub`;
CREATE SCHEMA IF NOT EXISTS `LHUB` DEFAULT CHARACTER SET latin1 ;
USE `LHUB` ;


CREATE TABLE IF NOT EXISTS `LHUB`.`employee` (
   employee_id INTEGER PRIMARY KEY AUTO_INCREMENT,
   street VARCHAR(50),
   city VARCHAR(50),
   state VARCHAR(2),
   zip VARCHAR(13),
   hourly_rate INTEGER UNSIGNED,
   last_name VARCHAR(256) NOT NULL,
   first_name VARCHAR(256) NOT NULL,
   employee_type VARCHAR(256) NOT NULL,
   phone_number CHAR(12) NOT NULL,
   email VARCHAR(50) NOT NULL,
   gender VARCHAR(50),
   birthdate DATE
);

CREATE TABLE IF NOT EXISTS `LHUB`.`client` (
   client_id INTEGER PRIMARY KEY AUTO_INCREMENT,
   street VARCHAR(50),
   city VARCHAR(50),
   state VARCHAR(2),
   zip VARCHAR(10),
   last_name VARCHAR(256) NOT NULL,
   first_name VARCHAR(256) NOT NULL,
   email VARCHAR(50) NOT NULL,
   phone_number CHAR(12) NOT NULL
);

CREATE TABLE IF NOT EXISTS `LHUB`.`client_case` (
   case_id INTEGER PRIMARY KEY AUTO_INCREMENT,
   start_date DATE NOT NULL,
   close_date DATE,
   client_id INTEGER NOT NULL,
   FOREIGN KEY (client_id) REFERENCES client(client_id)
);

CREATE TABLE IF NOT EXISTS `LHUB`.`case_file` (
   case_file_id INTEGER PRIMARY KEY AUTO_INCREMENT,
   case_id INTEGER NOT NULL,
   employee_id INTEGER NOT NULL,
   file VARCHAR(50),
   FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
   FOREIGN KEY (case_id) REFERENCES client_case(case_id)
);

CREATE TABLE IF NOT EXISTS `LHUB`.`billing_statement` (
   statement_id INTEGER PRIMARY KEY AUTO_INCREMENT,
   employee_id INTEGER NOT NULL,
   case_id INTEGER NOT NULL,
   communication_type VARCHAR(50) NOT NULL,
   number_of_hours DECIMAL(4,2) UNSIGNED NOT NULL,
   FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
   FOREIGN KEY (case_id) REFERENCES client_case(case_id)
);

CREATE TABLE IF NOT EXISTS `LHUB`.`employee_billing` (
   statement_id INTEGER,
   employee_id INTEGER,
   PRIMARY KEY(statement_id, employee_id),
   FOREIGN KEY (statement_id) REFERENCES billing_statement(statement_id),
   FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

CREATE TABLE IF NOT EXISTS `LHUB`.`events` (
   event_id INTEGER PRIMARY KEY AUTO_INCREMENT,
   description VARCHAR(2048) NOT NULL,
   location VARCHAR(1048),
   date_time DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS `LHUB`.`employee_event` (
   event_id INTEGER,
   employee_id INTEGER,
   PRIMARY KEY(event_id, employee_id),
   FOREIGN KEY (event_id) REFERENCES events(event_id),
   FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

CREATE TABLE IF NOT EXISTS `LHUB`.`client_event` (
   event_id INTEGER,
   client_id INTEGER,
   PRIMARY KEY(event_id, client_id),
   FOREIGN KEY (event_id) REFERENCES events(event_id),
   FOREIGN KEY (client_id) REFERENCES client(client_id)
);

CREATE TABLE IF NOT EXISTS `LHUB`.`employee_client` (
   employee_id INTEGER,
   client_id INTEGER,
   PRIMARY KEY(employee_id, client_id),
   FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
   FOREIGN KEY (client_id) REFERENCES client(client_id)
);