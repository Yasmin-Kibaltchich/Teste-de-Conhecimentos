CREATE TABLE "Vaga" (
	"CdVaga"	INTEGER NOT NULL UNIQUE,
	"CdStatus"	INTEGER NOT NULL,
	"DataCadastro"	DATE NOT NULL,
	"UfVaga"	TEXT  NOT NULL,
	"Salario"	REAL NOT NULL,
	PRIMARY KEY("CdVaga" AUTOINCREMENT)
);


CREATE TABLE "StatusVaga" (
	"CdStatus"	INTEGER NOT NULL UNIQUE,
	"NomeStatus"	TEXT NOT NULL,
	PRIMARY KEY("CdStatus" AUTOINCREMENT)
);


CREATE TABLE "Empresa" (
	"CdEmpresa"	INTEGER NOT NULL UNIQUE,
	"CdStatus"	INTEGER NOT NULL,
	"Nome"	TEXT NOT NULL,
	"Endereco"	TEXT NOT NULL,
	"Telefone"	TEXT NOT NULL,
	"Cnpj"	TEXT NOT NULL,
	"DataCadastro"	DATE NOT NULL,
	PRIMARY KEY("CdEmpresa" AUTOINCREMENT)
);


CREATE TABLE "StatusEmpresa" (
	"CdStatus"	INTEGER NOT NULL UNIQUE,
	"NomeStatus"	TEXT NOT NULL,
	PRIMARY KEY("CdStatus" AUTOINCREMENT)
);

CREATE TABLE "Cliente" (
	"CdCliente"	INTEGER NOT NULL UNIQUE,
	"CdStatus"	INTEGER NOT NULL,
	"Nome"	TEXT NOT NULL,
	"Telefone"	TEXT NOT NULL,
	"Cpf"	TEXT NOT NULL,
	"Endereco"	TEXT NOT NULL,
	"Email"	TEXT NOT NULL,
	"DataCadastro"	DATE NOT NULL,
	PRIMARY KEY("CdCliente" AUTOINCREMENT)
);

CREATE TABLE "StatusCliente" (
	"CdStatus"	INTEGER NOT NULL UNIQUE,
	"NomeStatus"	TEXT NOT NULL,
	PRIMARY KEY("CdStatus" AUTOINCREMENT)
);