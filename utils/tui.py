from rich.console import Console
from rich.layout import Layout
from rich import panel, live, text

console = Console()

class TUI:

    def __init__(self):
        self.layout = Layout()

        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="result", size=10),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )

        self.layout["main"].split_row(
            Layout(name="left"),
            Layout(name="right"),
        )

        self.layout["header"].update(text.Text("LOLdle Solver", justify="center"))

    
    def print_new_champ(self, champ: str):
        self.layout["header"].update(
            text.Text.assemble("Now guessing: ", (champ, "bold magenta"))
        )


    def winning_screen(self, live, champ: str, steps: int):
        live.update(panel.Panel("Won: " + champ))