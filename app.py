from flask import Flask, render_template, request, redirect, url_for,session
import pandas as pd
app = Flask(__name__)

def read_menu_data(filename):
    """Reads the file and returns a dictionary of semesters, subjects, and years."""
    menu_data = {}  # Dictionary to store menu hierarchy
    with open(filename, "r") as file:
        for line in file:
            menu_data.append(line)
    return menu_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def semester():
    read_menu_data("menu_data.txt")
    folders = list()
    names=[]
    return render_template('semester.html', folders=folders,names=names)

if __name__ == '__main__':
    app.run(debug=True)
