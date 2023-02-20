import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser,font,filedialog,messagebox
import os
#-----------------------------------


file_name = None
x = "AceOFHeart"
main_application = tk.Tk()
main_application.geometry("1280x720")
main_application.title("AceOfHeart")





#--------------------------------------------------















#---------------------------------------------------

#---------------------------------------------------[Methods OF File Options]------------------------------------------------------

def new_file(event=None):
    main_application.title("Untitled")
    global file_name 
    scroll.delete(1.0, END)
    
def open_file(event=None):
    input_file_name = tk.filedialog.askopenfilename(defaultextension=".txt",
                                                    filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt"),("HTML", "*.html"),("CSS", "*.css"),("JavaScript", "*.js")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        main_application.title('{} - {}'.format(os.path.basename(file_name),x))
        scroll.delete(1.0, END)
        with open(file_name) as _file:
            scroll.insert(1.0, _file.read())
     
def write_to_file(file_name):
    try:
        content = scroll.get(1.0, 'end')
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except IOError:
        pass  


def save_as(event=None):
    input_file_name = tk.filedialog.asksaveasfilename(defaultextension=".txt",
                                                      filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt"),("HTML", "*.html"),("CSS", "*.css"),("JavaScript", "*.js")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        main_application.title('{} - {}'.format(os.path.basename(file_name),x))
    return "break"

def browseFiles(event=None): 
    filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("Text files","*.txt*"),("all files","*.*")))

def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
    return "break"

def exit_editor(event=None):
    if tk.messagebox.askokcancel("EXIT", "Are you sure?"):
        main_application.destroy()
#---------------------------------------------------[Methods OF EDIT Options]------------------------------------------------------

def cut(event=None):
    scroll.text.event_generate("<<Cut>>")
    return "break"

def copy(event=None):
    scroll.text.event_generate("<<Copy>>")
    return "break"

def paste(event=None):
    scroll.text.event_generate("<<Paste>>")
    return "break"

def clearAll(event=None):
    scroll.text.delete(1.0,END)

def find_text(event=None):
    search_toplevel = Toplevel(main_application)
    search_toplevel.title('Find Text')
    search_toplevel.transient(main_application)
    search_toplevel.resizable(False, False)
    Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')
    search_entry_widget = Entry(search_toplevel, width=25)
    search_entry_widget.grid(row=0, column=1, padx=20, pady=20, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(search_toplevel, text='Ignore Case', variable=ignore_case_value).grid(row=1, column=1, sticky='e', padx=2, pady=2)
    Button(search_toplevel, text="Find All", underline=0,
           command=lambda: search_output(
               search_entry_widget.get(), ignore_case_value.get(),
               scroll, search_toplevel, search_entry_widget)
           ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

    def close_search_window():
        scroll.text.tag_remove('match', '1.0', END)
        search_toplevel.destroy()
    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
    return "break"

def search_output(needle,if_ignore_case, scroll, search_toplevel, search_box):
    scroll.text.tag_remove('match','1.0', END)
    matches_found=0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = scroll.text.search(needle,start_pos, nocase=if_ignore_case, stopindex=END)
            if not start_pos:
                break

            end_pos = '{} + {}c'. format(start_pos, len(needle))
            scroll.text.tag_add('match', start_pos, end_pos)
            matches_found +=1
            start_pos = end_pos
        scroll.text.tag_config('match', background='yellow', foreground='blue')
    search_box.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found)) 
    
#---------------------------------------------------[METHODS OF TOOLBARS]----------------------------------------------
def change_font(main_application):
    global current_font_family
    current_font_family = font_family.get()
    scroll.text.configure(font=(current_font_family,current_font_size))
    
def change_fontsize(main_application):
    global current_font_size
    current_font_size = size_var.get()
    scroll.text.configure(font=(current_font_family,current_font_size))

def change_bold():
    text_property = tk.font.Font(font=scroll.text['font'])
    if text_property.actual()['weight'] == 'normal':
        scroll.text.configure(font=(current_font_family,current_font_size,'bold'))
    if text_property.actual()['weight'] == 'bold':
        scroll.text.configure(font=(current_font_family,current_font_size,'normal'))
        
