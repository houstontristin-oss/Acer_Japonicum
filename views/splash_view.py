from __future__ import annotations

from pathlib import Path

import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from view_constants import (
    SPLASH_BACKGROUND_COLOR,
    SPLASH_BASE_FILL,
    SPLASH_DONE_HOLD_DURATION,
    SPLASH_FADE_IN_DURATION,
    SPLASH_FADE_OUT_DURATION,
    SPLASH_FRAME_BORDER_WIDTH,
    SPLASH_FRAME_CENTER_X,
    SPLASH_FRAME_CENTER_Y,
    SPLASH_FRAME_COLOR,
    SPLASH_FRAME_FILL,
    SPLASH_FRAME_HEIGHT,
    SPLASH_FRAME_WIDTH,
    SPLASH_HOLD_DURATION,
    SPLASH_LEAF_ALPHA,
    SPLASH_LEAF_MAX_SCALE,
    SPLASH_LEAF_MIN_SCALE,
    SPLASH_MASCOT_CENTER_X,
    SPLASH_MASCOT_CENTER_Y,
    SPLASH_MASCOT_HEIGHT,
    SPLASH_MASCOT_WIDTH,
    SPLASH_STUDIO_TEXT,
    SPLASH_TEXT_SIZE,
    SPLASH_TEXT_X,
    SPLASH_TEXT_Y,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHARACTER_IMAGE = PROJECT_ROOT / "assets" / "images" / "squishy_squinch.png"
FALLBACK_CHARACTER_IMAGE = PROJECT_ROOT / "assets" / "images" / "the_jiggler.jpg"
MAPLE_LEAF_IMAGE = PROJECT_ROOT / "assets" / "images" / "maple_leaf.jpg"


class SplashView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.phase = "fade_in"
        self.phase_time = 0.0

        self.fade_in_duration = SPLASH_FADE_IN_DURATION
        self.hold_duration = SPLASH_HOLD_DURATION
        self.fade_out_duration = SPLASH_FADE_OUT_DURATION
        self.done_hold_duration = SPLASH_DONE_HOLD_DURATION

        self.background_alpha = 0
        self.dev_tag_alpha = 0
        self.mascot_alpha = 0

        self.dev_text = arcade.Text(
            SPLASH_STUDIO_TEXT,
            SPLASH_TEXT_X,
            SPLASH_TEXT_Y,
            (255, 255, 255, self.dev_tag_alpha),
            font_size=SPLASH_TEXT_SIZE,
            anchor_x="center",
            anchor_y="center",
            bold=True,
            multiline=True,
            width=260,
            align="center",
        )

        self.mascot_texture = self._load_mascot_texture()
        self.leaf_texture = self._load_leaf_texture()

        self.background_sprite = None
        self.background_sprite_list = arcade.SpriteList()
        self.leaf_sprite_list = arcade.SpriteList()

        self._build_sprites()

        arcade.set_background_color(SPLASH_BACKGROUND_COLOR)

    def _load_mascot_texture(self) -> arcade.Texture | None:
        if CHARACTER_IMAGE.exists():
            return arcade.load_texture(CHARACTER_IMAGE)
        if FALLBACK_CHARACTER_IMAGE.exists():
            return arcade.load_texture(FALLBACK_CHARACTER_IMAGE)
        return None

    def _load_leaf_texture(self) -> arcade.Texture | None:
        if MAPLE_LEAF_IMAGE.exists():
            return arcade.load_texture(MAPLE_LEAF_IMAGE)
        return None

    def _build_sprites(self) -> None:
        if self.mascot_texture:
            tex_w = self.mascot_texture.width
            tex_h = self.mascot_texture.height

            self.background_sprite = arcade.Sprite()
            self.background_sprite.texture = self.mascot_texture
            self.background_sprite.center_x = SPLASH_MASCOT_CENTER_X
            self.background_sprite.center_y = SPLASH_MASCOT_CENTER_Y
            self.background_sprite.scale = min(
                SPLASH_MASCOT_WIDTH / tex_w,
                SPLASH_MASCOT_HEIGHT / tex_h,
            )
            self.background_sprite.alpha = self.mascot_alpha
            self.background_sprite_list.append(self.background_sprite)

        if self.leaf_texture:
            self._build_leaf_sprites()

    def _build_leaf_sprites(self) -> None:
        placements = [
            (120, 735, 0.07, -124),
            (240, 635, 0.06, 18),
            (365, 725, 0.055, -30),
            (520, 615, 0.065, 26),
            (675, 735, 0.06, -10),
            (1230, 820, 0.065, 128),
            (1100, 615, 0.055, -18),
            (770, 615, 0.055, -218),
            (760, 415, 0.055, -18),
            (945, 735, 0.06, 12),
            (85, 135, 0.065, 22),
            (235, 230, 0.055, -14),
            (395, 820, 0.06, 68),
            (555, 400, 0.055, -26),
            (1180, 130, 0.065, 116),
            (1305, 245, 0.055, -12),
            (1065, 190, 0.06, 40),
            (800, 110, 0.05, -201),
        ]

        for center_x, center_y, scale, angle in placements:
            leaf = arcade.Sprite()
            leaf.texture = self.leaf_texture
            leaf.center_x = center_x
            leaf.center_y = center_y
            leaf.scale = max(SPLASH_LEAF_MIN_SCALE, min(scale, SPLASH_LEAF_MAX_SCALE))
            leaf.angle = angle
            leaf.alpha = 0
            self.leaf_sprite_list.append(leaf)

    def on_show_view(self) -> None:
        arcade.set_background_color(SPLASH_BACKGROUND_COLOR)

    def on_update(self, delta_time: float) -> None:
        self.phase_time += delta_time

        if self.phase == "fade_in":
            progress = min(self.phase_time / self.fade_in_duration, 1.0)
            alpha = int(255 * progress)

            self.background_alpha = alpha
            self.dev_tag_alpha = alpha
            self.mascot_alpha = alpha

            if progress >= 1.0:
                self.phase = "hold"
                self.phase_time = 0.0

        elif self.phase == "hold":
            self.background_alpha = 255
            self.dev_tag_alpha = 255
            self.mascot_alpha = 255

            if self.phase_time >= self.hold_duration:
                self.phase = "fade_out_tag"
                self.phase_time = 0.0

        elif self.phase == "fade_out_tag":
            progress = min(self.phase_time / self.fade_out_duration, 1.0)
            fade_alpha = int(255 * (1.0 - progress))

            self.background_alpha = 255
            self.dev_tag_alpha = fade_alpha
            self.mascot_alpha = fade_alpha

            if progress >= 1.0:
                self.phase = "done"
                self.phase_time = 0.0

        elif self.phase == "done":
            self.background_alpha = 255
            self.dev_tag_alpha = 0
            self.mascot_alpha = 0

            if self.phase_time >= self.done_hold_duration:
                from views.title_menu_view import TitleMenuView
                self.window.show_view(TitleMenuView())

        if self.background_sprite:
            self.background_sprite.alpha = self.mascot_alpha

        leaf_alpha = min(self.background_alpha, SPLASH_LEAF_ALPHA)
        for leaf in self.leaf_sprite_list:
            leaf.alpha = leaf_alpha

    def on_draw(self) -> None:
        self.clear()
        self._draw_background()
        self._draw_leaf_sprites()
        self._draw_mascot_frame()
        self._draw_dev_text()

    def _draw_background(self) -> None:
        arcade.draw_lrbt_rectangle_filled(
            0,
            SCREEN_WIDTH,
            0,
            SCREEN_HEIGHT,
            SPLASH_BASE_FILL,
        )

    def _draw_leaf_sprites(self) -> None:
        if len(self.leaf_sprite_list) > 0:
            self.leaf_sprite_list.draw()

        if len(self.background_sprite_list) > 0:
            self.background_sprite_list.draw()

    def _draw_mascot_frame(self) -> None:
        if self.mascot_alpha <= 0:
            return

        left = SPLASH_FRAME_CENTER_X - SPLASH_FRAME_WIDTH / 2
        right = SPLASH_FRAME_CENTER_X + SPLASH_FRAME_WIDTH / 2
        bottom = SPLASH_FRAME_CENTER_Y - SPLASH_FRAME_HEIGHT / 2
        top = SPLASH_FRAME_CENTER_Y + SPLASH_FRAME_HEIGHT / 2

        arcade.draw_lrbt_rectangle_filled(
            left,
            right,
            bottom,
            top,
            (*SPLASH_FRAME_FILL, min(self.mascot_alpha, 45)),
        )
        arcade.draw_lrbt_rectangle_outline(
            left,
            right,
            bottom,
            top,
            (*SPLASH_FRAME_COLOR, self.mascot_alpha),
            SPLASH_FRAME_BORDER_WIDTH,
        )

    def _draw_dev_text(self) -> None:
        if self.dev_tag_alpha <= 0:
            return

        self.dev_text.color = (255, 255, 255, self.dev_tag_alpha)
        self.dev_text.draw()