import pygame
from pygame.locals import *
pygame.font.init()
sudoku_data = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

GRAY = (128,128,128)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BROWN = (255,128,0)
BLUE = (0,0,255)
SKY = (0,255,255)


class board:
    def __init__(self,row,col,width,height,screen):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.screen = screen
        self.selected = None
        self.cubes = [[Cube(sudoku_data[i][j],i,j,self.width,self.height) for j in range(self.col)] for i in range(self.row)]
        self.update_model()
        self.data = None

    def update_model(self):
        self.data = [[self.cubes[i][j].val for j in range(self.col)] for i in range(self.row)]
    
    def enter_value(self,value):
        row,col = self.selected
        if(self.cubes[row][col].val==0):
            self.cubes[row][col].set_value(value)
            self.update_model()

            if(valid(self.data,row,col,value) and self.solve()):
                return True
            else:
                self.cubes[row][col].set_value(0)
                self.cubes[row][col].set_temp_val(0)
                self.update_model()
                return False

    def click(self,pos):
        
        if(pos[1]<self.height and pos[0]<self.width):
            width_gap = self.width/9
            x = pos[0]//width_gap
            y = pos[1]//width_gap
            return (int(y),int(x))
        else:
            return None

    def draw(self):
        width_gap = self.width / 9
        #Making the grid lines
        for i in range(self.row+1):
            if(i%3==0 and i!=0):
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.screen,BLACK,(0,i*width_gap),(self.width,i*width_gap),thick)
            pygame.draw.line(self.screen,BLACK,(i*width_gap,0),(i*width_gap,self.height),thick)

        #Making the data entered
        for i in range(self.row):
            for j in range(self.col):
                self.cubes[i][j].draw(self.screen)
    
    def select(self,row,col):
        for i in range(self.row):
            for j in range(self.col):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row,col)
    
    def sketch(self,val):
        row = self.selected[0]
        col = self.selected[1]
        self.cubes[row][col].set_temp_val(val)

    def is_finished(self):
        for i in range(self.row):
            for j in range(self.col):
                if(self.cubes[i][j].val==0):
                    return False
        return True

    def find_empty(self):
        for i in range(self.row):
            for j in range(self.col):
                if(self.data[i][j]==0):
                    return (i,j)
        return None

    def solve(self):
        empty_block = self.find_empty()
        if(empty_block==None):
            return True
        row,col = empty_block
        for i in range(1,10):
            if(valid(self.data,row,col,i)):
                self.data[row][col] = i
                if(self.solve()):
                    return True
                self.data[row][col]=0
        return False
    def solve_grid(self):
        self.update_model()
        empty_block = self.find_empty()

        if(empty_block==None):
            return True
        row,col = empty_block
        for i in range(1,10):
            if(valid(self.data,row,col,i)):
                self.cubes[row][col].set_value(i)
                self.data[row][col] = i
                self.cubes[row][col].draw_new_change(self.screen,guess = True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)
                
                if(self.solve_grid()):
                    return True
                self.cubes[row][col].set_value(0)
                self.data[row][col] = 0
                self.update_model()
                self.cubes[row][col].draw_new_change(self.screen,guess = False)
                pygame.display.update()
                pygame.time.delay(100)
        return False


    def clear(self):
        row,col = self.selected
        if(self.cubes[row][col].val == 0):
            self.cubes[row][col].set_temp_val(0)


 
class Cube:
    rows = 9 
    cols = 9
    def __init__(self,val,row,col,width,height):
        self.row = row
        self.col = col
        self.val = val
        self.width = width
        self.height = height
        self.selected = False
        self.temp = 0
    
    def draw(self,screen):
        font = pygame.font.SysFont("comicsans",40)

        width_gap = self.width/9
        y = self.row*width_gap
        x = self.col*width_gap

        if(self.temp!=0 and self.val==0):
            text = font.render(str(self.temp),1,GRAY)
            screen.blit(text,(x+5,y+5))
        elif(not(self.val==0)):
            text = font.render(str(self.val),1,BLACK)
            
            screen.blit(text, (x + (width_gap/2 - text.get_width()/2), y + (width_gap/2 - text.get_height()/2)))
        if(self.selected):
            pygame.draw.rect(screen,RED,(x,y,width_gap,width_gap),3)
    
    def draw_new_change(self,screen,guess):
        font = pygame.font.SysFont("comicsans",40)

        width_gap = self.width/9
        y = self.row*width_gap
        x = self.col*width_gap

        pygame.draw.rect(screen,WHITE,(x,y,width_gap,width_gap),0)
        text = font.render(str(self.val),1,BLACK)
        screen.blit(text, (x + (width_gap/2 - text.get_width()/2), y + (width_gap/2 - text.get_height()/2)))
        if(guess==True):
            pygame.draw.rect(screen,GREEN,(x,y,width_gap,width_gap),3)
        else:
            pygame.draw.rect(screen,RED,(x,y,width_gap,width_gap),3)



    def set_value(self,val):
        self.val = val
    
    def set_temp_val(self,val):
        self.temp = val

    