def change_italic():
    text_property = tk.font.Font(font=scroll.text['font'])
    if text_property.actual()['slant'] == 'roman':
        scroll.text.configure(font=(current_font_family,current_font_size,'italic'))
    if text_property.actual()['slant'] == 'italic':
        scroll.text.configure(font=(current_font_family,current_font_size,'roman'))
        
def change_underline():
    text_property = tk.font.Font(font=scroll.text['font'])
    if text_property.actual()['underline'] == 0:
        scroll.text.configure(font=(current_font_family,current_font_size,'underline'))
    if text_property.actual()['underline'] == 1:
        scroll.text.configure(font=(current_font_family,current_font_size,'normal'))

def change_font_color():
    color_var = tk.colorchooser.askcolor()
    scroll.text.configure(fg=color_var[1])

def align_left():
    text_content = scroll.text.get(1.0, 'end')
    scroll.text.tag_config('left', justify=tk.LEFT)
    scroll.text.delete(1.0,tk.END)
    scroll.text.insert(tk.INSERT, text_content, 'left')

def align_center():
    text_content = scroll.text.get(1.0, 'end')
    scroll.text.tag_config('center', justify=tk.CENTER)
    scroll.text.delete(1.0,tk.END)
    scroll.text.insert(tk.INSERT, text_content, 'center')

def align_right():
    text_content = scroll.text.get(1.0, 'end')
    scroll.text.tag_config('right', justify=tk.RIGHT)
    scroll.text.delete(1.0,tk.END)
    scroll.text.insert(tk.INSERT, text_content, 'right')
#-----------------------------------------------------[Select All]-------------------------------------
def select_all(event=None):
    scroll.text.tag_add('sel', '1.0', 'end')
    return "break"
#-----------------------------------------------------[Color Theme]-------------------------------------------
def change_theme():
    chosen_theme = theme_choice.get()
    color_tuple = color_dict.get(chosen_theme)
    fg_color,bg_color = color_tuple[0],color_tuple[1]
    scroll.text.config(background=bg_color,fg=fg_color)

#----------------------------------------------------[ENCTYPTION]------------------------------------------

def x():
    FONT = ("Arial", 12, "bold") 
    
    class CaesarCipherGUI:
        def __init__(self, master):
            master.title("Encrypt/Decrypt")
            self.plaintext = tk.StringVar(master, value="")
            self.ciphertext = tk.StringVar(master, value="")
            self.key = tk.IntVar(master)
    
            # Plaintext controls
            self.plain_label = tk.Label(master, text="Enter Massage : ", fg="black").grid(row=0, column=0)
            
            self.plain_entry = tk.Entry(master, textvariable=self.plaintext, width=30)
            self.plain_entry.grid(row=0, column=1, padx=20)
            
            self.encrypt_button = tk.Button(master, text="Encrypt",command=lambda: self.encrypt_callback()).grid(row=0, column=2)
            self.plain_clear = tk.Button(master, text="Clear",command=lambda: self.clear('plain')).grid(row=0, column=3)
    
            # Key controls
            self.key_label = tk.Label(master, text="Key").grid(row=1, column=0)
            self.key_entry = tk.Entry(master, textvariable=self.key, width=10).grid(row=1, column=1,
                                                                                            sticky=tk.W, padx=20)
    
            # Ciphertext controls
            self.cipher_label = tk.Label(master, text="Crypted : ").grid(row=2, column=0)
            self.cipher_entry = tk.Entry(master,
                                        textvariable=self.ciphertext, width=30)
            self.cipher_entry.grid(row=2, column=1, padx=20)
            self.decrypt_button = tk.Button(master, text="Decrypt",
                                            command=lambda: self.decrypt_callback()).grid(row=2, column=2)
            self.cipher_clear = tk.Button(master, text="Clear",
                                        command=lambda: self.clear('cipher')).grid(row=2, column=3)
    
        def clear(self, str_val):
            if str_val == 'cipher':
                self.cipher_entry.delete(0, 'end')
            elif str_val == 'plain':
                self.plain_entry.delete(0, 'end')
    
        def get_key(self):
            try:
                key_val = self.key.get()
                return key_val
            except tk.TclError:
                pass
    
        def encrypt_callback(self):
            key = self.get_key()
            ciphertext = encrypt(self.plain_entry.get(), key)
            self.cipher_entry.delete(0, tk.END)
            self.cipher_entry.insert(0, ciphertext)
    
        def decrypt_callback(self):
            key = self.get_key()
            plaintext = decrypt(self.cipher_entry.get(), key)
            self.plain_entry.delete(0, tk.END)
            self.plain_entry.insert(0, plaintext)
    
    
    def encrypt(plaintext, key):
        ciphertext = ""
        for char in plaintext.upper():
            if char.isalpha():
                ciphertext += chr((ord(char) + key - 65) % 26 + 65)
            else:
                ciphertext += char
        return ciphertext
    
    
    def decrypt(ciphertext, key):
        plaintext = ""
        for char in ciphertext.upper():
            if char.isalpha():
                plaintext += chr((ord(char) - key - 65) % 26 + 65)
            else:
                plaintext += char
        return plaintext
    
    
    if __name__ == "__main__":
        root = tk.Tk()
        caesar = CaesarCipherGUI(root)
        root.mainloop()
