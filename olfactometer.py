class Olfactometer:
    def __init__(self, aromas):
        """
        Initialize the Olfactometer class
        """
        self.good_smell = aromas[0]
        self.bad_smell = aromas[1]

    def activate(self, aroma):
        self.print_aroma(aroma)
        return
    
    def deactivate(self, aroma):
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
        concentration = aroma / 5
        print(f"\tAroma : {smell}, concentration = {100 * concentration}%")
        