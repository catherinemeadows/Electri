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
    latitude decimal (6,4),
    longitude decimal (6,4),
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

-- USERS
insert into user(username, user_password, fname, lname, email, organization)
values ("admin", "admin", "Admin", "User", "admin_fake@email.com", "DC MPD");

-- ALERTS
-- alerts with matches in db: 
insert into alerts(alert_id, alert_status, city, alert_state, latitude, longitude, license_plate, make, model, vehicle_year, color, color_rgb)
values (00010000, 1, "Washington, DC", "DC", 38.9072, 77.0639, "FN9173", "Toyota", "Camry", 2010, "Black");

insert into alerts(alert_id, alert_status, city, alert_state, license_plate, make, model, vehicle_year, color, color_rgb)
values (00010001, 1, "Cincinnati", "OH", 39.1031, 84.5120, "AA00AA", "Ford", "Bronco", 2016, "Blue");

insert into alerts(alert_id, alert_status, city, alert_state, license_plate, make, model, vehicle_year, color, color_rgb)
values (00010002, 1, "Boston", "MA", 42.3601, 71.0589, "215BG2", "Honda", "Civic", 2017, "White"); 

-- alerts with no matches: 
insert into alerts(alert_id, alert_status, city, alert_state, license_plate, make, model, vehicle_year, color, color_rgb)
values (00010003, 0, "Phoenix", "AZ", 33.4484, 112.0704, "BY8567", "Ford", "F-150", 2018, "Red"); 

-- insert into alerts(alert_id, alert_status, city, alert_state, license_plate, make, model, vehicle_year, color, color_rgb)
-- values (00010004, 0, )

-- insert into alerts(alert_id, alert_status, city, alert_state, license_plate, make, model, vehicle_year, color, color_rgb)
-- values (00010005, 0, )

-- insert into alerts(alert_id, alert_status, city, alert_state, license_plate, make, model, vehicle_year, color, color_rgb)
-- values (00010005, 0, )

-- insert into alerts(alert_id, alert_status, city, alert_state, license_plate, make, model, vehicle_year, color, color_rgb)
-- values (00010007, 0, )
