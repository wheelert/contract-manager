#!/usr/bin/env python3
import gi
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio, GObject, Adw, GLib
from datetime import datetime
from database import Database
from date_widget import DateEntry

class ContractManagerApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.ww.ContractManager',
                        flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.db = Database()
        
    def do_activate(self):
        win = MainWindow(application=self)
        win.present()

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title('Contract Manager')
        self.set_default_size(1200, 800)
        
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.set_content(self.main_box)
        
        self.build_sidebar()
        
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.content_box.set_hexpand(True)
        self.content_box.set_vexpand(True)
        self.main_box.append(self.content_box)
        
        self.header = Adw.HeaderBar()
        self.content_box.append(self.header)
        
        self.view_stack = Gtk.Stack()
        self.view_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.content_box.append(self.view_stack)
        
        self.build_contracts_view()
        self.build_subscriptions_view()
        self.build_licenses_view()
        
        self.show_contracts_view()
        
    def build_sidebar(self):
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar.add_css_class('sidebar')
        sidebar.set_size_request(250, -1)
        self.main_box.append(sidebar)
        
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        title_box.set_margin_top(20)
        title_box.set_margin_bottom(20)
        title_box.set_margin_start(20)
        title_box.set_margin_end(20)
        title_box.set_halign(Gtk.Align.CENTER)
        
        title_label = Gtk.Label(label='Contract Manager')
        title_label.add_css_class('title-2')
        title_box.append(title_label)
        sidebar.append(title_box)
        
        nav_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        nav_box.set_spacing(8)
        nav_box.set_margin_start(12)
        nav_box.set_margin_end(12)
        sidebar.append(nav_box)
        
        self.contracts_btn = Gtk.Button(label='Contracts')
        self.contracts_btn.set_halign(Gtk.Align.FILL)
        self.contracts_btn.connect('clicked', self.on_contracts_clicked)
        nav_box.append(self.contracts_btn)
        
        self.subscriptions_btn = Gtk.Button(label='Subscriptions')
        self.subscriptions_btn.set_halign(Gtk.Align.FILL)
        self.subscriptions_btn.connect('clicked', self.on_subscriptions_clicked)
        nav_box.append(self.subscriptions_btn)
        
        self.licenses_btn = Gtk.Button(label='License Keys')
        self.licenses_btn.set_halign(Gtk.Align.FILL)
        self.licenses_btn.connect('clicked', self.on_licenses_clicked)
        nav_box.append(self.licenses_btn)
        
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(20)
        separator.set_margin_bottom(20)
        sidebar.append(separator)
        
        actions_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        actions_box.set_spacing(8)
        actions_box.set_margin_start(12)
        actions_box.set_margin_end(12)
        sidebar.append(actions_box)
        
        export_btn = Gtk.Button(label='Export Database')
        export_btn.set_halign(Gtk.Align.FILL)
        export_btn.connect('clicked', self.on_export_clicked)
        actions_box.append(export_btn)
        
        import_btn = Gtk.Button(label='Import Database')
        import_btn.set_halign(Gtk.Align.FILL)
        import_btn.connect('clicked', self.on_import_clicked)
        actions_box.append(import_btn)
        
    def build_contracts_view(self):
        self.contracts_view = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.view_stack.add_named(self.contracts_view, 'contracts')
        
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        toolbar.set_margin_top(12)
        toolbar.set_margin_bottom(12)
        toolbar.set_margin_start(12)
        toolbar.set_margin_end(12)
        toolbar.set_spacing(8)
        self.contracts_view.append(toolbar)
        
        add_btn = Gtk.Button(label='Add Contract')
        add_btn.add_css_class('suggested-action')
        add_btn.connect('clicked', self.on_add_contract)
        toolbar.append(add_btn)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        self.contracts_view.append(scrolled)
        
        self.contracts_store = Gtk.ListStore(str, str, str, str, str, str)
        self.contracts_tree = Gtk.TreeView(model=self.contracts_store)
        
        columns = [
            ('Name', 0, True),
            ('Vendor', 1, True),
            ('Contract #', 2, True),
            ('Start Date', 3, True),
            ('End Date', 4, True),
            ('Value', 5, True)
        ]
        
        for title, col_id, expand in columns:
            renderer = Gtk.CellRendererText()
            renderer.set_property('ellipsize', True)
            column = Gtk.TreeViewColumn(title, renderer, text=col_id)
            column.set_resizable(True)
            column.set_expand(expand)
            column.set_sort_column_id(col_id)
            column.set_clickable(True)
            self.contracts_tree.append_column(column)
        
        self.contracts_tree.set_headers_clickable(True)
        self.contracts_tree.connect('row-activated', self.on_contract_activated)
        scrolled.set_child(self.contracts_tree)
        
        self.refresh_contracts()
        
    def build_subscriptions_view(self):
        self.subscriptions_view = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.view_stack.add_named(self.subscriptions_view, 'subscriptions')
        
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        toolbar.set_margin_top(12)
        toolbar.set_margin_bottom(12)
        toolbar.set_margin_start(12)
        toolbar.set_margin_end(12)
        toolbar.set_spacing(8)
        self.subscriptions_view.append(toolbar)
        
        add_btn = Gtk.Button(label='Add Subscription')
        add_btn.add_css_class('suggested-action')
        add_btn.connect('clicked', self.on_add_subscription)
        toolbar.append(add_btn)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        self.subscriptions_view.append(scrolled)
        
        self.subscriptions_store = Gtk.ListStore(str, str, str, str, str, str, str)
        self.subscriptions_tree = Gtk.TreeView(model=self.subscriptions_store)
        
        columns = [
            ('Name', 0, True),
            ('Provider', 1, True),
            ('Plan', 2, True),
            ('Billing Cycle', 3, True),
            ('Cost', 4, True),
            ('Next Billing', 5, True),
            ('Auto-Renew', 6, False)
        ]
        
        for title, col_id, expand in columns:
            renderer = Gtk.CellRendererText()
            renderer.set_property('ellipsize', True)
            column = Gtk.TreeViewColumn(title, renderer, text=col_id)
            column.set_resizable(True)
            column.set_expand(expand)
            column.set_sort_column_id(col_id)
            column.set_clickable(True)
            self.subscriptions_tree.append_column(column)
        
        self.subscriptions_tree.set_headers_clickable(True)
        self.subscriptions_tree.connect('row-activated', self.on_subscription_activated)
        scrolled.set_child(self.subscriptions_tree)
        
        self.refresh_subscriptions()
        
    def build_licenses_view(self):
        self.licenses_view = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.view_stack.add_named(self.licenses_view, 'licenses')
        
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        toolbar.set_margin_top(12)
        toolbar.set_margin_bottom(12)
        toolbar.set_margin_start(12)
        toolbar.set_margin_end(12)
        toolbar.set_spacing(8)
        self.licenses_view.append(toolbar)
        
        add_btn = Gtk.Button(label='Add License')
        add_btn.add_css_class('suggested-action')
        add_btn.connect('clicked', self.on_add_license)
        toolbar.append(add_btn)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        self.licenses_view.append(scrolled)
        
        self.licenses_store = Gtk.ListStore(str, str, str, str, str, str, str)
        self.licenses_tree = Gtk.TreeView(model=self.licenses_store)
        
        columns = [
            ('Name', 0, True),
            ('Software', 1, True),
            ('License Key', 2, True),
            ('Type', 3, True),
            ('Seats', 4, False),
            ('Activation', 5, True),
            ('Expiration', 6, True)
        ]
        
        for title, col_id, expand in columns:
            renderer = Gtk.CellRendererText()
            renderer.set_property('ellipsize', True)
            column = Gtk.TreeViewColumn(title, renderer, text=col_id)
            column.set_resizable(True)
            column.set_expand(expand)
            column.set_sort_column_id(col_id)
            column.set_clickable(True)
            self.licenses_tree.append_column(column)
        
        self.licenses_tree.set_headers_clickable(True)
        self.licenses_tree.connect('row-activated', self.on_license_activated)
        scrolled.set_child(self.licenses_tree)
        
        self.refresh_licenses()
    
    def refresh_contracts(self):
        self.contracts_store.clear()
        contracts = self.get_application().db.get_contracts()
        for c in contracts:
            self.contracts_store.append([
                c['name'],
                c['vendor'],
                c['contract_number'] or '',
                c['start_date'] or '',
                c['end_date'] or '',
                f"{c['currency']} {c['value']}" if c['value'] else ''
            ])
    
    def refresh_subscriptions(self):
        self.subscriptions_store.clear()
        subs = self.get_application().db.get_subscriptions()
        for s in subs:
            self.subscriptions_store.append([
                s['name'],
                s['provider'],
                s['plan'] or '',
                s['billing_cycle'] or '',
                f"{s['currency']} {s['cost']}" if s['cost'] else '',
                s['next_billing_date'] or '',
                'Yes' if s['auto_renew'] else 'No'
            ])
    
    def refresh_licenses(self):
        self.licenses_store.clear()
        licenses = self.get_application().db.get_licenses()
        for l in licenses:
            key_display = l['license_key']
            if len(key_display) > 20:
                key_display = key_display[:20] + '...'
            self.licenses_store.append([
                l['name'],
                l['software'],
                key_display,
                l['license_type'] or '',
                str(l['seats']) if l['seats'] else '1',
                l['activation_date'] or '',
                l['expiration_date'] or ''
            ])
    
    def show_contracts_view(self):
        self.view_stack.set_visible_child_name('contracts')
        self.header.set_title_widget(Gtk.Label(label='Contracts'))
        
    def show_subscriptions_view(self):
        self.view_stack.set_visible_child_name('subscriptions')
        self.header.set_title_widget(Gtk.Label(label='Subscriptions'))
        
    def show_licenses_view(self):
        self.view_stack.set_visible_child_name('licenses')
        self.header.set_title_widget(Gtk.Label(label='License Keys'))
    
    def on_contracts_clicked(self, btn):
        self.show_contracts_view()
        
    def on_subscriptions_clicked(self, btn):
        self.show_subscriptions_view()
        
    def on_licenses_clicked(self, btn):
        self.show_licenses_view()
    
    def on_add_contract(self, btn):
        dialog = ContractDialog(self, None)
        dialog.present()
        
    def on_add_subscription(self, btn):
        dialog = SubscriptionDialog(self, None)
        dialog.present()
        
    def on_add_license(self, btn):
        dialog = LicenseDialog(self, None)
        dialog.present()
    
    def on_contract_activated(self, tree, path, column):
        contracts = self.get_application().db.get_contracts()
        if path.get_indices()[0] < len(contracts):
            dialog = ContractDialog(self, contracts[path.get_indices()[0]])
            dialog.present()
    
    def on_subscription_activated(self, tree, path, column):
        subs = self.get_application().db.get_subscriptions()
        if path.get_indices()[0] < len(subs):
            dialog = SubscriptionDialog(self, subs[path.get_indices()[0]])
            dialog.present()
    
    def on_license_activated(self, tree, path, column):
        licenses = self.get_application().db.get_licenses()
        if path.get_indices()[0] < len(licenses):
            dialog = LicenseDialog(self, licenses[path.get_indices()[0]])
            dialog.present()
    
    def on_export_clicked(self, btn):
        def on_save(dialog, result):
            try:
                file = dialog.save_finish(result)
                if file:
                    path = file.get_path()
                    try:
                        self.get_application().db.export_all(path)
                        self.show_toast('Database exported successfully')
                    except Exception as e:
                        self.show_error_dialog(f'Export failed: {e}')
            except GLib.Error as e:
                if e.code != Gtk.DialogError.DISMISSED:
                    self.show_error_dialog(f'Export failed: {e}')
        
        dialog = Gtk.FileDialog.new()
        dialog.set_title('Export Database')
        dialog.set_initial_name('contract_backup.json')
        
        filter_store = Gio.ListStore.new(Gtk.FileFilter)
        filter_json = Gtk.FileFilter()
        filter_json.set_name('JSON files')
        filter_json.add_pattern('*.json')
        filter_store.append(filter_json)
        dialog.set_filters(filter_store)
        
        dialog.save(self, None, on_save)
    
    def on_import_clicked(self, btn):
        def on_open(dialog, result):
            try:
                file = dialog.open_finish(result)
                if file:
                    path = file.get_path()
                    try:
                        self.get_application().db.import_backup(path)
                        self.refresh_contracts()
                        self.refresh_subscriptions()
                        self.refresh_licenses()
                        self.show_toast('Database imported successfully')
                    except Exception as e:
                        self.show_error_dialog(f'Import failed: {e}')
            except GLib.Error as e:
                if e.code != Gtk.DialogError.DISMISSED:
                    self.show_error_dialog(f'Import failed: {e}')
        
        dialog = Gtk.FileDialog.new()
        dialog.set_title('Import Database')
        
        filter_store = Gio.ListStore.new(Gtk.FileFilter)
        filter_json = Gtk.FileFilter()
        filter_json.set_name('JSON files')
        filter_json.add_pattern('*.json')
        filter_store.append(filter_json)
        dialog.set_filters(filter_store)
        
        dialog.open(self, None, on_open)
    
    def show_toast(self, message):
        pass  # Toast overlay would go here
        
    def show_error_dialog(self, message):
        dialog = Adw.MessageDialog.new(self, 'Error', message)
        dialog.add_response('ok', 'OK')
        dialog.present()

