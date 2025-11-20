import customtkinter as ctk
import src_files.args as ag
from PIL import Image
import DB.ddl as ddl
import DB.dml as dml
import utils
import DB.dql as dql

class Widgets:

    class Entry:

        def __init__(self,
                    screen,
                    placeholder_text,
                    width,
                    height,
                    posx,
                    posy,
                    /,
                    *,
                    show = '',
                    border_color = ag.pattern_style['main_color'],
                    fg_color = ag.pattern_style['background_color'],
                    fontstyle = ag.pattern_style['font_style'],
                    fontsize = 15,
                    mode = 'center'):
            self.entry = ctk.CTkEntry(screen,
                                        placeholder_text = placeholder_text,
                                        fg_color = fg_color,
                                        border_color = border_color,
                                        font = (fontstyle, fontsize),
                                        width = width,
                                        height = height,
                                        show = show)
            self.entry.place(relx = posx, rely = posy, anchor = mode)
        
        def get_delete(self):
            value = self.entry.get()
            self.entry.delete(0, ctk.END)
            return value
        
        def get(self):
            return self.entry.get()

    class Button:

        def __init__(self,
                    screen,
                    text,
                    posx,
                    posy,
                    /,
                    associated_func,
                    *,
                    width = ag.pattern_style['button_width'],
                    height = ag.pattern_style['button_height'],
                    color = ag.pattern_style['main_color'],
                    hover_color = ag.pattern_style['hover_color'],
                    border_color = ag.pattern_style['border_color'],
                    text_color = 'black',
                    font = (ag.pattern_style['font_style'], ag.pattern_style['text_size_for_button']),
                    border_width = 5,
                    img = None,
                    hover = True,
                    roundness = 10,
                    mode = 'center'
                    ):
            self.button = ctk.CTkButton(screen,
                                        text = text,
                                        height = height,
                                        width = width,
                                        fg_color = color,
                                        border_color = border_color,
                                        border_width = border_width,
                                        hover_color = hover_color,
                                        text_color = text_color,
                                        font = font,
                                        command = associated_func,
                                        image = img,
                                        hover = hover,
                                        corner_radius = roundness)
            self.button.place(relx = posx, rely = posy, anchor = mode)
        
        def pos(self, posx, posy):
            self.button.place(relx = posx, rely = posy, anchor = 'center')

    class Label:

        def __init__(self,
                    screen,
                    text,
                    posx,
                    posy,
                    size,
                    /,
                    *,
                    font = ag.pattern_style['font_style'],
                    color = ag.pattern_style['main_color'],
                    mode = 'center'
                    ):
            self.mode = mode
            self.label = ctk.CTkLabel(screen,
                                        text = text,
                                        font = (font, size),
                                        text_color = color)
            self.label.place(relx = posx, rely = posy, anchor = self.mode)

        def pos(self, posx, posy):
            self.label.place(relx = posx, rely = posy, anchor = self.mode)

class Window:

    def __init__(self, width, height, icon_path, title, /):
        ctk.set_appearance_mode('dark')
        self.root = ctk.CTk()
        self.root.geometry(f'{width}x{height}')
        self.root.iconbitmap(icon_path)
        self.root.title(title)
        self.root.resizable(False, False)
        self.widget = Widgets() #Used to access the widgets
    
    def open_window(self):
        self.root.mainloop()

    def close_window(self): #close the window
        self.root.destroy()

class Error_screen(Window):

    def __init__(self,
                icon_path,
                title,
                error_text,
                error_size,
                /,
                *,
                posx_label = 0.5,
                posy_label = 0.3,
                posx_button = 0.5,
                posy_button = 0.6,
                width = 600,
                height = 200):
        super().__init__(width, height, icon_path, title)
        self.error_label = self.widget.Label(self.root,
                                error_text,
                                posx_label,
                                posy_label,
                                error_size,
                                color = '#ff3300')
        self.button = self.widget.Button(self.root,
                            'OK',
                            posx_button,
                            posy_button,
                            associated_func = self.close_window,
                            width = 100,
                            height = 50,
                            color = '#ff3300',
                            hover_color = '#b32400')

