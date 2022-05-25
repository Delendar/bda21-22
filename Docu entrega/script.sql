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