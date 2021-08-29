from typing import List, Union

import matplotlib.pyplot as pyplot
import numpy
from matplotlib.figure import Figure


def plot_hor_bars(
    labels: List[str], widths: List[Union[int, float]], x_label: str, title: str
) -> Figure:
    fig, ax = pyplot.subplots()
    fig.set_size_inches(10, 10)
    y_pos = numpy.arange(len(labels))

    ax.barh(y_pos, widths, align="center")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(x_label)
    ax.set_title(title)

    return fig