def valid(data,row,col,value):
    #Checking in the row
    for i in range(9):
        if(data[row][i]==value and i!=col):
            return False
    #Checking in the column
    for i in range(9):
        if(data[i][col]==value and i!=row):
            return False
    """
    Checking in the box
    First we have to get the first row and column corresponding to the row, col
    For this, we can get this logically as it repeats after every 3 intervals by
    first_row_box = row-row%3
    first_col_box = col-col%3
    """
    first_row_box = row//3
    first_col_box = col//3
    for i in range(3):
        for j in range(3):
            if(data[first_row_box*3+i][first_col_box*3+j]==value and first_row_box*3+i!=row and first_col_box*3+j!=col):
                return False
    return True

def draw_screen(screen,grid):
    screen.fill(WHITE)
    font = pygame.font.SysFont("comicsans",40)
    text = font.render("Made with ",1,BLACK)
    
    P = font.render("P",1,RED)
    Y = font.render("Y",1,BROWN)
    G = font.render("G",1,GREEN)
    A = font.render("A",1,BLUE)
    M = font.render("M",1,SKY)
    E = font.render("E",1,BLACK)
    space = font.render(" ",1,BLACK)
    sum_text = 265
    """
    Analysing the widths of the texts
    print(text.get_width(),P.get_width(),Y.get_width(),G.get_width(),A.get_width(),M.get_width(),E.get_width(),space.get_width())
    ==> 140 18 18 21 20 22 18 8
    ==> 265
    """
    #screen.blit(text,(grid.width/2-text.get_width()/2,grid.height+text.get_height()/2))
    text_pos = ((grid.width-sum_text)/2,grid.height+text.get_height()/2)
    screen.blit(text,text_pos)
    P_pos = (text_pos[0]+text.get_width(),grid.height+P.get_height()/2)
    screen.blit(P,P_pos)
    Y_pos = (P_pos[0]+P.get_width(),grid.height+Y.get_height()/2)
    screen.blit(Y,Y_pos)
    G_pos = (Y_pos[0]+Y.get_width(),grid.height+G.get_height()/2)
    screen.blit(G,G_pos)
    A_pos = (G_pos[0]+G.get_width(),grid.height+A.get_height()/2)
    screen.blit(A,A_pos)
    M_pos = (A_pos[0]+A.get_width(),grid.height+M.get_height()/2)
    screen.blit(M,M_pos)
    E_pos = (M_pos[0]+M.get_width(),grid.height+E.get_height()/2)
    screen.blit(E,E_pos)



    grid.draw()

def main():
    screen = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    grid = board(9,9,540,540,screen)
    key = None
    run = True
    while(run):
        for event in pygame.event.get():
            if(event.type == QUIT):
                run = False
            if(event.type == KEYDOWN):
                if(event.key == K_1 or event.key == K_KP1):
                    key = 1
                if(event.key == K_2 or event.key == K_KP2):
                    key = 2
                if(event.key == K_3 or event.key == K_KP3):
                    key = 3
                if(event.key == K_4 or event.key == K_KP4):
                    key = 4
                if(event.key == K_5 or event.key == K_KP5):
                    key = 5
                if(event.key == K_6 or event.key == K_KP6):
                    key = 6
                if(event.key == K_7 or event.key == K_KP7):
                    key = 7
                if(event.key == K_8 or event.key == K_KP8):
                    key = 8
                if(event.key == K_9 or event.key == K_KP9):
                    key = 9
                
                if(event.key == K_SPACE):
                    grid.solve_grid()

                if(event.key == K_DELETE):
                    grid.clear()
                    key = None

                if(event.key==K_RETURN):
                    #print("Entered at Gate 1")
                    row,col = grid.selected
                    if(grid.cubes[row][col].temp!=0):
                        #print("Entered at Gate 2")
                        if(grid.enter_value(grid.cubes[row][col].temp)):
                            print("Success")
                        else:
                            print("Wrong")
                        key = None
                        if(grid.is_finished()):
                            print("Game Over")

            if(event.type==MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
                clicked = grid.click(pos)
                if(clicked):
                    grid.select(clicked[0],clicked[1])
                    key = None

        if(grid.selected and key!=None):
            grid.sketch(key)
            #print(grid.selected)
        
        draw_screen(screen,grid)
        pygame.display.update()

if __name__ == "__main__":
    main()
    pygame.quit()