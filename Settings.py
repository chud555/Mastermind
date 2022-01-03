# TODO: Figure out what things are needed to store and restore a session
from GridCanvas import GridCanvas
from pathlib import Path
from os.path import exists

class Settings():
    home_dir = str(Path.home())
    settings_file = "mastermind_settings.txt"
    settings_f = home_dir + "\\" + settings_file
    
    # The settings list var_name field is variables that can resolved at run time
    settings_list = [{"var_name":"GridCanvas.curr_x_size", "var_value":"Not Found"},
                     {"var_name":"GridCanvas.curr_y_size", "var_value":"Not Found"}]

    def save():
        with open(Settings.settings_f, 'w') as fh:
            for setting in Settings.settings_list:
                print("eval : " + setting["var_name"] + " value : " + str(eval(setting["var_name"])))
                fh.write(setting["var_name"] + " : " + str(eval(setting["var_name"])) + "\n")

    def load():
        if(exists(Settings.settings_f)):
            with open(Settings.settings_f, 'r') as fh:
                for line in fh:
                    for setting in Settings.settings_list:
                        if len(line.split(setting["var_name"] + " : ")) == 2:
                            setting["var_value"] = line.split(setting["var_name"] + " : ")[1][:-1]

        # TODO: Actually wire these up as they are needed
        for setting in Settings.settings_list:
            print(str(setting))