class Items:
    attack = 0
    defence = 0
    curr_X = 0
    curr_Y = 0
    is_equipped = False
    equipped_by = False
    name = ""
    code = ""

    def set_defaultPosition(self, x, y,name, code):
        self.curr_X = x
        self.curr_Y = y
        self.name = name
        self.code = code
        return [self.curr_X, self.curr_Y]

    def set_ItemBaseAttributes(self, atk, defnc):
        self.attack = atk
        self.defence = defnc
        return [self.attack, self.defence]

    def get_Position(self):
        return [self.curr_X, self.curr_Y]

    def get_FinalData(self,knights):
        return (
				(self.curr_X,self.curr_Y) if not self.is_equipped  else knights[self.equipped_by].get_Position(),  # POS
                self.is_equipped # Equip?
                )