class Success_screen(Window):

    def __init__(self,
                icon_path,
                title,
                suc_text,
                suc_size,
                /,
                *,
                posx_label = 0.5,
                posy_label = 0.3,
                posx_button = 0.5,
                posy_button = 0.6,
                width = 600,
                height = 200):
        super().__init__(width, height, icon_path, title)
        self.error_label = self.widget.Label(self.root,
                                suc_text,
                                posx_label,
                                posy_label,
                                suc_size,
                                color = '#66ff66')
        self.button = self.widget.Button(self.root,
                            'OK',
                            posx_button,
                            posy_button,
                            associated_func = self.close_window,
                            width = 100,
                            height = 50,
                            color = '#66ff66',
                            hover_color = '#00cc00')
#refactorated until this place.

class Login_Register(Window):

    into_login = True
    out_login = True
    into_register = True
    out_register = True

    permission_to_call_next_window = False

    user_id = None

    def __init__(self, conn, width = ag.window_size['Login'][0], height = ag.window_size['Login'][1], icon_path = None, title = 'welcome'):
        super().__init__(width, height, icon_path, title)
        self.conn = conn
        self.Call_Login_Widgets()
    
    def Call_Login_Widgets(self):
        self.titlex, self.titley = [0.5, -0.2]
        self.framex, self.framey = [-0.5, 0.43]
        self.login_buttonx, self.login_buttony = [-0.3, 0.75]
        self.register_buttonx, self.register_buttony = [1.3, 0.75]
        self.title_label = self.widget.Label(self.root, 'Login Screen', self.titlex, self.titley, 50)
        self.user_frame = ctk.CTkFrame(self.root,
                                          width = 500,
                                          height = 300)
        self.user_frame.place(relx = self.framex, rely = self.framey, anchor = 'center')
        self.username_label = self.widget.Label(self.user_frame, 'username', 0.25, 0.1, 30)
        self.user_entry = self.widget.Entry(self.user_frame,
                                'type the user name',
                                ag.pattern_style['entry_width'],
                                ag.pattern_style['entry_height'],
                                0.5,
                                0.3,
                                fontsize = 25)
        self.pw_label = self.widget.Label(self.user_frame, 'password',0.25, 0.5, 30)
        self.pw_entry = self.widget.Entry(self.user_frame,
                                'type the password',
                                ag.pattern_style['entry_width'],
                                ag.pattern_style['entry_height'],
                                0.5,
                                0.7,
                                fontsize = 25,
                                show = '*')
        self.control = ctk.StringVar(value = 'on')
        self.check = ctk.CTkCheckBox(self.user_frame,
                                     variable = self.control,
                                     onvalue = 'on',
                                     offvalue = 'off',
                                     text = 'hide',
                                     command = self.hide_login,
                                     hover_color = ag.pattern_style['hover_color'],
                                     fg_color = ag.pattern_style['main_color'],
                                     corner_radius = 100,
                                     border_color = ag.pattern_style['main_color'],
                                     font = (ag.pattern_style['font_style'], 19))
        self.check.place(relx = 0.2, rely = 0.88, anchor = 'center')
        self.login_button = self.widget.Button(self.root, 'SIGN IN', self.login_buttonx, self.login_buttony, self.sign_in)
        self.register_button = self.widget.Button(self.root, 'SIGN UP', self.register_buttonx, self.register_buttony, self.sign_up)
        self.error_label = self.widget.Label(self.root, "", 0.5, 0.83, 20, color = '#ff3300')
        self.move_in_login()

    def call_register_widgets(self):

        self.titleregx, self.titleregy = [0.5, -0.1]
        self.regframex, self.regframey = [-0.5, 0.5]
        self.reg_user_labelx, self.reg_user_labely = [0.5, 0.05]
        self.reg_user_entryx, self.reg_user_entryy = [0.5, 0.13]
        self.reg_last_labelx, self.reg_last_labely = [0.2, 0.28]
        self.reg_last_entryx, self.reg_last_entryy = [0.25, 0.35]
        self.reg_first_entryx, self.reg_first_entryy = [0.75, 0.35]
        self.reg_email_labelx, self.reg_email_labely = [0.5, 0.5]
        self.reg_email_entryx, self.reg_email_entryy = [0.5, 0.57]
        self.reg_pw_labelx, self.reg_pw_labely = [0.2, 0.72]
        self.reg_pw_entryx, self.reg_pw_entryy = [0.25, 0.79]
        self.reg_cpw_firstx, self.reg_cpw_firsty = [0.7, 0.72]
        self.reg_cpw_entryx, self.reg_cpw_entryy = [0.75, 0.79]
        self.regcheckx, self.regchecky = [0.12, 0.9]
        self.submmit_buttonx, self.submmit_buttony = [0.5, 1.1]
        self.go_back_buttonx, self.go_back_buttony = [1.1, 0.12]
        #Defining the title
        self.titlereg_label = self.widget.Label(self.root, 'Sign Up Screen', self.titleregx, self.titleregy, 50)
        #Defining the frame
        self.reg_frame = ctk.CTkFrame(self.root, width = 400,height = 350)
        self.reg_frame.place(relx = self.regframex, rely = self.regframey, anchor = 'center')
        #Defining the widgets inside the frame
        self.reg_user_label = self.widget.Label(self.reg_frame, 'Username', self.reg_user_labelx, self.reg_user_labely, 15)
        self.reg_user_entry = self.widget.Entry(self.reg_frame, 'type username', 200, 30, self.reg_user_entryx, self.reg_user_entryy)
        #defining first and last name
        self.reg_first_label = self.widget.Label(self.reg_frame, 'First name', self.reg_last_labelx, self.reg_last_labely, 15)
        self.reg_first_entry = self.widget.Entry(self.reg_frame, 'type first name', 180, 30, 0.25, 0.35)
        self.reg_last_label = self.widget.Label(self.reg_frame, 'Last Name', 0.7, 0.28, 15)
        self.reg_last_entry = self.widget.Entry(self.reg_frame, 'type last name', 180, 30, self.reg_first_entryx, self.reg_first_entryy)
        #defining the email
        self.reg_email_label = self.widget.Label(self.reg_frame, 'Email', self.reg_email_labelx, self.reg_email_labely, 15)
        self.reg_email_entry = self.widget.Entry(self.reg_frame, 'type email', 350, 30, self.reg_email_entryx, self.reg_email_entryy)
        #defining password
        self.reg_pw_label = self.widget.Label(self.reg_frame, 'Password', self.reg_pw_labelx, self.reg_pw_labely, 15)
        self.reg_pw_entry = self.widget.Entry(self.reg_frame, 'type password', 180, 30, self.reg_pw_entryx, self.reg_pw_entryy, show = '*')
        self.reg_cpw_label = self.widget.Label(self.reg_frame, 'Confirm Password', self.reg_cpw_firstx, self.reg_cpw_firsty, 15)
        self.reg_cpw_entry = self.widget.Entry(self.reg_frame, 'type password again', 180, 30, self.reg_cpw_entryx, self.reg_cpw_entryy, show = '*')
        self.regcontrol = ctk.StringVar(value = 'on')
        self.regcheck = ctk.CTkCheckBox(self.reg_frame,
                                     variable = self.regcontrol,
                                     onvalue = 'on',
                                     offvalue = 'off',
                                     text = 'hide',
                                     command = self.hide_register,
                                     hover_color = ag.pattern_style['hover_color'],
                                     fg_color = ag.pattern_style['main_color'],
                                     corner_radius = 100,
                                     border_color = ag.pattern_style['main_color'],
                                     font = (ag.pattern_style['font_style'], 15),
                                     width = 6,
                                     height = 6,
                                     text_color = ag.pattern_style['main_color'])
        self.regcheck.place(relx = self.regcheckx, rely = self.regchecky, anchor = 'center')
        self.submmit_button = self.widget.Button(self.root, 'SUBMMIT', self.submmit_buttonx, self.submmit_buttony, self.submmit)
        self.go_back_image = ctk.CTkImage(light_image = Image.open('images/go_back.png'), size = (28, 28))
        self.go_back_button = self.widget.Button(self.root,
                                     '',
                                     self.go_back_buttonx,
                                     self.go_back_buttony,
                                     self.go_back,
                                     width = 50,
                                     height = 50,
                                     img = self.go_back_image)
        #Error Label
        self.regerror_label = self.widget.Label(self.root, '', 0.5, 0.82, 20, color = '#ff3300')

    @classmethod
    def turn_true(cls):
        cls.into_login = True
        cls.out_login = True
        cls.into_register = True
        cls.out_register = True

    def move_in_login(self):
        if self.framex < 0.5:
            self.framex += 0.02
            self.user_frame.place(relx = self.framex, rely = self.framey, anchor = 'center')
        if self.titley < 0.1:
            self.titley += 0.01
            self.title_label.pos(posx = self.titlex, posy = self.titley)
        if self.login_buttonx < 0.3:
            self.login_buttonx += 0.02
            self.login_button.pos(posx = self.login_buttonx, posy = self.login_buttony)
        if self.register_buttonx > 0.7:
            self.register_buttonx -= 0.02
            self.register_button.pos(posx = self.register_buttonx, posy = self.register_buttony)
        if not self.framex < 0.5 and not self.titley < 0.1 and not self.login_buttonx < 0.3 and not self.register_buttonx > 0.7:
            Login_Register.into_login = False
        if Login_Register.into_login:
            self.root.after(2, self.move_in_login)

    def sign_up(self):
        self.call_register_widgets()
        self.move_out_login()

    def move_out_login(self):
        if Login_Register.out_login:
            if self.framex > -1:
                self.framex -= 0.02
                self.user_frame.place(relx = self.framex, rely = self.framey, anchor = 'center')
            if self.titley > -0.2:
                self.titley -= 0.01
                self.title_label.pos(posx = self.titlex, posy = self.titley)
            if self.login_buttonx > -0.3:
                self.login_buttonx -= 0.02
                self.login_button.pos(posx = self.login_buttonx, posy = self.login_buttony)
            if self.register_buttonx < 1.3:
                self.register_buttonx += 0.02
                self.register_button.pos(posx = self.register_buttonx, posy = self.register_buttony)
            if not self.framex > -1 and not self.titley > -0.2 and not self.login_buttonx > -0.3 and not self.register_buttonx < 1.3:
                Login_Register.out_login = False
        else:
            if self.titleregy < 0.1:
                self.titleregy += 0.01
                self.titlereg_label.pos(posx = self.titleregx, posy = self.titleregy)
            if self.regframex < 0.5:
                self.regframex += 0.02
                self.reg_frame.place(relx = self.regframex, rely = self.regframey, anchor = 'center')
            if self.go_back_buttonx > 0.9:
                self.go_back_buttonx -= 0.01
                self.go_back_button.pos(posx = self.go_back_buttonx, posy = self.go_back_buttony)
            if self.submmit_buttony > 0.9:
                self.submmit_buttony -= 0.01
                self.submmit_button.pos(posx = self.submmit_buttonx, posy = self.submmit_buttony)
            if not self.titleregy < 0.1 and not self.regframex < 0.5 and not self.go_back_buttonx > 0.9 and not self.submmit_buttony > 0.9:
                Login_Register.into_register = False
        if Login_Register.out_login or Login_Register.into_register:
                self.root.after(2, self.move_out_login)
        else:
            Login_Register.turn_true()

    def go_back(self):
        self.regerror_label.label.configure(text = "")
        if Login_Register.out_register:
            if self.titleregy > -0.1:
                self.titleregy -= 0.01
                self.titlereg_label.pos(posx = self.titleregx, posy = self.titleregy)
            if self.regframex > -0.5:
                self.regframex -= 0.01
                self.reg_frame.place(relx = self.regframex, rely = self.regframey, anchor = 'center')
            if self.go_back_buttonx < 1.1:
                self.go_back_buttonx += 0.01
                self.go_back_button.pos(posx = self.go_back_buttonx, posy = self.go_back_buttony)
            if self.submmit_buttony < 1.1:
                self.submmit_buttony += 0.01
                self.submmit_button.pos(posx = self.submmit_buttonx, posy = self.submmit_buttony)
            if not self.titleregy > -0.1 and not self.regframex > -0.5 and not self.go_back_buttonx < 1.1 and not self.submmit_buttony < 1.1:
                Login_Register.out_register = False
        else:
            if self.framex < 0.5:
                self.framex += 0.02
                self.user_frame.place(relx = self.framex, rely = self.framey, anchor = 'center')
            if self.titley < 0.1:
                self.titley += 0.01
                self.title_label.pos(posx = self.titlex, posy = self.titley)
            if self.login_buttonx < 0.3:
                self.login_buttonx += 0.02
                self.login_button.pos(posx = self.login_buttonx, posy = self.login_buttony)
            if self.register_buttonx > 0.7:
                self.register_buttonx -= 0.02
                self.register_button.pos(posx = self.register_buttonx, posy = self.register_buttony)
            if not self.framex < 0.5 and not self.titley < 0.1 and not self.login_buttonx < 0.3 and not self.register_buttonx > 0.7:
                Login_Register.into_login = False
        if Login_Register.out_register or Login_Register.into_login:
                self.root.after(2, self.go_back)
        else:
            Login_Register.turn_true()

    def submmit(self):
        username = self.reg_user_entry.get()
        first_name = self.reg_first_entry.get()
        last_name = self.reg_last_entry.get()
        email = self.reg_email_entry.get()
        pw = self.reg_pw_entry.get()
        check_pw = self.reg_cpw_entry.get()
        if '' in (username, first_name, last_name, email, pw, check_pw):
            self.regerror_label.label.configure(text = "ERROR: You've left an empty entry!")
        else:
            if pw != check_pw:
                self.regerror_label.label.configure(text = "ERROR: Passwords don't match. Check it again!")
            else:
                if len(check_pw) < 8:
                    self.regerror_label.label.configure(text = 'ERROR: Password must have at least 8 characters!')
                else:
                    if utils.valid_email(email):
                        try:
                            dml.load_user(self.conn, username, first_name, last_name, email, pw)
                        except Exception as e:
                            print(e)
                            self.regerror_label.label.configure(text = str(e))
                        else:
                            self.suc = Success_screen(None, 'Success Screen', 'User added with success', 20)
                            self.suc.open_window()
                    else:
                        self.regerror_label.label.configure(text = 'ERROR: Email must have the format ___@___.com')
        
    def sign_in(self):
        username = self.user_entry.get()
        password = self.pw_entry.get()
        if '' in (username, password):
            self.error_label.label.configure(text = 'ERROR: You must fill all entries')
        else:
            if dql.search_user(self.conn, username, password):
                self.root.destroy()
                self.main_screen = Main_Screen()
                self.main_screen.open_window()
            else:
                self.error_label.label.configure(text = 'Wrong password or username!')
            '''self.users_data = dql.fetch_user(self.conn)
            every_username = self.users_data['username']
            every_password = self.users_data['password']
            for ind in range(len(every_username)):
                if username == every_username[ind] and password == every_password[ind]:
                    print('OK')
                else:
                    self.error_label.label.configure(text = 'Wrong password or username!')'''

    def hide_login(self):
        if self.control.get() == 'off':
            self.pw_entry.entry.configure(show = '')
        else:
            self.pw_entry.entry.configure(show = '*')

    def hide_register(self):
        if self.regcontrol.get() == 'off':
            self.reg_pw_entry.entry.configure(show = '')
            self.reg_cpw_entry.entry.configure(show = '')
        else:
            self.reg_pw_entry.entry.configure(show = '*')
            self.reg_cpw_entry.entry.configure(show = '*')

