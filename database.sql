use tree;

create table user(
    id int primary key not null auto_increment,
    name varchar(20),
    sex char(4),
    email varchar(40),
    city char(10),
    phone varchar(20) not null,
    password varchar(20) not null,
    imgUrl varchar(50) not null
);

create table identity(
    id int primary key not null auto_increment,
    user_id int not null,
    job char(5) not null,
    date year not null,
    foreign key (user_id) references user(id)
);

create table relation(
    id int primary key not null auto_increment,
    tea_id int not null,
    stu_id int not null,
    t_name varchar(20) not null,
    t_imgurl varchar(50) not null,
    stu_name varchar(20) not null
);