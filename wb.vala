static int main(string[] args) {
  Gtk.init(ref args);

  var window = new Gtk.Window(Gtk.WindowType.TOPLEVEL);
  window.title = "Vala Webkit Test";
  window.destroy += Gtk.main_quit;

  var vbox = new Gtk.VBox(false, 0);
  window.add(vbox);
  
  var location = new Gtk.Entry();
  vbox.pack_start(location, false, true, 0);
  
  var webview = new WebKit.WebView();
  vbox.pack_start(webview, true, true, 0);
  
  var statusbar = new Gtk.Label("statusbar");
  vbox.pack_start(statusbar, false, true, 0);
  
  window.show_all();
  
  Gtk.main();
  return 0;
}
