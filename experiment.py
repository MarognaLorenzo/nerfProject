import time
import random
from Olfactometer import Olfactometer
import sys
import helpers
import asyncio


elapsed_time = 0

def wait_time(seconds: int, mess: str = None, sleep = True):
    if mess is not None:
        print(f'\t{mess}')
    global elapsed_time
    elapsed_time += seconds
    if sleep:
        time.sleep(seconds)

async def countdown(seconds):
    for i in range(seconds):
        print(f"Countdown: {i+1}")
        await asyncio.sleep(1)


def main(h):
    n_combinations = (h.n_concentrations * h.n_aromas) + 1
    olfactometer = Olfactometer(aromas=h.aromas, boards = h.boards, port= h.port, use = h.use)

    for block in range(h.n_blocks):
        print(f"Block {block}")
        wait_time(h.pre_block, sleep=h.sleep)
        combinations = list(range(n_combinations))
        # random.shuffle(combinations)

        for aroma in combinations:
            print("\t-------------------------")

            # Odor exposure
            olfactometer.activate(aroma)

            wait_time(h.odor_exposure, f"odor exposure with aroma: {aroma}", h.sleep)
            olfactometer.deactivate(aroma)

            # Recovery time
            wait_time(h.recovery, "recovery", h.sleep)

            # The patients votes for validation
            wait_time(h.vote, "vote", h.sleep)

            # additional recovery
            final_recovery = random.randrange(h.final_recovery_min, h.final_recovery_max)
            wait_time(final_recovery, "final recovery", h.sleep)
        
        wait_time(h.after_block_rest, "end block")

    print(f"Total time: {elapsed_time/60} minutes")

if __name__ == "__main__":
    assert len(sys.argv) > 1, "Please pass the configuration file to the script."
    hparams = helpers.parse_configuration_yaml(sys.argv[1])
    main(hparams)