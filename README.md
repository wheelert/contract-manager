# Contract Manager

A GTK4 application for managing contracts, subscriptions, and license keys.

## Features

- **Contracts**: Track vendor contracts with start/end dates, values, and renewal reminders
- **Subscriptions**: Manage recurring subscriptions with billing cycles and auto-renewal tracking
- **License Keys**: Store and organize software license keys with activation and expiration dates
- **Backup/Restore**: Export and import your entire database as JSON

## Requirements

- Python 3.8+
- GTK4
- Libadwaita
- PyGObject

## Installation

### Install dependencies

```bash
# Debian/Ubuntu
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1

# Fedora
sudo dnf install python3-gobject gtk4 libadwaita

# Arch
sudo pacman -S python-gobject gtk4 libadwaita
```

### Install Python packages

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python3 src/main.py
```

Or make it executable:

```bash
chmod +x src/main.py
./src/main.py
```

## Data Storage

Data is stored in SQLite database at `data/contracts.db`.

## Project Structure

```
contract-manager/
├── src/
│   ├── __init__.py
│   ├── main.py          # GTK4 application entry point
│   └── database.py      # SQLite database operations
├── data/                # Database storage
├── requirements.txt
└── README.md
```

## Database Schema

### Contracts
- id, name, vendor, contract_number
- start_date, end_date
- value, currency
- description, document_path
- renewal_reminder

### Subscriptions
- id, name, provider, plan
- billing_cycle, cost, currency
- start_date, next_billing_date
- auto_renew, website, notes

### Licenses
- id, name, software, license_key
- license_type, seats
- activation_date, expiration_date
- vendor, order_id, notes

## License

MIT
