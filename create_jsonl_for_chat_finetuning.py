import pandas as pd    
import json    
import openpyxl as openpyxl    


def create_message_object(row, template): #creates a function that takes a row and a template as input
    messages = [{"role":"system","content":template['system']},
                {"role":"user","content":template['user'].format(**row)},
                {"role":"assistant","content":template['assistant'].format(**row)}] #fills in the system, user, and assistant messages with the data from the row
    message_obj = {"messages": messages} #creates a message object with the system, user, and assistant messages
    return message_obj #returns the message object

templates = [    
    {    
        "system": "You are acting as a tax jurisdiction/geolocation expert. You are familiar with all United States tax jurisdictions/localities in all states including all U.S. states, U.S. counties, U.S. cities, and U.S. zip codes associated to these locations.",
        "user": "Provide a summary of tax jurisdiction data for Tax Area ID {Tax Area ID}:",    
        "assistant": "The tax jurisdiction with Tax Area ID {Tax Area ID} is located in the {Country}, {State} state, with Zip Code {Zip Code}, in {County} county, and the city of {City}."    
    }, 
    {    
        "system": "You are acting as a tax jurisdiction/geolocation expert. You are familiar with all United States tax jurisdictions/localities in all states including all U.S. states, U.S. counties, U.S. cities, and U.S. zip codes associated to these locations.",
        "user": "Provide a summary of tax jurisdiction data for Zip Code {Zip Code}:",    
        "assistant": "The tax jurisdiction with Zip Code {Zip Code} has Tax Area ID {Tax Area ID}, is located in the {Country}, {State} state, in {County} county, and the city of {City}."    
    },    
    {    
        "system": "You are acting as a tax jurisdiction/geolocation expert. You are familiar with all United States tax jurisdictions/localities in all states including all U.S. states, U.S. counties, U.S. cities, and U.S. zip codes associated to these locations.",
        "user": "Provide a summary of tax jurisdiction data for a record with Tax Area ID {Tax Area ID} and Zip Code {Zip Code}:",    
        "assistant": "The tax jurisdiction with Tax Area ID {Tax Area ID} and Zip Code {Zip Code} is located in the {Country}, {State} state, in {County} county, and the city of {City}."    
    },    
    {    
        "system": "You are acting as a tax jurisdiction/geolocation expert. You are familiar with all United States tax jurisdictions/localities in all states including all U.S. states, U.S. counties, U.S. cities, and U.S. zip codes associated to these locations.",
        "user": "Provide a summary of tax jurisdiction data for a record with City {City} in the State {State}:",    
        "assistant": "The tax jurisdiction of City {City} in State {State} state is located in the {Country}, with Tax Area ID {Tax Area ID}, with Zip Code {Zip Code}, and the county of {County}."    
    }   
]    
    
excel_file = "Location_Training.xlsx" # A file with geolocation data for various tax jurisdictions
dtype = {"Zip Code": str, "Tax Area ID": str} #sets the datatypes to str for Zip Code and Tax Area ID
df = pd.read_excel(excel_file,"Geolocation Data", dtype=dtype) #reads the excel file into a dataframe
df['Zip Code'] = df['Zip Code'].apply(lambda x: x.zfill(5)) #fills in leading zeros for zip codes
df['Tax Area ID'] = df['Tax Area ID'].apply(lambda x: x.zfill(9)) #fills in leading zeros for tax area IDs
    
chat_format_pairs = [] #creates an empty list to store the chat format pairs
for _, row in df.iterrows(): #iterates through each row in the dataframe
    adjusted_row = row.to_dict() #converts the row to a dictionary
    for template in templates: #iterates through each template
        template_msg = create_message_object(adjusted_row, template) #creates the chat format pairs
        chat_format_pairs.append(template_msg) #appends the chat format pairs to the list

with open("chat_format_pairs.json", "w") as f: #opens a file to write the chat format pairs
    json.dump(chat_format_pairs, f, indent=2) #writes the chat format pairs to the file

