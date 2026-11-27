"""Extended Birthday Problem: Monte Carlo simulation for 3+ shared birthdays."""
from collections import Counter
import random
import math
import matplotlib.pyplot as plt


def has_shared_birthday(birthdays, min_matches=2):
    """True if at least `min_matches` people share a birthday."""
    if not birthdays:
        return False
    # Fast check for classic 2-person problem
    if min_matches == 2:
        return len(birthdays) != len(set(birthdays))
    # Frequency count check for 3+ people
    counts = Counter(birthdays)
    return max(counts.values()) >= min_matches


def simulate(group_size, trials=10000, min_matches=3, rng=None):
    if group_size < 0 or trials <= 0:
        raise ValueError('Use a nonnegative group size and positive trial count.')
    if rng is None:
        rng = random.Random()
    matches = 0
    for _ in range(trials):
        birthdays = [rng.randint(1, 365) for _ in range(group_size)]
        if has_shared_birthday(birthdays, min_matches=min_matches):
            matches += 1
    return matches / trials


def theoretical_two_way(group_size):
    """Exact probability for at least 2 shared birthdays (from Video 2/3)."""
    if group_size > 365:
        return 1.0
    return 1 - math.prod((365 - i) / 365 for i in range(group_size))


def main():
    trials = 10000
    rng = random.Random(217)
    
    # Larger group sizes are needed to see the 3-person curve rise
    sizes = [10, 23, 40, 60, 75, 85, 88, 90, 100, 120, 150]
    
    print(f'{trials:,} trials per group size')
    print(f'{"People":>6} {"2+ Match (Sim)":>16} {"3+ Match (Sim)":>16}')
    
    results_2 = []
    results_3 = []
    
    for n in sizes:
        p2 = simulate(n, trials, min_matches=2, rng=rng)
        p3 = simulate(n, trials, min_matches=3, rng=rng)
        results_2.append(p2)
        results_3.append(p3)
        print(f'{n:6d} {p2:16.2%} {p3:16.2%}')

    # Plotting the comparison graph for Video 4
    x_dense = list(range(1, 151))
    plt.figure(figsize=(9, 5))
    
    # 2-person curve (Exact line + Simulated dots)
    plt.plot(x_dense, [100 * theoretical_two_way(n) for n in x_dense], 
             label='2+ Shared Birthdays (Exact)', color='steelblue')
    plt.scatter(sizes, [100 * p for p in results_2], color='steelblue', zorder=3)
    
    # 3-person curve (Simulated curve)
    plt.plot(sizes, [100 * p for p in results_3], marker='o', 
             label='3+ Shared Birthdays (Monte Carlo)', color='darkorange', zorder=3)
    
    # 50% threshold reference lines
    plt.axhline(50, linestyle='--', color='gray', alpha=0.6, label='50% Threshold')
    plt.axvline(23, linestyle=':', color='steelblue', alpha=0.7)
    plt.axvline(88, linestyle=':', color='darkorange', alpha=0.7)
    
    plt.text(24, 5, 'n = 23\n(2-way 50%)', color='steelblue', fontsize=9)
    plt.text(89, 5, 'n = 88\n(3-way 50%)', color='darkorange', fontsize=9)
    
    plt.xlabel('Number of people')
    plt.ylabel('Probability of shared birthday (%)')
    plt.title('Birthday Problem: 2-Person vs. 3-Person Matches')
    plt.ylim(0, 100)
    plt.xlim(0, 150)
    plt.legend()
    plt.grid(alpha=0.2)
    plt.tight_layout()
    plt.savefig('birthday_comparison_3way.png', dpi=180)
    plt.close()


if __name__ == '__main__':
    main()