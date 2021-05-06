from settings import Settings
import numpy as np
import win32api
import win32con
import copy


class GameLogic:

    def __init__(self, stats):
        self.settings_vis = Settings()
        self.stats = stats
        self.chessboard = np.zeros([30, 30], dtype=int)
        self.ship_self = {'location': np.array([29, 29], dtype=int), 'missile': 4}
        self.ship_enemy = {'location': np.array([0, 0], dtype=int), 'missile': 4}
        self.missile_location = [{}, {}]
        self.missile_travelled = [{}, {}]

    def get_ship(self, ship_number):
        if ship_number == 1:
            ship = self.ship_self
        elif ship_number == 0:
            ship = self.ship_enemy
        else:
            win32api.MessageBox(0, "输入的 ship_number 无效，可能影响程序运行！", "警告", win32con.MB_ICONWARNING)
            ship = self.ship_self
        return ship

    def move(self, ship_number, direction):
        """
        :param ship_number: 0 代表对敌机操作，1 代表对己方飞机操作
        :param direction: 1, 2, 3, 4 分别对应 上，下，左，右
        :return: move 操作是否成功
        """

        ship = self.get_ship(ship_number)
        flag_is_moved = False

        if direction == 1:
            if ship['location'][1] >= 1:
                ship['location'][1] -= 1
                flag_is_moved = True
        elif direction == 2:
            if ship['location'][1] <= 28:
                ship['location'][1] += 1
                flag_is_moved = True
        elif direction == 3:
            if ship['location'][0] >= 1:
                ship['location'][0] -= 1
                flag_is_moved = True
        elif direction == 4:
            if ship['location'][0] <= 28:
                ship['location'][0] += 1
                flag_is_moved = True
        else:
            win32api.MessageBox(0, "输入的 direction 无效，可能影响程序运行！", "警告", win32con.MB_ICONWARNING)
        self.stats.next_operation()

        # print("ship_number:", ship_number, "direction", direction, "ship_location:", ship['location'])
        return flag_is_moved

    def launch(self, ship_number):
        """
        :param ship_number: 0 代表导弹属于敌机，1 代表导弹属于己方飞机
        """

        ship = self.get_ship(ship_number)

        if ship['missile'] >= 1:
            ship['missile'] -= 1
            self.missile_location[ship_number][3 - ship['missile']] = copy.copy(ship['location'])
            self.missile_travelled[ship_number][3 - ship['missile']] = 0

        self.stats.next_operation()

    def trace(self, ship_number, missile_number):
        """
        :param ship_number: 0 代表导弹属于敌机，1 代表导弹属于己方飞机
        :param missile_number: 用 0 ~ 3 表示
        :return: 游戏是否结束，导弹行动（(0,0))-消失，其余对应动作），即是否有飞机被导弹击中，根据operation可判断胜利方
        """
        game_over = False
        goal_location = self.get_ship(1 - ship_number)['location']
        self_location = self.missile_location[ship_number][missile_number]
        action = [0, 0]

        # print("goal_location:", goal_location, "self_location:", self_location)
        distance = abs(goal_location[0] - self_location[0]) + abs(goal_location[1] - self_location[1])
        if distance <= 2:
            self.missile_location[ship_number][missile_number] = np.array([-1, -1], dtype=int)
            self.missile_travelled[ship_number][missile_number] = -1
            game_over = self.is_hit(self.missile_travelled[ship_number][missile_number] + distance)
            return game_over, action

        if self.missile_travelled[ship_number][missile_number] >= 20:
            self.missile_location[ship_number][missile_number] = np.array([-1, -1], dtype=int)
            self.missile_travelled[ship_number][missile_number] = -1
            return False, action

        for i in range(2):
            if abs(goal_location[0] - self_location[0]) > abs(goal_location[1] - self_location[1]):
                choose_number = 0
            elif abs(goal_location[0] - self_location[0]) < abs(goal_location[1] - self_location[1]):
                choose_number = 1
            else:
                tmp = np.random.random()
                if tmp >= 0.5:
                    choose_number = 0
                else:
                    choose_number = 1
            if goal_location[choose_number] > self_location[choose_number]:
                self.missile_location[ship_number][missile_number][choose_number] += 1
                action[i] = 2 * (2 - choose_number)
            else:
                self.missile_location[ship_number][missile_number][choose_number] -= 1
                action[i] = 3 - 2 * choose_number
            self.missile_travelled[ship_number][missile_number] += 1

        # print("ship_number:", ship_number, "missile_number:", missile_number)
        # print("\tmissile_location:", self.missile_location[ship_number][missile_number])
        # print("\tmissile_travelled:", self.missile_travelled[ship_number][missile_number])
        return game_over, action

    def is_hit(self, missile_travelled):
        if missile_travelled <= 2:
            return True
        else:
            tmp = np.random.random()
            if tmp > missile_travelled / 20 - 0.1:
                return True
        return False

    def show(self):
        print("chessboard:\n", self.chessboard)
        print("ship_self: location: ", self.ship_self['location'], "\tmissile:", self.ship_self['missile'])
        print("ship_enemy: location: ", self.ship_enemy['location'], "\tmissile:", self.ship_enemy['missile'])
