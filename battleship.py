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
        self.team_name = "Meh"
        # self.ships = ships
        # self.opponent_board = opponent_board
        self.info = 1
        self.set_ships()

    def set_ships(self):
        #coordinates,size of shipe,orientation 0-horizontal 1-vertical 
        #random initialization 
        self.ships = [
            [1,1,5,1],
            [2,1,5,1],
            [3,1,4,1],
            [4,1,4,1],
            [5,1,3,1]
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
            if row.count(-1) > maxH:
                maxH = row.count(-1)
                hIndex = i
            i+=1
        
        maxY = -1
        yIndex = -1
        for col in range(10):
            localCount = 0
            for row in range(10):
                if self.opponent_board[row][col] == -1:
                    localCount += 1
            if localCount > maxY:
                maxY = localCount
                yIndex = col

        return (hIndex, yIndex)

    def attack(self):
        # if self.info == 1:
        #     self.opponent_board[self.lasthit[0]][self.lasthit[1]] = 1
        # elif self.info == 0:
        #     self.opponent_board[self.lasthit[0]][self.lasthit[1]] = 0
        if self.info == 3:
            sq = self.getHawkeyeCoord()
            return sq
        #Below code is for Random guess
        #need the lowest key
        # min_ship = list(self.ships_left.keys()).sort()[0] #This gives us the least number to check for parity
        # self.parityFn(min_ship)
        self.probs()

        square = self.indexOfMax()
        self.lasthit = square
        return square
        # return (x, y)
    
    
    def probs(self):
        for ship in self.ships_left.keys():
            for count in range(self.ships_left[ship]): #Doing this for each left ship
                for orientation in [0,1]:
                    row = 0
                    while row < 10:
                        col = 0
                        while col<10:
                            if self.opponent_board[row][col] == -1:
                                if (orientation == 1 and row+(ship-1)<10) or (orientation == 0 and col+(ship-1)<10):
                                    flag = True
                                    for i in range(1,ship):
                                        if (orientation == 1 and self.opponent_board[row+i][col] == -1) or (orientation == 0 and self.opponent_board[row][col+i] == -1):
                                            continue 
                                        else:
                                            flag=False 
                                            break
                                    if flag == True:
                                       for j in range(ship):
                                            if orientation==1: 
                                               self.heatmap[row+j][col]+=1
                                            else: #orientation 0
                                                self.heatmap[row][col+j]+=1
                            elif self.opponent_board[row][col] == 0: #It has been hit
                                # print(str(row) + "  " + str(col))
                                right = left = top = bottom = False
                                if row > 0 and self.opponent_board[row-1][col] == -1 :
                                    bottom = True #True meaning not yet hit
                                    # print("Bottom")
                                if row<9 and self.opponent_board[row+1][col] == -1 :
                                    top = True
                                    # print("Top")
                                if col < 9 and self.opponent_board[row][col+1] == -1:
                                    right = True
                                    # print("Right")
                                if col > 0 and self.opponent_board[row][col-1] == -1:
                                    left = True
                                    # print("Left")
                                else:
                                    pass


                                # for row in self.opponent_board:
                                #     print(row)
                                
                                #if all 4 are free, then increase all
                                if bottom == True and top == True and left == True and right == True:
                                    self.heatmap[row-1][col] += 999
                                    self.heatmap[row+1][col] += 999
                                    self.heatmap[row][col-1] += 999
                                    self.heatmap[row][col+1] += 999
                                elif bottom == True and top == True: #If only bottom and top are empty (Horizontally hit happened)
                                    if right == True: #If right wasnt hit
                                        if self.opponent_board[row][col+1] == -1:
                                            self.heatmap[row][col+1] += 999
                                    else: #If left wasn't hit
                                        if self.opponent_board[row][col-1] == -1:
                                            self.heatmap[row][col-1] += 999
                                elif right == True and left == True:
                                    if bottom == True:
                                        if self.opponent_board[row-1][col] == -1:
                                            self.heatmap[row-1][col] += 999
                                    else:
                                        if self.opponent_board[row+1][col] == -1:
                                            self.heatmap[row+1][col] += 999

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
        self.info = info
        # info = 1 for miss, 0 for a hit, -1 for an out of range shooting, 2 for special move nullify. 3 for your next move to be a Hawkeye Shot
        # if info != -1 and info == 0:
        self.opponent_board[x][y] = info

#driver code

# ob = BattleShip()
# ob.set_ships()
# ob.attack()
# ob.attack()