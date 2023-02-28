class Character: 
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        
    def move(self, adjusted_x, adjusted_y):
        self.x += adjusted_x
        self.y += adjusted_y
    
    def input_handler(self, key):
        if key == pygame.K_LEFT: 
            self.move(-1, 0)
        elif key == pygame.K_RIGHT:
            self.move(1, 0)
        elif key == pygame.K_UP:
            self.move(0, -1)
        elif key == pygame.K_DOWN:
            self.move(0, 1)
            