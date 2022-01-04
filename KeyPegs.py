from Globals import Globals
from GridCanvas import GridCanvas
from ColorPeg import ColorPeg

# TODO: Using this like a static class, but could make the name shorter when referencing it, maybe using @classmethod
# I don't like decorators
class KeyPegs():
    peg_list = []
    hidden = False
    hide_block_color = "#D0D0D0"
    canvas = None

    def init_pegs(canvas):
        KeyPegs.canvas = canvas
        KeyPegs.peg_list = []        

        for ind in Globals.PEG_IND_LIST:
            KeyPegs.peg_list.append(ColorPeg(KeyPegs.canvas.peg_x_loc_list[ind], KeyPegs.canvas.key_y_loc, is_clickable=True))

    def move_pegs():
        for ind, k_peg in zip(Globals.PEG_IND_LIST, KeyPegs.peg_list):
            k_peg.move_peg(KeyPegs.canvas.peg_x_loc_list[ind], KeyPegs.canvas.key_y_loc)

    def draw_pegs():
        KeyPegs.move_pegs()
        if KeyPegs.hidden:
            # Don't need to draw the keys in this case. Deactivate them also
            KeyPegs.canvas.create_rectangle((KeyPegs.canvas.peg_x_loc_list[0] - KeyPegs.canvas.curr_x_step / 4),
                                            (KeyPegs.canvas.key_y_loc - KeyPegs.canvas.curr_y_step / 4),
                                            (KeyPegs.canvas.peg_x_loc_list[3] + KeyPegs.canvas.curr_x_step / 4),
                                            (KeyPegs.canvas.key_y_loc + KeyPegs.canvas.curr_y_step / 4),                                    
                                            fill=KeyPegs.hide_block_color)
        else:
            for k_peg in KeyPegs.peg_list:
                k_peg.draw_peg(KeyPegs.canvas, KeyPegs.canvas.smallest_step)

    def set_hidden(is_hidden):
        KeyPegs.hidden = is_hidden

        # If key pegs are hidden, can't be clicked
        for ind in Globals.PEG_IND_LIST:
            KeyPegs.peg_list[ind].is_clickable = not is_hidden

    def check_click(x_pos, y_pos, forward = True):
        for ind in Globals.PEG_IND_LIST:
            KeyPegs.peg_list[ind].check_click(x_pos, y_pos, forward)

    def set_random(blanks_only=False):
        for ind in Globals.PEG_IND_LIST:
            if not blanks_only or KeyPegs.peg_list[ind].state == ColorPeg.States.EMPTY:
                KeyPegs.peg_list[ind].set_random()
