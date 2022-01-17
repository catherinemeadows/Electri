set foreign_key_checks = 0;

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS alerts;
DROP TABLE IF EXISTS image_info;

set foreign_key_checks = 1;

-- generate tables
CREATE TABLE user (
    username varchar(32) not null,
    user_password varchar(32) not null,
    fname varchar(32),
    lname varchar(32),
    email varchar(50),
    organization varchar(50)
);

CREATE TABLE alerts (
    alert_id int(8) not null auto_increment,
    alert_status int(1) not null,
    city varchar(32),
    alert_state varchar(32),
    license_plate varchar(8),
    make varchar(32),
    model varchar(32),
    vehicle_year int (4),
    color varchar(20),
    color_rgb blob,
    PRIMARY KEY(alert_id)
);

CREATE TABLE image_info (
    img_id int(8) auto_increment,
    img_path varchar(32) not null,
    colors blob,
    make varchar(32),
    model varchar(32),
    vehicle_year int(4),
    license_plate varchar(32),
    PRIMARY KEY(img_id)
);

CREATE TABLE matches (
    match_id int(8) not null auto_increment,
    img_id int(8) not null,
    alert_id int(8) not null,
    FOREIGN KEY (img_id) REFERENCES image_info(img_id),
    FOREIGN KEY (alert_id) REFERENCES alerts(alert_id),
    PRIMARY KEY(match_id)
);
