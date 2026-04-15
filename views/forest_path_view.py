from __future__ import annotations

import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from core.camera import GameCamera
from player.player import Player
from views.view_transition import ViewTransitionMixin


class ForestPathView(arcade.View, ViewTransitionMixin):
    def __init__(self, spawn_key: str = "from_home") -> None:
        super().__init__()

        arcade.set_background_color((34, 66, 44))

        self.world_width = 1800
        self.world_height = 1400

        self.world_left = 0
        self.world_right = self.world_width
        self.world_bottom = 0
        self.world_top = self.world_height

        self.spawn_points = {
            "from_home": (1660, 680),
        }

        spawn_x, spawn_y = self.spawn_points.get(spawn_key, self.spawn_points["from_home"])

        self.player = Player(
            center_x=spawn_x,
            center_y=spawn_y,
            width=36,
            height=48,
            speed=260,
        )

        self.camera = GameCamera()

        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

        self.title_text = arcade.Text(
            "Forest Path",
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
        self.location_text = arcade.Text(
            "Forest Trail",
            20,
            SCREEN_HEIGHT - 88,
            (207, 220, 196),
            font_size=13,
        )

        self.home_return_zone = {
            "left": self.world_width - 40,
            "right": self.world_width,
            "bottom": 600,
            "top": 760,
        }

        self._setup_transition_system()

    def on_draw(self) -> None:
        self.clear()

        self.camera.use()
        self._draw_world()
        self.player.draw()

        self.window.default_camera.use()
        self._draw_ui()
        self.draw_transition()

    def on_update(self, delta_time: float) -> None:
        if self.is_transitioning:
            self.update_transition(delta_time)
            return

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
            self.world_left,
            self.world_right,
            self.world_bottom,
            self.world_top,
        )

        self._check_exit_triggers()

        self.camera.follow(
            self.player.center_x,
            self.player.center_y,
            self.world_width,
            self.world_height,
        )

    def _check_exit_triggers(self) -> None:
        from views.home_exterior_view import HomeExteriorView

        in_right_band = self.player.right >= self.home_return_zone["left"]
        in_height = self.home_return_zone["bottom"] <= self.player.center_y <= self.home_return_zone["top"]

        if in_right_band and in_height:
            self.begin_transition(HomeExteriorView, "from_forest")

    def _draw_world(self) -> None:
        self._draw_sky()
        self._draw_ground()
        self._draw_path()
        self._draw_trees()
        self._draw_signpost()
        self._draw_hidden_maju()

    def _draw_sky(self) -> None:
        arcade.draw_lrbt_rectangle_filled(
            0,
            self.world_width,
            self.world_height * 0.72,
            self.world_height,
            (126, 164, 194),
        )

    def _draw_ground(self) -> None:
        arcade.draw_lrbt_rectangle_filled(
            0,
            self.world_width,
            0,
            self.world_height,
            (56, 92, 56),
        )

    def _draw_path(self) -> None:
        path = (128, 102, 76)
        inner = (152, 124, 92)

        arcade.draw_line_strip(
            [
                (self.world_width, 680),
                (1500, 670),
                (1220, 700),
                (960, 760),
                (760, 860),
                (620, 1010),
                (530, 1210),
            ],
            path,
            120,
        )
        arcade.draw_line_strip(
            [
                (self.world_width, 680),
                (1500, 670),
                (1220, 700),
                (960, 760),
                (760, 860),
                (620, 1010),
                (530, 1210),
            ],
            inner,
            80,
        )

    def _draw_trees(self) -> None:
        positions = [
            (1520, 870, 52),
            (1410, 540, 48),
            (1260, 960, 56),
            (1120, 540, 50),
            (950, 1030, 58),
            (840, 610, 44),
            (720, 1140, 54),
            (620, 760, 48),
            (480, 930, 46),
            (390, 1180, 52),
            (300, 870, 42),
        ]

        for x, y, radius in positions:
            arcade.draw_lrbt_rectangle_filled(x - 10, x + 10, y - 60, y + 20, (84, 58, 40))
            arcade.draw_circle_filled(x, y + 35, radius, (112, 64, 40))
            arcade.draw_circle_filled(x - radius * 0.55, y + 20, radius * 0.7, (136, 82, 48))
            arcade.draw_circle_filled(x + radius * 0.55, y + 20, radius * 0.7, (150, 100, 54))

    def _draw_signpost(self) -> None:
        sign_x = 930
        sign_y = 790

        arcade.draw_lrbt_rectangle_filled(sign_x - 7, sign_x + 7, sign_y - 20, sign_y + 70, (84, 66, 42))
        arcade.draw_lrbt_rectangle_filled(sign_x - 54, sign_x + 34, sign_y + 38, sign_y + 58, (116, 92, 58))
        arcade.draw_lrbt_rectangle_filled(sign_x - 14, sign_x + 66, sign_y + 8, sign_y + 28, (116, 92, 58))

    def _draw_hidden_maju(self) -> None:
        arcade.draw_circle_filled(1090, 905, 16, (20, 20, 24))
        arcade.draw_circle_filled(1078, 920, 6, (20, 20, 24))
        arcade.draw_circle_filled(1102, 920, 6, (20, 20, 24))
        arcade.draw_circle_filled(1084, 906, 2, (240, 230, 140))
        arcade.draw_circle_filled(1096, 906, 2, (240, 230, 140))

    def _draw_ui(self) -> None:
        self.title_text.draw()
        self.instructions_text.draw()
        self.location_text.draw()

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