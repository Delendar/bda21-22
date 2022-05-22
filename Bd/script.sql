drop table estadistica_vacuna cascade;
drop table recomendacion_vacuna cascade;
drop table recomendacion cascade;
drop table vacuna cascade;
drop table estadistica cascade;

create table recomendacion(
	cod_recomendacion numeric(4),
	organizacion varchar(20) not null,
	descripcion varchar(50) not null,
	constraint pk_recomendacion primary key (cod_recomendacion));

create table vacuna(
	cod_vacuna numeric(4),
	nombre_vacuna varchar(20) not null unique,
	constraint pk_vacuna primary key (cod_vacuna));

create table estadistica(
    cod_estadistica numeric(4),
    nombre_estadistica varchar(20) not null unique,
    constraint pk_estadistica primary key (cod_estadistica));

create table estadistica_vacuna(
    cod_vacuna numeric(4),
    cod_estadistica numeric(4),
    valor numeric(12,2) not null,
    descripcion varchar(50),
    constraint pk_est_vac primary key (cod_vacuna, cod_estadistica),
    constraint fk_est_vac_vacuna foreign key (cod_vacuna) references vacuna,
    constraint fk_est_vac_estadistica foreign key (cod_estadistica) references estadistica);

create table recomendacion_vacuna(
	cod_vacuna numeric(4),
	cod_recomendacion numeric(4),
	fecha_aplicacion date not null,
	constraint pk_rec_vac primary key (cod_recomendacion, cod_vacuna),
	constraint fk_rec_vac_recomendacion foreign key (cod_recomendacion) references recomendacion,
	constraint fk_rec_vac_vacuna foreign key (cod_vacuna) references vacuna);

insert into vacuna (cod_vacuna, nombre_vacuna) values(1001,'PFZIER');
insert into vacuna (cod_vacuna, nombre_vacuna) values(1002,'ASTRAZENECA');
insert into vacuna (cod_vacuna, nombre_vacuna) values(1003,'JANHSEN');

insert into recomendacion (cod_recomendacion, organizacion, descripcion) values(0100,'OMS','No a mayores de 65');
insert into recomendacion (cod_recomendacion, organizacion, descripcion) values(0200,'OMS','No a mayores de 50');
insert into recomendacion (cod_recomendacion, organizacion, descripcion) values(0300,'SANIDAD','No a mayores de 55');

insert into estadistica (cod_estadistica, nombre_estadistica) values(1, 'DOSIS_NECESARIAS');
insert into estadistica (cod_estadistica, nombre_estadistica) values(2, 'PRECIO_DOSIS');

insert into recomendacion_vacuna (cod_vacuna, cod_recomendacion, fecha_aplicacion)
    values(1002, 0100, to_date('10/03/2021','DD/MM/YY'));
insert into recomendacion_vacuna (cod_vacuna, cod_recomendacion, fecha_aplicacion)
    values(1002, 0200, to_date('20/03/2021','DD/MM/YY'));
insert into recomendacion_vacuna (cod_vacuna, cod_recomendacion, fecha_aplicacion)
    values(1002, 0300, to_date('25/03/2021','DD/MM/YY'));
insert into recomendacion_vacuna (cod_vacuna, cod_recomendacion, fecha_aplicacion)
    values(1001, 0100, to_date('15/02/2021','DD/MM/YY'));

insert into estadistica_vacuna (cod_vacuna, cod_estadistica, valor, descripcion)
    values (1001, 1, 2, null);
insert into estadistica_vacuna (cod_vacuna, cod_estadistica, valor, descripcion)
    values (1001, 2, 10, null);
insert into estadistica_vacuna (cod_vacuna, cod_estadistica, valor, descripcion)
    values (1002, 1, 3, null);
insert into estadistica_vacuna (cod_vacuna, cod_estadistica, valor, descripcion)
    values (1002, 2, 9, null);