import pygame
from modul.my_json import*
from modul.dataclass import*
from random import randint
from itertools import groupby
pygame.init()
pygame.mixer.init()
class Window:
    def __init__(self,dict_win, menu_or_game):
        self.KIND_WIN = menu_or_game
        self.WIDTH = dict_win["WIDHT"]
        self.HIGHT = dict_win["HIDHT"]
        self.COLOR = dict_win["COLOR_GAME"]
        self.IMAGE = dict_win["IMAGE_GAME"]
        self.IMAGE_MENU = dict_win["IMAGE_MENU"]
        self.NAME_IMAGE = self.IMAGE
        self.NAME_IMAGE_MENU = self.IMAGE_MENU
        self.CAPTION = dict_win["CAPTION"]
        self.FPS = dict_win["FPS"]
        self.ICON = dict_win["ICON"]
        self.NAME_ICON = self.ICON
        self.IMAGE = self.load(self.IMAGE,self.WIDTH,self.HIGHT)
        self.IMAGE_MENU = self.load(self.IMAGE_MENU,self.WIDTH,self.HIGHT)
        self.ICON = self.load(self.ICON,20,20)
        pygame.display.set_icon(self.ICON)
        pygame.display.set_caption(self.CAPTION)
        self.WIN = pygame.display.set_mode((self.WIDTH,self.HIGHT))
        self.CLOCK = pygame.time.Clock()
        if self.KIND_WIN == "game":
            self.BTN_MENU = Button(self.WIDTH//10, self.HIGHT//10,self.WIDTH - self.WIDTH//10-10,5,(120,120,0),None,"Menu",(0,0,0),"20179.ttf")

    def load(self,image,w,h):
        if image:
            image = paths_json(image,"image")
            image = pygame.image.load(image)
            image = pygame.transform.scale(image,(w,h))
        else:
            image = None
        return image
    def reset(self): 
        if self.IMAGE and self.KIND_WIN=="game":#Проверяем наличые картинкы
            self.WIN.blit(self.IMAGE,(0,0))
        elif self.IMAGE_MENU and self.KIND_WIN=="menu":
            self.WIN.blit(self.IMAGE_MENU,(0,0))#Рисуем картинку на окне(win) вказуем какую картинку рисуем, кортежом вказуем кординаты откуда рисуем
        elif self.COLOR:# есле картинку не нашло но есть цвет
            self.WIN.fill(self.COLOR)
        if self.KIND_WIN == "game":
            self.BTN_MENU.reset(self.WIN)
class Game_bird:
    def __init__(self,dict_game):
        self.MAP = dict_game["GAME_MAP"]
        self.BIRD_IMAGE = dict_game["LIST_BIRD_IMG"]
        self.COUNT_BIRD_TASK = dict_game["COUNT_BIRD_TASK"]
        self.IMAGE = None
        self.W_BIRD = dict_game["WIDHT"]//(2*len(self.BIRD_IMAGE))
        self.X_BIRD = dict_game["WIDHT"]//5
        self.Y_BIRD = dict_game["HIDHT"]-dict_game["WIDHT"]//2
        self.STATS = Stats(dict_game)
        self.MAP_RECT = []
        self.make_rect() 
    def load_image(self,name_image):
        self.IMAGE = name_image
        self.IMAGE = paths_json(name_image,"image")
        self.IMAGE = pygame.image.load(self.IMAGE)
        self.IMAGE = pygame.transform.scale(self.IMAGE,(self.W_BIRD,self.W_BIRD))
    def reset(self,win,dict_game):
        y = self.Y_BIRD
        for i in range(len(self.BIRD_IMAGE)):
            x = self.X_BIRD
            for j in range(len(self.BIRD_IMAGE)):
                num = self.MAP[i][j]
                self.load_image(self.BIRD_IMAGE[num])
                win.blit(self.IMAGE,(x,y))
                x+=self.W_BIRD
            y+=self.W_BIRD
        self.STATS.reset(win,dict_game)
    def make_rect(self): 
        y = self.Y_BIRD
        for i in range(len(self.BIRD_IMAGE)):
            x = self.X_BIRD
            self.MAP_RECT.append([])
            for j in range(len(self.BIRD_IMAGE)):
                self.MAP_RECT[i].append(pygame.rect.Rect(x,y,self.W_BIRD,self.W_BIRD))
                x+=self.W_BIRD
            y+=self.W_BIRD
    def check_line(self):
        for line in self.MAP:
            start = 0
            for j, grop in groupby(line):
                leng = len(list(grop))
                if leng >= 3:
                    if j == self.STATS.BIRD_TASK:
                        self.STATS.PLAYER_TASK+=leng
                    row = self.MAP.index(line)
                    for i in range(row,0,-1):
                        self.MAP[i][start:start+leng]=self.MAP[i-1][start:start+leng]
                    spisok = []
                    for i in range(0,leng):
                        spisok.append(randint(0,6))
                    self.MAP[0][start:start+leng] = spisok
                start += leng
    def map_trans(self):
        map_t = []
        for i in range(len(self.BIRD_IMAGE)):
            map_t.append([])
            for j in range(len(self.BIRD_IMAGE)):
                map_t[i].append(self.MAP[j][i])
        self.MAP = map_t
    def check_row(self):
        self.map_trans()
        self.check_line2()
        self.map_trans()
    def check_line2(self):
        for line in self.MAP:
            start = 0
            for j, grop in groupby(line):
                leng = len(list(grop))
                if leng >= 3:
                    if j == self.STATS.BIRD_TASK:
                        self.STATS.PLAYER_TASK+=leng
                    del line[start:start+leng]
                    for i in range(0,leng):
                        number = randint(0,6)
                        line.insert(i,number)
                start += leng
class Stats:#класс статистика
    def __init__(self,dict_game):
        self.BIRD_TASK = dict_game["BIRD_TASK"]#Пташку которую нужно собрать
        self.COUNT_BIRD_TASK = dict_game["COUNT_BIRD_TASK"]
        self.MAX_BIRD_MOVE = dict_game["COUNT_MOVE"]#Макс ходов
        self.PLAYER_TASK = dict_game["PLAYER_TASK"]#Собрать
        self.PLAYER_MOVE = dict_game["PLAYER_MOVE"]#Ходов
        self.TXT_PLAYER_TASK = Button(dict_game["WIDHT"]//8,dict_game["HIDHT"]//3,10,5,None,None,"Залишилось:" +str(self.COUNT_BIRD_TASK-self.PLAYER_TASK),(0,0,0),"20179.ttf")#ето переменая сколько собрать
        self.TXT_PLAYER_MOVE = Button(dict_game["WIDHT"]//8,dict_game["HIDHT"]//3,10,5+self.TXT_PLAYER_TASK.BUTTON_TEXT.TEXT_OBJ.get_height(),None,None,"Залишилось ходів:" +str(self.MAX_BIRD_MOVE-self.PLAYER_MOVE),(0,0,0),"20179.ttf")#
    def show_end_text(self, win,dict_game ,txt_end_game):
        self.TXT_END_GAME = Button(dict_game["WIDHT"]//2,dict_game["HIDHT"]//2,dict_game["WIDHT"]//2-dict_game["WIDHT"]//4,dict_game["HIDHT"]//55,None,None,txt_end_game,(255,0,0),"20179.ttf")
        self.TXT_END_GAME.reset(win)

    def chek_game(self):#проверка конца игры
        if self.MAX_BIRD_MOVE[0] > self.PLAYER_MOVE:
            if self.BIRD_TASK[0] < self.PLAYER_TASK:
                print("win")
        else:
            print("game_over")
    def reset(self,win,dict_game):
        self.TXT_PLAYER_TASK = Button(dict_game["WIDHT"]//6,dict_game["HIDHT"]//2,10,5,None,None,"Залишилось:" +str(self.COUNT_BIRD_TASK-self.PLAYER_TASK),(0,0,0),"20179.ttf")#ето переменая сколько собрать
        self.TXT_PLAYER_MOVE = Button(dict_game["WIDHT"]//6,dict_game["HIDHT"]//2,10,5+self.TXT_PLAYER_TASK.BUTTON_TEXT.TEXT_OBJ.get_height(),None,None,"Залишилось ходів:" +str(self.MAX_BIRD_MOVE-self.PLAYER_MOVE),(0,0,0),"20179.ttf")#
        self.TXT_PLAYER_MOVE.reset(win)
        self.TXT_PLAYER_TASK.reset(win)
def create_restart_game(win,game):
    #
    dict_restart = dict()
    #
    dict_restart["WIDHT"] = win.WIDTH
    dict_restart["HIDHT"] = win.HIGHT
    dict_restart["COLOR_GAME"] = win.COLOR
    dict_restart["IMAGE_GAME"] = win.NAME_IMAGE
    dict_restart["CAPTION"] = win.CAPTION 
    dict_restart["FPS"] = win.FPS
    dict_restart["ICON"] = win.NAME_ICON
    dict_restart["IMAGE_MENU"] = win.NAME_IMAGE_MENU
    #
    dict_restart["GAME_MAP"] = game.MAP
    dict_restart["LIST_BIRD_IMG"] = game.BIRD_IMAGE
    #
    dict_restart["COUNT_BIRD_TASK"] = game.STATS.COUNT_BIRD_TASK
    dict_restart["BIRD_TASK"] = game.STATS.BIRD_TASK
    dict_restart["COUNT_BIRD_TASK"] = game.STATS.COUNT_BIRD_TASK
    dict_restart["COUNT_MOVE"] = game.STATS.MAX_BIRD_MOVE
    dict_restart["PLAYER_TASK"] = game.STATS.PLAYER_TASK 
    dict_restart["PLAYER_MOVE"] = game.STATS.PLAYER_MOVE

    write_json("sett_menu_restart.json","json",dict_restart)

def resize_win(width, height,dict_win,win):
    dict_win["WIDHT"] = width
    dict_win["HIDHT"] = height
    write_json("sett_menu.json","json",dict_win)
    win.WIN = pygame.display.set_mode((width,height))
    win.IMAGE_MENU = win.NAME_IMAGE_MENU
    win.IMAGE_MENU = win.load(win.IMAGE_MENU,width,height)
    return dict_win



class Music:
    def __init__(self,dict_mucis):
        self.ON_OFF = True
        self.FON = dict_mucis["FON"]
        pygame.mixer.music.load(paths_json(self.FON[0],"music"))

        self.CHANGE = pygame.mixer.Sound(paths_json("chek.mp3", "music"))

    def play_fon(self,number):
        if self.ON_OFF:
            pygame.mixer.music.load(paths_json(self.FON[number-1],"music"))
            pygame.mixer.music.play()
    def play_music(self):
        if self.ON_OFF:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()