#!/usr/bin/env python
import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

builder = Gtk.Builder()
builder.add_from_file("./gtranslate.glade")
clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

input_text = builder.get_object('input_text')
output_text = builder.get_object('output_text')
combo_lang = builder.get_object('combo_lang')
        
def copy_output_text(widget):
    textbuffer = output_text.get_buffer()
    start_iter = textbuffer.get_start_iter()
    end_iter = textbuffer.get_end_iter()
    text = textbuffer.get_text(start_iter, end_iter, True) 
    clipboard.set_text(text, -1)
        
def paste_input_text(widget):
    text = clipboard.wait_for_text()
    input_text.get_buffer().set_text(text)

input_paste_button = builder.get_object('input_paste_button')
input_paste_button.connect("clicked", paste_input_text)

output_copy_button = builder.get_object('output_copy_button')
output_copy_button.connect("clicked", copy_output_text)

def run_process(exe):    
    textbuffer = input_text.get_buffer()
    start_iter = textbuffer.get_start_iter()
    end_iter = textbuffer.get_end_iter()
    text = textbuffer.get_text(start_iter, end_iter, True) 
    line = subprocess.check_output(['trans', "-brief", exe, text])
    output_text.get_buffer().set_text(str(line.decode("utf-8")))

def on_combo_lang_changed(combo):
        index = combo.get_active()
        if index == 0:
            run_process(':es')
        if index == 1:
            run_process(':en')
        if index == 2:
            run_process(':de')
        if index == 3:
            run_process(':fr')

def translate(combo):
    index = combo_lang.get_active()
    if index == 0:
        run_process(':es')
    if index == 1:
        run_process(':en')
    if index == 2:
        run_process(':de')
    if index == 3:
        run_process(':fr')

translate_button = builder.get_object('translate_button')
translate_button.connect("clicked", translate)

combo_lang.connect("changed", on_combo_lang_changed)

lang_types = ["Translate the text to spanish", "Translate the text to english", "Translate the text to german", "Translate the text to french"]

for types in lang_types:
    combo_lang.append_text(types)
    combo_lang.set_active(0)


window = builder.get_object("main_window")
window.connect('destroy', Gtk.main_quit)
window.show_all()

Gtk.main()

