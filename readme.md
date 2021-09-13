# Random sampler
The purpose of this class is to pick a "random" number of elements of a list every week, while making sure that the same elements are not picked twice before the list is exhausted.

This is achieved by calculating the elapsed time between the time of instantiation and an arbitrary root date and using this to generate a new fixed seed every time the list is exhausted.

## Usage:

You can either import it into your code or run it from the command line with `python -m`.
Regardless of how the sampler is called, a log with the results is written to a `sampler.log` file.
### Importing the module into your code:

```Python
from random_sampler import RandomSampler

# Instantiate the class with a fixed list of elements and a number of samples per week.
elements = [n for n in range(7)]
sampler = RandomSampler(elements, 2)

# Get a unique sample for this week
sample = sampler.get_sample()
print(sample)
```

### Getting a sample from a file:

`$ python -m random_sampler fromfile FILENAME SAMPLES`

Where `FILENAME` is a file containing the list of elements to sample from (one per line), and `SAMPLES` is the number of weekly samples.

### Unit tests

To run the built-in unit tests, execute this from the command line:

`$ python -m random_sampler runtest`

## Notes:

1. This functionality relies on the date at the time of instantiation to determine the seed of the list shuffler.
2. It also assumes that the list is fixed is constant (elements should always be in the same order).
3. If an element is added or removed from the list in between runs, you might get unreliable results until the next fixed seed is generated.
4. If the number of elements is not a multiple of the number of weekly samples, leftovers will be inserted at the top of the list upon the next seed reset.