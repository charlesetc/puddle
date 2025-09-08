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
    def update(self):
        self.controller.text_label.text = self.controller.get_time()


class Rotary(App):
    def update(self):
        self.controller.text_label.text = str(self.controller.encoder.position)

class Menu(App):
    def update(self):
        if self.controller.button.value == 0:
            self.controller.run("rotary")

        self.controller.text_label.text = "Menu"
