import pygame#Импортируем полностю пайгейм
from modul.my_json import*#Импортируем my_json с папки modul(це наш власный иодуль)
pygame.init()#Иницильзуем пайгейм

#Создаем клас Setting
class Setting:
    #создаем функцию конструктор __init__ (self - вказуем что конструктор пренадлежыт класу,вказуем необходимые параметры с  словныка setting,вказуем кординаты на которых будут рисовать, цвет, и картинку)
    def __init__ (self,width=setting["WIDHT"],hight=setting["HIDHT"],x=0,y=0,color=setting["COLOR"],image = None):
        self.WIDTH = width
        self.HIGHT = hight 
        self.Y = y
        self.X = x
        self.COLOR = color
        self.IMAGE = image
        if self.IMAGE:#Проверка есть ли картинка
            self.IMAGE = paths_json(self.IMAGE,"image")#Загружаем путь картинкы (назву,назву папкы)
            self.IMAGE = pygame.image.load(self.IMAGE)#загружаем картинку (путь)
            self.IMAGE = pygame.transform.scale(self.IMAGE,(self.WIDTH,self.HIGHT))#трансформируем картинку под нужные размеры(картинка(размеры екрана))
    #Создаем функцию обновления екрана
    def reset(self,win): 
        if self.IMAGE:#Проверяем наличые картинкы
            win.blit(self.IMAGE,(self.X,self.Y))#Рисуем картинку на окне(win) вказуем какую картинку рисуем, кортежом вказуем кординаты откуда рисуем
        elif self.COLOR:# есле картинку не нашло но есть цвет
            win.fill(self.COLOR)#Тогда окно заливаем цветом rgb
#Создаем клас Text
class Text:
    #Создаем функцию конструктора __init__(self - вказуем что конструктор пренадлежыт класу,font - шрифт,text - текст,x и y кординаты,color-цвет текста который получым после создания)
    def __init__(self,font,text,x,y,color):
        self.TEXT = text
        self.X = x 
        self.Y = y
        self.FONT_FAMILY = font
        self.COLOR = color
        if self.FONT_FAMILY:# проверяем наличые шрифта
            self.FONT_FAMILY = paths_json(self.FONT_FAMILY,"Font")#записуем в поле шрифта путь(название,папку)где находитса шрифт
        else:#есле шрифта нету
            self.FONT_FAMILY = None#Обозначаем что его нет
        self.FONT_SIZE = 100#Ставим максимальный размер(как по мне ето слишком даже есле на шыроком екране прыложение открыть,ну конечно есле на небосребе играть тогда норм)
        self.FONT = pygame.font.Font(self.FONT_FAMILY,self.FONT_SIZE)#Создаем текст с шрифтом и размером
        
        #Создаем функцию обновление размера текста в душках кроме надоедлего self еще есть btn - кнопка
    def resize(self,btn):
        self.TEXT_OBJ = self.FONT.render(self.TEXT,True,self.COLOR)#рендерим обьєкт текста(текст,вкл зглажывание,цвет)
        w,h = self.TEXT_OBJ.get_width(),self.TEXT_OBJ.get_height()#Узнаем размер у обьєкта текста
        while w > btn.WIDTH-15 or h > btn.HIGHT-15 :#делаем постояно по текст не влезит в кнопку
            self.FONT_SIZE -= 5 #Отнимаем от размера шрифта 5
            self.FONT = pygame.font.Font(self.FONT_FAMILY,self.FONT_SIZE)#Обновляем текст
            self.TEXT_OBJ = self.FONT.render(self.TEXT,True,self.COLOR)#Рендерим сам текст(теперь он существует)
            w,h = self.TEXT_OBJ.get_width(),self.TEXT_OBJ.get_height()#Записуем в переменіе размеры текста чтоб есле текст не влезает уменшыть его
        self.Y =btn.BUTTON.y + (btn.HIGHT -h)//2# получаем y кнопки додаем размер кнопки - размер текста поделены на 2
        self.X =btn.BUTTON.x + (btn.WIDTH -w)//2# получаем x кнопки додаем размер кнопки - размер текста поделены на 2
        #Создаем функцию обновление рзмера текста в душках self, win - окно, btn - екземпляр кнопки
    def reset(self,win,btn):
        self.resize(btn)#запускам функцию resize класа Text через селф
        win.blit(self.TEXT_OBJ,(self.X,self.Y))#рисуем обьєкт текста на кординатах в кортеже
    def update(self,new_text):
        self.TEXT = new_text
        self.TEXT_OBJ = self.FONT.render(self.TEXT,True,self.COLOR)
