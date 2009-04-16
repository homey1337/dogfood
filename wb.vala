public class WebBrowser : Object {
  public Gtk.Window window;
  public Gtk.Entry location;
  public WebKit.WebView webview;
  public Gtk.Entry statusbar;
  
  public void init() {
    this.window = new Gtk.Window(Gtk.WindowType.TOPLEVEL);
    this.window.title = "vwb";
    this.window.destroy += Gtk.main_quit;

    /*
       UI
    */    

    var vbox = new Gtk.VBox(false, 0);
    this.window.add(vbox);
    
    this.location = new Gtk.Entry();
    vbox.pack_start(this.location, false, true, 0);
    
    this.webview = new WebKit.WebView();
    vbox.pack_start(this.webview, true, true, 0);
    
    this.statusbar = new Gtk.Entry();
    vbox.pack_start(this.statusbar, false, true, 0);

    /*
      Signals
    */

    this.location.activate += (source) => {
      this.load_url(source.get_text());
    };

    this.statusbar.activate += (source) => {
      this.run_command(source.get_text());
    };
    
    this.webview.hovering_over_link += (view, title, uri) => {
      // TODO: file a bug against vala so webkit has nullable strings in this signal
      // TODO: better statusbar :)
      if (uri != null) {
        this.statusbar.set_text(uri);
      } else {
        this.statusbar.set_text("");
      }
    };
    
    // TODO: other signals
  }
  
  public void show_all() {
    this.window.show_all();
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
  wb.init();
  wb.show_all();

  wb.webview.open("http://google.com/");

  Gtk.main();
  return 0;
}
