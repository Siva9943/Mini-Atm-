create table atm_databases(
id int primary key,
user_name varchar(255) not null ,
pin_code int not null,
balance bigint not null
)
select * from atm_databases