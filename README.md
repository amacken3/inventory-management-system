# Inventory Management System

This is a Flask-based inventory management system for a small retail/e-commerce setup. The app lets employees manage local inventory items, look up product information from the OpenFoodFacts API, and interact with the backend through a command-line interface.

The project uses an in-memory Python list to simulate the store’s inventory database. OpenFoodFacts is used only as an external product lookup tool. When a product is imported, the app pulls product details from OpenFoodFacts, combines them with local inventory fields like price and stock, and stores the result in the local in-memory inventory list.

Because the inventory is stored in memory, changes work while the Flask server is running, but the inventory resets when the server restarts.

## Features

- View all inventory items
- View a single inventory item by ID
- Add a new inventory item manually
- Update inventory fields like price, stock, name, or brand
- Delete inventory items
- Search OpenFoodFacts by barcode
- Import OpenFoodFacts product data into the local inventory
- Use a CLI to interact with the Flask API
- Unit tests for Flask routes, CLI functions, and external API behavior

## Tech Used

- Python
- Flask
- Requests
- Pytest
- unittest.mock
- argparse
- OpenFoodFacts API

## Project Structure

```txt
inventory-management-system/
│
├── app.py
├── cli.py
├── inventory_cli.py
├── Pipfile
├── Pipfile.lock
├── README.md
│
├── data/
│   └── inventory_data.py
│
├── services/
│   ├── inventory_service.py
│   └── openfoodfacts_service.py
│
└── tests/
    ├── test_cli.py
    ├── test_external_api.py
    └── test_inventory_routes.py
```
## Setup

```bash
git clone https://github.com/amacken3/inventory-management-system.git

cd inventory-management-system

pipenv install

pipenv shell
```

## Run Flask Server

```bash
pipenv run python app.py

http://127.0.0.1:5555
```

## Using the CLI

Before using the CLI, start the Flask server in one terminal:

```bash
pipenv run python inventory_cli.py list
pipenv run python inventory_cli.py get 1
pipenv run python inventory_cli.py search 3017624010701
pipenv run python inventory_cli.py import 3017624010701 --price 5.99 --stock 12
pipenv run python inventory_cli.py update 1 --stock 30
pipenv run python inventory_cli.py delete 2
```

## Running the Tests
```bash
pipenv run pytest -x

pipenv run pytest
```
