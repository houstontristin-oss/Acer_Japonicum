import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class GameplayView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        arcade.set_background_color((34, 80, 52))

        # Player
        self.player_width = 36
        self.player_height = 48
        self.player_x = SCREEN_WIDTH / 2
        self.player_y = 120
        self.player_speed = 260

        # Input state
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

        # Path boundaries
        self.path_left = 430
        self.path_right = 850
        self.path_bottom = 0
        self.path_top = SCREEN_HEIGHT

    def on_draw(self) -> None:
        self.clear()
        self._draw_world()
        self._draw_player()
        self._draw_ui()

    def on_update(self, delta_time: float) -> None:
        dx = 0.0
        dy = 0.0

        if self.move_up:
            dy += self.player_speed * delta_time
        if self.move_down:
            dy -= self.player_speed * delta_time
        if self.move_left:
            dx -= self.player_speed * delta_time
        if self.move_right:
            dx += self.player_speed * delta_time

        new_x = self.player_x + dx
        new_y = self.player_y + dy

        half_w = self.player_width / 2
        half_h = self.player_height / 2

        # Keep player inside the path
        min_x = self.path_left + half_w
        max_x = self.path_right - half_w
        min_y = self.path_bottom + half_h
        max_y = self.path_top - half_h

        self.player_x = max(min_x, min(new_x, max_x))
        self.player_y = max(min_y, min(new_y, max_y))

    def _draw_world(self) -> None:
        # Sky tint at top
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, SCREEN_HEIGHT * 0.74, SCREEN_HEIGHT,
            (120, 170, 205)
        )

        # Forest floor background
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
            (58, 96, 54)
        )

        # Main path
        arcade.draw_lrbt_rectangle_filled(
            self.path_left, self.path_right, self.path_bottom, self.path_top,
            (146, 118, 82)
        )

        # Path center highlight
        arcade.draw_lrbt_rectangle_filled(
            self.path_left + 65, self.path_right - 65, self.path_bottom, self.path_top,
            (161, 132, 95)
        )

        # Forest walls
        arcade.draw_lrbt_rectangle_filled(
            0, self.path_left, 0, SCREEN_HEIGHT,
            (42, 74, 38)
        )
        arcade.draw_lrbt_rectangle_filled(
            self.path_right, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
            (42, 74, 38)
        )

        # Simple tree trunks on left
        for y in range(40, SCREEN_HEIGHT, 110):
            arcade.draw_lrbt_rectangle_filled(60, 84, y, y + 90, (92, 64, 42))
            arcade.draw_circle_filled(72, y + 105, 36, (36, 92, 40))
            arcade.draw_circle_filled(50, y + 96, 24, (42, 102, 46))
            arcade.draw_circle_filled(94, y + 95, 24, (42, 102, 46))

        # Simple tree trunks left-inner
        for y in range(90, SCREEN_HEIGHT, 140):
            arcade.draw_lrbt_rectangle_filled(205, 227, y, y + 84, (92, 64, 42))
            arcade.draw_circle_filled(216, y + 98, 32, (36, 92, 40))
            arcade.draw_circle_filled(195, y + 93, 21, (42, 102, 46))
            arcade.draw_circle_filled(236, y + 93, 21, (42, 102, 46))

        # Simple tree trunks on right
        for y in range(60, SCREEN_HEIGHT, 110):
            arcade.draw_lrbt_rectangle_filled(SCREEN_WIDTH - 84, SCREEN_WIDTH - 60, y, y + 90, (92, 64, 42))
            arcade.draw_circle_filled(SCREEN_WIDTH - 72, y + 105, 36, (36, 92, 40))
            arcade.draw_circle_filled(SCREEN_WIDTH - 50, y + 96, 24, (42, 102, 46))
            arcade.draw_circle_filled(SCREEN_WIDTH - 94, y + 95, 24, (42, 102, 46))

        # Simple tree trunks right-inner
        for y in range(110, SCREEN_HEIGHT, 140):
            arcade.draw_lrbt_rectangle_filled(SCREEN_WIDTH - 227, SCREEN_WIDTH - 205, y, y + 84, (92, 64, 42))
            arcade.draw_circle_filled(SCREEN_WIDTH - 216, y + 98, 32, (36, 92, 40))
            arcade.draw_circle_filled(SCREEN_WIDTH - 195, y + 93, 21, (42, 102, 46))
            arcade.draw_circle_filled(SCREEN_WIDTH - 236, y + 93, 21, (42, 102, 46))

        # Barrier hint lines where forest begins
        arcade.draw_line(self.path_left, 0, self.path_left, SCREEN_HEIGHT, (82, 60, 36), 3)
        arcade.draw_line(self.path_right, 0, self.path_right, SCREEN_HEIGHT, (82, 60, 36), 3)

    def _draw_player(self) -> None:
        left = self.player_x - self.player_width / 2
        right = self.player_x + self.player_width / 2
        bottom = self.player_y - self.player_height / 2
        top = self.player_y + self.player_height / 2

        # Shadow
        arcade.draw_ellipse_filled(
            self.player_x,
            bottom - 4,
            self.player_width * 0.9,
            10,
            (0, 0, 0, 70),
        )

        # Body
        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, (224, 210, 174))
        arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, (58, 45, 32), 2)

        # Shirt
        arcade.draw_lrbt_rectangle_filled(left + 4, right - 4, bottom + 8, bottom + 26, (58, 102, 152))

        # Headband / hair line
        arcade.draw_lrbt_rectangle_filled(left + 3, right - 3, top - 9, top - 3, (70, 52, 36))

    def _draw_ui(self) -> None:
        arcade.draw_text(
            "Gameplay Movement Test",
            20,
            SCREEN_HEIGHT - 34,
            arcade.color.WHITE,
            font_size=20,
            bold=True,
        )

        arcade.draw_text(
            "Move with WASD or arrow keys   |   ESC = return to menu",
            20,
            SCREEN_HEIGHT - 62,
            (226, 234, 226),
            font_size=14,
        )

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