import argparse 
import pathlib 
import json 

import numpy as np 
import matplotlib.pyplot as plt
from collections import defaultdict 


def get_perf_dict(output_dir):
    """ Get the performance of FIO containers with different memory allocated for a given workload. 
    """

    perf_dict = defaultdict(list)
    for output_path in output_dir.iterdir():

        # check if the clat file exists that means fio run is complete, not the same if JSON file exists
        clat_file_substring = "_clat.1.log"
        if clat_file_substring in str(output_path):

            file_name = output_path.name 
            json_file_stem = file_name.split(clat_file_substring)[0]
            json_file_name = "{}.json".format(json_file_stem)
            json_file_path = output_dir.joinpath(json_file_name)
            memory_mb = int(json_file_stem.split("_")[0])

            with json_file_path.open("r") as json_handle:
                perf_dict[memory_mb].append(json.load(json_handle))

    return perf_dict


def get_plot_data_from_perf_dict(perf_dict):
    """ From the memory_dict, get the x and y values to be plotted. The x axis will contain memory 
        values. The y axis will contain a list of mean latency of a run. Plot the min, max and mean 
        latency of this list for each y-axis list. 
    """

    x = np.zeros(len(perf_dict))
    y = np.zeros(len(perf_dict))
    yerr = np.zeros(shape=((len(perf_dict), 2)))
    for perf_index, memory_size_mb in enumerate(sorted(perf_dict)):
        x[perf_index] = memory_size_mb

        memory_perf_result = perf_dict[memory_size_mb]
        mean_latency_array = np.zeros(len(next(iter(perf_dict.values()))))
        for experiment_index, experiment_results in enumerate(memory_perf_result):
            read_lat_data = experiment_results["jobs"][0]["read"]["clat_ns"]
            mean_latency_array[experiment_index] = read_lat_data["mean"]

        y[perf_index] = np.mean(mean_latency_array)/1000000
        yerr[perf_index] = [
            (np.mean(mean_latency_array)-np.min(mean_latency_array))/1000000,
            (np.max(mean_latency_array)-np.mean(mean_latency_array))/1000000
        ]

    return x, y, yerr 


def plot_min_max_mean(x, y, yerr):
    """ Plot mean value of arrays in y along with the min and max value to show variation. 
    """

    plt.figure(figsize=[14, 6])
    plt.rcParams.update({'font.size': 25 })

    plt.ylabel("Normalized Mean Latency")
    plt.xlabel("Memory (MB)")
    plt.vlines(2000, 0, 1, linestyle="dashed", color=["red"], label="Working Set Size")

    norm_y = (y[1:] - np.min(y[1:]))/(np.max(y[1:])-np.min(y[1:]))

    plt.plot(x[1:], norm_y, "--o", markersize=15)
    plt.xticks(x)
    plt.legend()
    plt.tight_layout()
    plt.savefig("lat_vs_mem.png")


def main(output_dir):
    perf_dict = get_perf_dict(output_dir)
    x, y, yerr = get_plot_data_from_perf_dict(perf_dict)
    plot_min_max_mean(x, y, yerr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot the memory against latency for FIO docker runs.")
    parser.add_argument("output_dir", type=pathlib.Path, help="Directory containing FIO output files.")
    args = parser.parse_args()

    main(args.output_dir)