#---------------------------------------------------[All classes]------------------------------------------------------
class ScrollText(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = tk.Text(self, bg='silver', foreground="black", 
                            insertbackground='black',
                            selectbackground="green", width=120, height=30)

        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.numberLines = TextLineNumbers(self, width=40, bg='grey')
        self.numberLines.attach(self.text)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.numberLines.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numberLines.redraw()


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill="black")
            i = self.textwidget.index("%s+1line" % i)



#-----------------------------------------------------[ToolBar]--------------------------------------------------
tool_bar = ttk.Label(main_application)
tool_bar.pack(side=tk.TOP, fill=tk.X)


                #++Font box++
font_tuple = tk.font.families()
font_family = tk.StringVar()
font_box = ttk.Combobox(tool_bar,width=20,textvariable=font_family, state='readonly')
font_box['values'] = font_tuple
font_box.current(font_tuple.index('Arial'))
font_box.grid(row=0,column=0,padx=0)
                #++Size box++
size_var = tk.IntVar()
font_size = ttk.Combobox(tool_bar,width=14,textvariable=size_var,state='readonly')
font_size['values'] = tuple(range(8,80,2))
font_size.current(4)
font_size.grid(row=0,column=1,padx=5)
                #++Bold btn++
bold_icon = tk.PhotoImage(file='Icons/bold.png')
bold_btn = ttk.Button(tool_bar, image=bold_icon)
bold_btn.grid(row=0,column=2,padx=2)

                #++Italic btn++
italic_icon = tk.PhotoImage(file='Icons/italic.png')
italic_btn = ttk.Button(tool_bar, image=italic_icon)
italic_btn.grid(row=0,column=3,padx=2)


                #++Underline btn++
underline_icon = tk.PhotoImage(file='Icons/underline-text.png')
underline_btn = ttk.Button(tool_bar,image=underline_icon)
underline_btn.grid(row=0,column=4,padx=2)

                #font color button

font_color_icon = tk.PhotoImage(file='Icons/text.png')
font_color_btn = ttk.Button(tool_bar, image=font_color_icon)
font_color_btn.grid(row=0,column=5,padx=2)


#aling
align_left_icon = tk.PhotoImage(file='Icons/align-to-left.png')
align_left_btn = ttk.Button(tool_bar, image= align_left_icon)
align_left_btn.grid(row=0,column=6,padx=2)

align_center_icon = tk.PhotoImage(file='Icons/align.png')
align_center_btn = ttk.Button(tool_bar, image= align_center_icon)
align_center_btn.grid(row=0,column=7,padx=2)

