import json
from pathlib import Path
import os
import xml.etree.ElementTree as ET

p = Path(__file__).parents[0]

def xml_to_flat_json(xml_file, json_file):
    """
    Convert an XML file to a flat JSON structure.

    :param xml_file: Path to the input XML file.
    :param json_file: Path to the output JSON file.
    """
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Prepare a dictionary for the flat JSON structure
    flat_translations = {}

    # Traverse the XML structure
    for category in root.findall('category'):
        category_name = category.get('name')
        for item in category.findall('item'):
            item_name = item.get('name')
            combined_name = f"{category_name};{item_name}"
            flat_translations[combined_name] = item.text.strip() if item.text else ""

    # Write the flat JSON to the output file
    with open(json_file, 'w', encoding='utf-8') as json_out:
        json.dump(flat_translations, json_out, ensure_ascii=False, indent=4)

# Example usage:


 
# iterate over files in
# that directory
for filename in os.listdir(p):
    if ".xml" in filename:
        f = os.path.join(p, filename)
        # checking if it is a file
        if os.path.isfile(f):
            xml_to_flat_json(os.path.join(p, filename), os.path.join(p, filename[:-4] + ".json"))