class Main_Screen(Window):

    def __init__(self, width = 1200, height = 700, icon_path = None, title = 'Main Screen'):
        super().__init__(width, height, icon_path, title)
        self.menu_frame = ctk.CTkFrame(self.root, width = 1300, height = 120)
        self.menu_frame.place(relx = -0.02, rely = 0.0, anchor = 'nw')
        self.menu_msg = self.widget.Label(self.menu_frame, 'WELCOME TO THE MOVIE-DB APP', 0.5, 0.2, 25)
        self.search = self.widget.Button(self.menu_frame, 'SEARCH', 0.4, 0.65, self.search_movie)
        self.analyze = self.widget.Button(self.menu_frame, 'ANALYZE', 0.6, 0.65, self.analyze_DB)
        self.main_frame = ctk.CTkFrame(self.root, width = 1110, height = 540)
        self.main_frame.place(relx = 0.04, rely = 0.2, anchor = 'nw')

    def recreate_frame(self):
        self.main_frame.destroy()
        self.main_frame = ctk.CTkFrame(self.root, width = 1110, height = 540)
        self.main_frame.place(relx = 0.04, rely = 0.2, anchor = 'nw')

    def search_movie(self):
        self.recreate_frame()

    def analyze_DB(self):
        self.recreate_frame()

if __name__ == '__main__':
    suc = Main_Screen()
    suc.open_window()