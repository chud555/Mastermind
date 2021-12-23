class TextObj():
    def __init__(self, x_loc, y_loc, text_val):
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.text = text_val
        self.x_loc_2 = self.x_loc + (len(text_val) * 20)
        self.y_loc_2 = self.y_loc + 20
        self.green = "#20FF20"
        self.black = "#000000"
        self.color = self.black
        
    def is_over_text(self, x_coord, y_coord):
        hovered_on = False
        """
        print("x_coord : " + str(x_coord))
        print("y_coord : " + str(y_coord))
        print("self.x_loc + (len(self.text) * 5) : " + str(self.x_loc + (len(self.text) * 5)))
        print("self.x_loc - (len(self.text) * 5) : " + str(self.x_loc - (len(self.text) * 5)))
        print("self.y_loc + 10: " + str(self.y_loc + 10))
        print("self.y_loc - 10 : " + str(self.y_loc - 10))
        """        
        
        if x_coord < self.x_loc + (len(self.text) * 5) and \
           x_coord > self.x_loc - (len(self.text) * 5) and \
           y_coord < self.y_loc + 10 and \
           y_coord > self.y_loc - 10:
            # print("hovered over text : x_coord - " + str(x_coord) + " y_coord - " + str(y_coord))
            hovered_on = True
        return hovered_on

    def move_text(self, x_pos, y_pos):
        self.x_loc = x_pos
        self.y_loc = y_pos
        self.x_loc_2 = self.x_loc + (len(self.text) * 20)
        self.y_loc_2 = self.y_loc + 20