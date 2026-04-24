import math
import statistics
import matplotlib.pyplot as plt

from search.setup.eight_puzzle_benchmark import EightPuzzleProblem
from search.setup.instance_generator import generate_exact_depth_instances
from search.search.a_star import a_star_search
from search.search.sma import sma_star_search

#CONFIG
from setup.eight_puzzle_benchmark import perturbed_manhattan_heuristic as heuristic
DEPTH = 20
INSTANCES_PER_DEPTH = 3
MEMORY_FRACTIONS = [i / 100 for i in range(20, 151, 5)]

def run_sma_memory_suite():
    print("\n=== SMA* memory benchmark ===")

    instances = generate_exact_depth_instances(DEPTH, INSTANCES_PER_DEPTH)

    x_vals = []
    y_vals = []

    for frac in MEMORY_FRACTIONS:
        ratios = []
        pruned_vals = []

        for state in instances:
            problem = EightPuzzleProblem(state)
            _, m_a = a_star_search(problem, heuristic)

            memory_limit = max(DEPTH, int(frac * m_a.peak_stored_nodes))

            problem = EightPuzzleProblem(state)
            _, m_s = sma_star_search(problem, heuristic, memory_limit=memory_limit)

            if m_s.solution_found and m_a.nodes_expanded > 0:
                ratios.append(m_s.nodes_expanded / m_a.nodes_expanded)

            pruned_vals.append(m_s.sma_pruned_nodes)

        avg_ratio = summarize_metric(ratios)

        print(f"memory SMA*/A* ratio: {frac:.2f}")
        print("  nodes expanded ratio:", format_float(avg_ratio,0))
        print("  pruned:", int(summarize_metric(pruned_vals)/1000)*1000)

        x_vals.append(frac)
        y_vals.append(avg_ratio)

    # Plot
    plt.figure()
    plt.plot(x_vals, y_vals, marker='o')

    plt.xlabel("Memory / A* Memory")
    plt.ylabel("SMA* / A* Node Expansions")
    plt.title("SMA* Memory Tradeoff")

    plt.grid(True)
    plt.savefig("plots/sma_memory_ratio.png")
    plt.show()

# Helpers
def summarize_metric(values):
    clean = [v for v in values if v is not None]
    return statistics.mean(clean) if clean else float("nan")


def format_float(x, decimals=5):
    if x is None or math.isnan(x):
        return "nan"
    if decimals == 0:
        return int(round(x, decimals))
    return round(x, decimals)

if __name__ == "__main__":
    run_sma_memory_suite()