# ye olde stupid simple web browser

import os
import gtk
import gobject
import webkit
import urllib

gtk.gdk.threads_init()

HOMEPAGE='http://www.google.com/'
APPNAME='wb'

class WebBrowser:

  WB_COUNT=0

  def clear_sb_d(self, d=1000):
    def _c():
      self.statusbar.set_text('')
      self.sb_timeout = None
      return False
    if self.sb_timeout is not None:
      gobject.source_remove(self.sb_timeout)
    self.sb_timeout = gobject.timeout_add(d, _c)

  def load_url(self, url):
    if url.startswith('g '):
      url = 'http://www.google.com/search?q=%s' % urllib.quote_plus(url[2:])
    elif url.startswith('w '):
      url = 'http://en.wikipedia.org/w/index.php?title=Special%%3ASearch&search=%s&go=Go' % urllib.quote_plus(url[2:])
    elif url.find('://') < 0:
      url = 'http://%s' % url
    self.webview.open(url)

  def __init__(self):
    WebBrowser.WB_COUNT += 1

    self.window = gtk.Window()
    def close(*args):
      WebBrowser.WB_COUNT -= 1
      if WebBrowser.WB_COUNT == 0:
        gtk.main_quit()
      else:
        self.window.destroy()
    self.window.connect('delete_event', close)
    self.window.set_title(APPNAME)

    vb = gtk.VBox()
    self.window.add(vb)
    
    self.location = gtk.Entry()
    self.location.set_property('has-frame', False)
    vb.pack_start(self.location, False, True)
    
    vb.pack_start(gtk.HSeparator(), False, True)
    
    def act(entry):
      url = entry.get_text()
      self.load_url(url)
    self.location.connect('activate', act)
    
    self.webview = webkit.WebView()
    vb.pack_start(self.webview, True, True)
    self.webview.get_settings().set_property('enable-plugins', False) # no plugins
    
    def hovering(view, title, uri):
      if uri is not None:
        self.statusbar.set_text(uri)
      else:
        self.statusbar.set_text('')
    self.webview.connect('hovering-over-link', hovering)

    def load_started(view, frame):
      self.statusbar.set_text('loading ...')
    self.webview.connect('load-started', load_started)

    def load_committed(view, frame):
      self.statusbar.set_text('loading %s ...' % frame.get_uri())
      self.location.set_text(frame.get_uri())
    self.webview.connect('load-committed', load_committed)

    def load_progress_changed(view, progress):
      q = self.statusbar.get_text()
      if q.endswith('...'):
        self.statusbar.set_text('%s (%d%%)' % (q, progress))
      else:
        self.statusbar.set_text('%s (%d%%)' % (q[:q.find('...')+4], progress))
    self.webview.connect('load-progress-changed', load_progress_changed)

    def load_finished(view, frame):
      self.statusbar.set_text('done.')
      self.location.set_text(frame.get_uri() or '')
      self.clear_sb_d()
    self.webview.connect('load-finished', load_finished)

    def title_changed(view, frame, title):
      self.window.set_title('%s - wb' % title)
    self.webview.connect('title-changed', title_changed)

    def create_web_view(view, frame):
      return WebBrowser().webview
    self.webview.connect('create-web-view', create_web_view)
    
    def web_view_ready(view):
      self.show_all()
    self.webview.connect('web-view-ready', web_view_ready)

    vb.pack_start(gtk.HSeparator(), False, True)

    self.statusbar = gtk.Entry()
    #self.statusbar.set_alignment(0, 0)
    self.statusbar.set_property('editable', False)
    self.statusbar.set_property('has-frame', False)
    vb.pack_start(self.statusbar, False, True)
    
    self.sb_timeout = None
  
    # keyboard...
    def krl(widget, event):
      key = event.keyval
      if event.state & gtk.gdk.MOD4_MASK:
        "probably won't use too many s- keys"
      elif event.state & gtk.gdk.MOD1_MASK:
        "this is the alt key ..."
      elif event.state & gtk.gdk.CONTROL_MASK:
        "control! where most of my keys live"
        if event.keyval == gtk.keysyms.l:
          self.location.grab_focus()
          self.location.select_region(0, -1)
        elif event.keyval == gtk.keysyms.q:
          gtk.main_quit()
        elif event.keyval == gtk.keysyms.w:
          close()
        elif event.keyval == gtk.keysyms.n:
          self.webview.go_forward()
        elif event.keyval == gtk.keysyms.p:
          self.webview.go_back()
      else:
        "not too many keys here!"
    self.window.connect('key-release-event', krl)

  def show_all(self):
    self.window.show_all()

# make it go!
if __name__ == '__main__':
  import sys

  wb = WebBrowser()

  if len(sys.argv) <= 1:
    wb.load_url(HOMEPAGE)
  else:
    wb.load_url(' '.join(sys.argv[1:]))

  wb.show_all()
  gtk.main()
