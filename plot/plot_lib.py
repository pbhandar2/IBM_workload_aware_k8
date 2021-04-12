import numpy as np 
import pathlib
import matplotlib.pyplot as plt 
import plot_constant


def get_latency_array(file_path):
    latency_array = []
    with file_path.open("r") as f:
        line = f.readline().rstrip()
        while line:
            split_line = line.split(",")
            latency = int(split_line[1])
            latency_array.append(latency)
            line = f.readline().rstrip()
    return latency_array


def get_read_write_latency_array(file_path):
    read_latency_array = []
    write_latency_array = []
    with file_path.open("r") as f:
        line = f.readline().rstrip()
        while line:
            split_line = line.split(",")
            latency = int(split_line[1])
            op = int(split_line[2])

            if op == 0:
                read_latency_array.append(latency)
            elif op == 1:
                write_latency_array.append(latency)

            line = f.readline().rstrip()
    return read_latency_array, write_latency_array


def get_latency_array_windows_by_size(file_path, size):
    cur_size = 0
    cur_latency_array = []
    final_latency_array = []
    with file_path.open("r") as f:
        line = f.readline().rstrip()
        while line:
            split_line = line.split(",")
            latency = int(split_line[1])
            cur_size += int(split_line[3])

            if cur_size > size:
                final_latency_array.append(cur_latency_array)
                cur_latency_array = []
                cur_size = 0 
            else:
                cur_latency_array.append(latency)

            line = f.readline().rstrip()
    
    # the last period
    final_latency_array.append(cur_latency_array)
    return final_latency_array


def plot_percentile(ax, data_array, percentile_array=range(11), label=None):
    latency_percentile_array = np.percentile(data_array, percentile_array)
    ax.plot(percentile_array, latency_percentile_array, label=label)


def plot_percentile_from_log_file(ax, workload_name, label=None):
    clat_file_name = "{}_clat.1.log".format(workload_name)
    clat_file_path = pathlib.Path(plot_constant.LAT_LOG_PATH).joinpath(clat_file_name)

    latency_array = np.array(get_latency_array(clat_file_path), dtype=float)
    latency_array = latency_array/1000 # convert to microseconds

    plot_percentile(ax, latency_array, label=label)
    

def plot_percentiles_time_windows(ax, workload_name, size):
    clat_file_name = "{}_clat.1.log".format(workload_name)
    clat_file_path = pathlib.Path(plot_constant.LAT_LOG_PATH).joinpath(clat_file_name)

    window_latency_array = get_latency_array_windows_by_size(clat_file_path, size)

    for window_index, window_latency in enumerate(window_latency_array):
        plot_percentile(ax, window_latency, label=window_index)

        print(window_index, np.mean(window_latency), max(window_latency), min(window_latency))
