import sys
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, GtkLayerShell, Gdk

class LockScreen(Gtk.Window):
    def __init__(self):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)

        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.OVERLAY)
        GtkLayerShell.set_exclusive_zone(self, -1)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, True)

        # Force Wayland to route all keyboard events to this invisible window
        GtkLayerShell.set_keyboard_mode(self, GtkLayerShell.KeyboardMode.EXCLUSIVE)

        self.connect("key-press-event", self.on_key_press)
        
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
        self.set_app_paintable(True)

        self.apply_css()

        # EventBox absorbs all mouse clicks so they don't reach the video or desktop
        event_box = Gtk.EventBox()
        self.add(event_box)

    def apply_css(self):
        css = b"window { background-color: transparent; }"
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_key_press(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        state = event.state

        ctrl = bool(state & Gdk.ModifierType.CONTROL_MASK)
        alt = bool(state & Gdk.ModifierType.MOD1_MASK)
        super_key = bool(state & Gdk.ModifierType.SUPER_MASK) or bool(state & Gdk.ModifierType.MOD4_MASK)

        if ctrl and alt and super_key and keyname == 'space':
            sys.exit(0)
        
        return True # Absorb and drop all other keystrokes

if __name__ == "__main__":
    win = LockScreen()
    win.show_all()
    Gtk.main()