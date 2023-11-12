import pandas as pd
import re

class Pipeline:
    def __init__(self):
        self.filters = list()

    def add(self, filter):
        self.filters.extend(filter)

    def execute(self, input):
        for filter in self.filters:
            input = filter(input)
        return input

def filter_duplicates(data):
    data.drop_duplicates(subset=['ID', 'Name'], inplace=True, ignore_index=True)
    return data

def business_status(data):
    converter = {
        'OPERATIONAL': 'Отворено',
        'CLOSED_TEMPORARILY': 'Привремено затворено',
        'CLOSED': 'Затворено'
    }
    data['Business status'] = data['Business status'].map(converter)
    return data

def append_consecutives(input_map):
    temporary_map = {}

    last_entry = None
    for day, hours in input_map.items():
        if not temporary_map:
            temporary_map[day] = hours
            last_entry = (day, hours)
        if hours == last_entry[1]:
            last_entry = (day, hours)
        else:
            temporary_map[last_entry[0]] = last_entry[1]
            last_entry = (day, hours)

    temporary_map.setdefault(last_entry[0], last_entry[1])

    final_string = ""
    last_entry = None
    cc = 0

    for day, hours in temporary_map.items():
        if last_entry is None:
            last_entry = (day, hours)
            if len(temporary_map) == 1:
                final_string += f"Monday - Sunday: {hours}"
        else:
            if last_entry[1] == hours:
                final_string += f"{last_entry[0]} - {day}: {hours} "
                last_entry = (day, hours)
            else:
                cc += 1
                if cc == 2:
                    final_string += f" {last_entry[0]}: {last_entry[1]}"
                    cc = 0
                    last_entry = (day, hours)
                else:
                    last_entry = (day, hours)

    if not final_string.endswith(temporary_map[list(temporary_map.keys())[-1]]):
        final_string += f" {list(temporary_map.keys())[-1]}: {temporary_map[list(temporary_map.keys())[-1]]}"

    return final_string

def filter_working_hours(data):
    if not pd.isna(data['Opening hours'].iloc[0]) and len(str(data['Opening hours'].iloc[0])) > 25:
        formatted_string = format_opening_hours(data['Opening hours'].iloc[0])
        data['Opening hours'] = formatted_string
    else:
        data['Opening hours'] = 'Not found'
    return data

def format_opening_hours(opening_hours_string):
    # Replace Unicode escape sequences with actual characters
    formatted_string = re.sub(r"u202f", "\u202F", opening_hours_string)  # Narrow no-break space
    formatted_string = re.sub(r"u2009", "\u2009", formatted_string)  # Thin space

    # Remove single quotes from the beginning and end
    formatted_string = formatted_string[1:-1].replace("'", "")
    opening_hours_array = formatted_string.split(", ")

    # Create a dictionary to store days with their respective Opening hours
    day_to_hours_map = {}

    for day_hours in opening_hours_array:
        day, hours = day_hours.split(":", 1)
        day_to_hours_map[day] = hours

    formatted_string = append_consecutives(day_to_hours_map)

    return formatted_string

if __name__ == '__main__':
    combining_data = pd.read_csv("C:/Users/jorda/OneDrive/Десктоп/Homework DIANS/combaining_data.csv", encoding='latin1')
    pipeline = Pipeline()
    pipeline.add([filter_duplicates, business_status, filter_working_hours])
    result = pipeline.execute(combining_data)
    result.to_csv(("C:/Users/jorda/OneDrive/Десктоп/Homework DIANS/filtered_data.csv"))