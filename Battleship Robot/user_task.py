'''!    @file user_task.py
        @brief                                  Runs the user interface for the battleship game
                                                
        @author                                 OConnell, Joseph
        @author                                 Hefter, David
                                                
        @date                                   November 15, 2022
'''
import pyb, time

def taskUserFcn(columnNum, rowNum, jam, shoot, FireSignal):
    full = ' ● '
    empty = ' ○ '
    boardstate = [['  a  ','  b  ','  c  ','  d  '],
              ['  e  ','  f  ','  g  ','  h  '],
              ['  i  ','  j  ','  k  ','  l  '],
              ['  m  ','  n  ','  o  ','  p  '],]
    ammostate = [full, full, full, full, full, full, full, full, full, full, full, full]
    state = 0
    jamprint = False
    ser = pyb.USB_VCP()
    hit = 0
    ammo = 12
    while True:
        if jam.get():
            if not jamprint:
                print('\n\nCease fire, armaments jammed!\nPress "u" when unjammed.')
                jamprint = True
            if ser.any():
                charIn = ser.read(1).decode()
                if charIn in {'u' , 'U'}:
                    jamprint = False
                    jam.put(False)
                    FireSignal.put(False)
                    state = 0
        else:
            if state == 0:
                print(f'\033[H\033[J')
                printboard(boardstate, ammostate)
                state = 1
            if state == 1:
                if ser.any():
                    ##  @brief      Most recent character inputted to keyboard
                    # 
                    charIn = ser.read(1).decode()
                    if charIn in {'a' , 'A'}:
                        columnNum.put(0)
                        rowNum.put(0)
                        state = 2
                    elif charIn in {'b' , 'B'}:
                        columnNum.put(1)
                        rowNum.put(0)
                        state = 2
                    elif charIn in {'c' , 'C'}:
                        columnNum.put(2)
                        rowNum.put(0)
                        state = 2
                    elif charIn in {'d' , 'D'}:
                        columnNum.put(3)
                        rowNum.put(0)
                        state = 2
                    elif charIn in {'e' , 'E'}:
                        columnNum.put(0)
                        rowNum.put(1)
                        state = 2
                    elif charIn in {'f' , 'F'}:
                        columnNum.put(1)
                        rowNum.put(1)
                        state = 2
                    elif charIn in {'g' , 'G'}:
                        columnNum.put(2)
                        rowNum.put(1)
                        state = 2
                    elif charIn in {'h' , 'H'}:
                        columnNum.put(3)
                        rowNum.put(1)
                        state = 2
                    elif charIn in {'i' , 'I'}:
                        columnNum.put(0)
                        rowNum.put(2)
                        state = 2
                    elif charIn in {'j' , 'J'}:
                        columnNum.put(1)
                        rowNum.put(2)
                        state = 2
                    elif charIn in {'k' , 'K'}:
                        columnNum.put(2)
                        rowNum.put(2)
                        state = 2
                    elif charIn in {'l' , 'L'}:
                        columnNum.put(3)
                        rowNum.put(2)
                        state = 2
                    elif charIn in {'m' , 'M'}:
                        columnNum.put(0)
                        rowNum.put(3)
                        state = 2
                    elif charIn in {'n' , 'N'}:
                        columnNum.put(1)
                        rowNum.put(3)
                        state = 2
                    elif charIn in {'o' , 'O'}:
                        columnNum.put(2)
                        rowNum.put(3)
                        state = 2
                    elif charIn in {'p' , 'P'}:
                        columnNum.put(3)
                        rowNum.put(3)
                        state = 2
                    elif charIn in {'r' , 'R'}:
                        state = 7
                        st = time.ticks_ms()
                        print('Reloaded!!')
                        
            elif state == 2:
                shoot.put(True)
                print('Hit [h] or Miss [m]?')
                ammostate[12-ammo]=empty  
                ammo-=1    
                state = 3
            elif state == 3:
                if ser.any():
                    print('read')
                    charIn = ser.read(1).decode()
                    if charIn in {'h' , 'H'}:
                        boardstate[rowNum.get()][columnNum.get()] = ' (X) '
                        state = 0
                        print(state)
                        hit+=1
                        if hit==5:
                            state = 4
                    elif charIn in {'m' , 'M'}:
                        boardstate[rowNum.get()][columnNum.get()] = ' ( ) '
                        state = 0
                        print(state)
                    if ammo <= 0:
                        state = 5
            elif state == 4:
                print(f'\033[H\033[J')
                printboard(boardstate, ammostate)
                print('\n\nVICTORY!!!')
                state = 6
            elif state == 5:
                print(f'\033[H\033[J')
                printboard(boardstate, ammostate)
                print('\n\nOUT OF AMMO!!!')
                state = 6
            elif state == 6:
                pass
            # reload state
            elif state == 7:
                ammo = 12
                ammostate = [full, full, full, full, full, full, full, full, full, full, full, full]
                if time.ticks_ms() > st+1000:
                    state = 0
                
                
        yield
            
def printboard(boardstate, ammostate):
    '''!@brief      Prints the user interface menu
        @details    A series of print states that forms the user interface menu
    '''
    topline =    '┌─────┬─────┬─────┬─────┐'
    middleline = '├─────┼─────┼─────┼─────┤'
    bottomline = '└─────┴─────┴─────┴─────┘'
    
        
    print(topline)
    print('│'+boardstate[0][0]+'│'+boardstate[0][1]+'│'+boardstate[0][2]+'│'+boardstate[0][3]+'│')
    print(middleline)
    print('│'+boardstate[1][0]+'│'+boardstate[1][1]+'│'+boardstate[1][2]+'│'+boardstate[1][3]+'│'+ammostate[0]+ammostate[1])
    print(middleline+ammostate[2]+ammostate[3])
    print('│'+boardstate[2][0]+'│'+boardstate[2][1]+'│'+boardstate[2][2]+'│'+boardstate[2][3]+'│'+ammostate[4]+ammostate[5])
    print(middleline+ammostate[6]+ammostate[7])
    print('│'+boardstate[3][0]+'│'+boardstate[3][1]+'│'+boardstate[3][2]+'│'+boardstate[3][3]+'│'+ammostate[8]+ammostate[9])
    print(bottomline+ammostate[10]+ammostate[11])
    print('Call your shot!')

if __name__=='__main__':
    columnNum, rowNum, jam, shoot = 0,0,False,False
    taskUserFcn(columnNum, rowNum, jam, shoot)