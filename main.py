import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import time
from datetime import datetime as dt
import tkinter as tk
from tkinter import ttk
from tkinter import Frame, LabelFrame, Label, Entry, Text, Button
import re

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Рассылка VK')
        self.geometry('500x500')
        self['background'] = 'yellow'
        self.resizable(width=False, height=False)

        token = ""
        vk_session = vk_api.VkApi(token=token)  
        vk_session._auth_token()
        self.vk = vk_session.get_api()

        self.widgets()


    def widgets(self):
        s = ttk.Style()
        self.main_frame = ttk.Frame(self, 
                                    width=500, 
                                    height=500, 
                                    borderwidth=0, 
                                    relief='solid',
                                    padding=[10, 10],)
        s.configure('TFrame', background='grey')

        self.frame_idGroup = LabelFrame(self.main_frame,
                                        text='id группы',
                                        background='grey')
        
        def check_idGroup(id):
            result =  re.match("\d{0,9}$", id) is not None
            if result and len(id) == 9:
                self.change_label_group(id)
            return result

        check = (self.register(check_idGroup), "%P")
        self.id_group = Entry(self.frame_idGroup, 
                                  width=27,
                                  validate="key",
                                  validatecommand=check)
        

        self.frame_textMessage = LabelFrame(self.main_frame, 
                                       width=50,
                                       text='Текст сообщения',
                                       background='grey')
        
        self.textMessage = Text(self.frame_textMessage, 
                                  width=28,
                                  height=20)
        
        self.frame_infoGroup = LabelFrame(self.main_frame, 
                                       width=50,
                                       text='Информация о группе',
                                       background='grey')
        
        self.infoGroup = Label(self.frame_infoGroup,
                                 background='#cfcabe', 
                                 text='',
                                 height=10,
                                 width=27,
                                 anchor='nw',
                                 wraplength=200)
        
        self.button_start = Button(self.main_frame, 
                                   width=48, 
                                   height=1,
                                   text='Начать рассылку',
                                   font='15',
                                   command=self.start_rass)


        self.frame_idGroup.place(x = 1, rely = 0.01)
        self.id_group.pack()

        self.textMessage.pack()
        self.frame_textMessage.place(relx=0.5, rely=0.01)

        self.frame_infoGroup.place(relx = 0.01, rely=0.15)
        self.infoGroup.pack()

        self.button_start.place(relx=0.01, rely=0.9)
        self.main_frame.pack(anchor='nw', padx=5, pady=5)
        

    def change_label_group(self, id):
        info = self.vk.groups.getById(group_id=id, fields='members_count')
        try:
            if info == None:
                print('None')
            else:
                self.infoGroup['text'] = f"{info[0]['name']}\n\nКол-во участников: {info[0]['members_count']}"
        except:
            self.infoGroup['text'] = 'Нет данных'
        

    def start_rass(self):
        membersGroup = self.vk.groups.getMembers(group_id=self.id_group.get())
        for i in membersGroup['items']:
            self.vk.messages.send(user_id = i,
                            message = membersGroup.get(),
                            random_id = get_random_id())



if __name__ == '__main__':
    app = Gui()
    app.mainloop()



    

 
