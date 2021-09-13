from random_sampler import RandomSampler
import unittest
import argparse
from pathlib import Path

def sample_from_file(args: argparse.Namespace) -> list:
    with args.file as file:
        elements = file.read().splitlines()
    sampler = RandomSampler(elements, args.samples)
    sample = sampler.get_sample()
    print(f"This week's sample: {sample}. For more details, see sampler.log")
    return sample

def run_tests(args: argparse.Namespace) -> unittest.TestResult:
    test_loader = unittest.TestLoader()
    test_result = unittest.TestResult()
    test_directory = str(Path(__file__).resolve().parent / 'tests')
    test_suite = test_loader.discover(test_directory, pattern='test_*.py')
    test_suite.run(result=test_result)

    if test_result.wasSuccessful():
        print("Test successful. See sampler_test.log for details.")
    else:
        print("Test failed. See details below:")
        print(test_result.errors)
    return test_result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='random_sampler')
    subparsers = parser.add_subparsers(dest='command', required=True)

    parser_file = subparsers.add_parser('fromfile', help='Get sample of a list of elements loaded from a file.')
    parser_file.add_argument('file', type=argparse.FileType('r', encoding='utf-8'), help='Filename containing list of elements to sample from, one per line.')
    parser_file.add_argument('samples', type=int, help='Number of samples per week.')
    parser_file.set_defaults(func=sample_from_file)
        
    parser_test = subparsers.add_parser('runtest', help='Run unittests for this module and log results.')
    parser_test.set_defaults(func=run_tests)
    args = parser.parse_args()
    
    args.func(args)




