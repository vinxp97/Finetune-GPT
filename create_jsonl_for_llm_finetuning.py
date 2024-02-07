import pandas as pd
import json
import openpyxl as openpyxl


def create_prompt_completion_pairs(row, templates): #creates a function that takes a row and a list of templates as input
    pairs = [] #creates an empty list to store the prompt completion pairs for the row from each template
    for template in templates: #iterates through each template
        prompt = template['prompt'].format(**row) #fills in the prompt with the data from the row
        completion = template['completion'].format(**row) #fills in the completion with the data from the row
        pairs.append({"prompt": prompt, "completion": completion}) #appends the prompt completion pair to the list
    return pairs #returns the list of prompt completion pairs

# Define the templates for the prompt and completion
templates = [
    {
        "prompt": "Provide a summary of tax jurisdiction data for Tax Area ID {Tax Area ID}:",
        "completion": "The tax jurisdiction with Tax Area ID {Tax Area ID} is located in the {Country}, {State} state, with Zip Code {Zip Code}, in {County} county, and the city of {City}."
    },
    {
        "prompt": "Provide a summary of tax jurisdiction data for Zip Code {Zip Code}:",
        "completion": "The tax jurisdiction with Zip Code {Zip Code} has Tax Area ID {Tax Area ID}, is located in the {Country}, {State} state, in {County} county, and the city of {City}."
    },
    {
        "prompt": "Provide a summary of tax jurisdiction data for a record with Tax Area ID {Tax Area ID} and Zip Code {Zip Code}:",
        "completion": "The tax jurisdiction with Tax Area ID {Tax Area ID} and Zip Code {Zip Code} is located in the {Country}, {State} state, in {County} county, and the city of {City}."
    },
    {
        "prompt": "Provide a summary of tax jurisdiction data for a record with City {City} in the State {State}:",
        "completion": "The tax jurisdiction of City {City} in State {State} state is located in the {Country}, with Tax Area ID {Tax Area ID}, with Zip Code {Zip Code}, and the county of {County}."
    }
]

excel_file = "Location_Training.xlsx" # A file with geolocation data for various tax jurisdictions
dtype = {"Zip Code": str, "Tax Area ID": str} #sets the datatypes to str for Zip Code and Tax Area ID
df = pd.read_excel(excel_file,"Geolocation Data", dtype=dtype) #reads the excel file into a dataframe


df['Zip Code'] = df['Zip Code'].apply(lambda x: x.zfill(5)) #fills in leading zeros for zip codes
df['Tax Area ID'] = df['Tax Area ID'].apply(lambda x: x.zfill(9)) #fills in leading zeros for tax area IDs

prompt_completion_pairs = [] #creates an empty list to store the prompt completion pairs
for _, row in df.iterrows(): #iterates through each row in the dataframe
    # Apply custom logic or adjustments to the row if needed
    adjusted_row = row.to_dict() #converts the row to a dictionary
    pairs = create_prompt_completion_pairs(adjusted_row, templates) #creates the prompt completion pairs
    prompt_completion_pairs.extend(pairs) #appends the prompt completion pairs to the list

with open("prompt_completion_pairs.json", "w") as f: #opens a file to write the prompt completion pairs
    json.dump(prompt_completion_pairs, f, indent=2) #writes the prompt completion pairs to the file