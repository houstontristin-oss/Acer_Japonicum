import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE



class GameplayView(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        arcade.set_background_color((34, 80, 52))

    def on_draw(self) -> None:
        self.clear()

        arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, 180, (78, 121, 76))
        arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 180, SCREEN_HEIGHT, (122, 176, 205))

        arcade.draw_text(
            "Gameplay Placeholder",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 30,
            arcade.color.WHITE,
            font_size=34,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_text(
            "This is where your first playable town test will go.",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 20,
            (235, 240, 235),
            font_size=16,
            anchor_x="center",
        )

        arcade.draw_text(
            "Press ESC to return to menu",
            SCREEN_WIDTH / 2,
            70,
            (235, 240, 235),
            font_size=14,
            anchor_x="center",
        )

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            from views.title_menu_view import TitleMenuView
            self.window.show_view(TitleMenuView())