from entities import Brick
from settings import BRICK_ROWS, BRICK_COLS


def build_bricks(layout):
    bricks = []
    for row_i, row in enumerate(layout):
        for col_i, hits in enumerate(row):
            if hits > 0:
                bricks.append(Brick(col_i, row_i, hits))
    return bricks


def level_1():
    """Wide-to-narrow pyramid: full top, narrowing each pair of rows."""
    L = []
    for row in range(BRICK_ROWS):
        margin = row // 2
        r = [0] * BRICK_COLS
        for col in range(margin, BRICK_COLS - margin):
            r[col] = 1
        L.append(r)
    return L


def level_2():
    """Checkerboard; top two rows are 2-hit."""
    L = []
    for row in range(BRICK_ROWS):
        r = []
        for col in range(BRICK_COLS):
            if (row + col) % 2 == 0:
                r.append(2 if row < 2 else 1)
            else:
                r.append(0)
        L.append(r)
    return L


def level_3():
    """Diamond centred on grid; top rows 3-hit, mid 2-hit, outer 1-hit."""
    L = [[0] * BRICK_COLS for _ in range(BRICK_ROWS)]
    cx = BRICK_COLS // 2
    cy = BRICK_ROWS // 2
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            dist = abs(row - cy) + abs(col - cx)
            if dist <= 4:
                if row < 2:
                    L[row][col] = 3
                elif row < 4:
                    L[row][col] = 2
                else:
                    L[row][col] = 1
    return L


def level_4():
    """Fortress: outer ring 3-hit, interior 2-hit."""
    L = []
    for row in range(BRICK_ROWS):
        r = []
        for col in range(BRICK_COLS):
            on_border = (row == 0 or row == BRICK_ROWS - 1
                         or col == 0 or col == BRICK_COLS - 1)
            r.append(3 if on_border else 2)
        L.append(r)
    return L


def level_5():
    """Full grid: top 2 rows 3-hit, middle 3 rows 2-hit, bottom 2 rows 1-hit."""
    L = []
    for row in range(BRICK_ROWS):
        hits = 3 if row < 2 else (2 if row < 5 else 1)
        L.append([hits] * BRICK_COLS)
    return L


LEVELS = [level_1, level_2, level_3, level_4, level_5]
