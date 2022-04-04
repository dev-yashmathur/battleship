import random

class BattleShip:
    ships_left = dict({5:2, 4: 2, 3:1})
    opponent_board = [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    ]
    def __init__(self):
        self.team_name = "Meh"
        self.ships = ships
        self.opponent_board = opponent_board
        self.info = -1

    def set_ships(self):
        #coordinates,size of shipe,orientation 0-horizontal 1-vertical
        self.ships = [
            [1,1,5,0],
            [2,1,5,0],
            [3,1,4,0],
            [4,1,4,0],
            [5,1,3,0]
        ]
        return self.ships

    def attack(self):
        #need the lowest key 
        min_ship = list(self.ships_left.keys()).sort()[0] #This gives us the least number to check for parity
       # return (x, y)
    heatmap = [[0 for _ in range(10)] for _ in range(10)]
    parity = [[0 for _ in range(10)] for _ in range(10)]
    def probs(self):
        for ship in self.ships_left.keys():
            for count in range(self.ships_left[ship]): #Doing this for each left ship
                for orientation in [0,1]:
                    row = 0
                    while row < 10:
                        col = 0
                        while col<10:
                            if self.opponent_board[row][col] == -1:
                                if (orientation == 0 and row+ship<10) or (orientation == 1 and col+ship<10):
                                    flag = True
                                    for i in range(1,ship):
                                        if (orientation == 0 and self.opponent_board[row+i][col] == -1) or (orientation == 1 and self.opponent_board[row][col+i] == -1):
                                            continue 
                                        else:
                                            flag=False 
                                            break
                                    if flag == True:
                                       for i in range(ship):
                                            if orientation==0: 
                                               self.heatmap[row+i][col]+=1
                                            else:
                                                self.heatmap[row][col+i]+=1
                            col+=1
                        row+=1

    def parity(self):
       bias=0
       row=0
       col=0
       # 3 element parity 
       for i in row:
           for j in col:
               if (row+bias)%3==0:
                 self.parity[i][j]='R'
               elif (row+bias)%3==1:
                 self.parity[i][j]='G'
               else:
                   self.parity[i][j]='B'
             col+=1
             bias+=1
         row+=1



    def hit_or_miss(self, x, y, info):
        self.info = info
        # info = 1 for miss, 0 for a hit, -1 for an out of range shooting, 2 for special move nullify. 3 for your next move to be a Hawkeye Shot
        if info != -1 and info == 0:
            self.opponent_board[x][y] = info



