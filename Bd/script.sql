drop table recomendacion cascade constraints;
drop table hist_rec cascade constraints;
drop table vacuna cascade constraints;


create table recomendacion(
	cod_rec numeric(4),
	nombre_org varchar(20) not null,
	descripcion varchar(50) not null,
	constraint pk_recomen primary key (cod_rec));

create table vacuna(
	cod_vacuna numeric(4),
	nombre_v varchar(20) not null,
	dosis_nece numeric(1) not null,
	constraint pk_vacuna primary key (cod_vacuna));

create table hist_rec(
	fecha_rec date,
	cod_rec numeric(4),
	estado varchar(10) not null,
	cod_vacuna numeric(4) not null,
	constraint pk_histrec primary key (fecha_rec, cod_rec),
	constraint fk_histrec_crec foreign key (cod_rec) references recomendacion,
	constraint fk_histrec_cvacuna foreign key (cod_vacuna) references vacuna);


insert into vacuna values(1001,'Pfzier',2);
insert into vacuna values(1002,'AstraZeneca',2);
insert into vacuna values(1003,'Janhsen',1);

insert into recomendacion values(0100,'OMS','No a mayores de 65');
insert into recomendacion values(0200,'OMS','No a mayores de 50');
insert into recomendacion values(0300,'Sanidad','No a mayores de 55');

insert into hist_rec values(to_date('10/03/2021','DD/MM/YY'),0100,'No vigente',1002);
insert into hist_rec values(to_date('20/03/2021','DD/MM/YY'),0200,'Vigente',1002);
insert into hist_rec values(to_date('25/03/2021','DD/MM/YY'),0300,'Borrador',1002);
insert into hist_rec values(to_date('15/02/2021','DD/MM/YY'),0100,'Vigente',1001);
