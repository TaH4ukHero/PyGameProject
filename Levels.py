class First_Level:
    def __init__(self):
        self.hero = [1, 16]
        self.finish_flag = (40, 2), 'Finish'
        self.enemys = ([2, 3, 12], [12, 4, 19], [18, 6, 24], [29, 8, 24], [24, 11, 18])
        self.map_name = 'second.tmx'
        self.jump_height = 12


class Second_Level:
    def __init__(self):
        self.hero = [1, 12]
        self.finish_flag = (42, 3), 'Finish'
        self.map_name = 'Third.tmx'
        self.jump_height = 12


class Third_Level:
    def __init__(self):
        self.hero = [1, 16]
        self.finish_flag = (11, 8), 'Finish'
        self.map_name = 'Artem.tmx'
        self.enemys = [[13, 16, 16], [29, 8, 32], [36, 13, 39], [36, 4, 39]]
        self.jump_height = 11.5