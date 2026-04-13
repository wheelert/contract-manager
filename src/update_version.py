with open('database.py', 'r') as f:
    content = f.read()

# Update the licenses table schema to add version column
old_schema = """                license_type TEXT CHECK(license_type IN ('perpetual', 'subscription', 'trial', 'enterprise', 'oem')),
                seats INTEGER DEFAULT 1,"""

new_schema = """                license_type TEXT CHECK(license_type IN ('perpetual', 'subscription', 'trial', 'enterprise', 'oem')),
                version TEXT,
                seats INTEGER DEFAULT 1,"""

content = content.replace(old_schema, new_schema)

# Update add_license INSERT statement
old_add = """            INSERT INTO licenses (name, software, license_key, license_type, seats,
                                  activation_date, expiration_date, vendor, order_id, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data['name'], data['software'], data['license_key'], data.get('license_type'),
              data.get('seats', 1), data.get('activation_date'), data.get('expiration_date'),
              data.get('vendor'), data.get('order_id'), data.get('notes'))"""

new_add = """            INSERT INTO licenses (name, software, license_key, license_type, version, seats,
                                  activation_date, expiration_date, vendor, order_id, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data['name'], data['software'], data['license_key'], data.get('license_type'),
              data.get('version'), data.get('seats', 1), data.get('activation_date'), data.get('expiration_date'),
              data.get('vendor'), data.get('order_id'), data.get('notes'))"""

content = content.replace(old_add, new_add)

# Update update_license UPDATE statement
old_update = """            UPDATE licenses SET name=?, software=?, license_key=?, license_type=?, seats=?,
            activation_date=?, expiration_date=?, vendor=?, order_id=?, notes=?,
            updated_at=CURRENT_TIMESTAMP WHERE id=?
        """, (data['name'], data['software'], data['license_key'], data.get('license_type'),
              data.get('seats', 1), data.get('activation_date'), data.get('expiration_date'),
              data.get('vendor'), data.get('order_id'), data.get('notes'), license_id)"""

new_update = """            UPDATE licenses SET name=?, software=?, license_key=?, license_type=?, version=?, seats=?,
            activation_date=?, expiration_date=?, vendor=?, order_id=?, notes=?,
            updated_at=CURRENT_TIMESTAMP WHERE id=?
        """, (data['name'], data['software'], data['license_key'], data.get('license_type'),
              data.get('version'), data.get('seats', 1), data.get('activation_date'), data.get('expiration_date'),
              data.get('vendor'), data.get('order_id'), data.get('notes'), license_id)"""

content = content.replace(old_update, new_update)

# Update import_backup INSERT for licenses
old_import = """                INSERT INTO licenses (id, name, software, license_key, license_type, seats,
                                      activation_date, expiration_date, vendor, order_id, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (l.get('id'), l['name'], l['software'], l['license_key'], l.get('license_type'),
                  l.get('seats', 1), l.get('activation_date'), l.get('expiration_date'),
                  l.get('vendor'), l.get('order_id'), l.get('notes'))"""

new_import = """                INSERT INTO licenses (id, name, software, license_key, license_type, version, seats,
                                      activation_date, expiration_date, vendor, order_id, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (l.get('id'), l['name'], l['software'], l['license_key'], l.get('license_type'),
                  l.get('version'), l.get('seats', 1), l.get('activation_date'), l.get('expiration_date'),
                  l.get('vendor'), l.get('order_id'), l.get('notes'))"""

content = content.replace(old_import, new_import)

with open('database.py', 'w') as f:
    f.write(content)

print("Database updated with version field!")