align_right_icon = tk.PhotoImage(file='Icons/right-text-alignment.png')
align_right_btn = ttk.Button(tool_bar, image= align_right_icon)
align_right_btn.grid(row=0,column=8,padx=2)

#------------------------------------------------------------------------------------


scroll = ScrollText(main_application)
scroll.pack(expand='yes',fill='both')
scroll.text.focus()
main_application.after(200, scroll.redraw())


#font family and font size func.

current_font_family = 'Arial'
current_font_size = 10

font_box.bind("<<ComboboxSelected>>",change_font)
font_size.bind("<<ComboboxSelected>>",change_fontsize)

#button functionality

bold_btn.configure(command=change_bold)

#italic functionality

italic_btn.configure(command=change_italic)

#underline func.

underline_btn.configure(command=change_underline)

#font color functionality

font_color_btn.configure(command=change_font_color)

###left align funtionality

align_left_btn.configure(command=align_left)

###center align funtionality

align_center_btn.configure(command=align_center)

###left align funtionality

align_right_btn.configure(command=align_right)

def display_about(event=None):
    tk.messagebox.askokcancel("UNDER DEVELOPMENT")

#---------------------------------------------------[01 Header section]------------------------------------------------------

main_menu = tk.Menu()


                        #>>>>>>>Option Adding<<<<<<<
File = tk.Menu(main_menu, tearoff=False, foreground='Black',
                                         activebackground='#566D7E', activeforeground='white')
Edit = tk.Menu(main_menu, tearoff=False, foreground='Black',
                                         activebackground='#566D7E', activeforeground='white')
Selection = tk.Menu(main_menu, tearoff=False)
View = tk.Menu(main_menu, tearoff=False)
Colour_theme = tk.Menu(main_menu, tearoff=False)
Go = tk.Menu(main_menu, tearoff=False)
Run = tk.Menu(main_menu, tearoff=False)
Encryption = tk.Menu(main_menu, tearoff=False)
Help = tk.Menu(main_menu, tearoff=False)

                        #>>>>>>>Cascading<<<<<<<<
main_menu.add_cascade(label='File', menu=File)
main_menu.add_cascade(label='Edit', menu=Edit)
main_menu.add_cascade(label='Selection', menu=Selection)
main_menu.add_cascade(label='View', menu=View)
View.add_command(label='Notice', underline=0, command=display_about)
main_menu.add_cascade(label='Colour Theme', menu=Colour_theme)
main_menu.add_cascade(label='Go', menu=Go)
Go.add_command(label='Notice!', underline=0, command=display_about)
main_menu.add_cascade(label='Run', menu=Run)
Run.add_command(label='Notice', underline=0, command=display_about)
main_menu.add_cascade(label='Encryption', menu=Encryption)
main_menu.add_cascade(label='Help', menu=Help)
Help.add_command(label='Notice!', underline=0, command=display_about)



                        #+++++FILE+++++
#Icons
new_file_icon = tk.PhotoImage(file='Icons/add-file.png')
open_file_icon = tk.PhotoImage(file='Icons/open-folder.png')
open_folder_icon = tk.PhotoImage(file='Icons/folder.png')
save_icon = tk.PhotoImage(file='Icons/save.png')
save_as_icon = tk.PhotoImage(file='Icons/save-as.png')
exit_icon = tk.PhotoImage(file='Icons/logout.png')
#File options
File.add_command(label='New File',image=new_file_icon, compound=tk.LEFT, accelerator='Ctrl+N',command=new_file)
File.add_command(label='Open File',image=open_file_icon, compound=tk.LEFT, accelerator='Ctrl+O',command=open_file)
File.add_command(label='Open Folder',image=open_folder_icon, compound=tk.LEFT, accelerator='Ctrl+Shift+F',command=browseFiles)
File.add_command(label='Save',image=save_icon, compound=tk.LEFT, accelerator='Ctrl+S',command=save)
File.add_command(label='Save As',image=save_as_icon, compound=tk.LEFT, accelerator='Ctrl+Shift+A',command=save_as)
File.add_command(label='Exit',image=exit_icon, compound=tk.LEFT, accelerator='Ctrl+E',command=exit_editor)


                        #+++++EDIT+++++
