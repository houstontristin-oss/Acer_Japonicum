import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from core.camera import GameCamera
from player.player import Player


class GameplayView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        arcade.set_background_color((34, 80, 52))

        self.world_width = SCREEN_WIDTH
        self.world_height = 1600

        self.path_left = 430
        self.path_right = 850
        self.path_bottom = 0
        self.path_top = self.world_height

        self.player = Player(
            center_x=SCREEN_WIDTH / 2,
            center_y=120,
            width=36,
            height=48,
            speed=260,
        )
        self.title_text = arcade.Text(
            "Gameplay Movement Test",
            20,
            SCREEN_HEIGHT - 34,
            arcade.color.WHITE,
            font_size=20,
            bold=True,
        )
        self.instructions_text = arcade.Text(
            "Move with WASD or arrow keys   |   ESC = return to menu",
            20,
            SCREEN_HEIGHT - 62,
            (226, 234, 226),
            font_size=14,
        )

        self.camera = GameCamera()

        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

    def on_draw(self) -> None:
        self.clear()

        self.camera.use()
        self._draw_world()
        self.player.draw()

        self.window.default_camera.use()
        self._draw_ui()

    def on_update(self, delta_time: float) -> None:
        dx = 0.0
        dy = 0.0

        if self.move_up:
            dy += 1.0
        if self.move_down:
            dy -= 1.0
        if self.move_left:
            dx -= 1.0
        if self.move_right:
            dx += 1.0

        if dx != 0.0 or dy != 0.0:
            length = (dx ** 2 + dy ** 2) ** 0.5
            dx /= length
            dy /= length

        self.player.move(dx, dy, delta_time)
        self.player.clamp_to_bounds(
            self.path_left,
            self.path_right,
            self.path_bottom,
            self.path_top,
        )

        self.camera.follow(
            self.player.center_x,
            self.player.center_y,
            self.world_width,
            self.world_height,
        )

    def _draw_world(self) -> None:
        arcade.draw_lrbt_rectangle_filled(
            0, self.world_width, self.world_height * 0.82, self.world_height,
            (120, 170, 205)
        )

        arcade.draw_lrbt_rectangle_filled(
            0, self.world_width, 0, self.world_height,
            (58, 96, 54)
        )

        arcade.draw_lrbt_rectangle_filled(
            self.path_left, self.path_right, self.path_bottom, self.path_top,
            (146, 118, 82)
        )

        arcade.draw_lrbt_rectangle_filled(
            self.path_left + 65, self.path_right - 65, self.path_bottom, self.path_top,
            (161, 132, 95)
        )

        arcade.draw_lrbt_rectangle_filled(
            0, self.path_left, 0, self.world_height,
            (42, 74, 38)
        )
        arcade.draw_lrbt_rectangle_filled(
            self.path_right, self.world_width, 0, self.world_height,
            (42, 74, 38)
        )

        for y in range(40, int(self.world_height), 110):
            arcade.draw_lrbt_rectangle_filled(60, 84, y, y + 90, (92, 64, 42))
            arcade.draw_circle_filled(72, y + 105, 36, (36, 92, 40))
            arcade.draw_circle_filled(50, y + 96, 24, (42, 102, 46))
            arcade.draw_circle_filled(94, y + 95, 24, (42, 102, 46))

        for y in range(90, int(self.world_height), 140):
            arcade.draw_lrbt_rectangle_filled(205, 227, y, y + 84, (92, 64, 42))
            arcade.draw_circle_filled(216, y + 98, 32, (36, 92, 40))
            arcade.draw_circle_filled(195, y + 93, 21, (42, 102, 46))
            arcade.draw_circle_filled(236, y + 93, 21, (42, 102, 46))

        for y in range(60, int(self.world_height), 110):
            arcade.draw_lrbt_rectangle_filled(self.world_width - 84, self.world_width - 60, y, y + 90, (92, 64, 42))
            arcade.draw_circle_filled(self.world_width - 72, y + 105, 36, (36, 92, 40))
            arcade.draw_circle_filled(self.world_width - 50, y + 96, 24, (42, 102, 46))
            arcade.draw_circle_filled(self.world_width - 94, y + 95, 24, (42, 102, 46))

        for y in range(110, int(self.world_height), 140):
            arcade.draw_lrbt_rectangle_filled(self.world_width - 227, self.world_width - 205, y, y + 84, (92, 64, 42))
            arcade.draw_circle_filled(self.world_width - 216, y + 98, 32, (36, 92, 40))
            arcade.draw_circle_filled(self.world_width - 195, y + 93, 21, (42, 102, 46))
            arcade.draw_circle_filled(self.world_width - 236, y + 93, 21, (42, 102, 46))

        arcade.draw_line(self.path_left, 0, self.path_left, self.world_height, (82, 60, 36), 3)
        arcade.draw_line(self.path_right, 0, self.path_right, self.world_height, (82, 60, 36), 3)

    def _draw_ui(self) -> None:
        self.title_text.draw()
        self.instructions_text.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol in (arcade.key.W, arcade.key.UP):
            self.move_up = True
        elif symbol in (arcade.key.S, arcade.key.DOWN):
            self.move_down = True
        elif symbol in (arcade.key.A, arcade.key.LEFT):
            self.move_left = True
        elif symbol in (arcade.key.D, arcade.key.RIGHT):
            self.move_right = True
        elif symbol == arcade.key.ESCAPE:
            from views.title_menu_view import TitleMenuView
            self.window.show_view(TitleMenuView())

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        if symbol in (arcade.key.W, arcade.key.UP):
            self.move_up = False
        elif symbol in (arcade.key.S, arcade.key.DOWN):
            self.move_down = False
        elif symbol in (arcade.key.A, arcade.key.LEFT):
            self.move_left = False
        elif symbol in (arcade.key.D, arcade.key.RIGHT):
            self.move_right = False