import sqlite3 as lite

def initDatabase(dbCon):

    cur = dbCon.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='FCASE'")
    rows_fcase = cur.fetchall()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='IMAGE'")
    rows_image = cur.fetchall()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='MODULE'")
    rows_module = cur.fetchall()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='GLOBAL_MSG'")
    rows_person = cur.fetchall()

    if(len(rows_fcase) == 0 and len(rows_image) == 0 and len(rows_module) == 0 and
    len(rows_person) == 0):
        cur.execute("PRAGMA foreign_keys = ON")

        cur.execute("CREATE TABLE FCASE(\
            NAME          TEXT        NOT NULL,\
            DESCRIPTION   DATE        NOT NULL,\
            PRIMARY KEY (NAME))")

        cur.execute("CREATE TABLE IMAGE(\
           DUMP_HASH         BINARY(32)  NOT NULL,\
           CASE_NAME         TEXT        NOT NULL,\
           DESCRIPTION       TEXT        NOT NULL,\
           AQUISITION_DATE   DATE        NOT NULL,\
           DUMP_LOCATION     TEXT        NOT NULL,\
           FOREIGN KEY (CASE_NAME) REFERENCES FCASE(NAME),\
           PRIMARY KEY (DUMP_LOCATION, CASE_NAME))")

        cur.execute("CREATE TABLE MODULE(\
            NAME  TEXT  NOT NULL,\
            DESCRIPTION  TEXT  NOT NULL,\
            PRIMARY KEY (NAME))")

        cur.execute("CREATE TABLE GLOBAL_MSG(\
            ID                INTEGER     PRIMARY KEY AUTOINCREMENT NOT NULL,\
            CASE_NAME         TEXT        NOT NULL,\
            DUMP_HASH         BINARY(32)  NOT NULL,\
            AUTHOR            TEXT        NOT NULL,\
            RECIPIENT         TEXT        NOT NULL,\
            CONTENT           TEXT        NOT NULL,\
            MSG_TIMESTAMP     DATE        NOT NULL,\
            FOREIGN KEY (CASE_NAME) REFERENCES FCASE(NAME),\
            FOREIGN KEY (DUMP_HASH) REFERENCES IMAGE(DUMP_HASH))")


        #cur.execute("CREATE TABLE MESSAGE(\
        # ID                INTEGER     PRIMARY KEY AUTOINCREMENT NOT NULL,\
        # DUMP_HASH         BINARY(32)  NOT NULL,\
        # CASE_NAME         TEXT        NOT NULL,\
        # MODULE            TEXT        NOT NULL,\
        # SENDER            TEXT        NOT NULL,\
        # RECEIVER          TEXT        NOT NULL,\
        # CONTENT           TEXT        NOT NULL,\
        # MESSAGE_TIMESTAMP DATE        NOT NULL,\
        # FOREIGN KEY (DUMP_HASH)       REFERENCES IMAGE(DUMP_HASH),\
        # FOREIGN KEY (CASE_NAME)       REFERENCES FCASE(NAME),\
        # FOREIGN KEY (MODULE)          REFERENCES MODULE(NAME),\
        # FOREIGN KEY (SENDER)          REFERENCES PERSON(NAME),\
        # FOREIGN KEY (RECEIVER)        REFERENCES PERSON(NAME))")
    elif(len(rows_fcase) == 1 and len(rows_image) == 1 and len(rows_module) == 1 and
    len(rows_person) == 1):
        pass #Database has our tables
    else:
        raise Exception('Input Database has some tables used by Ramas. Possible Conflict. Aborting...')