class ContractDialog(Adw.Window):
    def __init__(self, parent, contract=None):
        super().__init__(transient_for=parent)
        self.parent = parent
        self.contract = contract
        self.is_edit = contract is not None
        
        self.set_title('Edit Contract' if self.is_edit else 'Add Contract')
        self.set_default_size(500, 600)
        self.set_modal(True)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(content)
        
        header = Adw.HeaderBar()
        content.append(header)
        
        form = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        form.set_margin_top(20)
        form.set_margin_bottom(20)
        form.set_margin_start(20)
        form.set_margin_end(20)
        form.set_spacing(12)
        content.append(form)
        
        self.name_entry = self.create_entry(form, 'Name *')
        self.vendor_entry = self.create_entry(form, 'Vendor *')
        self.contract_entry = self.create_entry(form, 'Contract Number')
        self.start_entry = self.create_date_entry(form, 'Start Date')
        self.end_entry = self.create_date_entry(form, 'End Date')
        self.value_entry = self.create_entry(form, 'Value')
        self.currency_entry = self.create_entry(form, 'Currency')
        self.desc_entry = self.create_text_view(form, 'Description')
        self.reminder_entry = self.create_entry(form, 'Renewal Reminder (days)')
        
        if contract:
            self.name_entry.set_text(contract['name'])
            self.vendor_entry.set_text(contract['vendor'])
            if contract['contract_number']:
                self.contract_entry.set_text(contract['contract_number'])
            if contract['start_date']:
                self.start_entry.set_text(contract['start_date'])
            if contract['end_date']:
                self.end_entry.set_text(contract['end_date'])
            if contract['value']:
                self.value_entry.set_text(str(contract['value']))
            if contract['currency']:
                self.currency_entry.set_text(contract['currency'])
            if contract['description']:
                buffer = self.desc_entry.get_buffer()
                buffer.set_text(contract['description'])
            self.reminder_entry.set_text(str(contract.get('renewal_reminder', 30)))
        else:
            self.currency_entry.set_text('USD')
            self.reminder_entry.set_text('30')
        
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        btn_box.set_spacing(8)
        btn_box.set_halign(Gtk.Align.END)
        btn_box.set_margin_top(20)
        form.append(btn_box)
        
        cancel_btn = Gtk.Button(label='Cancel')
        cancel_btn.connect('clicked', lambda x: self.close())
        btn_box.append(cancel_btn)
        
        save_btn = Gtk.Button(label='Save')
        save_btn.add_css_class('suggested-action')
        save_btn.connect('clicked', self.on_save)
        btn_box.append(save_btn)
        
        if self.is_edit:
            delete_btn = Gtk.Button(label='Delete')
            delete_btn.add_css_class('destructive-action')
            delete_btn.connect('clicked', self.on_delete)
            btn_box.append(delete_btn)
    
    def create_entry(self, parent, label_text):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_spacing(4)
        parent.append(box)
        
        label = Gtk.Label(label=label_text)
        label.set_halign(Gtk.Align.START)
        box.append(label)
        
        entry = Gtk.Entry()
        entry.set_halign(Gtk.Align.FILL)
        box.append(entry)
        return entry
    
    def create_date_entry(self, parent, label_text):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_spacing(4)
        parent.append(box)
        
        label = Gtk.Label(label=label_text)
        label.set_halign(Gtk.Align.START)
        box.append(label)
        
        date_entry = DateEntry()
        date_entry.set_halign(Gtk.Align.FILL)
        box.append(date_entry)
        return date_entry
    
    def create_text_view(self, parent, label_text):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_spacing(4)
        parent.append(box)
        
        label = Gtk.Label(label=label_text)
        label.set_halign(Gtk.Align.START)
        box.append(label)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_min_content_height(100)
        box.append(scrolled)
        
        text_view = Gtk.TextView()
        text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolled.set_child(text_view)
        return text_view
    
    def on_save(self, btn):
        name = self.name_entry.get_text().strip()
        vendor = self.vendor_entry.get_text().strip()
        
        if not name or not vendor:
            self.show_error('Name and vendor are required')
            return
        
        data = {
            'name': name,
            'vendor': vendor,
            'contract_number': self.contract_entry.get_text().strip() or None,
            'start_date': self.start_entry.get_text().strip() or None,
            'end_date': self.end_entry.get_text().strip() or None,
            'value': float(self.value_entry.get_text()) if self.value_entry.get_text() else None,
            'currency': self.currency_entry.get_text().strip() or 'USD',
            'description': self.desc_entry.get_buffer().get_text(
                self.desc_entry.get_buffer().get_start_iter(),
                self.desc_entry.get_buffer().get_end_iter(),
                False
            ).strip() or None,
            'renewal_reminder': int(self.reminder_entry.get_text()) if self.reminder_entry.get_text() else 30
        }
        
        db = self.parent.get_application().db
        if self.is_edit:
            db.update_contract(self.contract['id'], data)
        else:
            db.add_contract(data)
        
        self.parent.refresh_contracts()
        self.close()
    
    def on_delete(self, btn):
        dialog = Adw.MessageDialog.new(self, 'Delete Contract?', 
                                       'Are you sure you want to delete this contract?')
        dialog.add_response('cancel', 'Cancel')
        dialog.add_response('delete', 'Delete')
        dialog.set_response_appearance('delete', Adw.ResponseAppearance.DESTRUCTIVE)
        
        def on_response(dialog, response):
            if response == 'delete':
                self.parent.get_application().db.delete_contract(self.contract['id'])
                self.parent.refresh_contracts()
                self.close()
            dialog.destroy()
        
        dialog.connect('response', on_response)
        dialog.present()
    
    def show_error(self, message):
        dialog = Adw.MessageDialog.new(self, 'Error', message)
        dialog.add_response('ok', 'OK')
        dialog.present()

