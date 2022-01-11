from os import name
from pathlib import Path
import pandas as pd
import glob
import time

from pandas.core.frame import DataFrame

def import_trivial_names(*path_strings):
    data_parts = []
    for path_string in path_strings:
        path = Path(path_string)
        if not path.exists():
            continue
        
        data_part = pd.read_csv(path,sep = "\t")
        svg_rows = data_part["Trivialname"].str.contains(".svg")
        data_part = data_part[~svg_rows]
        png_rows = data_part["Trivialname"].str.contains(".png")
        data_part = data_part[~png_rows]
        PNG_rows = data_part["Trivialname"].str.contains(".PNG")
        data_part = data_part[~PNG_rows]
        jpg_rows = data_part["Trivialname"].str.contains(".jpg")
        data_part = data_part[~jpg_rows]
        data_part["Trivialname"] = data_part["Trivialname"].str.split(", ")
        data_part = data_part.explode("Trivialname")
        data_part["Trivialname"] = data_part["Trivialname"].str.split('(').str[0].str.strip()
        data_parts.append(data_part)
    return pd.concat(data_parts).fillna("")

def find_trivial_name(trivial_name,dataframe):
    if dataframe["Trivialname"].str.capitalize().str.startswith(trivial_name).any():
        result = dataframe[dataframe["Trivialname"].str.capitalize().str.startswith(trivial_name)]
        return result
    return None
            
def process_result(result):
    if isinstance(result, DataFrame) and result.empty or result is None:
        print("Dieser Trivialname ist nicht bekannt.")
        time.sleep(2)
        return True
    
    if len(result)==1:
        print(result.to_string(index=False))
        print("")
        time.sleep(3)
        return True
        
    else:
        print("Das Muster passt auf folgende Trivialnamen:")
        print(result["Trivialname"].to_string(index=False))
        print("")
        time.sleep(3)
        return False
    
def recommendation_console():
    trivial_names = [f for f in glob.glob("*_trivial_names.txt")]
    data = import_trivial_names(*trivial_names)
    topics = {"Alkohol": "alcohols_trivial_names.txt",
              "Aldehyd": "aldehydes_trivial_names.txt",
              "Aromat": "aromates_trivial_names.txt",
              "Kohlenhydrat": "carbohydrates_trivial_names.txt",
              "Kohlensäure-Derivat": "carbonic_acid_derivatives_trivial_names.txt",
              "Ester": "esters_trivial_names.txt",
              "Ether": "ethers_trivial_names.txt",
              "Kohlenwasserstoff": "hydrocarbons_trivial_names.txt",
              "Keton": "ketones_trivial_names.txt",
              "Metallorganyl": "metal_organic_compounds_trivial_names.txt",
              "Säure": "organic_acids_trivial_names.txt",
              "Salz": "organic_salts_trivial_names.txt",
              "Feststoff": "inorganic_solids_trivial_names.txt",
              "Flüssigkeit": "inorganic_liquids_trivial_names.txt",
              "Gas": "inorganic_gases_trivial_names.txt"}
    
    print("Willkommen zum Vorschlags-System für chemische Trivialnamen!")
    print("Für Trivialnamen-Vorschläge den Anfang des Trivialnamens eingeben")
    print("""Für Vorschläge zu organischen Verbindungen 'Alkohol', 'Aldehyd', 'Kohlenhydrat', 'Kohlensäure-Derivat',
'Ester', 'Ether', 'Kohlenwasserstoff', 'Keton', 'Metallorganyl', 'Säure' oder 'Salz' eingeben""")
    print("""Für Vorschläge zu inorganischen Verbindungen 'Feststoff', 'Flüssigkeit' oder 'Gas' eingeben""")
    while True:
        print("Bitte den gesuchten Trivialnamen eingeben. Zum Beenden 'quit'")
        search_term = input().capitalize().strip()
        if search_term == 'Quit':
            break
        if search_term in topics:
            processed = False
            while not processed:
                data_topic = import_trivial_names(topics[search_term])
                print(data_topic["Trivialname"].to_string(index=False))
                print(f"Welcher/Welche/Welches {search_term} wird gesucht?")
                topic_search_term = input().capitalize().strip()
                result_data = find_trivial_name(topic_search_term,data_topic)
                processed = process_result(result_data)
                if not processed:
                    print("In dieser Gruppe weitersuchen? (Y/N)")
                    continue_search = input()
                    if continue_search in ["Y","Yes","Ja","y","yes","ja"]:
                        continue
                    else:
                        processed = True
        else:
            result_data = find_trivial_name(search_term,data)
            process_result(result_data)
              

recommendation_console()
        
        
