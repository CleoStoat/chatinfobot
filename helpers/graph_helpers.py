import io

from matplotlib.figure import Figure


def fig2bytes(fig: Figure) -> bytes:
    """Convert a Matplotlib figure to a PIL Image and return it"""

    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    return buf
