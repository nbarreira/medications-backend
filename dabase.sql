
drop table if exists posology;
drop table if exists medications;
drop table if exists patient;

create table patient (
    id integer,
    username text not null,
    name text,
    surname text,
    primary key (id)
);


create table medications (
    id integer,
    patientId integer not null,
    name text not null,
    dosage real not null default 1,
    startDateTimestamp integer not null,
    treatment_duration integer not null default 1,
    primary key (id),
    constraint fk_medications foreign key (patientId) 
        references patient 
        on delete cascade
);

create table posology (
    medicationId integer,
    hour integer not null,
    minute integer not null,
    primary key (medicationId, hour, minute),
    constraint fk_posology foreign key(medicationId) 
        references medications
        on delete cascade
);