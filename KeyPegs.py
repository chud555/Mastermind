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
        KeyPegs.peg_list = []
        KeyPegs.canvas = canvas

        for ind in Globals.PEG_IND_LIST:
            KeyPegs.peg_list.append(ColorPeg(KeyPegs.canvas.peg_x_loc_list[ind], KeyPegs.canvas.key_y_loc, is_clickable=True))

    def move_pegs():
        for ind in Globals.PEG_IND_LIST:
            KeyPegs.peg_list[ind].move_peg(KeyPegs.canvas.peg_x_loc_list[ind], KeyPegs.canvas.key_y_loc)

    def draw_pegs(canvas):
        if KeyPegs.hidden:
            # Don't need to draw the keys in this case. Deactivate them also
            canvas.create_rectangle((KeyPegs.canvas.peg_x_loc_list[0] - KeyPegs.canvas.curr_x_step / 4),
                                    (KeyPegs.canvas.key_y_loc - KeyPegs.canvas.curr_y_step / 4),
                                    (KeyPegs.canvas.peg_x_loc_list[3] + KeyPegs.canvas.curr_x_step / 4),
                                    (KeyPegs.canvas.key_y_loc + KeyPegs.canvas.curr_y_step / 4),                                    
                                    fill=KeyPegs.hide_block_color)
        else:
            for ind in Globals.PEG_IND_LIST:
                KeyPegs.peg_list[ind].set_peg_size(KeyPegs.canvas.smallest_step)
                if KeyPegs.peg_list[ind].state == ColorPeg.States.EMPTY:
                    curr_size = KeyPegs.peg_list[ind].empty_size
                else:                
                    curr_size = KeyPegs.peg_list[ind].size
                canvas.create_oval(KeyPegs.peg_list[ind].x_loc - curr_size, 
                                   KeyPegs.peg_list[ind].y_loc - curr_size, 
                                   KeyPegs.peg_list[ind].x_loc + curr_size,
                                   KeyPegs.peg_list[ind].y_loc + curr_size, 
                                   fill=KeyPegs.peg_list[ind].state.value["color"],
                                   outline=KeyPegs.peg_list[ind].peg_outline_color)

    def set_hidden(is_hidden):
        KeyPegs.hidden = is_hidden

        # If key pegs are hidden, can't be clicked
        for ind in Globals.PEG_IND_LIST:
            KeyPegs.peg_list[ind].is_clickable = not is_hidden

    def check_click(x_pos, y_pos, forward):
        for ind in Globals.PEG_IND_LIST:
            KeyPegs.peg_list[ind].check_click(x_pos, y_pos, forward)

    def set_random(blanks_only=False):
        for ind in Globals.PEG_IND_LIST:
            if not blanks_only or KeyPegs.peg_list[ind].state == ColorPeg.States.EMPTY:
                KeyPegs.peg_list[ind].state
