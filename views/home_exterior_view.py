from __future__ import annotations

import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from core.camera import GameCamera
from player.player import Player
from views.view_transition import ViewTransitionMixin


class HomeExteriorView(arcade.View, ViewTransitionMixin):
    def __init__(self, spawn_key: str = "default") -> None:
        super().__init__()

        arcade.set_background_color((42, 78, 52))

        self.world_width = 1700
        self.world_height = 1200

        self.world_left = 0
        self.world_right = self.world_width
        self.world_bottom = 0
        self.world_top = self.world_height

        self.spawn_points = {
            "default": (1180, 170),
            "from_forest": (180, 470),
        }

        spawn_x, spawn_y = self.spawn_points.get(spawn_key, self.spawn_points["default"])

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
            "Grandparents' House Exterior",
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
            "Home Zone",
            20,
            SCREEN_HEIGHT - 88,
            (207, 220, 196),
            font_size=13,
        )

        self.house_left = 980
        self.house_right = 1320
        self.house_bottom = 350
        self.house_top = 610

        self.yard_left = 840
        self.yard_right = 1460
        self.yard_bottom = 150
        self.yard_top = 780

        self.trail_exit_zone = {
            "left": 0,
            "right": 40,
            "bottom": 380,
            "top": 560,
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
        from views.forest_path_view import ForestPathView

        in_left_band = self.player.left <= self.trail_exit_zone["right"]
        in_height = self.trail_exit_zone["bottom"] <= self.player.center_y <= self.trail_exit_zone["top"]

        if in_left_band and in_height:
            self.begin_transition(ForestPathView, "from_home")

    def _draw_world(self) -> None:
        self._draw_sky()
        self._draw_ground()
        self._draw_home_zone()
        self._draw_trail_head()
        self._draw_trees()

    def _draw_sky(self) -> None:
        arcade.draw_lrbt_rectangle_filled(
            0,
            self.world_width,
            self.world_height * 0.72,
            self.world_height,
            (145, 186, 216),
        )

    def _draw_ground(self) -> None:
        arcade.draw_lrbt_rectangle_filled(
            0,
            self.world_width,
            0,
            self.world_height,
            (76, 112, 68),
        )

    def _draw_home_zone(self) -> None:
        fence = (148, 148, 144)

        arcade.draw_lrbt_rectangle_filled(
            self.yard_left,
            self.yard_right,
            self.yard_bottom,
            self.yard_top,
            (108, 132, 94),
        )

        arcade.draw_lrbt_rectangle_filled(self.yard_left, self.yard_right, self.yard_top - 10, self.yard_top, fence)
        arcade.draw_lrbt_rectangle_filled(self.yard_left, self.yard_right, self.yard_bottom, self.yard_bottom + 10, fence)
        arcade.draw_lrbt_rectangle_filled(self.yard_left, self.yard_left + 10, self.yard_bottom, self.yard_top, fence)
        arcade.draw_lrbt_rectangle_filled(self.yard_right - 10, self.yard_right, self.yard_bottom, self.yard_top, fence)

        arcade.draw_lrbt_rectangle_filled(1060, 1240, self.yard_bottom, self.yard_bottom + 12, (150, 122, 88))

        arcade.draw_lrbt_rectangle_filled(
            self.house_left,
            self.house_right,
            self.house_bottom,
            self.house_top,
            (186, 176, 156),
        )

        arcade.draw_triangle_filled(
            (self.house_left + self.house_right) / 2,
            self.house_top + 120,
            self.house_left - 18,
            self.house_top - 5,
            self.house_right + 18,
            self.house_top - 5,
            (86, 66, 54),
        )

        arcade.draw_lrbt_rectangle_filled(1050, 1250, 310, 350, (114, 92, 74))
        arcade.draw_lrbt_rectangle_outline(1050, 1250, 310, 350, (70, 56, 44), 2)

        arcade.draw_lrbt_rectangle_filled(1115, 1175, 350, 520, (74, 60, 46))

        arcade.draw_lrbt_rectangle_filled(1012, 1068, 450, 525, (194, 222, 226))
        arcade.draw_lrbt_rectangle_filled(1232, 1288, 450, 525, (194, 222, 226))

        arcade.draw_lrbt_rectangle_outline(1012, 1068, 450, 525, (80, 92, 94), 2)
        arcade.draw_lrbt_rectangle_outline(1232, 1288, 450, 525, (80, 92, 94), 2)

        arcade.draw_lrbt_rectangle_filled(1372, 1392, 170, 220, (82, 64, 48))
        arcade.draw_lrbt_rectangle_filled(1360, 1404, 220, 248, (160, 48, 52))

    def _draw_trail_head(self) -> None:
        path = (150, 122, 88)
        inner = (166, 138, 102)

        arcade.draw_line_strip(
            [
                (1150, 150),
                (980, 230),
                (760, 340),
                (540, 430),
                (240, 470),
                (0, 470),
            ],
            path,
            126,
        )
        arcade.draw_line_strip(
            [
                (1150, 150),
                (980, 230),
                (760, 340),
                (540, 430),
                (240, 470),
                (0, 470),
            ],
            inner,
            82,
        )

    def _draw_trees(self) -> None:
        positions = [
            (840, 850, 48),
            (1020, 860, 56),
            (1280, 830, 52),
            (1480, 730, 46),
            (760, 170, 54),
            (1530, 220, 58),
            (520, 620, 52),
            (430, 770, 46),
            (290, 330, 44),
        ]

        for x, y, radius in positions:
            arcade.draw_lrbt_rectangle_filled(x - 10, x + 10, y - 60, y + 20, (92, 64, 42))
            arcade.draw_circle_filled(x, y + 35, radius, (132, 74, 44))
            arcade.draw_circle_filled(x - radius * 0.55, y + 20, radius * 0.7, (160, 94, 52))
            arcade.draw_circle_filled(x + radius * 0.55, y + 20, radius * 0.7, (176, 112, 58))

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