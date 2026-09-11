import sys
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, GtkLayerShell, Gdk

class WarningOverlay(Gtk.Window):
    def __init__(self):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self.connect("destroy", self.on_close)

        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.OVERLAY)
        GtkLayerShell.set_exclusive_zone(self, -1)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, True)

        self.set_name("overlay")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=30)
        vbox.set_halign(Gtk.Align.CENTER)
        vbox.set_valign(Gtk.Align.CENTER)
        self.add(vbox)

        label = Gtk.Label(label="⚠ CRITICAL THERMAL WARNING ⚠")
        label.set_name("warning_label")
        vbox.pack_start(label, False, False, 0)

        sub_label = Gtk.Label(label="Volume exceeds safe limits. Chassis temperature critical.")
        sub_label.set_name("subtitle")
        vbox.pack_start(sub_label, False, False, 10)

        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        btn_box.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(btn_box, False, False, 20)

        btn_decrease = Gtk.Button(label="Decrease Volume (60%)")
        btn_decrease.connect("clicked", self.on_decrease)
        btn_box.pack_start(btn_decrease, False, False, 0)

        btn_ignore = Gtk.Button(label="OVERRIDE (Keep Heating)")
        btn_ignore.connect("clicked", self.on_ignore)
        btn_box.pack_start(btn_ignore, False, False, 0)

        self.apply_css()

    def apply_css(self):
        css = b"""
        #overlay {
            background-color: rgba(15, 0, 0, 0.95);
        }
        @keyframes blink {
            0% { opacity: 1.0; text-shadow: 0px 0px 20px red; }
            50% { opacity: 0.6; text-shadow: none; }
            100% { opacity: 1.0; text-shadow: 0px 0px 20px red; }
        }
        #warning_label {
            color: #ff1111;
            font-size: 64px;
            font-weight: 900;
            animation: blink 1.2s ease-in-out infinite;
        }
        #subtitle {
            color: #ffaaaa;
            font-size: 24px;
            font-family: monospace;
        }
        button {
            font-size: 20px;
            font-weight: bold;
            padding: 12px 24px;
            background-color: #220000;
            color: #ffdddd;
            border: 2px solid #ff3333;
            border-radius: 4px;
            box-shadow: 0px 4px 10px rgba(255, 0, 0, 0.2);
        }
        button:hover {
            background-color: #ff3333;
            color: white;
            box-shadow: 0px 0px 15px rgba(255, 0, 0, 0.8);
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_decrease(self, button):
        sys.exit(0)

    def on_ignore(self, button):
        sys.exit(1)

    def on_close(self, window):
        sys.exit(1)

if __name__ == "__main__":
    win = WarningOverlay()
    win.show_all()
    Gtk.main()