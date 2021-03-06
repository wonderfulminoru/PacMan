import pygame, random
from settings import*

vec = pygame.math.Vector2

class Enemy:
    def __init__(self, app, pos, indx):
        self.app = app
        self.indx = indx
        self.grid_pos = pos
        self.start_pos = [pos.x, pos.y]
        self.direction = vec(0, 0)
        self.state = "origin"
        self.pix_pos = self.get_pix_pos()
        self.able_to_move = True
        self.speed = 5
        self.first_move = True

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed           
            self.grid_to_pix_pos()

        if self.moveable():
            self.move()
            self.set_speed()
            self.able_to_move = self.can_move()
                
    def grid_to_pix_pos(self):
        self.grid_pos.x = (self.pix_pos.x - self.app.cell_width//2)//self.app.cell_width
        self.grid_pos.y = (self.pix_pos.y - self.app.cell_height//2)//self.app.cell_height

    def can_move(self):
        if vec(self.grid_pos + self.direction) in self.app.walls:
            return False
        else: return True

    def moveable(self):
        if int(self.pix_pos.x) % self.app.cell_width == 15:
            if self.direction == vec(1,0) or self.direction == vec(-1,0) or self.direction == vec(0,0):
                return True
        if int(self.pix_pos.y) % self.app.cell_height == 15:
            if self.direction == vec(0,1) or self.direction == vec(0,-1) or self.direction == vec(0,0):
                return True 
        return False
    
    def move(self):
        self.get_random_direction()               

    def get_random_direction(self):
        if self.first_move:
            while True:
                number = random.randint(1,4)
                if number == 1:
                   x_dir, y_dir = 1, 0
                elif number == 2:
                    x_dir, y_dir = 0, 1
                elif number == 3:
                    x_dir, y_dir = -1, 0
                else:
                    x_dir, y_dir = 0, -1       
                next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
                if next_pos not in self.app.walls:
                    self.first_move = False
                    break
            self.direction = vec(x_dir, y_dir) 
        else: 
                while not self.can_move():      
                    number = random.randint(1,4)
                    if number == 1:
                       x_dir, y_dir = 1, 0
                    elif number == 2:
                        x_dir, y_dir = 0, 1
                    elif number == 3:
                        x_dir, y_dir = -1, 0
                    else:
                        x_dir, y_dir = 0, -1                        
                    self.direction = vec(x_dir, y_dir)              

    def get_pix_pos(self):
        return vec(self.grid_pos.x*self.app.cell_width + self.app.cell_width//2, 
        self.grid_pos.y*self.app.cell_height + self.app.cell_height//2)

    def draw(self):
        pygame.draw.circle(self.app.screen, self.get_colour(), (self.pix_pos.x, self.pix_pos.y), 10)

    def set_speed(self):
        if self.state == 'eatable':
            self.speed = 3
        else:
            self.speed = 5
        
    def get_colour(self):
        if self.state == 'origin':    
            if self.indx == 0:
                return (82, 0, 104)
            elif self.indx == 1:
                return (0, 255, 46)
            elif self.indx == 2:
                return (255, 55, 0)
            elif self.indx == 3:
                return (25, 0, 255)
        else:
            return (154, 205, 50)
    
