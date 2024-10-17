from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape  # Import escape for sanitization
import os
import csv

app = Flask(__name__)

# Read the folder structure from the text file
def read_menu_data(filename):
    menu_data = []
    with open(filename, "r") as file:
        for line in file:
            path = line.strip()
            folders_in_path = path.split("/")
            last_name = folders_in_path[-1]
            parent_path = "/".join(folders_in_path[:-1]) if len(folders_in_path) > 1 else "/"
            menu_data.append({
                'full_path': path,
                'parent_path': parent_path,
                'last_name': last_name,
                'hierarchy': folders_in_path
            })
    return menu_data

# Read files from a CSV
def read_files_data(csv_filename):
    files_data = {}
    with open(csv_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            folder_path, file_name = row
            if folder_path not in files_data:
                files_data[folder_path] = []
            files_data[folder_path].append(file_name)
    return files_data



@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/<path:subpath>')
def show_directory(subpath=''):
    # Load the folder and file data at startup
    folder_data = read_menu_data('menu_data.txt')
    files_data = read_files_data('files_data.csv')
    current_path = '/' + escape(subpath) if subpath else '/'  # Escape subpath for security
    subfolders = [folder for folder in folder_data if folder['parent_path'] == current_path]
    files = files_data.get(current_path, [])

    # Escape folder names for security in rendering
    # folder_names = [escape(folder['last_name']) for folder in subfolders]
    # Generate breadcrumb
    breadcrumb = current_path.strip('/').split('/')
    
    return render_template('directory.html', folders=[folder['last_name'] for folder in subfolders], files=files, folder_path=current_path, breadcrumb=breadcrumb)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