#Icons
Copy_icon = tk.PhotoImage(file='Icons/copy.png')
Paste_icon = tk.PhotoImage(file='Icons/paste.png')
clear_icon = tk.PhotoImage(file='Icons/rubber.png')
Cut_icon = tk.PhotoImage(file='Icons/ulu-blade.png')
find_icon = tk.PhotoImage(file='Icons/search.png')
#Edit options
Edit.add_command(label='Copy', image=Copy_icon, compound=tk.LEFT, accelerator='Ctrl+C',command=copy)
Edit.add_command(label='Paste', image=Paste_icon, compound=tk.LEFT, accelerator='Ctrl+V',command=paste)
Edit.add_command(label='Cut', image=Cut_icon, compound=tk.LEFT, accelerator='Ctrl+X',command=cut)
Edit.add_command(label='Clear All', image=clear_icon, compound=tk.LEFT, accelerator='Ctrl+Shift+A',command=clearAll)
Edit.add_command(label='Find', image=find_icon, compound=tk.LEFT, accelerator='Ctrl+F',command=find_text)

                        #+++++Selection+++++++
Selection.add_command(label='Select All', underline=7, accelerator='Ctrl+A', command=select_all)


#---------------------------------------------------[01 - END]------------------------------------------------]
status_bar1 = ttk.Label(scroll.text)
status_bar1.pack(side=tk.BOTTOM,padx=100)

tabControl = ttk.Notebook(main_application) 

tab1 = ttk.Frame(tabControl) 

tabControl.add(tab1, text ='RESULT -->')  
tabControl.pack(expand = 0, pady=30,padx=30,side=tk.LEFT)


ttk.Label(tab1, 
		text ="IN PROGRESS ....", foreground='red').grid(column = 0, 
							row = 0, 
							padx = 10, 
							pady = 10) 
  


Encryption.add_command(label='Start', underline=0, command=x)


def changed(event=None):
    if scroll.text.edit_modified():
        words = len(scroll.text.get(1.0,'end').split())
        characters = len(scroll.text.get(1.0,'end'))-1
        status_bar1.config(text=f'Character : {characters} Words : {words}')
    scroll.text.edit_modified(False)

scroll.text.bind('<<Modified>>',changed)


theme_choice = tk.StringVar()

color_dict = {
    'Dark' : ('#c4c4c4','#2d2d2d'),
    'Monokai' : ('#d3b774','#474747'),
    'Night Blue' : ('#ededed','#6b9dc2')
}
    
count = 0
for i in color_dict:
    Colour_theme.add_radiobutton(label = i, variable=theme_choice,compound=tk.LEFT, command=change_theme)
#---------------------------------------------------[SHORT KEYS]------------------------------------------------]
scroll.bind('<Control-N>', new_file)
scroll.bind('<Control-n>', new_file)
scroll.bind('<Control-O>',open_file)
scroll.bind('<Control-o>',open_file)
scroll.bind('<Control-Shift-F>',browseFiles)
scroll.bind('<Control-Shift-f>',browseFiles)
scroll.bind('<Control-S>',save)
scroll.bind('<Control-s>',save)
scroll.bind('<Control-Shift-A>',save_as)
scroll.bind('<Control-Shift-a>',save_as)
scroll.bind('<Control-E>',exit_editor)
scroll.bind('<Control-e>',exit_editor)

scroll.bind('<Control-C>',copy)
scroll.bind('<Control-c>',copy)
scroll.bind('<Control-V>',paste)
scroll.bind('<Control-v>',paste)
scroll.bind('<Control-X>',cut)
scroll.bind('<Control-x>',cut)
scroll.bind('<Control-Shift-C>',clearAll)
scroll.bind('<Control-Shift-c>',clearAll)
scroll.bind('<Control-F>',find_text)
scroll.bind('<Control-f>',find_text)

scroll.text.bind('<Control-A>', select_all)
scroll.text.bind('<Control-a>', select_all)


main_application.config(menu=main_menu)
main_application.mainloop()