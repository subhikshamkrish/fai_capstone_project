import math
import statistics
import matplotlib.pyplot as plt

from search.setup.eight_puzzle_benchmark import EightPuzzleProblem
from search.setup.instance_generator import generate_exact_depth_instances
from search.search.a_star import a_star_search
from search.search.ida import ida_star_search
from search.search.sma import sma_star_search



# CONFIG
from setup.eight_puzzle_benchmark import perturbed_manhattan_heuristic as heuristic
DEPTHS = [i for i in range(2, 21)]
INSTANCES_PER_DEPTH = 3
SMA_MEMORY_FACTOR = 2

# HELPERS
def summarize_metric(values):
    clean = [v for v in values if v is not None]
    return statistics.mean(clean) if clean else float("nan")


def format_float(x, decimals=5):
    if x is None or math.isnan(x):
        return "nan"

    return round(x, decimals)


# EXPERIMENT
def run_depth_suite():
    print("=== 8-puzzle A* / IDA* / SMA* benchmark ===")

    depths_list = []
    astar_log = []
    idastar_log = []
    smastar_log = []


    for depth in DEPTHS:
        print(f"\n--- Solution length target: {depth} ---")

        instances = generate_exact_depth_instances(depth, INSTANCES_PER_DEPTH)

        astar_expanded, idastar_expanded, smastar_expanded = [], [], []
        astar_runtime, idastar_runtime, smastar_runtime = [], [], []
        astar_cost, idastar_cost, smastar_cost = [], [], []
        astar_peak, smastar_pruned = [], []

        for state in instances:
            problem = EightPuzzleProblem(state)

            # A*
            _, m_a = a_star_search(problem, heuristic)
            astar_expanded.append(m_a.nodes_expanded)
            astar_runtime.append(m_a.runtime_sec)
            astar_cost.append(m_a.solution_cost)
            astar_peak.append(m_a.peak_stored_nodes)

            # IDA*
            problem = EightPuzzleProblem(state)
            _, m_i = ida_star_search(problem, heuristic)
            idastar_expanded.append(m_i.nodes_expanded)
            idastar_runtime.append(m_i.runtime_sec)
            idastar_cost.append(m_i.solution_cost)

            # SMA*
            sma_memory_limit = SMA_MEMORY_FACTOR * depth

            problem = EightPuzzleProblem(state)
            _, m_s = sma_star_search(
                problem,
                heuristic,
                memory_limit=sma_memory_limit, cutoff=20
            )

            smastar_expanded.append(m_s.nodes_expanded)
            smastar_runtime.append(m_s.runtime_sec)
            smastar_pruned.append(m_s.sma_pruned_nodes)

            if m_s.solution_found:
                smastar_cost.append(m_s.solution_cost)
            else:
                smastar_cost.append(None)


        print("A*")
        print("  avg expanded:", int(summarize_metric(astar_expanded)))
        print("  avg runtime (ms):", format_float(summarize_metric(astar_runtime)*1000,0))
        print("  avg peak stored:", int(summarize_metric(astar_peak)))

        print("IDA*")
        print("  avg expanded:", int(summarize_metric(idastar_expanded)))
        print("  avg runtime (ms):", format_float(summarize_metric(idastar_runtime)*1000,0))

        print("SMA*")
        print("  avg expanded:", int(summarize_metric(smastar_expanded)))
        print("  avg runtime (ms):", format_float(summarize_metric(smastar_runtime)*1000,0))
        print("  avg pruned:", int(summarize_metric(smastar_pruned)))


        avg_a = summarize_metric(astar_expanded)
        avg_i = summarize_metric(idastar_expanded)
        avg_s = summarize_metric(smastar_expanded)

        depths_list.append(depth)
        astar_log.append(math.log10(avg_a))
        idastar_log.append(math.log10(avg_i))
        smastar_log.append(math.log10(avg_s))



    # Plot
    plt.figure(figsize=(8, 6))

    plt.plot(depths_list, astar_log, marker='o', label='A*')
    plt.plot(depths_list, idastar_log, marker='o', label='IDA*')
    plt.plot(depths_list, smastar_log, marker='o', label='SMA*')

    plt.xlabel("Solution Length")
    plt.ylabel("log10(Nodes Expanded)")
    plt.title("Nodes Expanded vs Solution Length (8-Puzzle)")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("plots/a_ida_sma_nodes.png")
    plt.show()



if __name__ == "__main__":
    run_depth_suite()