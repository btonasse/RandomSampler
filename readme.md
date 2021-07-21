# Analyst sampler
The purpose of this class is to pick a "random" number of analysts every week,
while making sure that the same analyst is not picked again until all analysts have been picked.
This is achieved by calculating the elapsed time between the time of instantiation and an arbitrary root date
and using this to generate a new fixed seed every time the list of analysts is exhausted.

## Usage:
Instantiate this class with a list of analysts and a number of samples per week.
To get a unique sample, call `get_sample()` on the instance

## Caveats:
1) This functionality relies on the date at the time of instantiation to determine the seed of the list shuffler.
2) It also assumes that the list of analysts is constant (analysts should be passed always in the same order).
3) If an analyst is added or removed from the list, you might get unreliable results until the next fixed seed is generated.
4) If the list of analysts is not a multiple of the number of weekly samples, **there will be always someone left out**. 
    There is no provision to put the left out analysts at the top of the next shuffle result. *This can be implemented later*...