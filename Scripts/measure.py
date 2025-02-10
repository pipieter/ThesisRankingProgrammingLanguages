import argparse
import os

from Scripts.util.benchmark_args import (
    get_measure_binarytree_args,
    get_measure_external_merge_sort_args,
    get_measure_fib3_args,
    get_measure_io_number_args,
    get_measure_merge_sort_args,
    get_measure_pagerank_args,
)
from Scripts.util.run import run_benchmark
from Scripts.generate_input import verify_dir


ARGS_MAP = {
    "MergeSort": get_measure_merge_sort_args,
    "ExternalMergeSort": get_measure_external_merge_sort_args,
    "IONumber": get_measure_io_number_args,
    "Fib3": get_measure_fib3_args,
    "PageRank": get_measure_pagerank_args,
    "BinaryTree": get_measure_binarytree_args,
}


if __name__ == "__main__":
    LANGUAGES = ["C++", "C#", "Java", "PyPy", "Python", "Rust"]

    BENCHMARKS = sorted(list(set(ARGS_MAP.keys())))

    OPTIMIZATION = ["optimized", "unoptimized"]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--languages",
        type=str,
        nargs="+",
        default=LANGUAGES,
        choices=LANGUAGES,
        help="Which languages to benchmark. Default is all languages.",
    )
    parser.add_argument(
        "--benchmarks",
        type=str,
        nargs="+",
        default=BENCHMARKS,
        choices=BENCHMARKS,
        help="Which benchmarks to run. Default is all benchmarks.",
    )
    parser.add_argument(
        "--optimized",
        type=str,
        nargs="+",
        default=OPTIMIZATION,
        choices=OPTIMIZATION,
        help="Which optimization levels to use. Defaults to both optimized and unoptimized.",
    )
    parser.add_argument(
        "--warmups",
        type=int,
        default=0,
        help="The amount of warmup iterations before measuring.",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=1,
        help="The amount of iterations to perform, after warm-up.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=1000,
        help="The amount of iterations to perform, after warm-up.",
    )
    parser.add_argument(
        "--verbose",
        type=bool,
        default=False,
        action=argparse.BooleanOptionalAction,
    )

    args = parser.parse_args()
    languages = sorted(list(set(args.languages)))
    benchmarks = sorted(list(set(args.benchmarks)))
    optimizations = sorted(list(set(args.optimized)))
    verbose = args.verbose
    iterations = args.iterations
    warmups = args.warmups

    verify_dir(os.path.join("./Results"))

    for benchmark in benchmarks:
        benchmark_args = ARGS_MAP[benchmark]()

        for optimization in optimizations:
            optimized = optimization == "optimized"

            for identifier, arg in benchmark_args:
                args = {"ARGS": arg}

                for language in languages:
                    run_benchmark(
                        benchmark=benchmark,
                        language=language,
                        identifier=identifier,
                        optimized=optimized,
                        args=args,
                        timeout=1000,
                        iterations=iterations,
                        verbose=verbose,
                        warmups=warmups,
                    )
