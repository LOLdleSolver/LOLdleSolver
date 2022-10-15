import sys
import time
from rich import panel, console, table, box, prompt

from utils.enums import Categories


console = console.Console()

class Formatter:
    def prompt_mode():
        mode = prompt.Prompt.ask("Select mode", choices=["best", "worst", "random", "custom"], default="best")
        console.clear()
        return mode

    def prompt_champ():
        champ = prompt.Prompt.ask("Select starting champ")
        console.clear()
        return champ
    

    def print_new_champ(champ: str):
        console.print("\n")
        console.rule("Now guessing: [bold cyan]" + champ)


    def winning_screen(champ: str, steps: int) -> bool:
        console.print("\n")
        console.rule("[bold green]YOU WON")
        #console.print(panel.Panel("[green bold]YOU WON!!![/green bold]\n\nGuesses: [red bold]" + str(steps) + "[/red bold]\n\nThe winning champion was:\n[bold cyan]" + champ, padding=(2, 20)), justify="center")
        console.print(panel.Panel("The winning champion was:\n[bold cyan]" + champ + "[/bold cyan]\n\nGuesses: [red bold]" + str(steps), padding=(2, 20)), justify="center")
        console.print("\n")

        close = prompt.Prompt.ask("Do you want to close now?", choices=["y", "n"], default="y")
        
        if close:
            console.print("Goodbye!")
            return True

        return False

    
    def print_deletion_text(count: int, category: str, verb: str, value: str):
        if count > 0:
            console.print("Deleted [bold red]{}[/] entries, because their [italic bright_black]{}[/] {} [bold magenta]{}[/]".format(str(count), category, verb, value))


    def print_top_picks(names, scores):
        for name, score, index in zip(names, scores, range(len(names))):
            console.print("Top {} pick: [bold cyan]{}[/] with score [bold magenta]{}[/]".format(str(index + 1), name, str(score)))




    def init_champ_table(title: str):
        t =  table.Table(title=title, box=box.ROUNDED)

        t.add_column("Name", style="cyan bold")
        t.add_column("Gender")
        t.add_column("Position")
        t.add_column("Species")
        t.add_column("Resource")
        t.add_column("Range Type")
        t.add_column("Region")
        t.add_column("Year")

        return t

    def add_to_champ_table(t: table.Table, champ):
        t.add_row(champ["championName"], champ[Categories.GENDER.value], ", ".join(champ[Categories.POSITION.value]), ", ".join(champ[Categories.SPECIES.value]), champ[Categories.RESOURCE.value], ", ".join(champ[Categories.RANGE_TYPE.value]), ", ".join(champ[Categories.REGION.value]), champ[Categories.RELEASE_YEAR.value])
        return t

    def error(text):
        console.log(text, style="red bold")
        time.sleep(5)
        sys.exit()
