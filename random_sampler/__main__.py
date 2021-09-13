from random_sampler import RandomSampler
import unittest
import argparse
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='random_sampler')
    testargs = parser.add_mutually_exclusive_group(required=True)
    testargs.add_argument('-d', '--demo', action='store_true', help='Run a quick demo and log results.')
    testargs.add_argument('-t', '--unittest', action='store_true', help='Run unittests for this module and log results.')
    args = parser.parse_args()

    if args.unittest:
        test_loader = unittest.TestLoader()
        test_result = unittest.TestResult()
        test_directory = str(Path(__file__).resolve().parent / 'tests')
        test_suite = test_loader.discover(test_directory, pattern='test_*.py')
        test_suite.run(result=test_result)

        if test_result.wasSuccessful():
            print("Test successful. See sampler_test.log for details.")
            exit(0)
        else:
            print("Test failed. See details below:")
            print(test_result.errors)
            exit(-1)
    
    else:
        elements = [n for n in range(7)]
        sample_size = 2
        sampler = RandomSampler(elements, sample_size)
        sample = sampler.get_sample()
        exit(0)
