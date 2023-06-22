# DataWarehouse

# infoware-internship

A repository to hold utility code and examples for the Quipu Infoware Internship programme.

## Goal

Create a solution that will show data from several source and target tables and allow the user to load data from source to target.

This is a full-stack project that will cover both the backend of writing code that will load data from source to target, and a frontend part which includes writing views to display this data.

In the end, the interns should have a project that:
 - Extracts data from a source DB, cleans it (corrects dates, capitalizes names etc.) and loads it to a target DB.
 - Shows data from different tables by utilizing JQuery Datatables that work server-side so that the user can view large datasets.

These are all technologies that we do in IW, and the ETL process is similar although with less edge cases, so it is a nice introduction to how IW works.

## Steps

The first step of the task is to write code that will load data. This should work as an independent script that can be run with several parameters (Table Name, Date), but should still be modular enough that it can be re-used by the web app later on.

The second step is to create a Django project that will simply display data from the tables. The interns should then check the functionality of both parts - they should first check to see the source data, run the load, and check the target data and if has been corrected.

The third step is to combine these two parts - add a button that will run the load from the web. They should be able to run the full process and check the loaded data. Additionally, since there is a lot of data, ideally the web should display it as a server-side table.

To help with this, we have markdown files in extra/django and extra/sql. These are not meant to be taken as a literal order of operations, however they are split into files which can be read consecutively and contain tasks that will make the full project easier to complete, along with code snippets which can guide the interns.

## Tasks

The final project will be a working Data Warehouse model with scripts to fill it and a web view. This model will contain 3 tables: DimParty, DimContract and Contract. These will get data from the source DB, which contains multiple tables.

### ETL

The first task is to write a script which will fill the Target DBs. Example results for these tables:


DimParty

|PartyKey  |Name       |Surname  |DateOfBirth  |Gender  |Address      |PostalCode  |CityName     |RegionName       |Country  |Email              |
|----------|-----------|---------|-------------|--------|-------------|------------|-------------|-----------------|---------|-------------------|
|1         |Ivan       |Radel    |2000-01-01   |F       |Straße 9000  |0000        |Babenhausen  |germany - west   |Germany  |ivan@radel.com     |
|2         |Brianna    |Lesher   |2000-01-01   |M       |Straße 9002  |0000        |Frankfurt    |germany - west   |Germany  |brianna@lesher.com |


DimContract

|ContractKey  |ContractId  |PartyKey  |Currency  |Product             |BranchName       |OpeningDate   |ClosingDate|
|-------------|------------|----------|----------|--------------------|-----------------|--------------|-----------|
|1            |000000000   |4         |MZN       |Off Balance         |511 - Berlin     |2021-12-01    |2025-03-31 |
|2            |000000001   |10        |BYR       |Loro Accounts       |273 - Leipzig    |2021-02-01    |2025-01-31 |


FactContract

|ContractKey  |Date        |ContractStatus  |PrincipalBalance  |AccruedInterestBalance  |InterestRate|
|-------------|------------|----------------|------------------|------------------------|------------|
|1            |2022-08-31  |active          |84695.1180        |84.1076                 |10.6731     |
|2            |2022-08-31  |closed          |24811.1210        |439.2423                |3.2365      |
|3            |2022-08-31  |new             |21523.8732        |268.2366                |7.9170      |


In addition, the following cleaning will need to be done:

1. Customer emails might not be correct - data for these customers should not be collected.
    - To check if a customer has an invalid mail, just check if it contains `@`
2. Map genders to M/F/D.
3. Names, last names and cities might be lowercase - these must be caught and the first letter in each name and surname must be capital.
4. There might be duplicates in the source DB. These must be ignored when loading to target db.
5. Dates should be converted to datetime.

### Web app

Write a Django app that will display data from the source and target DBs. The app should have:

1. A home page which will show a list of links that point to available target tables. Each link should take you to a url that looks like `localhost/table/DimParty`.
2. These pages should show data for the target table and all related source tables.
3. The data should be in a table which is paginated on the server-side.
4. On each page, there should be a button that will run the load for the target table.