#Создаем клас Button и вказуем его родителя
class Button(Setting):
    #Создаем функцию конструктора __init__ (self, width и hight-размер окна,x и y-кординаты, color-цвет, image-картинка,text-текст,text_color-цвет текста,font-шрифт)
    def __init__(self,width,hight,x,y,color,image,text,text_color,font):
        super().__init__(width,hight,x,y,color,image)#берем у родителя(Setting) даные через супер такие как(width hight-размер окна,x и y-кординаты,color-цвет,image-картинку)крч почти все
        self.BUTTON=pygame.rect.Rect(self.X, self.Y,self.WIDTH, self.HIGHT)#Создаем рект добавляем ему кординаты и размеры окна
        self.BUTTON_TEXT=Text(font,text,x,y,text_color)#Создаем текст с помощу класа Text передаем ему значения шрифт,текст,кординаты,цвет
        self.BUTTON_TEXT.resize(self)
    #Создаем функцию обновление кнопок
    def reset(self,win):
        if self.IMAGE:#Проверяем наличее картинкы
            win.blit(self.IMAGE,(self.BUTTON.x,self.BUTTON.y))#Рисуем картинку как задний фон кнопке вказуем ему переменые картинку кординаты кнопок
        elif self.COLOR:#Есле нет картинкы
            pygame.draw.rect(win,self.COLOR,self.BUTTON)#Рисуем прямо угольник с помощу ректа вказуем ему окно,увет,рект
            #pygame.draw.reason(win,self.)
        self.BUTTON_TEXT.reset(win,self)#Создаем текст на кнопку и указуем ему переменые окно,self
#Создаем клас GroupButton и у него нет родителей(
class GroupButton:
    #Создаем функцию конструктора __init__(self,set_win-размеры окна,dict_btn-словнык)
    def __init__(self,set_win,dict_btn,work):
        self.COUNT = dict_btn["COUNT_BTN"]#загружаем количества текста с словныка 
        self.BTN_LIST = list()#создаем пустой список
        self.TEXT_LIST = dict_btn["TEXT_BTN"]#загружаем текст с словныка
        self.SET_WIN = set_win#тут даже коментировать незачем
        self.WORK = work
        self.creat_btn(dict_btn,self.SET_WIN)

    def creat_btn(self,dict_btn, new_set_win):
        self.resize(new_set_win)#вызываем функцию resize класа GroupButton через селф и вказуем ему размеры окна
        for i in range(self.COUNT):#повторюем пока range не дойдет до конца self.COUNT
            #79 строка очень огромная лучше ее розложыть н рядов 3+
            self.BTN_LIST.append(Button(self.BTN_W,self.BTN_H,self.BTN_X,self.BTN_Y,dict_btn["COLOR"],dict_btn["IMAGE"],self.TEXT_LIST[i],dict_btn["COLOR_TXT"],dict_btn["FONT"]))#Добавить в список(создаем с помощу класа Button(Высоту Шырену кнопок,кординаты кнопок,цвет(с словныка),картинку(с словныка),берем текст с списка[i],цвет текста(с словныка),шрифт(с словныка)))
            self.BTN_Y +=self.BTN_H//3 + self.BTN_H# опускаем кнопку по кординатам y на высоту кнопки//3(отступ) + высоту кнопки
    #Создаем функцию обновление размеров (self,new_set_win- тоже самое что и set_win только поновее)
    def resize(self,new_set_win):
        self.SET_WIN = new_set_win
        center_X,center_Y = self.SET_WIN["WIDHT"]//2,self.SET_WIN["HIDHT"]//2#узнаем центр екрана x и y просто размеры екрана делим на 2(то и то)
        self.BTN_W,self.BTN_H = self.SET_WIN["WIDHT"]//5,self.SET_WIN["HIDHT"]//10#создаем размеры высоту и шырену для кнопок
        center_btn_X, center_btn_Y = self.BTN_W//2,(self.BTN_H*self.COUNT + (self.COUNT-1) * self.BTN_H//3)//2#узнаем центр кнопок x и y размеры екрана делим на 2(то и то) + узнаем растояние между кнопок и делим н 2
        self.BTN_X,self.BTN_Y = center_X - center_btn_X, center_Y - center_btn_Y#Узнавшы все даные узнаем кординаты кнопок для етого центр x отнимаем центр кнопки x и центр y отнимаем центр кнопки y
    #Создаем функцию обновление кнопок (self, win - окно)
    def reset(self,win):
        if self.WORK:
            for i in range(self.COUNT):#Повторяем self.COUNT раз
                self.BTN_LIST[i].reset(win)#рисуем со списка self.BTN_LIST с помощу self.BTN_LIST[i] берем кнопку и обновляем на (win-окне)