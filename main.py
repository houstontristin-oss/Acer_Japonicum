"""
What Python is good at here
Python is good for:

2D sprite rendering
title screens and menus
fades, timers, tween-like animations
tile maps and camera movement
dialogue, UI, inventory, quests
turn-based combat
building a playable prototype fast

Where Python gets weaker is if you later try to make:
massive 3D worlds
very heavy real-time physics
giant performance-hungry particle systems
console-grade optimization
 """

import arcade

from views.splash_view import SplashView
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


def main() -> None:
    window = arcade.Window(
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        title=SCREEN_TITLE,
        update_rate=1 / 60,
        resizable=False,
    )
    window.show_view(SplashView())
    arcade.run()


if __name__ == "__main__":
    main()

    """
    Must add maple_leaf and background sprite to the list of sprites
     line 176, in on_draw
    self._draw_background()
    line 183, in _draw_background
    self.menu_background_sprite.draw()
    
    """
