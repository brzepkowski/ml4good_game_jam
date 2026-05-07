from entities import Brick

# Layout cells: 0 = empty, or a key from BRICK_DEFS
# Good bricks (must destroy all to win): 'SPD', 'WID', 'VPAD'
# Bad bricks  (cause effects when hit):  '+1', 'MA', 'GH'

_ = 0  # shorthand for empty cell


def build_bricks(layout):
    bricks = []
    for row_i, row in enumerate(layout):
        for col_i, cell in enumerate(row):
            if cell != 0:
                bricks.append(Brick(col_i, row_i, cell))
    return bricks


def level_1():
    """Foundation — mostly good bricks, light bad-brick resistance."""
    return [
        ['SPD','SPD','SPD','SPD','SPD','SPD','SPD','SPD','SPD','SPD'],
        ['WID','WID','WID','WID','WID','WID','WID','WID','WID','WID'],
        [ '+1',  _,  '+1',  _,  'MA',  _,  'GH',  _,  '+1',  _  ],
        [  _,  'GH',  _,  'GH',  _,  'GH',  _,  'GH',  _,  'GH' ],
        [  _,    _,    _,    _,    _,    _,    _,    _,    _,    _ ],
        [  _,    _,    _,    _,    _,    _,    _,    _,    _,    _ ],
        [  _,    _,    _,    _,    _,    _,    _,    _,    _,    _ ],
    ]


def level_2():
    """Interleaved — good and bad bricks alternate, first VPAD appears."""
    return [
        ['+1','SPD','+1','SPD','+1','SPD','+1','SPD','+1','SPD'],
        ['WID','MA','WID','MA','WID','MA','WID','MA','WID','MA'],
        ['GH','WID','GH','WID','GH','WID','GH','WID','GH','WID'],
        ['SPD','GH','SPD','GH','VPAD','GH','SPD','GH','SPD','GH'],
        ['+1','+1','+1','+1','+1','+1','+1','+1','+1','+1'],
        [  _,    _,    _,    _,    _,    _,    _,    _,    _,   _],
        [  _,    _,    _,    _,    _,    _,    _,    _,    _,   _],
    ]


def level_3():
    """Fortress — good bricks ringed by a wall of bad GH bricks."""
    return [
        ['GH','GH','GH','GH','GH','GH','GH','GH','GH','GH'],
        ['GH','SPD','SPD','SPD','VPAD','VPAD','SPD','SPD','SPD','GH'],
        ['GH','SPD','WID','WID','WID','WID','WID','WID','SPD','GH'],
        ['GH','SPD','WID','+1','MA','MA','+1','WID','SPD','GH'],
        ['GH','SPD','WID','WID','WID','WID','WID','WID','SPD','GH'],
        ['GH','SPD','SPD','SPD','SPD','SPD','SPD','SPD','SPD','GH'],
        ['GH','GH','GH','GH','GH','GH','GH','GH','GH','GH'],
    ]


def level_4():
    """Chaos — dense mix; good bricks scattered throughout."""
    return [
        ['MA','+1','GH','MA','+1','GH','MA','+1','GH','MA'],
        ['+1','SPD','MA','WID','GH','SPD','+1','WID','MA','GH'],
        ['GH','MA','SPD','+1','SPD','MA','WID','GH','SPD','+1'],
        ['MA','WID','GH','SPD','VPAD','GH','+1','SPD','WID','MA'],
        ['+1','GH','MA','WID','MA','SPD','GH','MA','+1','GH'],
        ['SPD','+1','GH','MA','SPD','+1','SPD','GH','MA','WID'],
        ['MA','MA','+1','+1','GH','GH','MA','MA','+1','+1'],
    ]


def level_5():
    """Final alignment — a handful of good bricks buried under a storm of bad."""
    return [
        ['MA','+1','MA','+1','MA','+1','MA','+1','MA','+1'],
        ['+1','MA','GH','MA','GH','MA','GH','MA','GH','MA'],
        ['GH','GH','SPD','GH','GH','GH','GH','SPD','GH','GH'],
        ['+1','MA','GH','WID','VPAD','VPAD','WID','GH','MA','+1'],
        ['GH','GH','SPD','GH','GH','GH','GH','SPD','GH','GH'],
        ['+1','MA','GH','MA','GH','MA','GH','MA','GH','MA'],
        ['MA','+1','MA','+1','MA','+1','MA','+1','MA','+1'],
    ]


LEVELS = [level_1, level_2, level_3, level_4, level_5]
