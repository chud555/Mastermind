from Globals import Globals
from GridCanvas import GridCanvas
from ColorPeg import ColorPeg

class KeyPegs():
    peg_list = []
    hidden = False
    hide_block_color = "#D0D0D0"

    def init_pegs():
        KeyPegs.peg_list = []

        for ind in Globals.PEG_IND_LIST:
            KeyPegs.peg_list.append(ColorPeg(GridCanvas.peg_x_loc_list[ind], GridCanvas.key_y_loc, is_clickable=True))

    def move_pegs():
        for ind in Globals.PEG_IND_LIST:
            KeyPegs.peg_list[ind].move_peg(GridCanvas.peg_x_loc_list[ind], GridCanvas.key_y_loc)

    def draw_pegs(canvas):
        if KeyPegs.hidden:
            # Don't need to draw the keys in this case. Deactivate them also
            for ind in Globals.PEG_IND_LIST:
                KeyPegs.peg_list[ind].is_clickable = False
            canvas.create_rectangle((GridCanvas.peg_x_loc_list[0] - GridCanvas.curr_x_step / 4),
                                    (GridCanvas.key_y_loc - GridCanvas.curr_y_step / 4),
                                    (GridCanvas.peg_x_loc_list[3] + GridCanvas.curr_x_step / 4),
                                    (GridCanvas.key_y_loc + GridCanvas.curr_y_step / 4),                                    
                                    fill=GridCanvas.hide_block_color)
        else:
            for ind in Globals.PEG_IND_LIST:
                KeyPegs.peg_list[ind].set_peg_size(GridCanvas.smallest_step)
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
