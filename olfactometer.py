from OlfSerial import OlfSerial
class Olfactometer(OlfSerial):
    def __init__(self, aromas, boards = None, use = True):
        """
        Initialize the Olfactometer class
        """
        self.good_smell = aromas[0]
        self.bad_smell = aromas[1]
        self.use = use
        super().__init__(port="/dev/tty.usbserial-FTWGRT8X")
        if boards:
            self.set_boards(boards)

    def activate(self, aroma):
        self.print_aroma(aroma)
        # BLUFF 
        if aroma == 0:
            return
        aroma += 1 + (aroma // 8)
        command = self.open_valve(aroma)
        if self.use:
            self.write(command)
        return
    
    def deactivate(self, aroma):
        # BLUFF 
        if aroma == 0:
            return
        command = self.open_valve(1 + (8* (aroma // 8)))
        if self.use:
            self.write(command)
        return

    def print_aroma(self, aroma):
        if aroma == 0: 
            print("\tbluff")
            return

        smell = ""
        if aroma <= 5:
            smell = self.good_smell
        else:
            smell = self.bad_smell
            aroma -= 5
        concentration = aroma/ 5
        print(f"\tAroma : {smell}, concentration = {100 * concentration}%")
        