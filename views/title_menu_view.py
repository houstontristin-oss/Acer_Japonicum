from __future__ import annotations

import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from view_constants import (
    MENU_BUTTON_ANIM_DURATION,
    MENU_BUTTON_GAP,
    MENU_BUTTON_HEIGHT,
    MENU_BUTTON_STAGGER,
    MENU_BUTTON_START_SCALE,
    MENU_BUTTON_WIDTH,
    MENU_PANEL_HEIGHT,
    MENU_PANEL_SLIDE_DURATION,
    MENU_PANEL_START_Y,
    MENU_PANEL_WIDTH,
    TITLE_BACKGROUND_COLOR,
    TITLE_BG_BOTTOM_BAND,
    TITLE_BG_FILL,
)
from views.gameplay_view import GameplayView
from views.load_view import LoadView
from views.settings_view import SettingsView


class MenuButton:
    def __init__(self, label: str, center_x: float, center_y: float, width: float, height: float):
        self.label = label
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height

        self.visible = False
        self.alpha = 0
        self.scale = MENU_BUTTON_START_SCALE

    @property
    def left(self) -> float:
        return self.center_x - (self.width * self.scale) / 2

    @property
    def right(self) -> float:
        return self.center_x + (self.width * self.scale) / 2

    @property
    def bottom(self) -> float:
        return self.center_y - (self.height * self.scale) / 2

    @property
    def top(self) -> float:
        return self.center_y + (self.height * self.scale) / 2

    def contains_point(self, x: float, y: float) -> bool:
        if not self.visible:
            return False
        return self.left <= x <= self.right and self.bottom <= y <= self.top

    def draw(self) -> None:
        if not self.visible:
            return

        fill = (28, 34, 40, self.alpha)
        border = (170, 215, 198, self.alpha)
        text_color = (235, 244, 237, self.alpha)

        arcade.draw_lrbt_rectangle_filled(self.left, self.right, self.bottom, self.top, fill)
        arcade.draw_lrbt_rectangle_outline(self.left, self.right, self.bottom, self.top, border, 3)

        arcade.draw_text(
            self.label,
            self.center_x,
            self.center_y,
            text_color,
            font_size=18,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )


class TitleMenuView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.panel_width = MENU_PANEL_WIDTH
        self.panel_height = MENU_PANEL_HEIGHT

        self.panel_target_y = SCREEN_HEIGHT / 2
        self.panel_y = MENU_PANEL_START_Y
        self.panel_slide_duration = MENU_PANEL_SLIDE_DURATION
        self.panel_time = 0.0
        self.panel_finished = False

        self.button_stagger = MENU_BUTTON_STAGGER
        self.button_anim_duration = MENU_BUTTON_ANIM_DURATION
        self.button_time = 0.0

        center_x = SCREEN_WIDTH / 2
        base_y = SCREEN_HEIGHT / 2 - 35
        gap = MENU_BUTTON_GAP

        self.buttons = [
            MenuButton("Play", center_x, base_y + gap, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT),
            MenuButton("Load", center_x, base_y, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT),
            MenuButton("Settings", center_x, base_y - gap, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT),
            MenuButton("Quit", center_x, base_y - gap * 2, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT),
        ]

        arcade.set_background_color(TITLE_BACKGROUND_COLOR)

    def on_show_view(self) -> None:
        arcade.set_background_color(TITLE_BACKGROUND_COLOR)

    def on_update(self, delta_time: float) -> None:
        if not self.panel_finished:
            self.panel_time += delta_time
            progress = min(self.panel_time / self.panel_slide_duration, 1.0)

            eased = 1 - (1 - progress) ** 3
            self.panel_y = MENU_PANEL_START_Y + (self.panel_target_y - MENU_PANEL_START_Y) * eased

            if progress >= 1.0:
                self.panel_y = self.panel_target_y
                self.panel_finished = True
                self.button_time = 0.0
        else:
            self.button_time += delta_time
            self._update_button_reveals()

    def _update_button_reveals(self) -> None:
        for i, button in enumerate(self.buttons):
            start_time = i * self.button_stagger
            end_time = start_time + self.button_anim_duration

            if self.button_time >= start_time:
                button.visible = True

                progress = min(max((self.button_time - start_time) / self.button_anim_duration, 0.0), 1.0)
                eased = 1 - (1 - progress) ** 3

                button.alpha = int(255 * eased)
                button.scale = MENU_BUTTON_START_SCALE + (1.0 - MENU_BUTTON_START_SCALE) * eased

                if self.button_time >= end_time:
                    button.alpha = 255
                    button.scale = 1.0

    def on_draw(self) -> None:
        self.clear()
        self._draw_background()
        self._draw_menu_panel()

    def _draw_background(self) -> None:
        arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, TITLE_BG_FILL)
        arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT * 0.24, TITLE_BG_BOTTOM_BAND)

        arcade.draw_text(
            "The Maju Mellenia",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 110,
            arcade.color.WHITE,
            font_size=48,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_text(
            "Your call to action is now",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 150,
            (190, 215, 205),
            font_size=15,
            anchor_x="center",
        )

    def _draw_menu_panel(self) -> None:
        center_x = SCREEN_WIDTH / 2
        left = center_x - self.panel_width / 2
        right = center_x + self.panel_width / 2
        bottom = self.panel_y - self.panel_height / 2
        top = self.panel_y + self.panel_height / 2

        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, (18, 22, 28))
        arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, (166, 214, 195), 3)

        arcade.draw_text(
            "Main Menu",
            center_x,
            top - 42,
            (235, 244, 237),
            font_size=24,
            anchor_x="center",
            bold=True,
        )

        for button in self.buttons:
            button.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        for menu_button in self.buttons:
            if menu_button.contains_point(x, y):
                self._handle_button(menu_button.label)
                break

    def _handle_button(self, label: str) -> None:
        if label == "Play":
            self.window.show_view(GameplayView())
        elif label == "Load":
            self.window.show_view(LoadView())
        elif label == "Settings":
            self.window.show_view(SettingsView())
        elif label == "Quit":
            arcade.exit()