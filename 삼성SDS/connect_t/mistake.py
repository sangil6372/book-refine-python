import json
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilenames


# Function to extract text from specific fields in JSON files
def extract_text_from_json(file_path, text_field='text'):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    extracted_data = []
    for entry in data:
        if text_field in entry and entry[text_field].strip():
            extracted_data.append({
                'page': entry.get('page', 'unknown'),
                'text': entry[text_field].strip()
            })

    return extracted_data


# Function to load existing JSON data from a file
def load_existing_json(output_file):
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []


# Function to save the combined data to a JSON file
def save_combined_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# Tkinter to open file dialog to select multiple JSON files
def select_files():
    Tk().withdraw()  # Hide Tkinter main window
    file_paths = askopenfilenames(title="Select JSON files", filetypes=[("JSON files", "*.json")])
    return file_paths


# Main processing function
def process_json_files(selected_files, output_file):
    combined_data = load_existing_json(output_file)

    for file_path in selected_files:
        extracted_text_data = extract_text_from_json(file_path)
        combined_data.extend(extracted_text_data)

    save_combined_json(combined_data, output_file)
    print(f'Updated JSON data has been saved to {output_file}')


# Select multiple JSON files using the file dialog
selected_files = select_files()

if selected_files:
    # Set the path for the output JSON file <-- change this to your desired path
    output_file = './combined_output.json'

    # Process the JSON files and update the existing JSON file
    process_json_files(selected_files, output_file)
else:
    print("No files were selected.")