class SubscriptionDialog(Adw.Window):
    def __init__(self, parent, subscription=None):
        super().__init__(transient_for=parent)
        self.parent = parent
        self.subscription = subscription
        self.is_edit = subscription is not None
        
        self.set_title('Edit Subscription' if self.is_edit else 'Add Subscription')
        self.set_default_size(500, 700)
        self.set_modal(True)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(content)
        
        header = Adw.HeaderBar()
        content.append(header)
        
        form = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        form.set_margin_top(20)
        form.set_margin_bottom(20)
        form.set_margin_start(20)
        form.set_margin_end(20)
        form.set_spacing(12)
        content.append(form)
        
        self.name_entry = self.create_entry(form, 'Name *')
        self.provider_entry = self.create_entry(form, 'Provider *')
        self.plan_entry = self.create_entry(form, 'Plan')
        
        # Billing cycle dropdown
        self.billing_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.billing_box.set_spacing(4)
        form.append(self.billing_box)
        
        billing_label = Gtk.Label(label='Billing Cycle')
        billing_label.set_halign(Gtk.Align.START)
        self.billing_box.append(billing_label)
        
        self.billing_combo = Gtk.DropDown()
        billing_model = Gtk.StringList()
        for cycle in ['', 'monthly', 'yearly', 'quarterly', 'weekly']:
            billing_model.append(cycle)
        self.billing_combo.set_model(billing_model)
        self.billing_box.append(self.billing_combo)
        
        self.cost_entry = self.create_entry(form, 'Cost')
        self.currency_entry = self.create_entry(form, 'Currency')
        self.start_entry = self.create_date_entry(form, 'Start Date')
        self.next_entry = self.create_date_entry(form, 'Next Billing Date')
        
        # Auto-renew switch
        renew_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        renew_box.set_spacing(8)
        form.append(renew_box)
        
        renew_label = Gtk.Label(label='Auto-Renew')
        renew_box.append(renew_label)
        
        self.renew_switch = Gtk.Switch()
        self.renew_switch.set_active(True)
        renew_box.append(self.renew_switch)
        
        self.website_entry = self.create_entry(form, 'Website')
        self.desc_entry = self.create_text_view(form, 'Description')
        self.notes_entry = self.create_text_view(form, 'Notes')
        
        if subscription:
            self.name_entry.set_text(subscription['name'])
            self.provider_entry.set_text(subscription['provider'])
            if subscription['plan']:
                self.plan_entry.set_text(subscription['plan'])
            if subscription['billing_cycle']:
                cycles = ['', 'monthly', 'yearly', 'quarterly', 'weekly']
                if subscription['billing_cycle'] in cycles:
                    self.billing_combo.set_selected(cycles.index(subscription['billing_cycle']))
            if subscription['cost']:
                self.cost_entry.set_text(str(subscription['cost']))
            if subscription['currency']:
                self.currency_entry.set_text(subscription['currency'])
            if subscription['start_date']:
                self.start_entry.set_text(subscription['start_date'])
            if subscription['next_billing_date']:
                self.next_entry.set_text(subscription['next_billing_date'])
            self.renew_switch.set_active(bool(subscription['auto_renew']))
            if subscription['website']:
                self.website_entry.set_text(subscription['website'])
            if subscription['description']:
                buffer = self.desc_entry.get_buffer()
                buffer.set_text(subscription['description'])
            if subscription['notes']:
                buffer = self.notes_entry.get_buffer()
                buffer.set_text(subscription['notes'])
        else:
            self.currency_entry.set_text('USD')
        
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        btn_box.set_spacing(8)
        btn_box.set_halign(Gtk.Align.END)
        btn_box.set_margin_top(20)
        form.append(btn_box)
        
        cancel_btn = Gtk.Button(label='Cancel')
        cancel_btn.connect('clicked', lambda x: self.close())
        btn_box.append(cancel_btn)
        
        save_btn = Gtk.Button(label='Save')
        save_btn.add_css_class('suggested-action')
        save_btn.connect('clicked', self.on_save)
        btn_box.append(save_btn)
        
        if self.is_edit:
            delete_btn = Gtk.Button(label='Delete')
            delete_btn.add_css_class('destructive-action')
            delete_btn.connect('clicked', self.on_delete)
            btn_box.append(delete_btn)
    
    def create_entry(self, parent, label_text):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_spacing(4)
        parent.append(box)
        
        label = Gtk.Label(label=label_text)
        label.set_halign(Gtk.Align.START)
        box.append(label)
        
        entry = Gtk.Entry()
        entry.set_halign(Gtk.Align.FILL)
        box.append(entry)
        return entry
    
    def create_date_entry(self, parent, label_text):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_spacing(4)
        parent.append(box)
        
        label = Gtk.Label(label=label_text)
        label.set_halign(Gtk.Align.START)
        box.append(label)
        
        date_entry = DateEntry()
        date_entry.set_halign(Gtk.Align.FILL)
        box.append(date_entry)
        return date_entry
    
    def create_text_view(self, parent, label_text):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_spacing(4)
        parent.append(box)
        
        label = Gtk.Label(label=label_text)
        label.set_halign(Gtk.Align.START)
        box.append(label)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_min_content_height(80)
        box.append(scrolled)
        
        text_view = Gtk.TextView()
        text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolled.set_child(text_view)
        return text_view
    
    def on_save(self, btn):
        name = self.name_entry.get_text().strip()
        provider = self.provider_entry.get_text().strip()
        
        if not name or not provider:
            self.show_error('Name and provider are required')
            return
        
        billing_cycle_idx = self.billing_combo.get_selected()
        cycles = ['', 'monthly', 'yearly', 'quarterly', 'weekly']
        billing_cycle = cycles[billing_cycle_idx] if billing_cycle_idx > 0 else None
        
        data = {
            'name': name,
            'provider': provider,
            'plan': self.plan_entry.get_text().strip() or None,
            'billing_cycle': billing_cycle,
            'cost': float(self.cost_entry.get_text()) if self.cost_entry.get_text() else None,
            'currency': self.currency_entry.get_text().strip() or 'USD',
            'start_date': self.start_entry.get_text().strip() or None,
            'next_billing_date': self.next_entry.get_text().strip() or None,
            'auto_renew': 1 if self.renew_switch.get_active() else 0,
            'website': self.website_entry.get_text().strip() or None,
            'description': self.desc_entry.get_buffer().get_text(
                self.desc_entry.get_buffer().get_start_iter(),
                self.desc_entry.get_buffer().get_end_iter(),
                False
            ).strip() or None,
            'notes': self.notes_entry.get_buffer().get_text(
                self.notes_entry.get_buffer().get_start_iter(),
                self.notes_entry.get_buffer().get_end_iter(),
                False
            ).strip() or None
        }
        
        db = self.parent.get_application().db
        if self.is_edit:
            db.update_subscription(self.subscription['id'], data)
        else:
            db.add_subscription(data)
        
        self.parent.refresh_subscriptions()
        self.close()
    
    def on_delete(self, btn):
        dialog = Adw.MessageDialog.new(self, 'Delete Subscription?', 
                                       'Are you sure you want to delete this subscription?')
        dialog.add_response('cancel', 'Cancel')
        dialog.add_response('delete', 'Delete')
        dialog.set_response_appearance('delete', Adw.ResponseAppearance.DESTRUCTIVE)
        
        def on_response(dialog, response):
            if response == 'delete':
                self.parent.get_application().db.delete_subscription(self.subscription['id'])
                self.parent.refresh_subscriptions()
                self.close()
            dialog.destroy()
        
        dialog.connect('response', on_response)
        dialog.present()
    
    def show_error(self, message):
        dialog = Adw.MessageDialog.new(self, 'Error', message)
        dialog.add_response('ok', 'OK')
        dialog.present()

