CREATE TABLE gps_data(
    uuid TEXT NOT NULL,
    latitude NUMBER NOT NULL,
    longitude NUMBER NOT NULL,
    altitude NUMBER NOT NULL,
    time TEXT NOT NULL,
    provider TEXT NOT NULL
);

pragma journal_mode = WAL;
