import json
from random import randint
import statistics

from utils.enums import Categories
from utils.formatter import Formatter, console



class Data:
    def __init__(self):
        try:
            with open('champinfo.json') as json_file:
                champs = json.load(json_file)
                self.champs = champs

        except:
            Formatter.error("Dataset not found! Please save champinfo.json in the same directory")

    def delete_entries_with(self, category: Categories, value: str):
        filtered_list = [champ for champ in self.champs if not value in champ[category.value]]

        Formatter.print_deletion_text(len(self.champs) - len(filtered_list), category.value, "includes (or is equal to)", value)

        self.champs = filtered_list

    def delete_entries_with_exact(self, category: Categories, values):
        filtered_list = [champ for champ in self.champs if not values == champ[category.value]]

        Formatter.print_deletion_text(len(self.champs) - len(filtered_list), category.value, "is equal to", values if isinstance(values, str) else ", ".join(values))

        self.champs = filtered_list

    def delete_entries_without(self, category: Categories, value: str):
        filtered_list = [champ for champ in self.champs if value in champ[category.value]]

        Formatter.print_deletion_text(len(self.champs) - len(filtered_list), category.value, "does not include", value)

        self.champs = filtered_list

    def delete_entries_without_exact(self, category: Categories, values):
        filtered_list = [champ for champ in self.champs if values == champ[category.value]]

        Formatter.print_deletion_text(len(self.champs) - len(filtered_list), category.value, "is not equal to", values if isinstance(values, str) else ", ".join(values))

        self.champs = filtered_list


    def delete_entries_without_all(self, category: Categories, value1: str, value2: str, value3: str = "", value4: str = "", value5: str = ""):
        filtered_list = [champ for champ in self.champs if value1 in champ[category.value] or value2 in champ[category.value] or value3 in champ[category.value] or value4 in champ[category.value] or value5 in champ[category.value]]

        Formatter.print_deletion_text(len(self.champs) - len(filtered_list), category.value, "does not include", value1 + " or " + value2)

        self.champs = filtered_list


    def get_random_champ(self):
        return self.champs[randint(0, len(self.champs) - 1)]

    def get_champ(self, name: str):
        try:
            return [c for c in self.champs if name.lower() == c["championName"].lower()][0]
        except:
            return None


    def get_next_champ(self, mode: str):
        if mode == "random":
            return self.get_random_champ()


        scores = {}

        median_year = statistics.median([int(c[Categories.RELEASE_YEAR.value]) for c in self.champs])

        for champ in self.champs:
            score = 0

            # year 
            score -= 50 * abs(median_year - int(champ[Categories.RELEASE_YEAR.value]))


            # GENDER and RANGE_TYPE are not considered, because they both have only two values -> Enough information is gathered either way
            for c in [Categories.RESOURCE, Categories.POSITION, Categories.SPECIES, Categories.REGION]:
                if isinstance(champ[c.value], str):
                    score += self._get_number_of_occurences_for(c, champ[c.value])
                else:
                    for v in champ[c.value]:
                        score += self._get_number_of_occurences_for(c, v)

            
            scores[champ["championName"]] = score


        scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=False if mode == "worst" else True))


        Formatter.print_top_picks(list(scores)[:3], list(scores.values())[:3])


        return [c for c in self.champs if c["championName"] == list(scores)[0]][0]


        
    def _get_number_of_occurences_for(self, category: Categories, value: str):
        return sum(1 for c in self.champs if value in c[category.value]) - 1



    def get_champ_table(self):
        self.champ_table = Formatter.init_champ_table("Champs in pool")

        champs = self.champs

        for champ in champs:
            self.champ_table = Formatter.add_to_champ_table(self.champ_table, champ)

        return self.champ_table
