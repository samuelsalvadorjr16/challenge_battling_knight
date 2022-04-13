from pathlib import Path
import json

class Files:
    def read_moves(self):
        """
            Read Move FIles
        """

        file1 = open("./moves.txt","r")
        movements  = file1.read().split('\n')

        print(movements)
        if movements[0] == 'GAME-START':
            movements.pop(0)

        if movements[-1] == 'GAME-END':
            movements.pop()

        print(movements)
        file1.close()

        return tuple(tuple(movement.split(':')) for movement in movements)

    def commit_results(self,result):

        
        return Path('./final_state.json').write_text(json.dumps(result))


