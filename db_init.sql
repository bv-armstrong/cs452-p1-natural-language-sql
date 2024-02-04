create table if not exists product_type (
    product_type_id int primary key,
    display_value varchar(20) not null
);

create table if not exists product (
    product_id int primary key,
    description varchar(50),
    product_type_id int,
    foreign key (product_type_id) references product_type (product_type_id)
);

create table if not exists vending_machine (
    vending_machine_id int primary key,
    location_name varchar(20),
    longitude decimal(9,6) not null,
    latitude decimal(8,6) not null
);

create table if not exists vending_machine_product (
    vending_machine_id int,
    product_id int,
    quantity int,
    price decimal(3,2),
    primary key (vending_machine_id, product_id),
    foreign key (vending_machine_id) references vending_machine (vending_machine_id),
    foreign key (product_id) references product (product_id)
);

create table if not exists user (
    user_id int primary key,
    name varchar(20)
);

create table if not exists user_vending_machine_starred (
    user_id int,
    vending_machine_id int,
    primary key (user_id, vending_machine_id),
    foreign key (user_id) references user (user_id),
    foreign key (vending_machine_id) references vending_machine (vending_machine_id)
);

create table if not exists user_product_starred (
    user_id int,
    product_id int,
    primary key (user_id, product_id),
    foreign key (user_id) references user (user_id),
    foreign key (product_id) references product (product_id)
);