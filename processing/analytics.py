from datetime import timedelta
from io import BytesIO

import matplotlib as mpl
from matplotlib import pyplot as plt


async def get_plot_buffer(lap_times: list[timedelta]) -> BytesIO:
    def set_plot_settings():
        mpl.rcParams["font.size"] = 16
        plt.figure(figsize=(12, 7))
        plt.grid(visible=True, which="major", axis="both", alpha=1)
        plt.xlabel("Lap number")
        plt.ylabel("Time in seconds")

    lap_numbers = [
        str(x) for x in range(1, len(lap_times) + 1)
    ]  # convert lap_numbers to strings to prevent redundant ticks
    lap_times_in_sec = [lap_time.seconds for lap_time in lap_times]

    set_plot_settings()
    plt.plot(lap_numbers, lap_times_in_sec, "-o")
    # plt.gca().set_ylim(bottom=0)

    # save plot into BytesIO object
    plot_file = BytesIO()
    plt.savefig(plot_file, format="png")
    plot_file.seek(0)  # reset the cursor

    return plot_file


def get_total_distance(lap_times: list[timedelta]) -> float:
    loop_distance = 0.4  # km
    return len(lap_times) * loop_distance


def get_laps_number(lap_times: list[timedelta]) -> int:
    return len(lap_times)


def get_total_time(lap_times: list[timedelta]) -> timedelta:
    sum_time = timedelta()
    for lap_time in lap_times:
        sum_time += lap_time
    return sum_time
