from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen, FallOutTransition, SwapTransition
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex
import math

DISABLE_MOUSE_INPUT = True

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 480

# Apply configuration for mouse input
if DISABLE_MOUSE_INPUT:
    Config.set('input', 'mouse', 'disable_multitouch')
else:
    Config.set('input', 'mouse', 'mouse,disable_multitouch')

class MainScreen(Screen):
    pass

class CalculatorScreen(Screen):
    pass

class NotesScreen(Screen):
    pass

class ScreenPiApp(App):
    def build(self):
        Window.fullscreen = 'auto'
        sm = ScreenManager()

        sm.transition = FallOutTransition()

        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CalculatorScreen(name='calculator'))
        sm.add_widget(NotesScreen(name='notes'))

        if DISABLE_MOUSE_INPUT:
            # Disable mouse input programmatically
            Window.bind(on_mouse_down=self._disable_mouse_input)
            Window.bind(on_mouse_up=self._disable_mouse_input)

        Window.bind(on_touch_down=self.on_touch_event)
        Window.bind(on_touch_move=self.on_touch_event)
        Window.bind(on_touch_up=self.on_touch_event)

        return sm

    def get_color(self, hex_value):
        return get_color_from_hex(hex_value)

    def _disable_mouse_input(self, *args):
        # This function will prevent mouse events from being processed
        return True

    # It seems it is pushing the correct buttons now
    def on_touch_event(self, instance, touch):
        # Invert the X coordinate
        inverted_x = 480 - touch.x
        inverted_y = 800 - touch.y

        original_x = touch.x

        translated_inverted_y = (inverted_y * SCREEN_WIDTH) / SCREEN_HEIGHT        
        translated_y = (original_x * SCREEN_HEIGHT) / SCREEN_WIDTH
        print("Translated y = " + str(translated_y))
        touch.x = translated_inverted_y
        print("Final x = " + str(touch.x))
        touch.y = translated_y
        print("final y = " + str(touch.y))

        return False  # Return False to allow the event to propagate


    def change_screen(self, screen_name):
        # if screen_name == "main":
        #     self.root.transition = SlideTransition(direction='down')
        # else:
        #     self.root.transition = SlideTransition(direction='up')
        self.root.current = screen_name

    def on_button_press(self, button):
        display = self.root.get_screen('calculator').ids.calc_display
        current_text = display.text

        if button.text == "=":
            try:
                display.text = str(eval(current_text))
            except Exception:
                display.text = "Error"
        elif button.text == "C":
            display.text = "0"
        elif button.text == "CE":
            display.text = current_text[:-1] or "0"
        elif button.text == "sqrt":
            try:
                display.text = str(math.sqrt(float(current_text)))
            except Exception:
                display.text = "Error"
        elif button.text == "sqr":
            try:
                display.text = str(float(current_text) ** 2)
            except Exception:
                display.text = "Error"
        elif button.text == "mod":
            display.text += "%"
        elif button.text == "^n":
            display.text += "**"
        elif button.text == "+/-":
            try:
                display.text = str(float(current_text) * -1)
            except Exception:
                display.text = "Error"
        else:
            if current_text == "0" or current_text == "Error":
                display.text = button.text
            else:
                display.text += button.text

    def on_clear(self, button):
        display = self.root.get_screen('calculator').ids.calc_display
        display.text = "0"

    def on_clear_entry(self, button):
        display = self.root.get_screen('calculator').ids.calc_display
        current_text = display.text
        display.text = current_text[:-1] or "0"

ScreenPiApp().run()