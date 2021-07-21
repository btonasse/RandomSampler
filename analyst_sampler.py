import random
from datetime import date


class RandomAnalyst:
    '''
    The purpose of this class is to pick a "random" number of analysts every week,
    while making sure that the same analyst is not picked again until all analysts have been picked.
    This is achieved by calculating the elapsed time between the time of instantiation and an arbitrary root date
    and using this to generate a new fixed seed every time the list of analysts is exhausted.

    Usage:
    Instantiate this class with a list of analysts and a number of samples per week.
    To get a unique sample, call get_sample() on the instance

    Caveats:
    1) This functionality relies on the date at the time of instantiation to determine the seed of the list shuffler.
    2) It also assumes that the list of analysts is constant (analysts should be passed always in the same order).
    3) If an analyst is added or removed from the list, you might get unreliable results until the next fixed seed is generated.
    4) If the list of analysts is not a multiple of the number of weekly samples, there will be always someone left out. 
       There is no provision to put the left out analysts at the top of the next shuffle result. This can be implemented later...
    '''
    ROOT_DATE = date(2021, 4, 28)
    def __init__(self, analysts: list, samples_per_week: int):
        # The list of analysts to sample from
        self.analysts = analysts
        
        # How many analysts to pick every week
        self.samples_per_week = samples_per_week
        
        # How many weeks have to pass until all analysts have been picked once
        self.weeks_to_exhaust_samples = len(self.analysts) // self.samples_per_week
        
        # Elapsed time since ROOT_DATE
        self.elapsed_days = self._get_elapsed_days()
        
        # Shuffle the list of analysts
        self.seed = self._calculate_seed()
        random.seed(self.seed)
        self.shuffled_analysts = self.analysts.copy()
        random.shuffle(self.shuffled_analysts)


    def _get_elapsed_days(self) -> int:
        '''
        Get number of elapsed days since arbitrary ROOT_DATE
        '''
        root_date = self.ROOT_DATE
        today = date.today()
        delta = today - root_date
        return delta.days

    def _calculate_seed(self) -> int:
        '''
        Return a seed for shuffling the list of analysts.
        
        The seed is reset when the number of elapsed days is a multiple of the number of days it takes until all analysts have been picked once (self.weeks_to_exhaust_samples*7).
        If the elapsed days are a multiple of this number, reset the seed (equal to the number of elapsed days).
        Otherwise use the last number of elapsed days that was a multiple of self.weeks_to_exhaust_samples*7

        This guaranteed that the list of analysts will be shuffled in the same way until everyone has been picked once.
        '''
        days_since_seed_was_reset = self.elapsed_days % (self.weeks_to_exhaust_samples*7)
        last_seed = self.elapsed_days - days_since_seed_was_reset
        return last_seed

    def get_sample(self) -> list:
        '''
        Get a number of analysts from the shuffled list.
        The size of the sample is determined at instantiation (self.samples_per_week)
        Which analysts to pick is decided by how many days have elapsed since the seed was modified
        '''
        picked_analysts = []
        
        weeks_since_seed_was_reset = (self.elapsed_days//7) % self.weeks_to_exhaust_samples
        start_index = weeks_since_seed_was_reset * self.samples_per_week
        end_index = start_index + self.samples_per_week
        
        try:
            picked_analysts = self.shuffled_analysts[start_index:end_index]
        except IndexError:
            print(f'''Not enough analysts to pick. Variables:
            Weeks since seed was reset: {weeks_since_seed_was_reset}
            Start and end slice indices: {start_index}:{end_index}
            Length of analysts list: {len(self.analysts)}
            ''')

        return picked_analysts



if __name__ == '__main__':
    analysts = [n for n in range(7)]
    x = RandomAnalyst(analysts, 2)

    print(f'Elapsed days since arbitrary date: {x.elapsed_days}')
    print(f'Elapsed weeks since arbitrary date: {x.elapsed_days//7}')
    print(f'Weeks until all analysts are used: {x.weeks_to_exhaust_samples}')
    print(f'Seed is: {x.seed}')

    print(f'Analysts: {x.analysts}')
    print(f'Shuffled analysts: {x.shuffled_analysts}')

    print(f'Sample for this week: {x.get_sample()}')










