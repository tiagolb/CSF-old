-- Activate foreign keys for the constraints
PRAGMA foreign_keys = ON;

-- Create table CASE
-- represents forensic case
CREATE TABLE FCASE(
   NAME          TEXT        NOT NULL,
   DESCRIPTION   DATE        NOT NULL,
   PRIMARY KEY (NAME)
);

-- Create table IMAGE
-- represents the dump examined
CREATE TABLE IMAGE(
   DUMP_HASH         BINARY(32)  NOT NULL,
   CASE_NAME         TEXT        NOT NULL,
   DESCRIPTION       TEXT        NOT NULL,
   AQUISITION_DATE   DATE        NOT NULL,
   DUMP_LOCATION     TEXT        NOT NULL,
   FOREIGN KEY (CASE_NAME) REFERENCES FCASE(NAME),
   PRIMARY KEY (DUMP_HASH)
);

-- Create table MODULE
-- represents the modules detected in a case
CREATE TABLE MODULE(
   NAME  TEXT  NOT NULL,
   PRIMARY KEY (NAME)
);

-- Create table PERSON
-- represents all communicators
CREATE TABLE PERSON(
   NAME        TEXT  NOT NULL,
   CASE_NAME   TEXT NOT NULL,
   LINK        TEXT,
   FOREIGN KEY (CASE_NAME) REFERENCES FCASE(NAME),
   PRIMARY KEY (NAME)
);

-- Create table MESSAGE
-- represents the data extracted from the analysis
CREATE TABLE MESSAGE(
   ID                INTEGER     PRIMARY KEY AUTOINCREMENT NOT NULL,
   DUMP_HASH         BINARY(32)  NOT NULL,
   CASE_NAME         TEXT        NOT NULL,
   MODULE            TEXT        NOT NULL,
   SENDER            TEXT        NOT NULL,
   RECEIVER          TEXT        NOT NULL,
   CONTENT           TEXT        NOT NULL,
   MESSAGE_TIMESTAMP DATE        NOT NULL,
   FOREIGN KEY (DUMP_HASH)       REFERENCES IMAGE(DUMP_HASH),
   FOREIGN KEY (CASE_NAME)       REFERENCES FCASE(NAME),
   FOREIGN KEY (MODULE)          REFERENCES MODULE(NAME),
   FOREIGN KEY (SENDER)          REFERENCES PERSON(NAME),
   FOREIGN KEY (RECEIVER)        REFERENCES PERSON(NAME)
);

-- Insert one case
INSERT INTO FCASE (NAME, DESCRIPTION)
VALUES ('Dona Branca', 'O caso da senhora de branco');


-- Insert three dumps
INSERT INTO IMAGE (DUMP_HASH, CASE_NAME, DESCRIPTION, AQUISITION_DATE, DUMP_LOCATION)
VALUES (0x1773, 'Dona Branca', 'First dump', CURRENT_TIMESTAMP, '/root/dump1');

INSERT INTO IMAGE (DUMP_HASH, CASE_NAME, DESCRIPTION, AQUISITION_DATE, DUMP_LOCATION)
VALUES (0x1774, 'Dona Branca', 'Second dump', CURRENT_TIMESTAMP, '/root/dump2');

INSERT INTO IMAGE (DUMP_HASH, CASE_NAME, DESCRIPTION, AQUISITION_DATE, DUMP_LOCATION)
VALUES (0x1775, 'Dona Branca', 'Third dump', CURRENT_TIMESTAMP, '/root/dump3');


-- Insert three modules
INSERT INTO MODULE (NAME)
VALUES ('Facebook');

INSERT INTO MODULE (NAME)
VALUES ('Twitter');

INSERT INTO MODULE (NAME)
VALUES ('Skype');


-- Insert two people
INSERT INTO PERSON (NAME, CASE_NAME)
VALUES ('Tiago', 'Dona Branca');

INSERT INTO PERSON (NAME, CASE_NAME)
VALUES ('Diogo', 'Dona Branca');


-- Insert messages from the first dump
INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1773, 'Dona Branca', 'Facebook', 'Tiago', 'Diogo', 'Hello World!', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1773, 'Dona Branca', 'Facebook', 'Diogo', 'Tiago', 'Hello There!', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1773, 'Dona Branca', 'Facebook', 'Tiago', 'Diogo', 'How are you!?', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1773, 'Dona Branca', 'Facebook', 'Tiago', 'Diogo', 'Do you have the bomb ready?', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1773, 'Dona Branca', 'Twitter', 'Diogo', 'Tiago', 'Lets speak on twitter for now...', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1773, 'Dona Branca', 'Twitter', 'Tiago', 'Diogo', 'Rogerio', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1773, 'Dona Branca', 'Twitter', 'Diogo', 'Tiago', 'Back to you', CURRENT_TIMESTAMP);


-- Insert messages from the second dump
INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1774, 'Dona Branca', 'Skype', 'Tiago', 'Diogo', 'Use Skype for a change', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1774, 'Dona Branca', 'Skype', 'Diogo', 'Tiago', 'Im testing DeltaShaper on Skype now', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1774, 'Dona Branca', 'Skype', 'Tiago', 'Diogo', 'Oh, OK', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1774, 'Dona Branca', 'Skype', 'Tiago', 'Diogo', 'Lunch?', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1774, 'Dona Branca', 'Twitter', 'Diogo', 'Tiago', 'Lets speak on twitter again', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1774, 'Dona Branca', 'Twitter', 'Tiago', 'Diogo', 'Rogerio', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1774, 'Dona Branca', 'Twitter', 'Diogo', 'Tiago', 'Back to you', CURRENT_TIMESTAMP);


-- Insert messages from the third dump
INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1775, 'Dona Branca', 'Facebook', 'Tiago', 'Diogo', 'Alahu Akbar', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1775, 'Dona Branca', 'Facebook', 'Diogo', 'Tiago', 'Dass', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1775, 'Dona Branca', 'Facebook', 'Tiago', 'Diogo', 'Run Forest', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1775, 'Dona Branca', 'Facebook', 'Tiago', 'Diogo', 'BUUUM', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1775, 'Dona Branca', 'Skype', 'Diogo', 'Tiago', 'Back to DeltaShaper', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1775, 'Dona Branca', 'Skype', 'Tiago', 'Diogo', 'Again?', CURRENT_TIMESTAMP);

INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP)
VALUES (0x1775, 'Dona Branca', 'Skype', 'Diogo', 'Tiago', 'Sigh', CURRENT_TIMESTAMP);