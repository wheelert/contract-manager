import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GObject, GLib
from datetime import datetime

class DateEntry(Gtk.Box):
    """A custom date entry widget with calendar popup."""
    
    def __init__(self, **kwargs):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, **kwargs)
        self.set_spacing(8)
        
        # Text entry for date display
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text('YYYY-MM-DD')
        self.entry.set_max_length(10)
        self.entry.connect('changed', self.on_entry_changed)
        self.entry.set_hexpand(True)
        self.append(self.entry)
        
        # Calendar button
        self.button = Gtk.Button()
        icon = Gtk.Image.new_from_icon_name('x-office-calendar-symbolic')
        self.button.set_child(icon)
        self.button.connect('clicked', self.on_button_clicked)
        self.append(self.button)
        
        self.popover = None
        self.calendar = None
        
    def on_entry_changed(self, entry):
        # Validate date format as user types
        text = entry.get_text()
        if len(text) == 10:  # YYYY-MM-DD
            try:
                datetime.strptime(text, '%Y-%m-%d')
                entry.remove_css_class('error')
            except ValueError:
                entry.add_css_class('error')
    
    def on_button_clicked(self, button):
        if self.popover and self.popover.is_visible():
            self.popover.popdown()
            return
        
        self.show_calendar_popup()
    
    def show_calendar_popup(self):
        # Parse current date or use today
        current_text = self.entry.get_text()
        if current_text:
            try:
                date = datetime.strptime(current_text, '%Y-%m-%d')
            except ValueError:
                date = datetime.now()
        else:
            date = datetime.now()
        
        # Create calendar widget
        self.calendar = Gtk.Calendar()
        
        # Set the date using GLib.DateTime
        g_date = GLib.DateTime.new_local(date.year, date.month, date.day, 0, 0, 0)
        self.calendar.select_day(g_date)
        
        # Create popover
        self.popover = Gtk.Popover()
        self.popover.set_child(self.calendar)
        self.popover.set_parent(self.button)
        
        # Connect selection - day-selected signal provides the calendar as first arg
        self.calendar.connect('day-selected', self.on_day_selected)
        
        self.popover.popup()
    
    def on_day_selected(self, calendar):
        # Get selected date using get_date() which returns GLib.DateTime
        date_time = calendar.get_date()
        year = date_time.get_year()
        month = date_time.get_month()
        day = date_time.get_day_of_month()
        
        date_str = f"{year:04d}-{month:02d}-{day:02d}"
        self.entry.set_text(date_str)
        self.popover.popdown()
    
    def get_text(self):
        return self.entry.get_text()
    
    def set_text(self, text):
        self.entry.set_text(text if text else '')
    
    def set_editable(self, editable):
        self.entry.set_editable(editable)
        self.button.set_sensitive(editable)
    
    def grab_focus(self):
        return self.entry.grab_focus()
