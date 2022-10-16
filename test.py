import time
from rich.console import Console
from rich.layout import Layout
from rich import panel, live

console = Console()
layout = Layout()

console.clear()


layout.split(
    Layout(name="header", size=3),
    Layout(name="result", size=10),
    Layout(name="main", ratio=1),
    Layout(name="footer", size=3)
)

layout["main"].split_row(
    Layout(name="left"),
    Layout(name="right"),
)

console.print(layout)

with live.Live(layout, refresh_per_second=10, screen=True) as live:
    i = 0
    while i < 5:
        layout["left"].update(
            "test " + str(i)
        )
        i += 1
        time.sleep(0.5)

        if i == 4:
            live.update(panel.Panel("won"))


