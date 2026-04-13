import sqlite3
import json
from datetime import datetime
from pathlib import Path

class Database:
    def __init__(self, db_path="data/contracts.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                vendor TEXT NOT NULL,
                contract_number TEXT,
                start_date TEXT,
                end_date TEXT,
                value REAL,
                currency TEXT DEFAULT 'USD',
                description TEXT,
                document_path TEXT,
                renewal_reminder INTEGER DEFAULT 30,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                provider TEXT NOT NULL,
                plan TEXT,
                billing_cycle TEXT CHECK(billing_cycle IN ('monthly', 'yearly', 'quarterly', 'weekly')),
                cost REAL,
                currency TEXT DEFAULT 'USD',
                start_date TEXT,
                next_billing_date TEXT,
                auto_renew INTEGER DEFAULT 1,
                description TEXT,
                website TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS licenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                software TEXT NOT NULL,
                license_key TEXT NOT NULL,
                license_type TEXT CHECK(license_type IN ('perpetual', 'subscription', 'trial', 'enterprise', 'oem')),
                version TEXT,
                seats INTEGER DEFAULT 1,
                activation_date TEXT,
                expiration_date TEXT,
                vendor TEXT,
                order_id TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def get_contracts(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contracts ORDER BY end_date ASC")
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    
    def add_contract(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contracts (name, vendor, contract_number, start_date, end_date, 
                                   value, currency, description, document_path, renewal_reminder)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data['name'], data['vendor'], data.get('contract_number'), 
              data.get('start_date'), data.get('end_date'), data.get('value'),
              data.get('currency', 'USD'), data.get('description'), 
              data.get('document_path'), data.get('renewal_reminder', 30)))
        conn.commit()
        conn.close()
    
    def update_contract(self, contract_id, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE contracts SET name=?, vendor=?, contract_number=?, start_date=?,
            end_date=?, value=?, currency=?, description=?, document_path=?,
            renewal_reminder=?, updated_at=CURRENT_TIMESTAMP WHERE id=?
        """, (data['name'], data['vendor'], data.get('contract_number'),
              data.get('start_date'), data.get('end_date'), data.get('value'),
              data.get('currency', 'USD'), data.get('description'),
              data.get('document_path'), data.get('renewal_reminder', 30), contract_id))
        conn.commit()
        conn.close()
    
    def delete_contract(self, contract_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contracts WHERE id=?", (contract_id,))
        conn.commit()
        conn.close()
    
    def get_subscriptions(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subscriptions ORDER BY next_billing_date ASC")
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    
    def add_subscription(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO subscriptions (name, provider, plan, billing_cycle, cost, currency,
                                       start_date, next_billing_date, auto_renew, description, website, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data['name'], data['provider'], data.get('plan'), data.get('billing_cycle'),
              data.get('cost'), data.get('currency', 'USD'), data.get('start_date'),
              data.get('next_billing_date'), data.get('auto_renew', 1), data.get('description'),
              data.get('website'), data.get('notes')))
        conn.commit()
        conn.close()
    
    def update_subscription(self, sub_id, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE subscriptions SET name=?, provider=?, plan=?, billing_cycle=?, cost=?,
            currency=?, start_date=?, next_billing_date=?, auto_renew=?, description=?,
            website=?, notes=?, updated_at=CURRENT_TIMESTAMP WHERE id=?
        """, (data['name'], data['provider'], data.get('plan'), data.get('billing_cycle'),
              data.get('cost'), data.get('currency', 'USD'), data.get('start_date'),
              data.get('next_billing_date'), data.get('auto_renew', 1), data.get('description'),
              data.get('website'), data.get('notes'), sub_id))
        conn.commit()
        conn.close()
    
    def delete_subscription(self, sub_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subscriptions WHERE id=?", (sub_id,))
        conn.commit()
        conn.close()
    
    def get_licenses(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM licenses ORDER BY expiration_date ASC")
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    
    def add_license(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO licenses (name, software, license_key, license_type, version, seats,
                                  activation_date, expiration_date, vendor, order_id, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data['name'], data['software'], data['license_key'], data.get('license_type'),
              data.get('version'), data.get('seats', 1), data.get('activation_date'), data.get('expiration_date'),
              data.get('vendor'), data.get('order_id'), data.get('notes')))
        conn.commit()
        conn.close()
    
    def update_license(self, license_id, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE licenses SET name=?, software=?, license_key=?, license_type=?, version=?, seats=?,
            activation_date=?, expiration_date=?, vendor=?, order_id=?, notes=?,
            updated_at=CURRENT_TIMESTAMP WHERE id=?
        """, (data['name'], data['software'], data['license_key'], data.get('license_type'),
              data.get('version'), data.get('seats', 1), data.get('activation_date'), data.get('expiration_date'),
              data.get('vendor'), data.get('order_id'), data.get('notes'), license_id))
        conn.commit()
        conn.close()
    
    def delete_license(self, license_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM licenses WHERE id=?", (license_id,))
        conn.commit()
        conn.close()
    
    def export_all(self, export_path):
        data = {
            'contracts': self.get_contracts(),
            'subscriptions': self.get_subscriptions(),
            'licenses': self.get_licenses(),
            'exported_at': datetime.now().isoformat()
        }
        with open(export_path, 'w') as f:
            json.dump(data, f, indent=2)
        return export_path
    
    def import_backup(self, import_path):
        with open(import_path, 'r') as f:
            data = json.load(f)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM contracts")
        cursor.execute("DELETE FROM subscriptions")
        cursor.execute("DELETE FROM licenses")
        
        for c in data.get('contracts', []):
            cursor.execute("""
                INSERT INTO contracts (id, name, vendor, contract_number, start_date, end_date,
                                     value, currency, description, document_path, renewal_reminder)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (c.get('id'), c['name'], c['vendor'], c.get('contract_number'), c.get('start_date'),
                  c.get('end_date'), c.get('value'), c.get('currency', 'USD'), c.get('description'),
                  c.get('document_path'), c.get('renewal_reminder', 30)))
        
        for s in data.get('subscriptions', []):
            cursor.execute("""
                INSERT INTO subscriptions (id, name, provider, plan, billing_cycle, cost, currency,
                                           start_date, next_billing_date, auto_renew, description, website, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (s.get('id'), s['name'], s['provider'], s.get('plan'), s.get('billing_cycle'),
                  s.get('cost'), s.get('currency', 'USD'), s.get('start_date'), s.get('next_billing_date'),
                  s.get('auto_renew', 1), s.get('description'), s.get('website'), s.get('notes')))
        
        for l in data.get('licenses', []):
            cursor.execute("""
                INSERT INTO licenses (id, name, software, license_key, license_type, version, seats,
                                      activation_date, expiration_date, vendor, order_id, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (l.get('id'), l['name'], l['software'], l['license_key'], l.get('license_type'),
                  l.get('version'), l.get('seats', 1), l.get('activation_date'), l.get('expiration_date'),
                  l.get('vendor'), l.get('order_id'), l.get('notes')))
        
        conn.commit()
        conn.close()
        return True
