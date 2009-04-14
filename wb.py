# ye olde stupid simple web browser

import gobject
import gtk
import os
import urllib
import webkit

gtk.gdk.threads_init()

HOMEPAGE='http://www.google.com/'
APPNAME='wb'

class WebBrowser:

  WB_COUNT=0
  
  def sb_show(self, key, value):
    if key not in self.sb_widgets:
      label = self.sb_widgets[key] = gtk.Label()
      label.set_alignment(0.0, 0.5)
    else:
      label = self.sb_widgets[key]

    label.set_text(value)
    if label not in self.statusbar.get_children():
      self.statusbar.pack_start(label)
    label.show()
    
  def sb_hide(self, key):
    if key in self.sb_widgets:
      self.statusbar.remove(self.sb_widgets[key])

  def poll_downloads(self):
    out = list()
    for download in self.downloads:
      self.sb_show(download.get_suggested_filename(), '%s (%.0f%%)' % (download.get_suggested_filename(), download.get_progress()*100))
      if download.get_progress() >= 1.0:
        out.append(download)
        self.sb_hide(download.get_suggested_filename())
    for download in out:
      self.downloads.remove(download)
    return True

  def __init__(self):
    WebBrowser.WB_COUNT += 1
    
    self.sb_widgets = dict()
    self.downloads = list()
    
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
        self.sb_show('link', uri)
      else:
        self.sb_hide('link')
    self.webview.connect('hovering-over-link', hovering)

    def load_started(view, frame):
      self.sb_show('loading', 'loading ...')
    self.webview.connect('load-started', load_started)

    def load_committed(view, frame):
      self.sb_show('loading', 'loading (0%) ...')
      self.location.set_text(frame.get_uri())
    self.webview.connect('load-committed', load_committed)

    def load_progress_changed(view, progress):
      self.sb_show('loading', 'loading (%d%%) ...' % progress)
    self.webview.connect('load-progress-changed', load_progress_changed)

    def load_finished(view, frame):
      self.location.set_text(frame.get_uri() or '')
      self.sb_hide('loading')
    self.webview.connect('load-finished', load_finished)

    def title_changed(view, frame, title):
      self.window.set_title('%s - %s' % (title, APPNAME))
    self.webview.connect('title-changed', title_changed)

    def create_web_view(view, frame):
      return WebBrowser().webview
    self.webview.connect('create-web-view', create_web_view)
    
    def web_view_ready(view):
      self.show_all()
    self.webview.connect('web-view-ready', web_view_ready)
    
    def download_requested(view, download):
      download.set_destination_uri('file:///home/homey1337/dl/%s' % download.get_suggested_filename())
      self.downloads.append(download)
      return True
    self.webview.connect('download-requested', download_requested)

    vb.pack_start(gtk.HSeparator(), False, True)

    self.statusbar = gtk.HBox()
    vb.pack_end(self.statusbar, False, True)
    
    self.sb_cmd = gtk.Entry()
    def act_cmd(entry):
      self.exec_command(entry.get_text())
    self.sb_cmd.connect('activate', act_cmd)
    def focus_out_event(widget, event):
      self.sb_cmd.hide()
    self.sb_cmd.connect('focus-out-event', focus_out_event)
    self.statusbar.pack_end(self.sb_cmd)
    
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
        elif event.keyval == gtk.keysyms.quoteright:
          self.sb_cmd.show()
          self.sb_cmd.grab_focus()
          self.sb_cmd.select_region(0, -1)
        elif event.keyval == gtk.keysyms.f:
          self.sb_cmd.show()
          self.sb_cmd.grab_focus()
          self.sb_cmd.set_text('/')
          self.sb_cmd.set_position(-1)
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
    
    gobject.timeout_add(1000, self.poll_downloads)

  def load_url(self, url):
    if url.startswith('g '):
      url = 'http://www.google.com/search?q=%s' % urllib.quote_plus(url[2:])
    elif url.startswith('w '):
      url = 'http://en.wikipedia.org/w/index.php?title=Special%%3ASearch&search=%s&go=Go' % urllib.quote_plus(url[2:])
    elif url.find('://') < 0:
      url = 'http://%s' % url
    self.webview.open(url)

  def exec_command(self, cmd):
    if cmd.startswith('/'):
      self.webview.search_text(cmd[1:], False, True, True)
    else:
      l = self.sb_cmd.get_text_length()
      self.sb_cmd.set_text('%s < unknown command' % self.sb_cmd.get_text())
      self.sb_cmd.select_region(l, -1)
  
  def show_all(self):
    self.window.show_all()
    self.sb_cmd.hide()

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
