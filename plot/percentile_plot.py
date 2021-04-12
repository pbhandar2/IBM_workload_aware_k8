import argparse 
import pathlib 
import plot_constant
import pandas as pd 
import numpy as np 
import plot_lib

import matplotlib.pyplot as plt 


def main(workload_name):
    fig, ax = plt.subplots()
    plot_lib.plot_percentile_from_log_file(ax, workload_name)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tester.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot percentiles of each period defined by the user.")
    parser.add_argument("workload_file_name", help="The name of file to load")
    args = parser.parse_args()
    main(args.workload_file_name)