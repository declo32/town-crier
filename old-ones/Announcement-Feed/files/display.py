#!/usr/bin/python

"""display v3 - Display the announcements from feed.pkl"""

from tkinter import *
from PIL import Image, ImageTk
import itertools

import utils

slide_interval = 1      # seconds
open_for = 5            # minutes

feed = itertools.cycle(  # The feed, but every time it goes to the end it goes back to the beginning
    utils.get_feed()
)


class MyApp(Tk):

    def __init__(self):
        Tk.__init__(self)

        fr = Canvas(self)
        fr.pack()

        self.canvas = Canvas(fr, height=400, width=600, background="#ccddff")
        self.canvas.pack()

        self.bind("<Escape>", exit)           # If you press escape, it exits
        self.attributes("-fullscreen", True)  # Sets it to fullscreen
        self.attributes("-topmost", True)     # In front of everything else

        self.slideshow()   # Runs the slideshow

        # self.after((open_for*60)*1000, self.destroy)  # For debugging

    def slideshow(self):
        # all positioning variables that concern the pictures and text will be relative to the position of the headings.

        headerx = 0
        headery = 0
        headerheight = 150
        wrap_length = 1500
        
        announcement = feed.__next__()  # Get the next announcement

        print("Displaying: %s" % announcement)

        header_label = Label(  # Make the header display what account the announcement is coming from.
            self,
            text=announcement.header,
            fg="midnight blue",
            justify="center",
            font=("Helvetica Neue", 60, "bold"),  # Was verdana
            bd=5,
            wraplength=wrap_length,
            background="#6699ff",
            anchor="center"
        )

        text_label = Label(  # Making the text display what the announcement is saying
            self,
            text=announcement.text,
            fg="midnight blue",
            justify="center",
            font=("Helvetica Neue", 40),
            wraplength=wrap_length,
            background="#ccddff"
        )

        label_image = Label(self)  # Setting and deleting the pictures

        if announcement.picture is not None:  # Litotes

            image = Image.open(announcement.picture)
            tkpi = ImageTk.PhotoImage(image)
            label_image.configure(image=tkpi)
            label_image.image = tkpi  # Trust me... this is necessary

            image_width, image_height = image.size
            picture_x = (self.winfo_width()/2)-(image_width/2)

            if image_width > image_height:  # If the picture is landscape
                if announcement.text == " ":  # If there's no text
                    label_image.place(
                        x=(self.winfo_width() / 2) - (image_width / 2),
                        y=(headery + headerheight + 100),
                        width=image_width,
                        height=image_height
                    )
                else:  # If there is text
                    label_image.place(
                        x=picture_x,
                        y=(self.winfo_height() - image_height - 50),
                        width=image_width,
                        height=image_height
                    )
                    text_label.config(anchor="n")
                    text_label.place(
                        x=headerx,
                        y=(50 + headerheight),
                        width=self.winfo_width(),
                        height=self.winfo_height()
                    )
            else:  # If the picture is square or portrait
                if announcement.text == " ":  # If there's no text
                    label_image.place(
                        x=((self.winfo_width() / 2) - (image_width / 2)),
                        y=(25 + headery + headerheight),
                        width=image_width,
                        height=image_height
                    )
                else:  # If there is text
                    label_image.config(anchor="e")
                    label_image.place(
                        x=(self.winfo_width() - image_width - 50),
                        y=(25 + headery + headerheight),
                        width=image_width,
                        height=image_height
                    )
                    text_label.config(anchor="nw")
                    text_label.config(justify="left")
                    text_label.config(wraplength=(wrap_length/2)-100)
                    text_label.place(
                        x=(50 + headerx),
                        y=(250 + headery + headerheight),
                        width=self.winfo_width(),
                        height=self.winfo_height()
                    )
        else:  # removes the picture
            label_image.destroy()
            text_label.place(x=headerx,
                             y=headerheight,
                             width=self.winfo_width(),
                             height=(200 + self.winfo_height() / 2))

        header_label.place(x=headerx,
                           y=headery,
                           width=self.winfo_width(),
                           height=headerheight)

        # the logo
        logo_img = Image.open(utils.LOGO_PATH)
        logo = ImageTk.PhotoImage(logo_img)
        logo_label = Label(self, image=logo, anchor="nw")
        logo_label.image = logo  # This seems like an unnecessary step, but keep it
        logo_label.place(x=0, y=0, width=logo_img.size[0], height=logo_img.size[1])

        huh = self.after(announcement.display_time, self.slideshow)

        # self.after_cancel(huh) - works ! so maybe can do from below Fn?

if __name__ == "__main__":
    root = MyApp()
    root.mainloop()
