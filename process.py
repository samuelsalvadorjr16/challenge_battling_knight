from knights import Knights
from items import Items
import constants as ct
from time import sleep
from files import Files

class Process:
    
    ItemsObj = Items()

    knights ={
            'R': Knights(), # RED
            'B': Knights(), # BLUE
            'G': Knights(), # GREEN
            'Y': Knights(), # YELLOW
        }

    ditems ={
        'A': Items(), # Axe
        'D': Items(), # Dagger
        'H': Items(), # Helment
        'M': Items(), # MagicStaff
        }

    def checkTiles(self,knight):
        #Check If Knight Equipment
        if not knight.inventory:
            print(knight.get_Position())
            for item in dict(sorted(self.ditems.items())):
                print('ITEM %s' % item)
                print(self.ditems[item].get_Position())
                if knight.get_Position() == self.ditems[item].get_Position():
                    #Assigned Equipement to Knights and Assigned Items Availabililty
                    knight.inventory = item
                    self.ditems[item].is_equipped  = True
                    self.ditems[item].equipped_by  = knight.code 

        #After Checking Equipment Check Other Knight Collision and For Battle Mode
        for sknight in self.knights:
            if knight.code == sknight:
                continue
            pknight = self.knights[sknight]
            if knight.get_Position() == pknight.get_Position():
                print('%s START TO CLASH WITH %s' %(knight.name,pknight.name))
                attacker_knight = knight
                defender_knight = pknight

                defender_knight_attribute = defender_knight.get_NetBattleAttribute(self.ditems)
                attacker_knight_attribute = attacker_knight.get_NetBattleAttribute(self.ditems)


                dead_knight = False

                #CHECK BATTLE RESULTS
                if attacker_knight_attribute['attack'] + ct.BONUS_SUPRISE_ATTACK > defender_knight_attribute['defence']:
                    dead_knight  = defender_knight
                else:
                    dead_knight  = attacker_knight_attribute

                if dead_knight:
                    print('%s IS DEAD' %(dead_knight.name))
                    #Check Dead Knight Inventory and Drop it
                    dead_knight.status="DEAD"
                    dead_knight.defence = 0
                    dead_knight.attack = 0
                    if dead_knight.inventory:
                        _ditems = self.ditems
                        _ditems[dead_knight.inventory].curr_X = dead_knight.curr_X
                        _ditems[dead_knight.inventory].curr_Y = dead_knight.curr_Y
                        _ditems[dead_knight.inventory].is_equipped = False
                        _ditems[dead_knight.inventory].equipped_by = False
                        dead_knight.inventory = False

    def processMovements(self):
        sfile = Files()
        
        movements = sfile.read_moves()
        print(self.knights[ct.RED].name)
        print(self.knights[ct.RED].curr_X)
        print(self.knights[ct.RED].curr_Y)
        for knight, movement in movements:
            print("Name : %s : %s move in %s" % (self.knights[knight].name, knight, ct.move_name[movement]))
            currKnight = self.knights[knight]

            if movement == 'N':
                currKnight.curr_X  -=1
            elif movement == 'E':
                currKnight.curr_Y  +=1
            elif movement == 'W':
                currKnight.curr_Y  -=1
            elif movement == 'S':
                currKnight.curr_X  +=1
            print(currKnight.get_Position())
            sleep(0.01)

            if currKnight.curr_X < 0 or currKnight.curr_X > 7  or currKnight.curr_Y < 0 or currKnight.curr_X > 7:
                print("%s Knight Drowned" % currKnight.name)
                currKnight.status = "DROWNED"
                currKnight.defence = 0
                currKnight.attack = 0
                #GET KNOWN LAST POSITION FOR THE ITEMS
                cur_X = currKnight.curr_X
                cur_Y = currKnight.curr_Y

                if cur_X < 0:
                    cur_X = 0
                if cur_X > 7:
                    cur_X = 7
                if cur_Y < 0:
                    cur_Y = 0
                if cur_Y > 7:
                    cur_Y = 7
                if currKnight.inventory:
                    self.ditems[currKnight.inventory].curr_X = cur_X
                    self.ditems[currKnight.inventory].curr_Y = cur_Y
                    self.ditems[currKnight.inventory].is_equipped = False
                    self.ditems[currKnight.inventory].equipped_by = False
                    
                    currKnight.inventory = False
                

            if currKnight.status not in ["DROWNED", "DEAD"]:
                self.checkTiles(currKnight)

        return {
                "red": self.knights[ct.RED].get_FinalData(self.ditems),
                "blue": self.knights[ct.BLUE].get_FinalData(self.ditems),
                "green": self.knights[ct.GREEN].get_FinalData(self.ditems),
                "yellow": self.knights[ct.YELLOW].get_FinalData(self.ditems),
                
            }

    def ExecuteGame(self):
        print('Knights')
        #SET KNIGHTS POSITION
        self.knights[ct.RED].set_DefaultValues(0,0,"RED", ct.RED)
        self.knights[ct.BLUE].set_DefaultValues(7,0,"BLUE", ct.BLUE)
        self.knights[ct.GREEN].set_DefaultValues(7,7,"GREEN", ct.GREEN)
        self.knights[ct.YELLOW].set_DefaultValues(0,7,"YELLOW", ct.YELLOW)

        print('Items')
        #SET ITEMS POSITION
        self.ditems[ct.AXE].set_defaultPosition(2,2,"Axe",ct.AXE)
        self.ditems[ct.DAGGER].set_defaultPosition(2,5,"Dagger",ct.DAGGER)
        self.ditems[ct.HELMET].set_defaultPosition(5,5,"Helmet",ct.HELMET)
        self.ditems[ct.MAGICSTAFF].set_defaultPosition(5,2,"MagicStaff",ct.MAGICSTAFF)

        #SET ITEMS ATTRIBUTES

        self.ditems[ct.AXE].set_ItemBaseAttributes(2,0)
        self.ditems[ct.DAGGER].set_ItemBaseAttributes(1,0)
        self.ditems[ct.HELMET].set_ItemBaseAttributes(0,1)
        self.ditems[ct.MAGICSTAFF].set_ItemBaseAttributes(1,1)

        

        res = self.processMovements()
        res['magic_staff']  = self.ditems[ct.MAGICSTAFF].get_FinalData(self.knights)
        res['helmet']  = self.ditems[ct.HELMET].get_FinalData(self.knights)
        res['dagger'] =  self.ditems[ct.DAGGER].get_FinalData(self.knights)
        res['axe']= self.ditems[ct.AXE].get_FinalData(self.knights)
        
                
        sfile = Files()
        sfile.commit_results(res)

