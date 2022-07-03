import pygame#Импортируем пайгейм полностю
from modul.my_json import*#ищем модуль my_json в папке modul це наш власный модуль
from modul.dataclass import*#ищем модуль dataclass в папке modul це наш власный модуль
from modul.game import*
from modul.datagame import Window

def re_creat_btn():
  
    btn_menu.BTN_LIST.clear()
    btn_music.BTN_LIST.clear()
    btn_setting.BTN_LIST.clear()
    btn_size.BTN_LIST.clear()

    btn_menu.creat_btn(setting_btn, setting)
    btn_setting.creat_btn(setting_btn_sett, setting)
    btn_size.creat_btn(setting_btn_size, setting)
    btn_music.creat_btn(setting_btn_music, setting)
   
setting = rid_json("sett_menu.json","json")#Вказуем назву файла("sett_menu.json") и папку(json) после чего загружаем содержымое в переменую
setting_btn = rid_json("sett_btn.json","json")#Вказуем назву файла("sett_btn.json") и папку(json) после чего загружаем содержымое в переменую
setting_btn_sett = rid_json("sett_btn_setting.json","json")
setting_btn_size = rid_json("sett_btn_size.json","json")
setting_btn_music = rid_json("sett_btn_music.json","json")

btn_menu = GroupButton(setting,setting_btn,True)#Создаем переменую в которой будут кнопки с класа GroupButton и вказуем обезательные переменые словнык в переменой setting и словнык setting_btn 
btn_setting = GroupButton(setting,setting_btn_sett,False)
btn_size = GroupButton(setting,setting_btn_size,False)
btn_music = GroupButton(setting,setting_btn_music,False)

music = Music(setting_btn_music)
def run():#Создаем функцию run
    global setting
    game = True#вказуем значення локальной перемене True она будет флагом
    win = Window(setting,'menu')
    # win = pygame.display.set_mode((setting["WIDHT"],setting["HIDHT"]))#Создаем окно с размерами в кортеже которые берем с переменой setting и ключом например setting["WIDHT"]
    # pygame.display.set_caption(setting["TITEL"])#Ставим название которое берем с переменой setting и ключом setting["TITEL"] на созданое ранее окно 
   
    while game:#Запускаем бесконечный цыкл пока game не равно False либо пока game = True
        # win.fill(setting["COLOR"])#Заливаем окно цветом который берем с словныка уже и так понятно с какого
        win.reset()
        btn_menu.reset(win.WIN)
        btn_setting.reset(win.WIN)
        btn_size.reset(win.WIN)
        btn_music.reset(win.WIN)
        for event in pygame.event.get():#Проверяем евенты - события
            if event.type == pygame.QUIT:#Проверяем нажатие на крестик в окне
                game = False#меняем локальную переменую на False - останавливаем цыкл
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_menu.WORK == True:
                    for i in range(len(setting_btn["TEXT_BTN"])):
                        if  btn_menu.BTN_LIST[i].BUTTON.collidepoint(event.pos):
                            if i == 0: 
                                game = False
                                run_game("new")
                            if i == 1:
                                game = False
                                run_game("restart")
                            if i == 2:
                                btn_menu.WORK = False
                                btn_setting.WORK = True
                            if i == 3:
                                game = False
                elif btn_setting.WORK:
                    for i in range(btn_setting.COUNT):
                        if  btn_setting.BTN_LIST[i].BUTTON.collidepoint(event.pos):
                                if i == 0: 
                                    btn_setting.WORK = False
                                    btn_size.WORK = True
                                if i == 1:
                                    btn_setting.WORK = False
                                    btn_music.WORK = True
                                if i == 2:
                                    btn_menu.WORK = True
                                    btn_setting.WORK = False

                elif btn_size.WORK:
                    for i in range(btn_size.COUNT):
                        if  btn_size.BTN_LIST[i].BUTTON.collidepoint(event.pos):
                                if i == 0: 
                                    setting = resize_win(1280,920,setting,win)
                                    re_creat_btn()
                                if i == 1:
                                    setting = resize_win(1080,720,setting,win)
                                    re_creat_btn()
                                if i == 2:
                                   setting = resize_win(720,480,setting,win)
                                   re_creat_btn()
                                if i == 3:
                                    btn_size.WORK = False
                                    btn_setting.WORK = True   
                elif btn_music.WORK:
                    for i in range(btn_music.COUNT):
                        if  btn_music.BTN_LIST[i].BUTTON.collidepoint(event.pos):
                                if i == 0: 
                                    if music.ON_OFF:
                                        music.ON_OFF = False
                                        pygame.mixer.music.stop()     
                                    else:
                                        music.ON_OFF = True
                                if i == 1:
                                   music.play_fon(1)
                                if i == 2:
                                    music.play_fon(2)
                                if i == 3:
                                    music.play_fon(3)
                                if i==4:
                                    btn_music.WORK = False
                                    btn_setting.WORK = True 
                                    pygame.mixer.music.stop()      

                            
           
        
        pygame.display.flip()#Обновляем екран