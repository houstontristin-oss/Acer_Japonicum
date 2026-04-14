import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class GameCamera:
    def __init__(self) -> None:
        self.camera = arcade.Camera2D()

    def follow(self, target_x: float, target_y: float, world_width: float, world_height: float) -> None:
        half_screen_w = SCREEN_WIDTH / 2
        half_screen_h = SCREEN_HEIGHT / 2

        camera_x = max(half_screen_w, min(target_x, world_width - half_screen_w))
        camera_y = max(half_screen_h, min(target_y, world_height - half_screen_h))

        self.camera.position = (camera_x, camera_y)

    def use(self) -> None:
        self.camera.use()