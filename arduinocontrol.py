from pyfirmata import Arduino, util
from pyfirmata import SERVO


board = Arduino('COM7')

iterator = util.Iterator(board)
iterator.start()

board.digital[10].mode = SERVO

board.digital[10].write(105)
