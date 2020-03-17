import time

import pyautogui

from config import Config
from coord import Coord
from imagesearch import imagesearcharea

'''
TODO make actions come from player(bot) class so the character and tibia can communicate
'''


class Player:
    __fought = bool
    __capacity = int
    __position = Coord
    __last_position = Coord

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        self.__position = position

    @property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, capacity):
        self.__capacity = capacity

    @property
    def last_position(self):
        return self.__last_position

    @last_position.setter
    def last_position(self, last_position):
        self.__last_position = last_position

    @property
    def fought(self):
        return self.__fought

    @fought.setter
    def fought(self, boolean):
        self.__fought = boolean

    # TODO spells

    def __init__(self):
        self.fought = False
        self.capacity = 999
        self.position = Coord([-1, -1])
        self.last_position = Coord([-1, -1])

    def __str__(self):
        return "(position) \n" + str(self.position) + '\n' \
               + "(up) \n" + str(Config.up) + '\n' \
               + "(down) \n" + str(Config.down) + '\n' \
               + "(left) \n" + str(Config.left) + '\n' \
               + "(right) \n" + str(Config.right) + '\n' \
               + "(last position) \n" + str(self.last_position) + '\n' \
               + "(capacity) \n" + str(self.capacity) + '\n'

    def is_fighting(self):
        print(Config.battle_list)
        if pyautogui.pixelMatchesColor(Config.battle_list.x, Config.battle_list.y, Config.red) or \
                pyautogui.pixelMatchesColor(Config.battle_list.x, Config.battle_list.y, Config.pink):
            self.fought = True

            self.follow(Config.follow, Config.green_follow)
            return True
        elif not pyautogui.pixelMatchesColor(Config.monster.x, Config.monster.y, Config.gray) and not self.fought:
            pyautogui.click(Config.monster.x, Config.monster.y)
            pyautogui.moveTo(5, 5)
            self.follow(Config.follow, Config.green_follow)
            return False

    def is_in_mark_center(self, mark, starter_mark):
        if self.position.x < Config.left or self.position.x > Config.right \
                or self.position.y < Config.up or self.position.y > Config.down:
            # if self.position == self.last_position:
            mark.x, mark.y = imagesearcharea(Config.markers[starter_mark], Config.map_begin.x,
                                             Config.map_begin.y, Config.map_end.x, Config.map_end.y)

            self.position.x = Config.map_begin.x + mark.x + 3
            self.position.y = Config.map_begin.y + mark.y + 3

            pyautogui.click(self.position.x, self.position.y)
            pyautogui.moveTo(5, 5)
            return True
        else:
            pyautogui.click(self.position.x, self.position.y)
            pyautogui.moveTo(5, 5)
            return False

    @staticmethod
    def heal():
        if not (pyautogui.pixelMatchesColor(Config.life_bar_low.x, Config.life_bar_low.y, Config.life_low)):
            pyautogui.press('f1')
        else:
            if not (pyautogui.pixelMatchesColor(Config.life_bar_high.x, Config.life_bar_high.y, Config.life_high)):
                pyautogui.press('f3')
            if not (pyautogui.pixelMatchesColor(Config.mana_bar.x, Config.mana_bar.y, Config.mana)):
                pyautogui.press('f2')

    def loot(self):
        self.fought = False
        time.sleep(0.7)

        pyautogui.keyDown('shift')
        pyautogui.click(button='right', x=Config.down_player.x, y=Config.down_player.y)
        pyautogui.click(button='right', x=Config.diag_down_left_player.x, y=Config.diag_down_left_player.y)
        pyautogui.click(button='right', x=Config.left_player.x, y=Config.left_player.y)
        pyautogui.click(button='right', x=Config.diag_up_left_player.x, y=Config.diag_up_left_player.y)
        pyautogui.click(button='right', x=Config.up_player.x, y=Config.up_player.y)
        pyautogui.click(button='right', x=Config.diag_up_right_player.x, y=Config.diag_down_right_player.y)
        pyautogui.click(button='right', x=Config.right_player.x, y=Config.right_player.y)
        pyautogui.click(button='right', x=Config.diag_down_right_player.x, y=Config.diag_down_right_player.y)
        pyautogui.keyUp('shift')

        pyautogui.moveTo(5, 5)

    @staticmethod
    def follow(follow, green_follow):
        if not pyautogui.pixelMatchesColor(follow.x, follow.y, green_follow):
            pyautogui.click(follow.x, follow.y)
            pyautogui.moveTo(5, 5)
