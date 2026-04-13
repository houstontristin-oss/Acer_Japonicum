import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE



class SettingsView(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        arcade.set_background_color((24, 30, 38))

    def on_draw(self) -> None:
        self.clear()

        arcade.draw_text(
            "Settings Placeholder",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 20,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_text(
            "Audio, display, and controls will go here.",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 16,
            (210, 220, 214),
            font_size=16,
            anchor_x="center",
        )

        arcade.draw_text(
            "Press ESC to return",
            SCREEN_WIDTH / 2,
            70,
            (210, 220, 214),
            font_size=14,
            anchor_x="center",
        )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            from views.title_menu_view import TitleMenuView
            self.window.show_view(TitleMenuView())