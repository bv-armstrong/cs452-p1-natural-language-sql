insert into product_type (product_type_id, display_value) values 
(1, "Drink"),
(2, "Snack");

insert into product (product_id, description, product_type_id) values 
(1, "Coke", 1),
(2, "Diet Coke", 1),
(3, "Lemonade", 1),
(4, "Chips", 2),
(5, "Bagel", null);

insert into vending_machine (vending_machine_id, location_name, longitude, latitude) values 
(1, "Building 1", -111.649315, 40.251842),
(2, "Building 2", -111.649178, 40.248305),
(3, "Break room", -111.647095, 40.248600);

insert into vending_machine_product (vending_machine_id, product_id, quantity, price) values 
(1, 1, 3, 1.25),
(1, 2, 5, 1.25),
(1, 4, 0, 1.00),
(1, 5, 2, 2.50),
(2, 1, 1, 1.50),
(2, 2, 4, 1.50),
(2, 3, 2, 1.50),
(3, 3, 0, 1.00),
(3, 4, 1, 0.75),
(3, 5, 6, 1.50);

insert into user (user_id, name) values 
(1, "John"),
(2, "Mary"),
(3, "Bob");

insert into user_vending_machine_starred (user_id, vending_machine_id) values 
(1, 1),
(1, 2),
(2, 3);

insert into user_product_starred (user_id, product_id) values 
(1, 1),
(1, 2),
(1, 5),
(2, 3),
(2, 5);
