import arcade


class Player:
    def __init__(
        self,
        center_x: float,
        center_y: float,
        width: float = 36,
        height: float = 48,
        speed: float = 260,
    ) -> None:
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.speed = speed

    @property
    def half_width(self) -> float:
        return self.width / 2

    @property
    def half_height(self) -> float:
        return self.height / 2

    @property
    def left(self) -> float:
        return self.center_x - self.half_width

    @property
    def right(self) -> float:
        return self.center_x + self.half_width

    @property
    def bottom(self) -> float:
        return self.center_y - self.half_height

    @property
    def top(self) -> float:
        return self.center_y + self.half_height

    def move(self, dx: float, dy: float, delta_time: float) -> None:
        self.center_x += dx * self.speed * delta_time
        self.center_y += dy * self.speed * delta_time

    def clamp_to_bounds(self, left: float, right: float, bottom: float, top: float) -> None:
        min_x = left + self.half_width
        max_x = right - self.half_width
        min_y = bottom + self.half_height
        max_y = top - self.half_height

        self.center_x = max(min_x, min(self.center_x, max_x))
        self.center_y = max(min_y, min(self.center_y, max_y))

    def draw(self) -> None:
        left = self.left
        right = self.right
        bottom = self.bottom
        top = self.top

        arcade.draw_ellipse_filled(
            self.center_x,
            bottom - 4,
            self.width * 0.9,
            10,
            (0, 0, 0, 70),
        )

        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, (224, 210, 174))
        arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, (58, 45, 32), 2)

        arcade.draw_lrbt_rectangle_filled(left + 4, right - 4, bottom + 8, bottom + 26, (58, 102, 152))
        arcade.draw_lrbt_rectangle_filled(left + 3, right - 3, top - 9, top - 3, (70, 52, 36))