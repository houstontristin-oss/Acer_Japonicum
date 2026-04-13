from __future__ import annotations

from pathlib import Path

import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from view_constants import (
    SPLASH_BACKGROUND_COLOR,
    SPLASH_BASE_FILL,
    SPLASH_BOTTOM_TINT,
    SPLASH_DONE_HOLD_DURATION,
    SPLASH_FADE_IN_DURATION,
    SPLASH_FADE_OUT_DURATION,
    SPLASH_FRAME_COLOR,
    SPLASH_FRAME_FILL,
    SPLASH_HOLD_DURATION,
    SPLASH_MASCOT_BOX_SIZE,
    SPLASH_MASCOT_FRAME_PADDING,
    SPLASH_TEXT_SIZE,
    SPLASH_TEXT_Y,
    SPLASH_TOP_TINT,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHARACTER_IMAGE = PROJECT_ROOT / "assets" / "images" / "squishy_squinch.png"
FALLBACK_CHARACTER_IMAGE = PROJECT_ROOT / "assets" / "images" / "the_jiggler.jpg"


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

        self.mascot_texture = self._load_mascot_texture()
        self.background_sprite = None
        self.background_sprite_list = arcade.SpriteList()

        self._build_sprites()

        arcade.set_background_color(SPLASH_BACKGROUND_COLOR)

    def _load_mascot_texture(self) -> arcade.Texture | None:
        if CHARACTER_IMAGE.exists():
            return arcade.load_texture(CHARACTER_IMAGE)
        if FALLBACK_CHARACTER_IMAGE.exists():
            return arcade.load_texture(FALLBACK_CHARACTER_IMAGE)
        return None

    def _build_sprites(self) -> None:
        if not self.mascot_texture:
            return

        tex_w = self.mascot_texture.width
        tex_h = self.mascot_texture.height

        self.background_sprite = arcade.Sprite()
        self.background_sprite.texture = self.mascot_texture
        self.background_sprite.center_x = SCREEN_WIDTH / 2
        self.background_sprite.center_y = SCREEN_HEIGHT / 2 - 10
        self.background_sprite.scale = min(SPLASH_MASCOT_BOX_SIZE / tex_w, SPLASH_MASCOT_BOX_SIZE / tex_h)
        self.background_sprite.alpha = self.background_alpha
        self.background_sprite_list.append(self.background_sprite)

    def on_show_view(self) -> None:
        arcade.set_background_color(SPLASH_BACKGROUND_COLOR)

    def on_update(self, delta_time: float) -> None:
        self.phase_time += delta_time

        if self.phase == "fade_in":
            progress = min(self.phase_time / self.fade_in_duration, 1.0)
            alpha = int(255 * progress)

            self.background_alpha = alpha
            self.dev_tag_alpha = alpha

            if progress >= 1.0:
                self.phase = "hold"
                self.phase_time = 0.0

        elif self.phase == "hold":
            self.background_alpha = 255
            self.dev_tag_alpha = 255

            if self.phase_time >= self.hold_duration:
                self.phase = "fade_out_tag"
                self.phase_time = 0.0

        elif self.phase == "fade_out_tag":
            progress = min(self.phase_time / self.fade_out_duration, 1.0)
            self.background_alpha = 255
            self.dev_tag_alpha = int(255 * (1.0 - progress))

            if progress >= 1.0:
                self.phase = "done"
                self.phase_time = 0.0

        elif self.phase == "done":
            self.background_alpha = 255
            self.dev_tag_alpha = 0

            if self.phase_time >= self.done_hold_duration:
                from views.title_menu_view import TitleMenuView
                self.window.show_view(TitleMenuView())

        if self.background_sprite:
            self.background_sprite.alpha = self.background_alpha

    def on_draw(self) -> None:
        self.clear()
        self._draw_background()
        self._draw_mascot_frame()
        self._draw_dev_text()

    def _draw_background(self) -> None:
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
            SPLASH_BASE_FILL
        )

        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, SCREEN_HEIGHT * 0.45, SCREEN_HEIGHT,
            (*SPLASH_TOP_TINT, min(self.background_alpha, 110))
        )

        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT * 0.22,
            (*SPLASH_BOTTOM_TINT, min(self.background_alpha, 120))
        )

        if len(self.background_sprite_list) > 0:
            self.background_sprite_list.draw()

    def _draw_mascot_frame(self) -> None:
        if not self.background_sprite or self.background_alpha <= 0:
            return

        sprite = self.background_sprite
        padding = SPLASH_MASCOT_FRAME_PADDING

        left = sprite.left - padding
        right = sprite.right + padding
        bottom = sprite.bottom - padding
        top = sprite.top + padding

        arcade.draw_lrbt_rectangle_filled(
            left, right, bottom, top,
            (*SPLASH_FRAME_FILL, min(self.background_alpha, 45))
        )
        arcade.draw_lrbt_rectangle_outline(
            left, right, bottom, top,
            (*SPLASH_FRAME_COLOR, self.background_alpha),
            3
        )

    def _draw_dev_text(self) -> None:
        if self.dev_tag_alpha <= 0:
            return

        arcade.draw_text(
            "BAYAZ STUDIOS",
            SCREEN_WIDTH / 2,
            SPLASH_TEXT_Y,
            (255, 255, 255, self.dev_tag_alpha),
            font_size=SPLASH_TEXT_SIZE,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )