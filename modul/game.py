import pygame
from modul.dataclass import*
from modul.my_json import*
from modul.datagame import*
import modul.menu as m

pygame.init() #зделал, на 2 пташках, но пропадает

def run_game(conect):
    if conect == "restart":
        try:
            set_game = rid_json("sett_menu_restart.json","json")
        except:
            set_game = rid_json("sett_menu.json","json")
    elif conect == "new":
        set_game = rid_json("sett_menu.json","json")
        del_reset()
    win_game = Window(set_game,'game')

    #back_menu = GroupButton(win_game,set_game,True)
    count_click = 0
    i_b,j_b = None,None 

    angry_birds = Game_bird(set_game)
    game = True
    paly = True
    m.music.play_music()
    while game:
        
        win_game.reset()#Заливаем окно цветом который берем с словныка уже и так понятно с какого
        angry_birds.reset(win_game.WIN,set_game)
        for event in pygame.event.get():#Проверяем евенты - события
            if event.type == pygame.QUIT:#Проверяем нажатие на крестик в окне
                game = False#меняем локальную переменую на False - останавливаем цыкл
                if paly:
                    create_restart_game(win_game,angry_birds)
                else:
                    del_reset()

                m.run()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if win_game.BTN_MENU.BUTTON.collidepoint(event.pos):
                    game = False#меняем локальную переменую на False - останавливаем цыкл
                    if paly:
                        create_restart_game(win_game,angry_birds)
                    else:
                       del_reset()
                    m.run()
                if paly:
                    for i in range(len(angry_birds.MAP_RECT)):
                        for j in range(len(angry_birds.MAP_RECT)):
                            if angry_birds.MAP_RECT[i][j].collidepoint(event.pos):
                                count_click +=1
                                if count_click == 1:
                                    i_b,j_b = i,j
                                    pygame.draw.rect(win_game.WIN,(120,0,0),angry_birds.MAP_RECT[i_b][j_b],width=10)
                                elif count_click == 2:
                                    pygame.draw.rect(win_game.WIN,(120,0,0),angry_birds.MAP_RECT[i][j],width=10)
                                    if (i == i_b and abs(j-j_b) == 1) or (j == j_b and abs(i-i_b) == 1):
                                        angry_birds.MAP[i][j],angry_birds.MAP[i_b][j_b] = angry_birds.MAP[i_b][j_b],angry_birds.MAP[i][j]
                                        angry_birds.STATS.PLAYER_MOVE+=1
                                        pygame.mixer.music.set_volume(5)
                                        m.music.CHANGE.play()
                                        pygame.mixer.music.set_volume(1)
                                    count_click = 0
                                    i_b,j_b=None,None
                
                if paly:
                    angry_birds.check_line()
                    angry_birds.check_row()

            if angry_birds.STATS.PLAYER_MOVE- angry_birds.STATS.MAX_BIRD_MOVE == 0:
                paly = False
                if angry_birds.STATS.PLAYER_TASK -  angry_birds.STATS.COUNT_BIRD_TASK == 0:
                    angry_birds.STATS.show_end_text(win_game.WIN,set_game, "YOU WIN!!!!")
                    
                else:
                    angry_birds.STATS.show_end_text(win_game.WIN,set_game, "YOU LOOSe :(")
                
            else:
                if angry_birds.STATS.PLAYER_TASK -  angry_birds.STATS.COUNT_BIRD_TASK == 0:
                    angry_birds.STATS.show_end_text(win_game.WIN,set_game, "YOU WIN!!!!")
                    paly = False


            pygame.display.flip()#Обновляем екран
            win_game.CLOCK.tick(win_game.FPS)