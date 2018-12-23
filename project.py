from Tkinter import *
from Tkinter import Canvas,Label,Tk,StringVar
import tkMessageBox
import random


from collections import deque
from random import choice
from collections import Counter

class Minesweeper:

    def __init__(self,master):
   
        self.tile_plain = PhotoImage(file = "images/tile_plain.gif")
        self.tile_clicked = PhotoImage(file = "images/tile_clicked.gif")
        self.tile_mine = PhotoImage(file = "images/tile_mine.gif")
        self.tile_flag = PhotoImage(file = "images/tile_flag.gif")
        self.tile_wrong = PhotoImage(file = "images/tile_wrong.gif")
        self.tile_no = []
        for x in range(1, 9):
            self.tile_no.append(PhotoImage(file = "images/tile_"+str(x)+".gif"))

        frame = Frame(master)
        frame.pack()

        self.label1 = Label(frame, text="Minesweeper")
        self.label1.grid(row = 0, column = 0, columnspan = 10)

        self.flags = 0
        self.correct_flags = 0
        self.clicked = 0

        # buttons
        self.buttons = dict({})
        self.mines = 0
        x_coord = 1
        y_coord = 0
        for x in range(0, 100):
            mine = 0
            
            gfx = self.tile_plain
          
            if random.uniform(0.0, 1.0) < 0.1:
                mine = 1
                self.mines += 1
            # 0 = Button widget
            # 1 = if a mine y/n (1/0)
            # 2 = state (0 = unclicked, 1 = clicked, 2 = flagged)
            # 3 = button id
            # 4 = [x, y] coordinates in the grid
            # 5 = nearby mines, 0 by default, calculated after placement in grid
            self.buttons[x] = [ Button(frame, image = gfx),
                                mine,
                                0,
                                x,
                                [x_coord, y_coord],
                                0 ]
            self.buttons[x][0].bind('<Button-1>', self.lclicked_wrapper(x))
            self.buttons[x][0].bind('<Button-3>', self.rclicked_wrapper(x))

            y_coord += 1
            if y_coord == 10:
                y_coord = 0
                x_coord += 1
        
        # lay buttons in grid
        for key in self.buttons:
            self.buttons[key][0].grid( row = self.buttons[key][4][0], column = self.buttons[key][4][1] )

        # find nearby mines and display number on tile
        for key in self.buttons:
            nearby_mines = 0
            if self.check_for_mines(key-9):
                nearby_mines += 1
            if self.check_for_mines(key-10):
                nearby_mines += 1
            if self.check_for_mines(key-11):
                nearby_mines += 1
            if self.check_for_mines(key-1):
                nearby_mines += 1
            if self.check_for_mines(key+1):
                nearby_mines += 1
            if self.check_for_mines(key+9):
                nearby_mines += 1
            if self.check_for_mines(key+10):
                nearby_mines += 1
            if self.check_for_mines(key+11):
                nearby_mines += 1
            
            self.buttons[key][5] = nearby_mines
            
        self.label2 = Label(frame, text = "Mines: "+str(self.mines))
        self.label2.grid(row = 11, column = 0, columnspan = 5)

        self.label3 = Label(frame, text = "Flags: "+str(self.flags))
        self.label3.grid(row = 11, column = 4, columnspan = 5)


    def check_for_mines(self, key):
        try:
            if self.buttons[key][1] == 1:
                return True
        except KeyError:
            pass

    def lclicked_wrapper(self, x):
        return lambda Button: self.lclicked(self.buttons[x])

    def rclicked_wrapper(self, x):
        return lambda Button: self.rclicked(self.buttons[x])

    def lclicked(self, button_data):
        if button_data[1] == 1: #if a mine
            # show all mines and check for flags
            for key in self.buttons:
                if self.buttons[key][1] != 1 and self.buttons[key][2] == 2:
                    self.buttons[key][0].config(image = self.tile_wrong)
                if self.buttons[key][1] == 1 and self.buttons[key][2] != 2:
                    self.buttons[key][0].config(image = self.tile_mine)
            # end game
            self.gameover()
        else:
            #change image
            if button_data[5] == 0:
                button_data[0].config(image = self.tile_clicked)
                self.clear_empty_tiles(button_data[3])
            else:
                button_data[0].config(image = self.tile_no[button_data[5]-1])
            # if not already set as clicked, change state and count
            if button_data[2] != 1:
                button_data[2] = 1
                self.clicked += 1
            if self.clicked == 100 - self.mines:
                self.victory()

    def rclicked(self, button_data):
        # if not clicked
        if button_data[2] == 0:
            button_data[0].config(image = self.tile_flag)
            button_data[2] = 2
            button_data[0].unbind('<Button-1>')
            # if a mine
            if button_data[1] == 1:
                self.correct_flags += 1
            self.flags += 1
            self.update_flags()
        # if flagged, unflag
        elif button_data[2] == 2:
            button_data[0].config(image = self.tile_plain)
            button_data[2] = 0
            button_data[0].bind('<Button-1>', self.lclicked_wrapper(button_data[3]))
            # if a mine
            if button_data[1] == 1:
                self.correct_flags -= 1
            self.flags -= 1
            self.update_flags()

    def check_tile(self, key, queue):
        try:
            if self.buttons[key][2] == 0:
                if self.buttons[key][5] == 0:
                    self.buttons[key][0].config(image = self.tile_clicked)
                    queue.append(key)
                else:
                    self.buttons[key][0].config(image = self.tile_no[self.buttons[key][5]-1])
                self.buttons[key][2] = 1
                self.clicked += 1
        except KeyError:
            pass

    def clear_empty_tiles(self, main_key):
        queue = deque([main_key])

        while len(queue) != 0:
            key = queue.popleft()
            self.check_tile(key-9, queue)      #top right
            self.check_tile(key-10, queue)     #top middle
            self.check_tile(key-11, queue)     #top left
            self.check_tile(key-1, queue)      #left
            self.check_tile(key+1, queue)      #right
            self.check_tile(key+9, queue)      #bottom right
            self.check_tile(key+10, queue)     #bottom middle
            self.check_tile(key+11, queue)     #bottom left
    
    def gameover(self):
        tkMessageBox.showinfo("Game Over", "You Lose!")
        global root
        root.destroy()

    def victory(self):
        tkMessageBox.showinfo("Game Over", "You Win!")
        global root
        root.destroy()

    def update_flags(self):
        self.label3.config(text = "Flags: "+str(self.flags))


