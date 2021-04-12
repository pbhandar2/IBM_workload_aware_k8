import argparse 
import pathlib 
import plot_constant
import pandas as pd 
import numpy as np 
import plot_lib

import matplotlib.pyplot as plt 


def main(workload_name, size=3*1024*1024*1024):
    fig, ax = plt.subplots()
    plot_lib.plot_percentiles_time_windows(ax, workload_name, size)
    plt.legend()
    plt.tight_layout()
    plt.savefig("tester_period.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot percentiles of each period defined by the user.")
    parser.add_argument("workload_file_name", help="The name of file to load")
    args = parser.parse_args()
    main(args.workload_file_name)