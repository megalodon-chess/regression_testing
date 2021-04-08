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

import sys
import time
import random
import chess
import chess.engine

NUM_GAMES = 64
RAND_MOVES = 3
TIME_CONTROL = (90, 0)


def test(base_path, new_path):
    score = 0
    games = 0

    while games < NUM_GAMES:
        sys.stdout.write(f"Game {games+1}: ")
        sys.stdout.flush()

        board = chess.Board()
        side = random.random() > 0.5
        if side:
            white = chess.engine.SimpleEngine.popen_uci(new_path)
            black = chess.engine.SimpleEngine.popen_uci(base_path)
        else:
            white = chess.engine.SimpleEngine.popen_uci(base_path)
            black = chess.engine.SimpleEngine.popen_uci(new_path)
        for i in range(RAND_MOVES):
            board.push(random.choice(list(board.generate_legal_moves())))

        wtime = TIME_CONTROL[0]
        btime = TIME_CONTROL[0]
        inc = TIME_CONTROL[1]
        while True:
            try:
                limit = chess.engine.Limit(white_clock=wtime, black_clock=btime, white_inc=inc, black_inc=inc)
                start = time.time()
                if board.turn:
                    board.push(white.play(board, limit).move)
                else:
                    board.push(black.play(board, limit).move)
                elapse = time.time() - start
                if board.turn:
                    wtime -= elapse
                    wtime += inc
                else:
                    btime -= elapse
                    btime += inc

                if board.is_game_over():
                    result = board.result()
                    break

            except chess.engine.EngineError:
                result = "ERROR"
                break

        print(f"Result is {result}")
        sys.stdout.flush()

        if side:
            if result == "1-0":
                score += 1
            elif result == "0-1":
                score -= 1
        games += 1
        white.quit()
        black.quit()

    return (games, score)
