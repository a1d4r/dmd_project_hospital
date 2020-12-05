SET FOREIGN_KEY_CHECKS = 0;
SET GROUP_CONCAT_MAX_LEN=32768;
SET @tables = NULL;
SELECT GROUP_CONCAT('`', table_name, '`') INTO @tables
  FROM information_schema.tables
  WHERE table_schema = (SELECT DATABASE());
SELECT IFNULL(@tables,'dummy') INTO @tables;

SET @tables = CONCAT('DROP TABLE IF EXISTS ', @tables);
PREPARE stmt FROM @tables;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
SET FOREIGN_KEY_CHECKS = 1;
SET SQL_MODE='ALLOW_INVALID_DATES';

CREATE TABLE person
(
    person_id     SERIAL PRIMARY KEY,
    ssn           char(11),
    address       varchar(100),
    name          varchar(20) NOT NULL,
    surname       varchar(20) NOT NULL,
    date_of_birth date        NOT NULL,
    sex           varchar(1)  NOT NULL
);

CREATE TABLE accountant
(
    person_id int REFERENCES person(person_id),
    length_of_service int,
    salary            int NOT NULL,
    PRIMARY KEY (person_id)
);

CREATE TABLE storekeeper
(
    person_id int REFERENCES person(person_id),
    length_of_service int,
    salary            int NOT NULL,
    PRIMARY KEY (person_id)
);

CREATE TABLE receptionist
(
    person_id int REFERENCES person(person_id),
    length_of_service int,
    salary            int NOT NULL,
    PRIMARY KEY (person_id)
);

CREATE TABLE doctor
(
    person_id int REFERENCES person(person_id),
    length_of_service int,
    salary            int NOT NULL,
    PRIMARY KEY (person_id)
);

CREATE TABLE nurse
(
    person_id int REFERENCES person(person_id),
    length_of_service int,
    salary            int NOT NULL,
    PRIMARY KEY (person_id)
);

CREATE TABLE patient
(
    person_id int REFERENCES person(person_id),
    PRIMARY KEY (person_id)
);

CREATE TABLE doctor_qualifications
(
    descrip  varchar(255) NOT NULL,
    person_id int REFERENCES doctor(person_id),
    PRIMARY KEY (person_id, descrip)
);

CREATE TABLE nurse_qualifications
(
    descrip  varchar(255) NOT NULL,
    person_id int REFERENCES nurse(person_id),
    PRIMARY KEY (person_id, descrip)
);

CREATE TABLE medicine
(
    medicine_id SERIAL PRIMARY KEY,
    price       int         NOT NULL,
    name        varchar(50) NOT NULL,
    description varchar(100)
);

CREATE TABLE appointment
(
    app_id     SERIAL PRIMARY KEY,
    app_time   datetime   NOT NULL,
    room       varchar(50) NOT NULL,
    patient_id int REFERENCES patient (person_id),
    doctor_id  int REFERENCES doctor (person_id),
    nurse_id   int REFERENCES nurse (person_id),
    rec_id     int REFERENCES receptionist (person_id)
);

CREATE TABLE service
(
    service_id  SERIAL PRIMARY KEY,
    name        varchar(20) NOT NULL,
    description varchar(100),
    price       int         NOT NULL
);

CREATE TABLE `order`
(
    order_id SERIAL PRIMARY KEY,
    doc_id   int REFERENCES doctor (person_id)
);

CREATE TABLE invoice
(
    patient_id       int REFERENCES patient (person_id),
    invoice_date     datetime NOT NULL,
    payment_due_date datetime NOT NULL,
    tax_amount       int       NOT NULL,
    total_amount     int       NOT NULL,
    inv_id           int REFERENCES `order` (order_id),
    PRIMARY KEY (inv_id)
);

CREATE TABLE medical_chart
(
    start_date date NOT NULL,
    chart_id   int REFERENCES patient (person_id),
    PRIMARY KEY (chart_id)
);

CREATE TABLE report
(
    create_time             datetime NOT NULL,
    results_of_consultation text      NOT NULL,
    report_id               SERIAL PRIMARY KEY,
    chart_id                int REFERENCES medical_chart (chart_id),
    doctor_id               int REFERENCES doctor (person_id),
    nurse_id                int REFERENCES nurse (person_id)
);

CREATE TABLE mail
(
    msg_id     SERIAL PRIMARY KEY,
    subject    varchar(100),
    message    varchar(500) NOT NULL,
    write_time time         NOT NULL,
    sender     int REFERENCES person (person_id),
    reciever   int REFERENCES person (person_id)
);

CREATE TABLE order_medicine
(
    ord_med_id SERIAL PRIMARY KEY,
    order_id   int REFERENCES `order` (order_id),
    medicine   int REFERENCES medicine (medicine_id)
);

CREATE TABLE order_service
(
    ord_ser_id SERIAL PRIMARY KEY,
    order_id   int REFERENCES `order` (order_id),
    service    int REFERENCES service (service_id)
);

CREATE TABLE manage_invoice
(
    man_inv_id SERIAL PRIMARY KEY,
    acc_id     int REFERENCES accountant (person_id),
    inv_id     int REFERENCES invoice (inv_id)
);

CREATE TABLE complete_order
(
    com_ord_id SERIAL PRIMARY KEY,
    order_id   int REFERENCES `order` (order_id),
    stk_id     int REFERENCES storekeeper (person_id)
);

CREATE TABLE request_medicine
(
    req_med_id  SERIAL PRIMARY KEY,
    doctor_id   int REFERENCES doctor (person_id),
    nurse_id    int REFERENCES nurse (person_id),
    medicine_id int REFERENCES medicine (medicine_id)
);

CREATE TABLE nurse_assigned
(
    nurse_doctor_id SERIAL PRIMARY KEY,
    doc_id          int REFERENCES doctor (person_id),
    nurse_id        int REFERENCES nurse (person_id)
);

CREATE TABLE provide_service
(
    prov_serv_id SERIAL PRIMARY KEY,
    doctor_id       int REFERENCES doctor (person_id),
    nurse_id        int REFERENCES nurse (person_id),
    ser_id          int REFERENCES service (service_id)
);
