from adafruit_display_text.label import Label
from terminalio import FONT


def simple_label(text):
    return Label(
        font=FONT,
        text=text,
        x=36,  # Adjusted X position to center for 144 width
        y=76,  # Adjusted Y position to center for 168 height
        scale=2,
        line_spacing=1.2,
        color=0x000000,
    )


class App:
    def __init__(self, controller):
        self.controller = controller

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self):
        pass


class Clock(App):
    def enter(self):
        self.text_label = simple_label("00:00:00")
        self.controller.clear_display()
        self.controller.add_widget(self.text_label)

    def update(self):
        self.text_label.text = self.controller.get_time()


class Rotary(App):
    def enter(self):
        self.text_label = simple_label("0")
        self.controller.clear_display()
        self.controller.add_widget(self.text_label)

    def update(self):
        self.text_label.text = str(self.controller.encoder.position)

class Menu(App):
    def enter(self):
        self.text_label = simple_label("Menu")
        self.controller.clear_display()
        self.controller.add_widget(self.text_label)

    def update(self):
        if self.controller.button.value == 0:
            self.controller.run("rotary")

        self.text_label.text = "Menu"
