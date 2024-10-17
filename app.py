from flask import Flask, render_template, request, redirect, url_for,session
import pandas as pd
app = Flask(__name__)

def read_menu_data(filename):
    """Reads the file and returns a dictionary of semesters, subjects, and years."""
    menu_data = {}  # Dictionary to store menu hierarchy
    with open(filename, "r") as file:
        for line in file:
            semester, subject, year = line.strip().split(",")
            semester_path = "/" + semester
            subject_path = "/" + subject
            year_path = "/" + year

            if semester_path not in menu_data:
                menu_data[semester_path] = {}
            if subject_path not in menu_data[semester_path]:
                menu_data[semester_path][subject_path] = []
            menu_data[semester_path][subject_path].append(year_path)
    
    return menu_data

# Load menu data from the file
menu_data = read_menu_data('data_share_bot\main_menu_buttons')
database=pd.read_csv("data_share_bot\datafile\data.csv")
# Dummy data for demonstration
# all_folders = [f"Folder {i}" for i in range(1, 101)]  # List of 100 folders

# from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def read_menu_data(filename):
    """Reads the file and returns a dictionary of semesters, subjects, and years."""
    menu_data = {}  # Dictionary to store menu hierarchy
    with open(filename, "r") as file:
        for line in file:
            semester, subject, year = line.strip().split(",")
            semester_path = "/" + semester
            subject_path = "/" + subject
            year_path = "/" + year

            if semester_path not in menu_data:
                menu_data[semester_path] = {}
            if subject_path not in menu_data[semester_path]:
                menu_data[semester_path][subject_path] = []
            menu_data[semester_path][subject_path].append(year_path)
    
    return menu_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def semester():
    semesters = list(menu_data.keys())
    return render_template('semester.html', semesters=semesters)

@app.route('/home/<semester>')
def subject(semester):
    subjects = menu_data.get("/" + semester, {})
    return render_template('subject.html', subjects=subjects, semester=semester)

@app.route('/home/<semester>/<subject>')
def year(semester, subject):
    years = menu_data.get("/" + semester, {}).get("/" + subject, [])
    return render_template('year.html', years=years, subject=subject, semester=semester)

@app.route('/home/<semester>/<subject>/<year>')
def resource(semester, subject, year):
    resources = ["Books", "PYQs", "Notes"]
    print(f"Semester: {semester}, Subject: {subject}, Year: {year}")  # Debugging print
    return render_template('resource.html', resources=resources, semester=semester, subject=subject, year=year)

@app.route('/home/<semester>/<subject>/<year>/<resource>')
def view_files(semester, subject, year, resource):
    database=pd.read_csv("data_share_bot\datafile\data.csv")
    print(semester)
    print(subject)
    print(year)
    print(resource)
    # Your code to handle the request and render the appropriate template
    semester_filter=database[database["semester"]=="/"+semester]
    print(semester_filter)
    subject_filter=semester_filter[semester_filter["subject"]=="/"+subject]
    year_filter=subject_filter[subject_filter["year"]=="/"+year]
    final_filter=year_filter[year_filter["resource_type"]=="/"+resource]

    columns_to_keep = ["cloud","file_name","file_link"]
    filesdf = final_filter[columns_to_keep]
    filesall = filesdf.reset_index(drop=True).values.tolist()
    length=len(filesall)
    lst=range(length)
    print("length of files",length)


    return render_template('files.html', semester=semester, subject=subject, year=year, resource=resource , files=filesall,rang=lst)

import requests

def get_file_download_url(bot_token, file_id):
    """
    Get the download URL for a file using its file_id.
    
    Parameters:
    bot_token (str): Your Telegram bot token.
    file_id (str): The file ID of the file to download.

    Returns:
    str: The download URL of the file, or None if there's an error.
    """
    database=pd.read_csv("data_share_bot\datafile\data.csv")
    # Get file path
    file_info_url = f'https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}'
    response = requests.get(file_info_url)

    if response.status_code == 200:
        file_path = response.json()['result']['file_path']
        download_url = f'https://api.telegram.org/file/bot{bot_token}/{file_path}'
        return download_url
    else:
        print(f"Error fetching file: {response.status_code} - {response.text}")
        return None


# # Example usage
# TOKEN = "7452688807:AAFewUJKZOniA8ldH9EACAh784l8KYSJE6g"  # Replace with your bot token
# FILE_ID = "BQACAgUAAxkBAAIIj2bC7iSY37pTzTBcgUrRR8y5ddGiAALdEQAC49QYVtdxPjv01wiLNQQ"  # Replace with the actual file ID

# download_url = get_file_download_url(TOKEN, FILE_ID)

# if download_url:
#     print(f"Download URL: {download_url}")

from fileurl import get_file_download_url  # Import the function to get direct link

@app.route('/home/<semester>/<subject>/<year>/<resource>/<file>', methods=['GET'])
def files(semester, subject, year, resource, file):
    # Filter the database
    semester_filter = database[database["semester"] == "/" + semester]
    subject_filter = semester_filter[semester_filter["subject"] == "/" + subject]
    year_filter = subject_filter[subject_filter["year"] == "/" + year]
    resource_filter = year_filter[year_filter["resource_type"] == "/" + resource]

    # Ensure the file ID is an integer if it's stored as such in the database
    try:
        final_filter = resource_filter[resource_filter["cloud"] == int(file)]
    except ValueError:
        return "Invalid file ID", 400

    # If no files are found
    if final_filter.empty:
        return "File not found", 404

    # Select the required columns
    columns_to_keep = ["file_name", "file_link", "file_id"]
    filesdf = final_filter[columns_to_keep]
    filesall = filesdf.reset_index(drop=True).values.tolist()

    # Safely access the file data
    if not filesall:
        return "No files available", 404

    # Extract the file data (name, telegram link, file id)
    file_data = filesall[0]
    file_name = file_data[0]
    telegram_link = file_data[1]
    file_id = file_data[2]

    # Get the direct link using the file ID
    TOKEN = "7452688807:AAFewUJKZOniA8ldH9EACAh784l8KYSJE6g"  # Replace with your bot token
    directlink = get_file_download_url(bot_token=TOKEN, file_id=file_id)

    # Render the template with file details
    return render_template('file.html', semester=semester, subject=subject, year=year, resource=resource, 
                           file=file, name=file_name, link=directlink, tele=telegram_link)


if __name__ == '__main__':
    app.run(debug=True)
