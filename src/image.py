#
#  Regression Testing
#  Scripts to run continuously to test ELO performance quarter-daily.
#  Copyright Megalodon Chess 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import pygame
pygame.init()

WIDTH, HEIGHT = 1920, 1080

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (60, 60, 220)


def image(results, path):
    image = pygame.Surface((WIDTH, HEIGHT))
    image.fill(WHITE)
    results = sorted(results, key=lambda x: x[1])
    font = pygame.font.SysFont("ubuntu", 36)

    # Axes and title
    pygame.draw.line(image, BLACK, (30, 30), (30, HEIGHT-20))
    pygame.draw.line(image, BLACK, (20, HEIGHT-30), (WIDTH-30, HEIGHT-30))
    text = font.render("Build vs v0.3.0", 1, BLACK)
    image.blit(text, (WIDTH/2 - text.get_width()/2, 25))

    # Lines
    x_start = 30
    y_start = HEIGHT - 30
    x_size = WIDTH - 60
    y_size = HEIGHT - 60
    x_step = x_size / (len(results)-1)

    max_y = max(results, key=lambda x: x[0])[0] + 10
    min_y = min(results, key=lambda x: x[0])[0] - 10

    prev_y = None
    prev_x = None
    for i, (elo, seconds, date) in enumerate(results):
        x = i*x_step + x_start
        y = (elo-min_y) / (max_y-min_y) * y_size
        y = y_start - y

        pygame.draw.circle(image, BLUE, (x, y), 3)
        if prev_y is not None:
            pygame.draw.line(image, BLUE, (prev_x, prev_y), (x, y))

        prev_x = x
        prev_y = y

    pygame.image.save(image, path)
