# Fisheries Blockchain Supply Chain - API Documentation

## Overview

This application is a blockchain-focused supply chain solution for fisheries. It is built to support the reporting of fish catch data from fishermen, determination of catch quotas by authorized parties, and storing data in a blockchain for transparency and traceability.

## Key Features

### 1. Fish Catch Reporting

- Fishermen (ship owners and captains) can report their fish catch data
- Data includes fish type, weight, quantity, and location (WPP - Fisheries Management Area)
- All catch data is validated against allocated quotas

### 2. Quota Management

- Regulatory authorities can set catch quotas for individual vessels
- Quota tracking at both individual vessel and global levels
- Automatic quota validation when reporting catches

### 3. Blockchain Integration

- All catch data and quota information are stored in a blockchain
- Ensures data integrity and prevents tampering
- Provides complete traceability of fish from catch to market

### 4. Role-Based Access Control

- Different user roles with specific permissions:
  - **Admin**: Manage master data and imports
  - **Ship Owner/Captain**: Report fish catch data
  - **Regulator**: Set catch quotas
  - **Auditor**: Audit catch data and quotas

## API Endpoints

### Authentication

#### User Registration

- **Endpoint**: `POST /register/`
- **Description**: Register a new user with specific role
- **Roles**: admin, pemilik_kapal (ship owner), nahkoda (captain), regulator, auditori (auditor)

#### User Login

- **Endpoint**: `POST /login/`
- **Description**: Authenticate user and obtain JWT tokens
- **Credentials**: Username or ship registration number + password

### Ship Management

#### Register New Ship

- **Endpoint**: `POST /api/kapal/input/`
- **Description**: Register a new fishing vessel (ship owners and admins only)
- **Permissions**: pemilik_kapal, admin

#### List Ships

- **Endpoint**: `GET /api/list-kapal/`
- **Description**: List all ships (role-dependent visibility)
- **Permissions**: All authenticated users

### Fish Catch Reporting

#### Batch Catch Input

- **Endpoint**: `POST /api/tangkapan/input/`
- **Description**: Report fish catch data in batches (admins only)
- **Validation**: Automatic quota checking
- **Permissions**: admin

#### Catch History

- **Endpoint**: `GET/POST /api/kapal/history/`
- **Description**: View catch history for a specific ship
- **Permissions**: All authenticated users

### Master Data

#### Fish Types

- **Endpoint**: `GET /api/master/jenis-ikan/`
- **Description**: List all fish types
- **Permissions**: All authenticated users

#### Fisheries Management Areas (WPP)

- **Endpoint**: `GET /api/master/wpp/`
- **Description**: List all Fisheries Management Areas
- **Permissions**: All authenticated users

### Quota Management

#### Set Ship Quota

- **Endpoint**: `POST /api/input/kuota/`
- **Description**: Set catch quota for a specific ship (regulators only)
- **Permissions**: regulator

### Data Import (Admin Only)

#### Import Ships

- **Endpoint**: `POST /api/import/kapal/`
- **Description**: Import ship data from CSV file
- **Permissions**: admin

#### Import Fish Types

- **Endpoint**: `POST /api/import/jenis-ikan/`
- **Description**: Import fish types from CSV file
- **Permissions**: admin

#### Import WPP

- **Endpoint**: `POST /api/import/wpp/`
- **Description**: Import Fisheries Management Areas from CSV file
- **Permissions**: admin

## Data Models

### User Roles

- **admin**: Full system access, data imports
- **pemilik_kapal**: Ship owner, can register ships
- **nahkoda**: Captain, can report catches
- **regulator**: Sets quotas for ships
- **auditori**: Audits data and quotas

### Core Entities

#### Ship (Kapal)

- `no_buku_kapal`: Unique ship registration number
- `nama_kapal`: Ship name

#### Fish Catch (TangkapanIkan)

- `kapal`: Associated ship
- `jenis_ikan`: Type of fish caught
- `weight`: Weight in kilograms
- `location`: Catch location (WPP)
- `created_at`: Timestamp

#### Quota (KuotaKapal)

- `kapal`: Associated ship
- `kuota`: Allocated quota (kg)
- `kuota_terpakai`: Used quota (kg)

#### Fish Types (JenisIkan)

- `nama`: Name of fish type

#### Fisheries Management Areas (WPP)

- `code`: Area code
- `name`: Area name

## Blockchain Integration

The application integrates with blockchain technology to ensure:

1. **Data Integrity**: All catch data is stored in an immutable ledger
2. **Transparency**: All stakeholders can verify catch data and quotas
3. **Traceability**: Complete history of fish from catch to market
4. **Compliance**: Automated validation against quotas and regulations

## Security

- JWT-based authentication
- Role-based access control
- CORS support for cross-origin requests
- Data validation and sanitization

## Technology Stack

- **Backend**: Django 5.2.5
- **API Framework**: Django REST Framework 3.16.1
- **Authentication**: Django REST Framework SimpleJWT
- **Documentation**: drf-spectacular
- **Database**: PostgreSQL
- **Blockchain**: [Integration details to be implemented]
