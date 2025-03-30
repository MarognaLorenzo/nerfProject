import time
import random
from olfactometer import Olfactometer

pre_block = 60
n_blocks =  6
n_concentrations = 5
n_aromas = 2
odor_exposure = 10
recovery = 10
vote = 10
after_block_rest = 120
sleep = False

elapsed_time = 0

def wait_time(seconds: int):
    global elapsed_time
    elapsed_time += seconds
    if sleep:
        time.sleep(seconds)

def main():
    n_combinations = (n_concentrations * n_aromas) + 1
    olfactometer = Olfactometer(["lavander", "bug"])

    for block in range(n_blocks):
        print(f"Block {block}")
        wait_time(pre_block)
        combinations = list(range(n_combinations))
        random.shuffle(combinations)
        for aroma in combinations:

            # Odor exposure
            olfactometer.activate(aroma)
            wait_time(odor_exposure)
            olfactometer.deactivate(aroma)

            # Recovery time
            wait_time(recovery)

            # The patients votes for validation
            wait_time(vote)

            # additional recovery
            final_recovery = random.randrange(10,20)
            wait_time(final_recovery)
        
        wait_time(after_block_rest)

    print(f"Total time: {elapsed_time/60} minutes")



if __name__ == "__main__":
    main()