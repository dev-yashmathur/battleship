class BattleShip:
    ships_left = dict({5:2, 4: 2, 3:1})

    lasthit = (-1,-1)
    right = -1
    left = -1
    top = -1
    bottom = -1

    heatmap = [[0 for _ in range(10)] for _ in range(10)]
    parity = [[0 for _ in range(10)] for _ in range(10)]
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
        self.team_name = "<Enter Team Name>"
        # self.ships = ships
        # self.opponent_board = opponent_board
        self.info = 1
        self.set_ships()

    def set_ships(self):
        #coordinates,size of shipe,orientation 0-horizontal 1-vertical 
        #random initialization 
        self.ships = [
            [1,1,5,1],
            [0,7,3,1],
            [9,3,4,1],
            [4,1,4,0],
            [2,8,4,0]
        ]
        return self.ships

    def indexOfMax(self):
        index = (0,0)
        max = 0
        i = 0
        for row in self.heatmap:
            j = 0
            for col in row:
                if col > max:
                    max = col
                    index = (i,j)
                j+=1
            i+=1
        return index

    def getHawkeyeCoord(self):
        maxH = -1
        hIndex = -1
        i = 0
        for row in self.opponent_board:
            if i == 0:
                i+=1
                continue
            if row.count(-1) > maxH:
                maxH = row.count(-1)
                hIndex = i
            i+=1
        
        maxY = -1
        yIndex = -1
        for col in range(1, 10):
            localCount = 0
            for row in range(10):
                if self.opponent_board[row][col] == -1:
                    localCount += 1
            if localCount > maxY:
                maxY = localCount
                yIndex = col

        return (hIndex, yIndex)

    def attack(self):
        myFile.write("LAST SQUARE WAS: " + str(self.lasthit) + "\n")
        for xyz in self.opponent_board:
            myFile.write(str(xyz) + "\n")
        myFile.write("\n\n\n")
        if self.info == 3:
            sq = self.getHawkeyeCoord()
            self.lasthit = sq
            for row_index in range(10):
                if self.opponent_board[row_index][sq[1]] == -1:
                    self.opponent_board[row_index][sq[1]] = 1
                if self.opponent_board[sq[0]][row_index] == -1:
                    self.opponent_board[sq[0]][row_index] = 1

            return sq
        #Below code is for Random guess
        #need the lowest key
        # min_ship = list(self.ships_left.keys()).sort()[0] #This gives us the least number to check for parity
        # self.parityFn(min_ship)
        self.probs()
        myFile.write("\n Heatmap: \n")
        for xyz in self.heatmap:
            myFile.write(str(xyz) + "\n")
        square = self.indexOfMax()
        self.lasthit = square
        return square
        # return (x, y)
    
    
    def probs(self):
        self.heatmap = [[0 for _ in range(10)] for _ in range(10)]
        for ship in self.ships_left.keys():
            for count in range(self.ships_left[ship]): #Doing this for each left ship
                for orientation in [0,1]:
                    row = 0
                    while row < 10:
                        col = 0
                        while col<10:
                            if self.opponent_board[row][col] in [-1, 0]:
                                if (orientation == 1 and row+(ship-1)<10) or (orientation == 0 and col+(ship-1)<10):
                                    flag = True
                                    for i in range(1,ship):
                                        if (orientation == 1 and self.opponent_board[row+i][col] in [-1, 0]) or (orientation == 0 and self.opponent_board[row][col+i] in [-1, 0]):
                                            continue 
                                        else:
                                            flag=False 
                                            break
                                    if flag == True:
                                       for j in range(ship):
                                            if orientation==1 and self.opponent_board[row+j][col] == -1: 
                                               self.heatmap[row+j][col]+=1
                                            elif orientation == 0 and self.opponent_board[row][col+j] == -1: #orientation 0
                                                self.heatmap[row][col+j]+=1
                            
                            
                            increased = False
                            if self.opponent_board[row][col] == 0: #It has been hit
                                if increased == False and row > 0 and self.opponent_board[row-1][col] == 0: #Below has been hit
                                    if row <9 and  self.opponent_board[row+1][col] == 0: #Up is Also HIT
                                        increased = True

                                # if increased == False and row < 9 and self.opponent_board[row+1][col] == 0: #Up has been hit
                                #     if row > 0 and  self.opponent_board[row-1][col] == 0: #Below is Also HIT
                                #         increased = True
                                
                                if increased == False and col > 0 and self.opponent_board[row][col-1] == 0: #Left has been hit
                                    if col < 9 and self.opponent_board[row][col+1] == 0: #Right is Also HIT
                                        increased = True

                                # if increased == False and col < 9  and self.opponent_board[row][col+1] == 0: #Right has been hit
                                #     if col > 0 and self.opponent_board[row][col-1] == 0: #Left is Also HIT
                                #         increased = True
                                #END OF BOTH SHOT
                                if increased == False and row > 0 and self.opponent_board[row-1][col] == 0: #Below has been hit
                                    if row <9 and  self.opponent_board[row+1][col] == -1: #Up is free
                                        self.heatmap[row+1][col]*= 999
                                        increased = True
                                        # continue #Just doing one at a time
                                
                                if increased == False and row < 9 and self.opponent_board[row+1][col] == 0: #Up has been hit
                                    if row > 0 and  self.opponent_board[row-1][col] == -1: #Below is free
                                        self.heatmap[row-1][col]*= 999
                                        increased = True
                                        # continue
                                
                                if increased == False and col > 0 and self.opponent_board[row][col-1] == 0: #Left has been hit
                                    if col < 9 and self.opponent_board[row][col+1] == -1: #Right is free
                                        self.heatmap[row][col+1]*= 999
                                        increased = True
                                        # continue
                                
                                if increased == False and col < 9  and self.opponent_board[row][col+1] == 0: #Right has been hit
                                    if col > 0 and self.opponent_board[row][col-1] == -1: #Left is free
                                        self.heatmap[row][col-1]*= 999
                                        increased = True
                                        # continue
                                #End of one hit along axis

                                if increased == False and row > 0 and self.opponent_board[row-1][col] == 1: #Below has been hit
                                    if row <9 and  self.opponent_board[row+1][col] == -1: #Up is free
                                        self.heatmap[row+1][col]*= 999
                                        increased = True
                                        # continue #Just doing one at a time
                                
                                if increased == False and row < 9 and self.opponent_board[row+1][col] == 1: #Up has been hit
                                    if row > 0 and  self.opponent_board[row-1][col] == -1: #Below is free
                                        self.heatmap[row-1][col]*= 999
                                        increased = True
                                        # continue
                                
                                if increased == False and col > 0 and self.opponent_board[row][col-1] == 1: #Left has been hit
                                    if col < 9 and self.opponent_board[row][col+1] == -1: #Right is free
                                        self.heatmap[row][col+1]*= 999
                                        increased = True
                                        # continue
                                
                                if increased == False and col < 9  and self.opponent_board[row][col+1] == 1: #Right has been hit
                                    if col > 0 and self.opponent_board[row][col-1] == -1: #Left is free
                                        self.heatmap[row][col-1]*= 999
                                        increased = True
                                        # continue

                                #End of one free along axis
                                if increased == False and row > 0 and self.opponent_board[row-1][col] == -1:
                                    self.heatmap[row-1][col] *= 999
                                if increased == False and row < 9 and self.opponent_board[row+1][col] == -1:
                                    self.heatmap[row+1][col] *= 999
                                if increased == False and col > 0 and self.opponent_board[row][col-1] == -1:
                                    self.heatmap[row][col-1] *= 999
                                if increased == False and col < 9 and self.opponent_board[row][col+1] == -1:
                                    self.heatmap[row][col+1] *= 999

                            col+=1
                        row+=1
        return   

             
    def parityFn(self, least):
        smallest = least
        # 3 element parity 
        for i in range(0,10):
            for j in range(0,10):
                self.parity[i][j] = (10*i+j)%smallest
                
    def hit_or_miss(self, x, y, info):
        myFile.write("Info: " + str(info) + ": " + str(x) + ", " + str(y) + "\n")
        self.info = info
        # info = 1 for miss, 0 for a hit, -1 for an out of range shooting, 2 for special move nullify. 3 for your next move to be a Hawkeye Shot
        # if info != -1 and info == 0:
        if info!= 3:
            self.opponent_board[x][y] = info
        if info == 2 or info == 3:
            self.opponent_board[x][y] = 0
        

#driver code

myFile = open("op.txt", "a")
# ob = BattleShip()
# ob.set_ships()
# ob.attack()
# for i in ob.heatmap:
#     print(i)
