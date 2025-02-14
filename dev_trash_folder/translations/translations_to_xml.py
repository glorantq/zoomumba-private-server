import os
import json
from lxml import etree
from pathlib import Path

p = Path(__file__).parents[0]

def create_xml_structure(parent, keys, value):
    if len(keys) == 1:
        item = etree.SubElement(parent, "item", name=keys[0])
        item.text = etree.CDATA(value)
    else:
        category = parent.find(f"category[@name='{keys[0]}']")
        if category is None:
            category = etree.SubElement(parent, "category", name=keys[0])
        create_xml_structure(category, keys[1:], value)

def prettify_xml(element):
    return etree.tostring(element, pretty_print=True, encoding="utf-8", xml_declaration=True).decode("utf-8")

def json_to_xml_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    for folder_name in os.listdir(input_folder):
        folder_path = os.path.join(input_folder, folder_name)
        json_file_path = os.path.join(folder_path, "en.json")
        
        if os.path.isdir(folder_path) and os.path.isfile(json_file_path):
            with open(json_file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            
            root = etree.Element("language")
            
            for key, value in data.items():
                parts = key.split(";")
                keys = parts[1:]
                create_xml_structure(root, keys, value)
            
            xml_output_path = os.path.join(output_folder, f"{folder_name[0:-5]}.xml")
            
            with open(xml_output_path, "w", encoding="utf-8") as f:
                f.write(prettify_xml(root))
            
            print(f"XML output saved to {xml_output_path}")

# Example usage
input_folder = os.path.join(p, "Zoomumba")
output_folder = os.path.join(p, "en")
json_to_xml_folder(input_folder, output_folder)