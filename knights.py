class Knights:
	if __name__ == '__main__':
		print('Init')

	life = 1
	defence = 1
	attack = 1
	curent_position = [0,0]
	curr_X = 0
	curr_Y = 0
	name = ""
	inventory = False
	status = False
	code = ""

	def update_status(self, num):
		self.life = num
		return True

	def get_status(self):
		return self.life

	def set_Position(self, x, y):
		self.curr_X = x
		self.curr_Y = y
		self.curent_position = [x,y]
		return [self.curr_X, self.curr_Y]

	def set_BasicAttributes(self, lf, defnc):
		self.life = lf
		self.defence = defnc
		return [self.life, self.defence]

	def set_DefaultValues(self, defX, defY, defName, defcode=False):
		self.set_Position(defX,defY)
		self.name = defName
		self.code = defcode

	def get_Position(self):
		return [self.curr_X, self.curr_Y]

	def get_NetBattleAttribute(self, items):
		life = self.life
		defence = self.defence
		attack = self.attack
		if self.inventory:
			equip =  items[self.inventory]
			attack += equip.attack
			defence += equip.defence
			return {'life':life,'attack': attack, 'defence':defence}
		return {'life':life,'attack': attack, 'defence':defence }

	def get_FinalData(self,items):

		battAttributes = self.get_NetBattleAttribute(items)
		
		return (
				(self.curr_X,self.curr_Y) if self.status in [False,"DEAD"]  else None,  # POS
				"LIVE" if not self.status else self.status, # STATUS
				None if not self.inventory else items[self.inventory].name, #INVENTORY
				battAttributes['attack'] if not self.status else 0,
				battAttributes['defence'] if not self.status else 0
		)

