"""Classic Birthday Problem: Monte Carlo simulation and exact comparison."""
import random
import math
import matplotlib.pyplot as plt


def has_shared_birthday(birthdays):
    """True if at least two people share a birthday."""
    return len(birthdays) != len(set(birthdays))


def simulate(group_size, trials=10000, rng=None):
    if group_size < 0 or trials <= 0:
        raise ValueError('Use a nonnegative group size and positive trial count.')
    if rng is None:
        rng = random.Random()
    matches = 0
    for _ in range(trials):
        birthdays = [rng.randint(1, 365) for _ in range(group_size)]
        if has_shared_birthday(birthdays):
            matches += 1
    return matches / trials


def theoretical_probability(group_size):
    if group_size < 0:
        raise ValueError('Group size must be nonnegative.')
    if group_size > 365:
        return 1.0
    return 1 - math.prod((365 - i) / 365 for i in range(group_size))


def main():
    trials = 10000
    rng = random.Random(217)
    sizes = [5, 10, 15, 20, 23, 25, 30, 40, 50, 60]
    results = [simulate(n, trials, rng) for n in sizes]
    print(f'{trials:,} trials per group size')
    print(f'{"People":>6} {"Simulated":>12} {"Theoretical":>12} {"Error (pp)":>12}')
    for n, estimate in zip(sizes, results):
        exact = theoretical_probability(n)
        print(f'{n:6d} {estimate:12.2%} {exact:12.2%} {100*abs(estimate-exact):12.2f}')
    print('\nEffect of trial count (23 people):')
    for count in [100, 1000, 10000, 100000]:
        estimate = simulate(23, count, random.Random(217))
        print(f'{count:>7,}: {estimate:.2%}; estimated standard error: {100*math.sqrt(estimate*(1-estimate)/count):.2f} percentage points')
    x = list(range(1, 61))
    plt.figure(figsize=(9, 5))
    plt.plot(x, [100*theoretical_probability(n) for n in x], label='Exact probability')
    plt.scatter(sizes, [100*p for p in results], label='Monte Carlo (10,000 trials)', zorder=3)
    plt.axhline(50, linestyle='--', alpha=.5)
    plt.axvline(23, linestyle=':', alpha=.5)
    plt.xlabel('Number of people')
    plt.ylabel('Probability of a shared birthday (%)')
    plt.title('The Birthday Problem: Theory vs. Simulation')
    plt.ylim(0, 100)
    plt.legend()
    plt.grid(alpha=.2)
    plt.tight_layout()
    plt.savefig('birthday_probability.png', dpi=180)
    plt.close()


if __name__ == '__main__':
    main()
