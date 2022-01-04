from Globals import Globals
from ColorPeg import ColorPeg
from ScorePeg import ScorePeg
from KeyPegs import KeyPegs
from TextObj import TextObj
# import traceback

# There are 10 guess rows, they have 4 distinct pieces, the label, the pegs, the "X" to submit a guess and the score
class GuessRow():
    def __init__(self, label, y_loc, canvas):
        self.label = label
        self.y_loc = y_loc
        self.submit_guess_text = None
        self.init_row(canvas)        

    def init_row(self, canvas):            
        self.peg_list = []        
        for ind in Globals.PEG_IND_LIST:
            self.peg_list.append(ColorPeg(canvas.peg_x_loc_list[ind], self.y_loc)) 
       
        self.submit_guess_text = TextObj(canvas.text_menu_x_loc, self.y_loc, "X")
        self.submit_guess_text.color = self.submit_guess_text.black        
        self.score_pegs = ScorePeg(canvas.score_pegs_x_loc, self.y_loc, canvas.smallest_step)

    def move_row(self, canvas):
        self.y_loc = canvas.guess_peg_y_loc_list[self.label -  1]
        for ind, peg in zip(Globals.PEG_IND_LIST, self.peg_list):
            peg.move_peg(canvas.peg_x_loc_list[ind], self.y_loc)
            self.submit_guess_text.move_text(canvas.peg_x_loc_list[ind], self.y_loc)

        self.score_pegs.move_peg(canvas.score_pegs_x_loc, self.y_loc, canvas.smallest_step)
        self.submit_guess_text.move_text(canvas.text_menu_x_loc, self.y_loc)

    def draw_row(self, canvas, curr_round):
        self.move_row(canvas)
        for peg in self.peg_list:
            peg.draw_peg(canvas, canvas.smallest_step)

        if GuessRows.mm.is_playable_round() and self.label <= curr_round:            
            canvas.create_text(canvas.curr_x_step / 2, self.y_loc, font=("Courier New", int(canvas.curr_x_step / 5.0)), fill="Black", text=str(self.label))            
            canvas.create_text(self.submit_guess_text.x_loc, self.submit_guess_text.y_loc, font=("Courier New", int(canvas.curr_x_step / 2.0)), fill=self.submit_guess_text.color, text=str(self.submit_guess_text.text))
        
        self.score_pegs.set_peg_size(canvas.smallest_step)
        
        if self.score_pegs.state_1 == ScorePeg.States.EMPTY:
            canvas.create_oval(self.score_pegs.p1_x_loc - self.score_pegs.empty_size, 
                               self.score_pegs.p1_y_loc - self.score_pegs.empty_size, 
                               self.score_pegs.p1_x_loc + self.score_pegs.empty_size,
                               self.score_pegs.p1_y_loc + self.score_pegs.empty_size, 
                               fill=self.score_pegs.state_1.value["color"],
                               outline=self.score_pegs.peg_outline_color)
        else:
            canvas.create_oval(self.score_pegs.p1_x_loc - self.score_pegs.size, 
                               self.score_pegs.p1_y_loc - self.score_pegs.size, 
                               self.score_pegs.p1_x_loc + self.score_pegs.size,
                               self.score_pegs.p1_y_loc + self.score_pegs.size, 
                               fill=self.score_pegs.state_1.value["color"],
                               outline=self.score_pegs.peg_outline_color)

        if self.score_pegs.state_2 == ScorePeg.States.EMPTY:
            canvas.create_oval(self.score_pegs.p2_x_loc - self.score_pegs.empty_size, 
                               self.score_pegs.p2_y_loc - self.score_pegs.empty_size, 
                               self.score_pegs.p2_x_loc + self.score_pegs.empty_size,
                               self.score_pegs.p2_y_loc + self.score_pegs.empty_size, 
                               fill=self.score_pegs.state_2.value["color"],
                               outline=self.score_pegs.peg_outline_color)
        else:
            canvas.create_oval(self.score_pegs.p2_x_loc - self.score_pegs.size, 
                               self.score_pegs.p2_y_loc - self.score_pegs.size, 
                               self.score_pegs.p2_x_loc + self.score_pegs.size,
                               self.score_pegs.p2_y_loc + self.score_pegs.size, 
                               fill=self.score_pegs.state_2.value["color"],
                               outline=self.score_pegs.peg_outline_color)

        if self.score_pegs.state_3 == ScorePeg.States.EMPTY:
            canvas.create_oval(self.score_pegs.p3_x_loc - self.score_pegs.empty_size, 
                               self.score_pegs.p3_y_loc - self.score_pegs.empty_size, 
                               self.score_pegs.p3_x_loc + self.score_pegs.empty_size,
                               self.score_pegs.p3_y_loc + self.score_pegs.empty_size, 
                               fill=self.score_pegs.state_3.value["color"],
                               outline=self.score_pegs.peg_outline_color)
        else:
            canvas.create_oval(self.score_pegs.p3_x_loc - self.score_pegs.size, 
                               self.score_pegs.p3_y_loc - self.score_pegs.size, 
                               self.score_pegs.p3_x_loc + self.score_pegs.size,
                               self.score_pegs.p3_y_loc + self.score_pegs.size, 
                               fill=self.score_pegs.state_3.value["color"],
                               outline=self.score_pegs.peg_outline_color)

        if self.score_pegs.state_4 == ScorePeg.States.EMPTY:
            canvas.create_oval(self.score_pegs.p4_x_loc - self.score_pegs.empty_size, 
                               self.score_pegs.p4_y_loc - self.score_pegs.empty_size, 
                               self.score_pegs.p4_x_loc + self.score_pegs.empty_size,
                               self.score_pegs.p4_y_loc + self.score_pegs.empty_size, 
                               fill=self.score_pegs.state_4.value["color"],
                               outline=self.score_pegs.peg_outline_color)
        else:
            canvas.create_oval(self.score_pegs.p4_x_loc - self.score_pegs.size, 
                               self.score_pegs.p4_y_loc - self.score_pegs.size, 
                               self.score_pegs.p4_x_loc + self.score_pegs.size,
                               self.score_pegs.p4_y_loc + self.score_pegs.size, 
                               fill=self.score_pegs.state_4.value["color"],
                               outline=self.score_pegs.peg_outline_color)

    def check_click(self, x_loc, y_loc, forward = True):        
        game_won = False
        for peg in self.peg_list:
            peg.check_click(x_loc, y_loc, forward)
            
        if self.submit_guess_text.color == self.submit_guess_text.green:            
            game_won = self.score_guess()
            if game_won:
                GuessRows.mm.set_game_round("win")
            elif(GuessRows.mm.set_game_round == 10):
                GuessRows.mm.set_game_round("lose")
            else:
                GuessRows.mm.set_game_round(GuessRows.mm.game_round + 1)                

        return game_won

    def motion(self, x_loc, y_loc):
        if self.submit_guess_text.is_over_text(x_loc, y_loc):
            # Can't click if there's empty spaces            
            if self.peg_list[0].state == ColorPeg.States.EMPTY or \
               self.peg_list[1].state == ColorPeg.States.EMPTY or \
               self.peg_list[2].state == ColorPeg.States.EMPTY or \
               self.peg_list[3].state == ColorPeg.States.EMPTY:
                self.submit_guess_text.color = self.submit_guess_text.red
            else:
                self.submit_guess_text.color = self.submit_guess_text.green
        else:
            self.submit_guess_text.color = self.submit_guess_text.black
        
    def set_inactive(self):        
        for peg in self.peg_list:
            peg.is_clickable = False
    
    def set_active(self):        
        for peg in self.peg_list:
            peg.is_clickable = True

    def score_guess(self):
        correct_guess = False

        score_list = [ScorePeg.States.EMPTY,
                      ScorePeg.States.EMPTY,
                      ScorePeg.States.EMPTY,
                      ScorePeg.States.EMPTY]

        if GuessRows.mm.is_playable_round():
            white_check_list = []
            # Check for black peg matches first
            for i in list(range(1, 5, 1)):
                if self.peg_list[i - 1].state == KeyPegs.peg_list[i - 1].state:
                    score_list[i - 1] = ScorePeg.States.BLACK
                else:
                    white_check_list.append(KeyPegs.peg_list[i - 1].state)
            for i in list(range(1, 5, 1)):
                if score_list[i - 1] != ScorePeg.States.BLACK and self.peg_list[i - 1].state in white_check_list:
                    white_check_list.remove(self.peg_list[i - 1].state)
                    score_list[i - 1] = ScorePeg.States.WHITE

            packed_score_list = []
            # Pack black pegs, then white pegs            
            for sc in score_list:                
                if sc == ScorePeg.States.BLACK:
                    packed_score_list.append(ScorePeg.States.BLACK)                    

            for sc in score_list:
                if sc == ScorePeg.States.WHITE:
                    packed_score_list.append(ScorePeg.States.WHITE)                    

            # print("score_list : " + str(score_list))
            for x in packed_score_list:
                if x == ScorePeg.States.BLACK:
                    if self.score_pegs.state_1 == ScorePeg.States.EMPTY:
                        self.score_pegs.state_1 = ScorePeg.States.BLACK
                    elif self.score_pegs.state_2 == ScorePeg.States.EMPTY:
                        self.score_pegs.state_2 = ScorePeg.States.BLACK
                    elif self.score_pegs.state_3 == ScorePeg.States.EMPTY:
                        self.score_pegs.state_3 = ScorePeg.States.BLACK
                    elif self.score_pegs.state_4 == ScorePeg.States.EMPTY:
                        self.score_pegs.state_4 = ScorePeg.States.BLACK
                elif x == ScorePeg.States.WHITE:
                    if self.score_pegs.state_1 == ScorePeg.States.EMPTY:
                        self.score_pegs.state_1 = ScorePeg.States.WHITE
                    elif self.score_pegs.state_2 == ScorePeg.States.EMPTY:
                        self.score_pegs.state_2 = ScorePeg.States.WHITE
                    elif self.score_pegs.state_3 == ScorePeg.States.EMPTY:
                        self.score_pegs.state_3 = ScorePeg.States.WHITE
                    elif self.score_pegs.state_4 == ScorePeg.States.EMPTY:
                        self.score_pegs.state_4 = ScorePeg.States.WHITE
            
            correct_guess = self.score_pegs.state_1 == ScorePeg.States.BLACK and \
                            self.score_pegs.state_2 == ScorePeg.States.BLACK and \
                            self.score_pegs.state_3 == ScorePeg.States.BLACK and \
                            self.score_pegs.state_4 == ScorePeg.States.BLACK

        return correct_guess

class GuessRows():
    canvas = None
    mm = None
    guess_rows = []      

    def init_rows(canvas, mm):
        GuessRows.canvas = canvas
        GuessRows.mm = mm 
        GuessRows.guess_rows = []
        for ind, y_loc in zip(Globals.GUESS_IND_LIST, canvas.guess_peg_y_loc_list):
            GuessRows.guess_rows.append(GuessRow(ind, y_loc, canvas))

    def draw_rows():        
        for row in GuessRows.guess_rows:            
            row.draw_row(GuessRows.canvas, GuessRows.mm.game_round)

    def check_click(x_pos, y_pos, forward = True):
        if GuessRows.mm.is_playable_round():            
            GuessRows.guess_rows[GuessRows.mm.game_round - 1].check_click(x_pos, y_pos, forward)

    def check_motion(x_pos, y_pos):
        if GuessRows.mm.is_playable_round():            
            GuessRows.guess_rows[GuessRows.mm.game_round - 1].motion(x_pos, y_pos)

    def set_curr_round(game_round):
        for row in GuessRows.guess_rows:
            row.set_inactive()
        GuessRows.guess_rows[int(game_round) - 1].set_active()
