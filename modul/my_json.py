import json#Импортируем джсон 
import os#Импортируем ос
def paths_json(namefile,namefolder):#создаем функцию для знаходження обсолюьного пути с обезательными переменами названием файла и папки в которой находитса той или иной файл
    s = os.path.abspath(__file__+"/..")#находим путь к файлу
    s = s.split("\\")#Разбиваем путь и переделуем его в список
    del s[-1]#удаляем последний елемент списка
    s = "\\".join(s)#обьэднуем спысок
    s = os.path.join(s,namefolder,namefile)#соиденяем абсолютний шлях
    return s#возращем то что получыли
#создаем словнык setting
setting = {"HIDHT": 800,
"WIDHT": 1200,
"COLOR":(153,0,76)}
#создаем функцию для записание и пере записание словника в json файл
def write_json(namefile,namefolder,namedict):#создаем функцию write_json с обезательными перемеными название файл, название папки, название словныка
    p = paths_json(namefile,namefolder)#находим и записуем абсолютный путь получая обезательные переменые названия файла и папки после чего записуем в переменую p 
    with open(p,"w",encoding="UTF-8") as file:#Открываем, создаем файл на запись с перемеными p(абсольтний шлях), w -запись, дальше не точно encoding="UTF-8" ето каким кодингом будем записывать
        json.dump(namedict,file,indent=4)#? вроде соеденить не помню
#write_json("sett_menu.json","json",setting)
#создаем функцию для чтение json файлов
def rid_json(namefile,namefolder):#создаем функцию rid_json с обезательными перемеными название файл, название папки
    p = paths_json(namefile,namefolder)#находим и записуем абсолютный путь получая обезательные переменые названия файла и папки после чего записуем в переменую p
    with open(p,"r",encoding="UTF-8") as file:#Открываем только для чтение с перемеными p(абсольтний шлях), r -только чтение, дальше не точно encoding="UTF-8" ето каким кодингом будем чытать
        namedict = json.load(file)#Загружаем(открываем) с джсон файла словнык
        return namedict#Возвращаем полученые даные
def del_reset():
        try:
                os.remove(paths_json("sett_menu_restart.json","json"))
        except:
                print("No reset file")