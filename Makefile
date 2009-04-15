wb:	wb.vala
	valac --thread --pkg gtk+-2.0 --pkg webkit-1.0 $< -o $@

gtk:	gtk.vala
	valac --pkg gtk+-2.0 $< -o $@
