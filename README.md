# Fisheries Blockchain Supply Chain Application

## Overview

This application is a blockchain-focused supply chain solution for fisheries. It is built to support the reporting of fish catch data from fishermen, determination of catch quotas by authorized parties, and storing data in a blockchain for transparency and traceability.

## Features

1. **Fish Catch Reporting** - Fishermen can report their fish catch data
2. **Quota Management** - Regulatory authorities can set catch quotas for vessels
3. **Blockchain Integration** - Data is stored in a blockchain for integrity and transparency
4. **Role-Based Access Control** - Different user roles with specific permissions

## Technology Stack

- Django 5.2.5
- Django REST Framework 3.16.1
- drf-spectacular for API documentation
- PostgreSQL database
- JWT authentication

## Setup Instructions

1. **Create and activate virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install requirements**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Install PostgreSQL adapter**:

   ```bash
   pip install psycopg2-binary
   ```

4. **Run migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**:

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

## API Documentation

This application uses drf-spectacular to provide comprehensive API documentation.

### Accessing Documentation

Once the server is running, you can access the following documentation endpoints:

1. **Swagger UI**: [http://localhost:8000/](http://localhost:8000/)

   - Interactive API documentation
   - Test endpoints directly from the browser

2. **Redoc UI**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

   - Clean, readable API documentation

3. **API Schema**: [http://localhost:8000/schema/](http://localhost:8000/schema/)

   - Machine-readable API schema in JSON/YAML format

4. **Blockchain Features Documentation**: [http://localhost:8000/blockchain-features/](http://localhost:8000/blockchain-features/)
   - Detailed documentation of blockchain supply chain features

### Documentation Files

The documentation is also available as Markdown files in the [dokumentasi](file:///Users/ROFI/Develop/proyek/ficio/dokumentasi) directory:

- [api_dokumentasi.md](file:///Users/ROFI/Develop/proyek/ficio/dokumentasi/api_dokumentasi.md) - API usage examples
- [blockchain_supply_chain_features.md](file:///Users/ROFI/Develop/proyek/ficio/dokumentasi/blockchain_supply_chain_features.md) - Detailed features documentation
- [drf_spectacular_setup_summary.md](file:///Users/ROFI/Develop/proyek/ficio/dokumentasi/drf_spectacular_setup_summary.md) - Summary of drf-spectacular setup

## User Roles

- **admin**: Full system access, data imports
- **pemilik_kapal** (ship owner): Register ships, report catches
- **nahkoda** (captain): Report fish catches
- **regulator**: Set catch quotas for ships
- **auditori** (auditor): Audit catch data and quotas

## Key Endpoints

### Authentication

- `POST /register/` - User registration
- `POST /login/` - User login

### Ship Management

- `POST /api/kapal/input/` - Register new ship
- `GET /api/list-kapal/` - List ships

### Fish Catch Reporting

- `POST /api/tangkapan/input/` - Report fish catch data
- `GET/POST /api/kapal/history/` - View catch history

### Quota Management

- `POST /api/input/kuota/` - Set ship quota

### Master Data

- `GET /api/master/jenis-ikan/` - List fish types
- `GET /api/master/wpp/` - List Fisheries Management Areas

### Data Import (Admin Only)

- `POST /api/import/kapal/` - Import ships from CSV
- `POST /api/import/jenis-ikan/` - Import fish types from CSV
- `POST /api/import/wpp/` - Import WPP data from CSV

## Development

### Running the Server

You can use the provided script to run the server:

```bash
./run_server.sh
```

### Documentation Development

The API documentation is automatically generated using drf-spectacular based on:

- View decorators (`@extend_schema`)
- Serializer field definitions
- Model field definitions

To enhance the documentation:

1. Add `@extend_schema` decorators to views
2. Add `help_text` to serializer fields
3. Update the `SPECTACULAR_SETTINGS` in [settings.py](file:///Users/ROFI/Develop/proyek/ficio/fishcast/settings.py)

## Blockchain Integration

The application is designed to integrate with blockchain technology to ensure:

- Data integrity through immutable ledger
- Transparency for all stakeholders
- Complete traceability from catch to market
- Compliance with quotas and regulations

_Note: The actual blockchain integration implementation is pending and will be added in future development._
