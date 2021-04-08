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

import os
import shutil
import time
from datetime import datetime
from elo import test as play_games
from image import image as create_image

PARENT = os.path.dirname(os.path.realpath(__file__))
BASE_PATH = os.path.join(PARENT, "Megalodon_base")
TEST_PATH = os.path.join(PARENT, "Megalodon_build")
REPO_PATH = os.path.join(PARENT, "megalodon")
INC = 8 * 3600  # Seconds


def main():
    while True:
        date = datetime.now().strftime("%m-%d-%Y %P-%M-%S %p")
        print(f"Starting regression test at time {date}.")

        print("Building latest Megalodon...")
        if not os.path.isdir(REPO_PATH):
            os.system(f"git clone https://github.com/megalodon-chess/megalodon.git {REPO_PATH}")
        os.chdir(REPO_PATH)
        os.system("git pull")
        os.system("./build.sh")
        shutil.copy(os.path.join(REPO_PATH, "build", "Megalodon"), TEST_PATH)

        time.sleep(INC)


main()
