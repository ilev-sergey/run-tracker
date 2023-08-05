from datetime import timedelta
from io import BytesIO

import matplotlib as mpl
from matplotlib import pyplot as plt


class Distance:
    def __init__(self, laps_number: int) -> None:
        self.laps_number = laps_number

    def __repr__(self) -> str:
        return f"Distance({self.laps_number})"

    @property
    def km(self) -> float:
        loop_distance = 0.4
        return self.laps_number * loop_distance

    @property
    def mi(self) -> float:
        loop_distance = 0.248548
        return self.laps_number * loop_distance


class Activity:
    def __init__(self, lap_times: list[timedelta]) -> None:
        self._lap_times = lap_times

    def __repr__(self) -> str:
        return f"Activity({self.lap_times})"

    @property
    def lap_times(self):
        return self._lap_times

    @property
    def distance(self) -> Distance:
        return Distance(len(self.lap_times))

    @property
    def laps_number(self) -> int:
        return len(self.lap_times)

    @property
    def time(self) -> timedelta:
        sum_time = timedelta()
        for lap_time in self.lap_times:
            sum_time += lap_time
        return sum_time

    async def plot_buffer(self) -> BytesIO:
        def set_plot_settings():
            mpl.rcParams["font.size"] = 16
            plt.figure(figsize=(12, 7))
            plt.grid(visible=True, which="major", axis="both", alpha=1)
            plt.xlabel("Lap number")
            plt.ylabel("Time in seconds")

        lap_numbers = [
            str(x) for x in range(1, self.laps_number + 1)
        ]  # convert lap_numbers to strings to prevent redundant ticks
        lap_times_in_sec = [lap_time.seconds for lap_time in self.lap_times]

        set_plot_settings()
        plt.plot(lap_numbers, lap_times_in_sec, "-o")

        # save plot into BytesIO object
        plot_file = BytesIO()
        plt.savefig(plot_file, format="png")
        plot_file.seek(0)  # reset the cursor

        return plot_file
