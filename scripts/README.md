Bank Customer Reviews ETL Pipeline & Database Ingestion

An end-to-end data engineering pipeline designed to ingest, clean, and map mobile banking customer reviews for the **Commercial Bank of Ethiopia (CBE)Bank of Abyssinia (BOA), and Dashen Bank. The pipeline processes raw data in Python using Pandas and securely migrates it to a relational PostgreSQL database via SQLAlchemy.

---

 Relational Schema Design

The storage layer relies on a relational normalized architecture to eliminate data repetition and guarantee structural integrity.

`banks` (Lookup Master Table): Stores structural application metadata and maps a primary key ID to each specific bank.
reviews` (Relational Data Table): Holds text contents, star ratings, and metadata for every review. It connects directly to the lookup table using a Foreign Key column (`bank_id`).

---

 Environment Setup & Installation Guide

Follow these instructions to stand up the data pipeline and database configuration locally.

1. Database Setup
Ensure you have PostgreSQL and pgAdmin 4 installed and running on your machine. 

Open pgAdmin or a terminal connection and create a target database instance:
```sql
CREATE DATABASE bank_reviews;