from tkinter import Canvas

class CanvasContainer(Canvas):
    default_x_size = 400
    default_y_size = 800

    
    def __init__(self,parent):
        Canvas.__init__(self,parent, width=CanvasContainer.default_x_size, height=CanvasContainer.default_y_size, highlightthickness = 0)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

    def __str__(self):
        out_str = ""
        out_str += "self.width  : " + str(self.width) + "\n"
        out_str += "self.height : " + str(self.height) + "\n"
        return out_str