public class WebBrowser : Object {
  Gtk.Window window;
  Gtk.Entry location;
  WebKit.WebView webview;
  Gtk.HBox statusbar;
  Gtk.Entry sb_cmd;
  
  public WebBrowser() {
    this.window = new Gtk.Window(Gtk.WindowType.TOPLEVEL);
    this.window.title = "vwb";
    this.window.destroy += Gtk.main_quit;

    /*
       UI
    */    

    var vbox = new Gtk.VBox(false, 0);
    this.window.add(vbox);
    
    this.location = new Gtk.Entry();
    this.location.set_has_frame(false);
    vbox.pack_start(this.location, false, true, 0);
    
    vbox.pack_start(new Gtk.HSeparator(), false, true, 0);
    
    this.webview = new WebKit.WebView();
    vbox.pack_start(this.webview, true, true, 0);
    
    vbox.pack_start(new Gtk.HSeparator(), false, true, 0);

    this.statusbar = new Gtk.HBox(false, 0);
    vbox.pack_start(this.statusbar, false, true, 0);
    
    this.statusbar.pack_end(new Gtk.Label(""), false, true, 0); // avoid "autohide"

    this.sb_cmd = new Gtk.Entry();
    this.sb_cmd.set_has_frame(false);
    this.statusbar.pack_end(this.sb_cmd, false, true, 0);

    /*
      Signals
    */

    this.location.activate += (source) => {
      this.load_url(source.get_text());
    };

    this.sb_cmd.activate += (source) => {
      this.run_command(source.get_text());
    };
    
    this.webview.hovering_over_link += (view, title, uri) => {
      // TODO: better statusbar :)
    };
    
    // TODO: other signals
  }
  
  public void show_all() {
    this.window.show_all();
    this.sb_cmd.hide();
  }

  public void load_url(string url) {
    string u;
    if (url.substring(0, 2) == "g ") {
      u = "http://google.com/search?q=%s".printf(Soup.URI.encode(url.substring(2, -1), ""));
    } else if (url.substring(0, 2) == "w ") {
      u = "http://en.wikipedia.org/w/index.php?title=Special%%3ASearch&search=%s&go=Go".printf(Soup.URI.encode(url.substring(2, -1), ""));
    } else if (!url.contains("://")) {
      u = "http://%s".printf(url);
    } else {
      u = url;
    }
    this.webview.open(u);
  }
  
  public void run_command(string command) {
    // TODO: find
  }
}

static int main(string[] args) {
  Gtk.init(ref args);

  var wb = new WebBrowser();
  wb.show_all();

  wb.load_url("http://google.com/");

  Gtk.main();
  return 0;
}
