from Globals import Globals
from ScorePeg import ScorePeg
from GridCanvas import GridCanvas
from TextObj import TextObj

class GuessRows():
    # There are 10 guess rows, they have 4 distinct pieces, the label, the pegs, the "X" to submit a guess and the score
    class GuessRow():
        label = ""
        peg_list = []
        submit_guess_text = None
        score_pegs = None

        def __init__(self, label, y_loc):
            self.label = str(label)
            self.peg_list = []
            for ind in Globals.PEG_IND_LIST:
                self.peg_list.append(GridCanvas.peg_x_loc_list[ind], y_loc)
            self.submit_guess_text = TextObj(GridCanvas.text_menu_x_loc, y_loc, "X")
            self.score_pegs = ScorePeg(GridCanvas.score_pegs_x_loc, y_loc, GridCanvas.smallest_step)

        def score_guess(self):
            correct_guess = False

            score_list = [ScorePeg.States.EMPTY,
                          ScorePeg.States.EMPTY,
                          ScorePeg.States.EMPTY,
                          ScorePeg.States.EMPTY]

            if (self.game_round != "win" and self.game_round != "lose"):
                curr_ind = 10 - self.game_round
                white_check_list = []
                # Check for black peg matches first
                for i in list(range(1, 5, 1)):
                    """
                    print("i : " + str(i))
                    print("self.guess_color_pegs[curr_ind] : " + str(self.guess_color_pegs[curr_ind]))
                    print("self.guess_color_pegs[curr_ind][i - 1] : " + str(self.guess_color_pegs[curr_ind][i - 1]))
                    """
                    if self.guess_color_pegs[curr_ind][i - 1].state == self.key_color_pegs[i - 1].state:
                        score_list[i - 1] = ScorePeg.States.BLACK
                    else:
                        white_check_list.append(self.key_color_pegs[i - 1].state)
                for i in list(range(1, 5, 1)):
                    if score_list[i - 1] != ScorePeg.States.BLACK and self.guess_color_pegs[curr_ind][i - 1].state in white_check_list:
                        white_check_list.remove(self.guess_color_pegs[curr_ind][i - 1].state)
                        score_list[i - 1] = ScorePeg.States.WHITE

                # print("score_list : " + str(score_list))
                for x in score_list:
                    if x == ScorePeg.States.BLACK:
                        if self.score_pegs[curr_ind].state_1 == ScorePeg.States.EMPTY:
                            self.score_pegs[curr_ind].state_1 = ScorePeg.States.BLACK
                        elif self.score_pegs[curr_ind].state_2 == ScorePeg.States.EMPTY:
                            self.score_pegs[curr_ind].state_2 = ScorePeg.States.BLACK
                        elif self.score_pegs[curr_ind].state_3 == ScorePeg.States.EMPTY:
                            self.score_pegs[curr_ind].state_3 = ScorePeg.States.BLACK
                        elif self.score_pegs[curr_ind].state_4 == ScorePeg.States.EMPTY:
                            self.score_pegs[curr_ind].state_4 = ScorePeg.States.BLACK
                    elif x == ScorePeg.States.WHITE:
                        if self.score_pegs[curr_ind].state_1 == ScorePeg.States.EMPTY:
                            self.score_pegs[curr_ind].state_1 = ScorePeg.States.WHITE
                        elif self.score_pegs[curr_ind].state_2 == ScorePeg.States.EMPTY:
                            self.score_pegs[curr_ind].state_2 = ScorePeg.States.WHITE
                        elif self.score_pegs[curr_ind].state_3 == ScorePeg.States.EMPTY:
                            self.score_pegs[curr_ind].state_3 = ScorePeg.States.WHITE
                        elif self.score_pegs[curr_ind].state_4 == ScorePeg.States.EMPTY:
                            self.score_pegs[curr_ind].state_4 = ScorePeg.States.WHITE
                
                correct_guess = self.score_pegs[curr_ind].state_1 == ScorePeg.States.BLACK and \
                                self.score_pegs[curr_ind].state_2 == ScorePeg.States.BLACK and \
                                self.score_pegs[curr_ind].state_3 == ScorePeg.States.BLACK and \
                                self.score_pegs[curr_ind].state_4 == ScorePeg.States.BLACK

            return correct_guess

    guess_row_list = []