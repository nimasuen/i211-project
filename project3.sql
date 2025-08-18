create table item(
id int primary key auto_increment,
name varchar(30),
summary varchar(100),
description varchar(200),
daily_rental_price varchar(30),
weight varchar(30),
image_path varchar(50),
item_condition varchar(30),
purchase_date date,
notes varchar(60),
currently_available varchar(30)
)engine=innodb;

create table person(
id int primary key auto_increment,
name varchar(30),
email varchar(30),
date_of_birth date,
mobile_phone_number varchar(30),
role varchar(30)
)engine=innodb;

create table rental(
person_id int not null,
item_id int not null,
checkout_date date,
due_date date,
return_date date,
foreign key(person_id) references person(id),
foreign key (item_id) references item(id)
)engine=innodb;


insert into item (id, name, summary, description, daily_rental_price, weight, image_path, item_condition, purchase_date, notes, currently_available) values
(101, '1-person tent', 'A one person backpacking tent', 'A one person tent is a compact shelter designed to accommodate a single camper', '$20', '10lbs', 'images/one_person_tent.jpg', 'good', '2017-06-23', 'Tents(2-4) need to be inspected', 'True'),
(102, '4-person tent', 'A 4-person backpacking tent', 'A spacious outdoor shelter designed to comfortably accommodate up to four campers', '$50', '20lbs', 'images/four_person_tent.jpg', 'fair', '2020-01-18', 'Tent(7) missing ground stakes', 'False'),
(103, 'Aluminum Walking Stick', 'A Strong sturdy aluminum stick', 'An aluminum walking stick is a lightweight and durable mobility aid made from aluminum alloy', '$30', '10lbs', 'images/aluminium_walking_stick.jpg', 'broken', '2006-10-22', 'All aluminum walking stakes are fine', 'False'),
(104, 'Deluxe Backpack', 'A deluxe backpack', 'A deluxe backpack is a high-quality, feature-rich bag designed with premium materials and ample organizational compartments', '$159', '10lbs', 'images/backpack.jpg', 'poor', '2017-06-23', 'Backpacks(9-12) need to be inspected', 'False'),
(105, 'Water Hydration Pack', 'A pack equipped with water', 'A water hydration pack is a specialized backpack equipped with a built-in water reservoir', '$15', '5lbs', 'images/hydration_pack.jpg', 'poor', '2022-12-06', 'Hydration packs all look fine', 'False'),
(106, 'Wooden Walking Stick', 'A rough wooden stick', 'A sturdy and traditional mobility aid crafted from wood', '$0', '4lbs', 'images/wooden_walking_stick.jpg', 'new', '2023-09-05', 'All broken wooden walking sticks have been disposed', 'True')
;

insert into person (id, name, email, date_of_birth, mobile_phone_number, role) values
(501, 'Barnebas Story','barnebasstory@example.com', '2022-10-08','765-317-4020', 'staff'),
(502, 'Chrisy Bawme', 'chrisybawme@example.com', '2020-08-15', '317-121-2591', 'member'),
(503, 'Gilbert Josham', 'gilbertjosham@example.com', '1997-02-14', '555-555-5555', 'staff'),
(504, 'Coreen Melchior', 'coreenmelchior@example.com', '1996-04-22', '317-174-7751', 'member'),
(505, 'Raphaela Radsdale', 'raphaelaradsdale@example.com', '1995-12-03', '219-461-1244', 'member'),
(506, 'Atlanta Pigdon', 'atlantapigdon@example.com', '1990-01-17', '574-146-5360', 'member')
;

insert into rental (person_id, item_id, checkout_date, due_date, return_date) values
(501, 101, '2017-06-03', '2017-07-07', '2017-07-13'),
(502, 102, '2020-01-18', '2020-02-01', '2020-02-01'),
(503, 103, '2006-10-22', '2006-11-05', '2006-12-01'),
(504, 104, '2017-06-23', '2017-07-07', '2017-06-30'),
(505, 105, '2022-12-06', '2022-12-20', '2022-12-14'),
(506, 106, '2023-09-05', '2023-09-24', '2023-10-31')
;