class LicenseDialog(Adw.Window):
    def __init__(self, parent, license_data=None):
        super().__init__(transient_for=parent)
        self.parent = parent
        self.license_data = license_data
        self.is_edit = license_data is not None
        
        self.set_title('Edit License' if self.is_edit else 'Add License')
        self.set_default_size(500, 650)
        self.set_modal(True)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(content)
        
        header = Adw.HeaderBar()
        content.append(header)
        
        form = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        form.set_margin_top(20)
        form.set_margin_bottom(20)
        form.set_margin_start(20)
        form.set_margin_end(20)
        form.set_spacing(12)
        content.append(form)
        
        self.name_entry = self.create_entry(form, 'Name *')
        self.software_entry = self.create_entry(form, 'Software *')
        self.key_entry = self.create_entry(form, 'License Key *')
        
        # License type dropdown
        type_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        type_box.set_spacing(4)
        form.append(type_box)
        
        type_label = Gtk.Label(label='License Type')
        type_label.set_halign(Gtk.Align.START)
        type_box.append(type_label)
        
        self.type_combo = Gtk.DropDown()
        type_model = Gtk.StringList()
        for t in ['', 'perpetual', 'subscription', 'trial', 'enterprise', 'oem']:
            type_model.append(t)
        self.type_combo.set_model(type_model)
        type_box.append(self.type_combo)
        
        self.seats_entry = self.create_entry(form, 'Seats')
        self.activation_entry = self.create_date_entry(form, 'Activation Date')
        self.expiration_entry = self.create_date_entry(form, 'Expiration Date')
        self.vendor_entry = self.create_entry(form, 'Vendor')
        self.order_entry = self.create_entry(form, 'Order ID')
        self.notes_entry = self.create_text_view(form, 'Notes')
        
        if license_data:
            self.name_entry.set_text(license_data['name'])
            self.software_entry.set_text(license_data['software'])
            self.key_entry.set_text(license_data['license_key'])
            
            if license_data['license_type']:
                types = ['', 'perpetual', 'subscription', 'trial', 'enterprise', 'oem']
                if license_data['license_type'] in types:
                    self.type_combo.set_selected(types.index(license_data['license_type']))
            
            self.seats_entry.set_text(str(license_data['seats']) if license_data['seats'] else '1')
            
            if license_data['activation_date']:
                self.activation_entry.set_text(license_data['activation_date'])
            if license_data['expiration_date']:
                self.expiration_entry.set_text(license_data['expiration_date'])
            if license_data['vendor']:
                self.vendor_entry.set_text(license_data['vendor'])
            if license_data['order_id']:
                self.order_entry.set_text(license_data['order_id'])
            if license_data['notes']:
                buffer = self.notes_entry.get_buffer()
                buffer.set_text(license_data['notes'])
        else:
            self.seats_entry.set_text('1')
        
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        btn_box.set_spacing(8)
        btn_box.set_halign(Gtk.Align.END)
        btn_box.set_margin_top(20)
        form.append(btn_box)
        
        cancel_btn = Gtk.Button(label='Cancel')
        cancel_btn.connect('clicked', lambda x: self.close())
        btn_box.append(cancel_btn)
        
        save_btn = Gtk.Button(label='Save')
        save_btn.add_css_class('suggested-action')
        save_btn.connect('clicked', self.on_save)
        btn_box.append(save_btn)
        
        if self.is_edit:
            delete_btn = Gtk.Button(label='Delete')
            delete_btn.add_css_class('destructive-action')
            delete_btn.connect('clicked', self.on_delete)
            btn_box.append(delete_btn)
    
    def create_entry(self, parent, label_text):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_spacing(4)
        parent.append(box)
        
        label = Gtk.Label(label=label_text)
        label.set_halign(Gtk.Align.START)
        box.append(label)
        
        entry = Gtk.Entry()
        entry.set_halign(Gtk.Align.FILL)
        box.append(entry)
        return entry
    
    def create_date_entry(self, parent, label_text):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_spacing(4)
        parent.append(box)
        
        label = Gtk.Label(label=label_text)
        label.set_halign(Gtk.Align.START)
        box.append(label)
        
        date_entry = DateEntry()
        date_entry.set_halign(Gtk.Align.FILL)
        box.append(date_entry)
        return date_entry
    
    def create_text_view(self, parent, label_text):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.set_spacing(4)
        parent.append(box)
        
        label = Gtk.Label(label=label_text)
        label.set_halign(Gtk.Align.START)
        box.append(label)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_min_content_height(100)
        box.append(scrolled)
        
        text_view = Gtk.TextView()
        text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolled.set_child(text_view)
        return text_view
    
    def on_save(self, btn):
        name = self.name_entry.get_text().strip()
        software = self.software_entry.get_text().strip()
        license_key = self.key_entry.get_text().strip()
        
        if not name or not software or not license_key:
            self.show_error('Name, software, and license key are required')
            return
        
        type_idx = self.type_combo.get_selected()
        types = ['', 'perpetual', 'subscription', 'trial', 'enterprise', 'oem']
        license_type = types[type_idx] if type_idx > 0 else None
        
        data = {
            'name': name,
            'software': software,
            'license_key': license_key,
            'license_type': license_type,
            'seats': int(self.seats_entry.get_text()) if self.seats_entry.get_text() else 1,
            'activation_date': self.activation_entry.get_text().strip() or None,
            'expiration_date': self.expiration_entry.get_text().strip() or None,
            'vendor': self.vendor_entry.get_text().strip() or None,
            'order_id': self.order_entry.get_text().strip() or None,
            'notes': self.notes_entry.get_buffer().get_text(
                self.notes_entry.get_buffer().get_start_iter(),
                self.notes_entry.get_buffer().get_end_iter(),
                False
            ).strip() or None
        }
        
        db = self.parent.get_application().db
        if self.is_edit:
            db.update_license(self.license_data['id'], data)
        else:
            db.add_license(data)
        
        self.parent.refresh_licenses()
        self.close()
    
    def on_delete(self, btn):
        dialog = Adw.MessageDialog.new(self, 'Delete License?', 
                                       'Are you sure you want to delete this license?')
        dialog.add_response('cancel', 'Cancel')
        dialog.add_response('delete', 'Delete')
        dialog.set_response_appearance('delete', Adw.ResponseAppearance.DESTRUCTIVE)
        
        def on_response(dialog, response):
            if response == 'delete':
                self.parent.get_application().db.delete_license(self.license_data['id'])
                self.parent.refresh_licenses()
                self.close()
            dialog.destroy()
        
        dialog.connect('response', on_response)
        dialog.present()
    
    def show_error(self, message):
        dialog = Adw.MessageDialog.new(self, 'Error', message)
        dialog.add_response('ok', 'OK')
        dialog.present()

def main():
    app = ContractManagerApp()
    app.run(sys.argv)

if __name__ == '__main__':
    main()
