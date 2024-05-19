import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# dependancy - fpdf2 library
#!pip install fpdf2
from fpdf import FPDF


import json
f = open('data/plans.json')
data = json.load(f)
metadata = data[0]
week = data[1]


# path is a path to icons folder
# week is an extracted plan in json format
def create_pdf(path, week, icon_size = 20):
    pdf = FPDF()
    pdf.add_page()
    # create title
    pdf.set_font("helvetica", "B", size=24)
    pdf.text(75, 15, "TRAINING PLAN")

    # create body
    pdf.set_font("helvetica", size=16)
    # starting position
    y = 25
    x = 15
    index = 0
    weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in week:
        # create weekday text
        pdf.text(x, y, text=weekday[index])
        y += 2
        # create images
        for exercise in day:
            name = exercise["name"]
            pdf.image(f"{path}/icons/{name}_icon.png", x, y, icon_size, icon_size)
            x += icon_size
        y += (icon_size + 10)
        x = 15
        index += 1
    pdf.output("training_plan.pdf")

create_pdf("Downloads", week)
