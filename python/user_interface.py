import logic
import matplotlib.pyplot as plot

def askForNumber(messageText):
    """
    Asks user for a number and keeps trying until the input can be parsed to a number.

    Joe.
    :param messageText:
    :return:
    """

    while True:
        try:
            _readNumber = int(raw_input(messageText))
            break
        except ValueError:
            print "ERROR: insert a valid number!"

    return _readNumber


# Presents the program to the user
print "\n" \
      "****************************************************\n" \
      "*                                                  *\n" \
      "*  DUAL CHANNEL IMPULSE RESPONSE MEASURING SYSTEM  *\n" \
      "*  MSc. Acoustics and Audio Technology - AAU 2015  *\n" \
      "*                                                  *\n" \
      "****************************************************\n\n"

myIR = logic.executeMeasurement(32768,44100,0.5,0.25,5.0)
plot.plot(myIR)
plot.show()
