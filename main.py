from datetime import datetime
import sys

from utils.driver import Driver
from utils.data import Data
from utils.enums import Categories, Results
from utils.formatter import Formatter, console


console.clear()


with console.status("Loading Dataset..."):
    data = Data()

mode = Formatter.prompt_mode()

with console.status("Preparing Browser..."):
    driver = Driver()



won = False
steps = 0

result = None


while won is False:

    if mode == "custom" and steps == 0:
        champ = None
        while champ is None:
            champ = data.get_champ(Formatter.prompt_champ())
    else:
        champ = data.get_next_champ(mode)


    Formatter.print_new_champ(champ["championName"])

    
    with console.status("Waiting for result..."):
        result = driver.input_champ(champ["championName"])
        
        if len([r for r in result.values() if r == Results.GOOD]) >= 6:
            won = True

    if result is None and steps > 0: break

    steps += 1

    with console.status("Optimizing dataset..."):
        for category in Categories:
            if result[category.value] == Results.BAD:
                # Champ has A and is bad
                if isinstance(champ[category.value], str): # Dont ask
                    data.delete_entries_with(category, champ[category.value]) # keep champs without A
                else:
                    for value in champ[category.value]: # Nevermind
                        data.delete_entries_with(category, value) # keep champs without A
                    
            
            elif result[category.value] == Results.GOOD:
                # champ has A and is good
                data.delete_entries_without_exact(category, champ[category.value]) # keep champs with A and only A


            elif result[category.value] == Results.PARTIAL:
                if len(champ[category.value]) == 1: # Champ has A and only A and is partially correct -> desired champ has A + unknown
                    data.delete_entries_without(category, champ[category.value][0]) # delete champs without A
                    data.delete_entries_with_exact(category, champ[category.value]) # delete champs with A and only A

                else: # Champ has A + B and is partially correct -> desired champ has A or B, but not A and B
                    data.delete_entries_with_exact(category, champ[category.value]) # delete champs that have exactly A + B
                    data.delete_entries_without_all(category, *champ[category.value]) # keep champs with either A or B
                
                
            elif result[category.value] == Results.SUPERIOR:            
                # Release year is higher than A
                for i in range(2009, int(champ[category.value])):
                    data.delete_entries_with_exact(category, str(i)) # Delete champs with lower release year than A (All champs between 2009 and guessed release year)
                
            elif result[category.value] == Results.INFERIOR:
                # Release year is lower than A
                for i in range(int(champ[category.value]), datetime.now().year + 1):    
                    data.delete_entries_with_exact(category, str(i)) # Delete champs with higher release year than A (All champs between the guessed release year and 2022)


    if won:
        if Formatter.winning_screen(champ["championName"], steps):
            driver.driver.quit()
            sys.exit()

    else:
        console.print("\n[bold red]" + str(len(data.champs)) + "[/bold red] {} remaining\n".format("Champs" if len(data.champs) > 1 else "Champ"))   
        console.print(data.get_champ_table())
