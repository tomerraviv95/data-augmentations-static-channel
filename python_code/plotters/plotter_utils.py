import datetime
import os
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np

from dir_definitions import FIGURES_DIR, PLOTS_DIR
from python_code.detectors.trainer import Trainer
from python_code.plotters.plotter_config import get_color, get_marker, get_linestyle
from python_code.utils.config_singleton import Config
from python_code.utils.python_utils import load_pkl, save_pkl

conf = Config()

MIN_BER_COEF = 0.2
MARKER_EVERY = 10


def get_ser_plot(dec: Trainer, run_over: bool, method_name: str, trial=None):
    print(method_name)
    # set the path to saved plot results for a single method (so we do not need to run anew each time)
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)
    file_name = '_'.join([method_name, str(conf.channel_type)])
    if trial is not None:
        file_name = file_name + '_' + str(trial)
    plots_path = os.path.join(PLOTS_DIR, file_name + '.pkl')
    print(plots_path)
    # if plot already exists, and the run_over flag is false - load the saved plot
    if os.path.isfile(plots_path) and not run_over:
        print("Loading plots")
        ser_total = load_pkl(plots_path)
    else:
        # otherwise - run again
        print("calculating fresh")
        ser_total = dec.evaluate()
        save_pkl(plots_path, ser_total)
    print(ser_total)
    return ser_total


def plot_by_values(all_curves: List[Tuple[np.ndarray, np.ndarray, str]], field_name, values: List[float], xlabel: str,
                   ylabel: str):
    # path for the saved figure
    current_day_time = datetime.datetime.now()
    folder_name = f'{current_day_time.month}-{current_day_time.day}-{current_day_time.hour}-{current_day_time.minute}'
    if not os.path.isdir(os.path.join(FIGURES_DIR, folder_name)):
        os.makedirs(os.path.join(FIGURES_DIR, folder_name))

    plt.figure()
    names = []
    for i in range(len(all_curves)):
        if all_curves[i][1] not in names:
            names.append(all_curves[i][1])

    mean_sers_dict = {}
    for method_name in names:
        mean_sers = []
        for ser, cur_name in all_curves:
            mean_ser = np.mean(ser)
            if cur_name != method_name:
                continue
            mean_sers.append(mean_ser)
        mean_sers_dict[method_name] = mean_sers

    for method_name in names:
        if field_name.split('_')[0] == 'SNR':
            plt.plot(values, mean_sers_dict[method_name], label=method_name.split('-')[1][1:],
                     color=get_color(method_name),
                     marker=get_marker(method_name),
                     linestyle=get_linestyle(method_name), linewidth=2.2)
        elif field_name == 'Pilots':
            mean_vals = np.array(mean_sers_dict['Regular Training'])
            plt.plot(values,
                     -np.log(np.array(mean_sers_dict[method_name]) / mean_vals),
                     label=method_name,
                     color=get_color(method_name),
                     marker=get_marker(method_name),
                     linestyle=get_linestyle(method_name), linewidth=2.2)

    plt.xticks(values, values)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(which='both', ls='--')
    plt.legend(loc='lower left', prop={'size': 15})
    plt.yscale('log')
    trainer_name = cur_name.split(' ')[0]
    plt.savefig(os.path.join(FIGURES_DIR, folder_name, f'coded_ber_versus_snrs_{trainer_name}.png'),
                bbox_inches='tight')
    plt.show()
