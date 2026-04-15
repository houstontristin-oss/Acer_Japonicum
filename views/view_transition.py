from __future__ import annotations

import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class ViewTransitionMixin:
    def _setup_transition_system(self) -> None:
        self.is_transitioning = False
        self.transition_phase = "idle"
        self.transition_alpha = 0
        self.transition_speed = 320
        self.pending_view_class = None
        self.pending_spawn_key = None

        self.fade_overlay = arcade.SpriteSolidColor(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            (0, 0, 0, 0),
        )
        self.fade_overlay.center_x = SCREEN_WIDTH / 2
        self.fade_overlay.center_y = SCREEN_HEIGHT / 2
        self.fade_overlay_list = arcade.SpriteList()
        self.fade_overlay_list.append(self.fade_overlay)

    def begin_transition(self, next_view_class, spawn_key: str) -> None:
        if self.is_transitioning:
            return

        self.is_transitioning = True
        self.transition_phase = "fade_out"
        self.pending_view_class = next_view_class
        self.pending_spawn_key = spawn_key

    def update_transition(self, delta_time: float) -> None:
        if not self.is_transitioning:
            return

        fade_step = int(self.transition_speed * delta_time)

        if self.transition_phase == "fade_out":
            self.transition_alpha = min(255, self.transition_alpha + fade_step)
            self.fade_overlay.alpha = self.transition_alpha

            if self.transition_alpha >= 255:
                self._finish_transition()

    def _finish_transition(self) -> None:
        if self.pending_view_class is None:
            self._reset_transition()
            return

        next_view = self.pending_view_class(spawn_key=self.pending_spawn_key)
        self.window.show_view(next_view)

    def _reset_transition(self) -> None:
        self.is_transitioning = False
        self.transition_phase = "idle"
        self.transition_alpha = 0
        self.fade_overlay.alpha = 0
        self.pending_view_class = None
        self.pending_spawn_key = None

    def draw_transition(self) -> None:
        if self.transition_alpha <= 0:
            return

        self.window.default_camera.use()
        self.fade_overlay_list.draw()