##def main():
##    global root
##    root = Tk()
##    root.title("Minesweeper")
##    minesweeper = Minesweeper(root)
##    root.mainloop()
##if __name__ == "__main__":
##    main()
        
class Game():
    WIDTH = 300
    HEIGHT = 500

    def start(self):
        
        self.level = 1
        self.score = 0
        self.speed = 500
        self.counter = 0
        self.create_new_game = True

        self.root = Tk()
        self.root.title("Tetris")

        self.status_var = StringVar() 
        self.status_var.set("Level: 1, Score: 0")
        self.status = Label(self.root, 
                textvariable=self.status_var, 
                font=("Helvetica", 10, "bold"))
        self.status.pack()
        
        self.canvas = Canvas(
                self.root, 
                width=Game.WIDTH, 
                height=Game.HEIGHT)
        self.canvas.pack()

        self.root.bind("<Key>", self.handle_events)
        self.timer()
        self.root.mainloop()
    
    def timer(self):
        if self.create_new_game == True:
            self.current_shape = Shape(self.canvas)
            self.create_new_game = False

        if not self.current_shape.fall():
            lines = self.remove_complete_lines()
            if lines:
                self.score += 10 * self.level**2 * lines**2
                self.status_var.set("Level: %d, Score: %d" % 
                        (self.level, self.score))

            self.current_shape = Shape(self.canvas)
            if self.is_game_over():
                self.create_new_game = True
                self.game_over()

            self.counter += 1
            if self.counter == 5:
                self.level += 1
                self.speed -= 20
                self.counter = 0
                self.status_var.set("Level: %d, Score: %d" % 
                        (self.level, self.score))
        
        self.root.after(self.speed, self.timer)

    def handle_events(self, event):
        
        if event.keysym == "Left": self.current_shape.move(-1, 0)
        if event.keysym == "Right": self.current_shape.move(1, 0)
        if event.keysym == "Down": self.current_shape.move(0, 1)
        if event.keysym == "Up": self.current_shape.rotate()

    def is_game_over(self):
        
        for box in self.current_shape.boxes:
            if not self.current_shape.can_move_box(box, 0, 1):
                return True
        return False

    def remove_complete_lines(self):
        shape_boxes_coords = [self.canvas.coords(box)[3] for box 
                in self.current_shape.boxes]
        all_boxes = self.canvas.find_all()
        all_boxes_coords = {k : v for k, v in 
                zip(all_boxes, [self.canvas.coords(box)[3] 
                    for box in all_boxes])}
        lines_to_check = set(shape_boxes_coords)
        boxes_to_check = dict((k, v) for k, v in all_boxes_coords.iteritems()
                if any(v == line for line in lines_to_check))
        counter = Counter()
        for box in boxes_to_check.values(): counter[box] += 1
        complete_lines = [k for k, v in counter.iteritems() 
                if v == (Game.WIDTH/Shape.BOX_SIZE)]
 
        if not complete_lines: return False

        for k, v in boxes_to_check.iteritems():
            if v in complete_lines:
                self.canvas.delete(k)
                del all_boxes_coords[k]
                
        for (box, coords) in all_boxes_coords.iteritems():
            for line in complete_lines:
                if coords < line:
                    self.canvas.move(box, 0, Shape.BOX_SIZE)
        return len(complete_lines)

    def game_over(self):
            self.canvas.delete(Tkinter.ALL)
            tkMessageBox.showinfo(
                    "Game Over", 
                    "You scored %d points." % self.score)

class Shape:
    
    BOX_SIZE = 20
    START_POINT = Game.WIDTH / 2 / BOX_SIZE * BOX_SIZE - BOX_SIZE
    SHAPES = (
            ("yellow", (0, 0), (1, 0), (0, 1), (1, 1)),     # square
            ("lightblue", (0, 0), (1, 0), (2, 0), (3, 0)),  # line
            ("orange", (2, 0), (0, 1), (1, 1), (2, 1)),     # right el
            ("blue", (0, 0), (0, 1), (1, 1), (2, 1)),       # left el
            ("green", (0, 1), (1, 1), (1, 0), (2, 0)),      # right wedge
            ("red", (0, 0), (1, 0), (1, 1), (2, 1)),        # left wedge
            ("purple", (1, 0), (0, 1), (1, 1), (2, 1)),     # symmetrical wedge
            )

    def __init__(self, canvas):
        
        self.boxes = [] # the squares drawn by canvas.create_rectangle()
        self.shape = choice(Shape.SHAPES) 
        self.color = self.shape[0]
        self.canvas = canvas

        for point in self.shape[1:]:
            box = canvas.create_rectangle(
                point[0] * Shape.BOX_SIZE + Shape.START_POINT,
                point[1] * Shape.BOX_SIZE,
                point[0] * Shape.BOX_SIZE + Shape.BOX_SIZE + Shape.START_POINT,
                point[1] * Shape.BOX_SIZE + Shape.BOX_SIZE,
                fill=self.color)
            self.boxes.append(box)

           
    def move(self, x, y):
        
        if not self.can_move_shape(x, y): 
            return False         
        else:
            for box in self.boxes: 
                self.canvas.move(box, x * Shape.BOX_SIZE, y * Shape.BOX_SIZE)
            return True

    def fall(self):
        
        if not self.can_move_shape(0, 1):
            return False
        else:
            for box in self.boxes:
                self.canvas.move(box, 0 * Shape.BOX_SIZE, 1 * Shape.BOX_SIZE)
            return True

    def rotate(self):
        
        boxes = self.boxes[:]
        pivot = boxes.pop(2)

        def get_move_coords(box):
            '''Return (x, y) boxes needed to rotate a box around the pivot.'''
            box_coords = self.canvas.coords(box)
            pivot_coords = self.canvas.coords(pivot)
            x_diff = box_coords[0] - pivot_coords[0]
            y_diff = box_coords[1] - pivot_coords[1]
            x_move = (- x_diff - y_diff) / self.BOX_SIZE
            y_move = (x_diff - y_diff) / self.BOX_SIZE
            return x_move, y_move

        
        for box in boxes:
            x_move, y_move = get_move_coords(box)
            if not self.can_move_box(box, x_move, y_move): 
                return False
            
        
        for box in boxes:
            x_move, y_move = get_move_coords(box)
            self.canvas.move(box, 
                    x_move * self.BOX_SIZE, 
                    y_move * self.BOX_SIZE)

        return True

    def can_move_box(self, box, x, y):
        
        x = x * Shape.BOX_SIZE
        y = y * Shape.BOX_SIZE
        coords = self.canvas.coords(box)
        
        # Returns False if moving the box would overrun the screen
        if coords[3] + y > Game.HEIGHT: return False
        if coords[0] + x < 0: return False
        if coords[2] + x > Game.WIDTH: return False

        # Returns False if moving box (x, y) would overlap another box
        overlap = set(self.canvas.find_overlapping(
                (coords[0] + coords[2]) / 2 + x, 
                (coords[1] + coords[3]) / 2 + y, 
                (coords[0] + coords[2]) / 2 + x,
                (coords[1] + coords[3]) / 2 + y
                ))
        other_items = set(self.canvas.find_all()) - set(self.boxes)
        if overlap & other_items: return False

        return True


    def can_move_shape(self, x, y):
        
        for box in self.boxes:
            if not self.can_move_box(box, x, y): return False
        return True


class Window(Frame,Minesweeper):
    def mines(self):
        self.foo1=Minesweeper(root)
    def tetris(self):
        self.foor=Game()
        self.foor.start()

        
    def CButtons(self):
        self.lMinesweeper=Button(self)
        self.lMinesweeper["text"]="Minsesweeper"
        self.lMinesweeper["fg"]="red"
        self.lMinesweeper["command"]=self.mines
        self.lMinesweeper.config(height="15",width="20")

        self.lMinesweeper.pack({"side":"left"})


        self.Tetris=Button(self)
        self.Tetris["text"]="Tetris"
        self.Tetris["fg"]="blue"
        self.Tetris["command"]=self.tetris
        self.Tetris.config(height="15",width="20")



        self.Tetris.pack({"side":"left"})
       
    def __init__(self,master=None):
         Frame.__init__(self,master)
         self.pack()
         
         self.CButtons()
         
root=Tk()
root.title('GAMESTORE')
app=Window(master=root)
app.mainloop()




