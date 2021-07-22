# Todo scenarios: 1) leftovers 2) Change in analyst list between weeks (change in order and/or length of list)

from unittest import TestCase
import unittest
from analyst_sampler import RandomSampler
from datetime import date, timedelta

class TestNoLeftovers(TestCase):
    '''
    Test a scenario where the number of analysts is a multiple of number of samples per week .
    '''
    def setUp(self) -> None:
        # Generate dummy analysts list
        self.analysts = [n for n in range(8)]
        # Set number of samples per week
        self.samples_per_week = 2
        # Set default root_date
        self.default_root_date = date.today()
        # Instantiate RandomSampler
        self.sampler = RandomSampler(self.analysts, self.samples_per_week)


    def test_nine_consecutive_weeks(self):
        '''
        Simulate nine consecutive weekly runs to check if the seed reset is working as intended.
        '''
        # Print test parameters
        print((f'Setting up sampler test with following parameters:\n'
               f'Arbitrary root date: {self.default_root_date}\n'
               f'Samples per week: {self.samples_per_week}\n'
               f'Weeks until all analysts are used: {self.sampler.weeks_to_exhaust_samples}\n'
               f'Analysts: {self.analysts}'))
        
        # Variable to track which analysts have been picked already
        picked_analysts = []
        # Track previous seed
        previous_seed = 0
        
        separator = '*'*40
        for week in range(9):
            print('\n'+separator)
            print(f'Running sampler on week {week}...')
            
            # Decrement ROOT_DATE to simulate the sampler being run in different weeks
            delta = timedelta(days = week*7)
            self.sampler.ROOT_DATE = self.default_root_date - delta
            # Reinitialize instance so the new root_date is taken into account
            self.sampler.__init__(self.analysts, self.samples_per_week)
            # Get sample for the week
            sample = self.sampler.get_sample()
           
            # Print initialized variables
            print((f'Elapsed days since root date: {self.sampler.elapsed_days}\n'
                   f'Elapsed weeks since root date: {self.sampler.elapsed_days//7}\n'
                   f'Calculated seed: {self.sampler.seed}\n'
                   f'Shuffled analysts: {self.sampler.shuffled_analysts}\n'
                   f'Weekly sample: {sample}'))

            # Check if elapsed days calculated correctly
            self.assertEqual(self.sampler.elapsed_days, delta.days, msg=f'Expected elapsed days: {delta.days}.')
            # Check if an analyst is not being picked twice before the seed resets
            self.assertNotIn(sample, picked_analysts, msg=f'Sample {sample} has already been picked for seed {self.sampler.seed}.')
            # Check that seed only resets once all analysts have been picked
            if self.sampler.seed == previous_seed:
                self.assertTrue(len(picked_analysts) < len(self.sampler.shuffled_analysts), msg=f'Length of picked analysts must be smaller than total length of analysts.')
            else:
                self.assertTrue(len(picked_analysts) == len(self.sampler.shuffled_analysts), msg=f'Seed can only reset once everyone has been picked once.')
                # New seed must be a multiple of sampler.weeks_to_exhaust_samples
                self.assertTrue(self.sampler.seed % self.sampler.weeks_to_exhaust_samples == 0
                    , msg=f'Seed {self.sampler.seed} is not a multiple of {self.sampler.weeks_to_exhaust_samples}')
                # Reset picked_analysts since seed was reset
                picked_analysts = []
            
            # Add week's sample to picked_analysts
            picked_analysts.extend(sample)
            # Update previous_seed
            previous_seed = self.sampler.seed
            print(separator)

if __name__ == '__main__':
    unittest.main()





