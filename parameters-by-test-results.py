import json
import re
from collections import defaultdict

# Load X1.json
with open("X1.json", "r", encoding="utf-8") as x1_file:
    x1_data = json.load(x1_file)

# Create a dictionary mapping synonyms to parameter names
synonym_to_parameter = {}
for entry in x1_data:
    param = entry["Abbreviation"]
    synonyms = entry.get("Synonyms", [])
    for synonym in synonyms:
        synonym_to_parameter[synonym.lower()] = param

# Read OCR-extracted text from the .txt file (replace with actual OCR output you want)
with open("0ab9800e-bc9a-4388-aaa2-d4fc05e7d111.txt", "r", encoding="utf-8") as txt_file:
    ocr_text = txt_file.read()

# Preprocessing: Tokenize into lines
lines = ocr_text.split("\n")

# Initialize a list to store structured test results
structured_results = []

# Regular expression pattern for extracting parameter values and unit
scientific_notation_pattern = re.compile(r"\s+(\d*\.*\d+\s*x10[\*|°]?\d+)\s*(\w*\/?[a-z]+\/?[\w.]*|\s*%)")
range_pattern = re.compile(r"[\(|\{]?(\d+\.?\d*[-\s]+\d+\.?\d*)[\)|\}]?\s*(\w*\/?[a-z]+\/?[\w.]*|\s*%)")
greater_or_less_pattern = re.compile(r"\s+[\(|\{]?([>|<]\s?\d*\.*\d+)[\)|\}]?\s*(\w*\/?[a-z]+\/?[\w.]*|\s*%)")
number_pattern = re.compile(r"\s+(\d*\.*\d+)[\)|\}]?\s*(\w*\/?[a-z]+\/?[\w.]*|\s*%)")

# Process each line
for line in lines:

    #Case normalization
    line = line.lower()
    
    #Repairing data
    line = line.replace("o.o","0.0").replace(" o."," 0.").replace(" /","/").replace("x“","x").replace("*x","x").replace(" of ","")

    # Check if the filtered line contains any key from synonym_to_parameter
    for synonym, param_name in synonym_to_parameter.items():
        if f" {synonym} " == line or \
           f" {synonym} " in f" {line} " or \
           line.startswith(f"{synonym} ") or \
           line.endswith(f" {synonym}"):

            print("================================================================================")
            print("Param:", synonym)
            print(line)

            if "and" in line:
                print("<Validation>: skip lines with 'and'")
                continue

            # Extract parameter name, value, and unit using the regex pattern
            
            #Scientific notation pattern
            scientific_notation_match = scientific_notation_pattern.search(line)

            if scientific_notation_match:
                param_value, param_unit = scientific_notation_match.groups()
                
                #the param_value found have to be after to the synonym value
                if line.find(param_value,0) < line.find(synonym,0):
                    print("<Validation>: Value:", param_value, "was found before the parameter:", synonym)
                    continue

                # Create a dictionary for the test result
                result_dict = {
                    "parameter": param_name,
                    "value": param_value,
                    "unit": param_unit    
                }
                structured_results.append(result_dict)
                print("<Validation>: Values found:", result_dict)
                break  # Stop searching once a match is found

            #Range pattern
            range_match = range_pattern.search(line)

            if range_match:
                param_value, param_unit = range_match.groups()
                
                #the param_value found have to be after to the synonym value
                if line.find(param_value,0) < line.find(synonym,0):
                    print("<Validation>: Value:", param_value, "was found before the parameter:", synonym)
                    continue

                # Create a dictionary for the test result
                result_dict = {
                    "parameter": param_name,
                    "value": param_value,
                    "unit": param_unit    
                }
                structured_results.append(result_dict)
                print("<Validation>: Values found:", result_dict)
                break  # Stop searching once a match is found

            #Greater or less than pattern
            greater_or_less_match = greater_or_less_pattern.search(line)

            if greater_or_less_match:
                param_value, param_unit = greater_or_less_match.groups()
                
                #the param_value found have to be after to the synonym value
                if line.find(param_value,0) < line.find(synonym,0):
                    print("<Validation>: Value:", param_value, "was found before the parameter:", synonym)
                    continue

                # Create a dictionary for the test result
                result_dict = {
                    "parameter": param_name,
                    "value": param_value,
                    "unit": param_unit    
                }
                structured_results.append(result_dict)
                print("<Validation>: Values found:", result_dict)
                break  # Stop searching once a match is found

            #Number match pattern
            number_match = number_pattern.search(line)

            if number_match:
                param_value, param_unit = number_match.groups()

                #exclude values whose number is included in the name of the synonym or param name
                if param_value in synonym and param_unit in synonym:
                    print("<Validation>: Value:", param_value, "or unit:", param_unit,"is part of the param name")
                    continue

                #the param_value found have to be after to the synonym value
                if line.find(param_value,0) < line.find(synonym,0):
                    print("<Validation>: Value:", param_value, "was found before the parameter:", synonym)
                    continue

                # Create a dictionary for the test result
                result_dict = {
                    "parameter": param_name,
                    "value": float(param_value),
                    "unit": param_unit   
                }
                structured_results.append(result_dict)
                print("<Validation>: Values found:", result_dict)
                break  # Stop searching once a match is found
            else:
                print("<Validation>: Param value and param unit not found")


print("================================================================================")
print("Original parameters dictionary obtained:")

# Deduplicate based on parameter name (retain only the first instance)
unique_results = defaultdict(list)
for result in structured_results:
    print(result)
    unique_results[result["parameter"]].append(result)

final_results = []
for param, results in unique_results.items():
    latest_result = results[len(results)-1]
    final_results.append(latest_result)

print("================================================================================")
print("Final parameters dictionary obtained:")

# Print the final structured results
for result in final_results:
    print(result)
