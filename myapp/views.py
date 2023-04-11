from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

#import necessary packages
import pandas as pd
from fpdf import FPDF
import json
import requests

class student:
    # define the student class to handle json input
    def __init__(self, json):
        self.name = json["name"]
        self.grade = json["grade"]
        self.date = json["date"]
        self.comment = json["comment"]
        self.tester = json["tester"]
        self.recommendation = json["recommendation"]
        self.result = pd.DataFrame(json["assessment_data"])
        self.question_count = len(json["assessment_data"])
        self.total_correct = sum(self.result["accuracy"])

def getImage(url, title):
    response = requests.get(url)
    if response.status_code == 200:
        with open(str(title)+".jpg", "wb") as f:
            f.write(response.content)

def generateReport(json_data):
    #initialize the instance of the student
    student1 = student(json_data)
    result = student1.result
    accu_weight = 1
    commu_weight = 2
    under_weight = 2
    speed = sum(result.speed)

    subjectl = result["subject"].tolist()
    accuracyl = result["accuracy"].tolist()
    communicationl = result["communication"].tolist()
    understandingl = result["understanding"].tolist()
    speedl = result["speed"].tolist()
    imgl = result["image"].tolist()

    pdf = FPDF()
    pdf.add_page()

    #set up of the header
    pdf.set_xy(0, 0)
    pdf.set_font('arial', 'B', 12)
    pdf.image(os.path.join("/Users/skwon/Documents/PDFmaker/Prepbox_logo2.png"), x = 15, y = 10, w = 40, h = 0, type = '', link = '')
    pdf.ln(25)
    #title
    pdf.cell(190, 10, "Grade Level Assessment Test Result for "+ student1.name, 0, 1,"C")
    #body
    pdf.set_font('arial', 'B', 9)
    #Summary part
    pdf.ln(5)
    pdf.cell(7)
    pdf.set_fill_color(91,155,213)
    pdf.set_text_color(255,255,255)
    pdf.cell(80, 5, "Level Test Summary", 0, 1, "L", fill=True)
    pdf.set_fill_color(0,0,0)
    pdf.set_text_color(0,0,0)
    pdf.set_font('arial', '', 9)
    pdf.cell(7)
    pdf.cell(50, 5, "Student Name:", 0, 0, 'L')
    pdf.cell(30, 5, student1.name, 0, 1, 'R')
    pdf.cell(7)
    pdf.cell(50, 5, "Student Grade:", 0, 0, 'L')
    pdf.cell(30, 5, str(student1.grade), 0, 1, 'R')
    pdf.cell(7)
    pdf.cell(50, 5, "Test Date:", 0, 0, 'L')
    pdf.cell(30, 5, str(student1.date), 0, 1, 'R')
    pdf.cell(7)
    pdf.cell(50, 5, "Tester:", 0, 0, 'L')
    pdf.cell(30, 5, str(student1.tester), 0, 1, 'R')
    pdf.ln(5)
    #The results
    pdf.set_font('arial', 'B', 9)
    pdf.set_fill_color(91,155,213)
    pdf.set_text_color(255,255,255)
    pdf.cell(7)
    pdf.cell(90, 5, "Subject", 0, 0, "L", fill=True)
    pdf.cell(30, 5, "Accuracy", 0, 0, "R", fill=True)
    pdf.cell(30, 5, "Proof of work", 0, 0, "R", fill=True)
    pdf.cell(30, 5, "Understanding", 0, 1, "R", fill=True)
    pdf.set_fill_color(0,0,0)
    pdf.set_text_color(0,0,0)
    pdf.set_font('arial', '', 10)
    for i in range(0,student1.question_count):
        pdf.cell(7)
        pdf.cell(90, 5, "Q"+str(i+1)+ ".: "+subjectl[i], 0, 0, "L")
        pdf.cell(30, 5, str(accuracyl[i]), 0, 0, "R")
        pdf.cell(30, 5, str(communicationl[i]), 0, 0, "R")
        pdf.cell(30, 5, str(understandingl[i]), 0, 1, "R")
    pdf.cell(7)
    pdf.set_font('arial', 'B', 9)
    pdf.cell(90, 5, "Total Score", "T", 0, "L")
    pdf.cell(30, 5, str(sum(accuracyl)), "T", 0, "R")
    pdf.cell(30, 5, str(sum(communicationl)), "T", 0, "R")
    pdf.cell(30, 5, str(sum(understandingl)), "T", 1, "R")

    pdf.cell(7)
    pdf.set_font('arial', '', 9)
    pdf.cell(90, 5, "Weight", 0, 0, "L")
    pdf.cell(30, 5, str(accu_weight), 0, 0, "R")
    pdf.cell(30, 5, str(commu_weight), 0, 0, "R")
    pdf.cell(30, 5, str(under_weight), 0, 1, "R")

    pdf.cell(7)
    pdf.set_font('arial', 'B', 9)
    pdf.cell(90, 5, "Total Weighted Score", "T", 0, "L")
    pdf.cell(30, 5, str(sum(accuracyl)*accu_weight), "T", 0, "R")
    pdf.cell(30, 5, str(sum(communicationl)*commu_weight), "T", 0, "R")
    pdf.cell(30, 5, str(sum(understandingl)*under_weight), "T", 1, "R")

    weighted_score = sum(accuracyl)*accu_weight + sum(communicationl)*commu_weight + sum(understandingl)*under_weight
    total_score = (accu_weight+commu_weight+under_weight)*student1.question_count
    weighted_score_percent = int((weighted_score/total_score)*100)
    accu_score = int(((sum(accuracyl)*accu_weight) / (student1.question_count*accu_weight))*100)
    commu_score = int(((sum(communicationl)*commu_weight) / (student1.question_count*commu_weight))*100)
    under_score = int(((sum(understandingl)*under_weight) / (student1.question_count*under_weight))*100)

    pdf.ln(5)
    pdf.cell(7)
    pdf.cell(140, 5, "Total Combined Score", 0, 0, "L")
    pdf.cell(40, 5, str(weighted_score_percent)+"%", 0, 1, "R")
    pdf.cell(7)
    pdf.cell(140, 5, "Time Spent", 0, 0, "L")
    pdf.cell(40, 5, str(sum(timel))+" minutes", 0, 1, "R")

    pdf.ln(5)
    pdf.set_font('arial', 'B', 9)
    pdf.set_fill_color(91,155,213)
    pdf.set_text_color(255,255,255)
    pdf.cell(7)
    pdf.cell(25, 5.5, " Category", 1, 0, "L", fill=True)
    pdf.cell(95, 5.5, str("Description"), 1, 0, "C", fill=True)
    pdf.cell(25, 5.5, str("Score"), 1, 0, "C", fill=True)
    pdf.cell(35, 5.5, str("Recommendation"), 1, 1, "C", fill=True)
    pdf.set_font('arial', '', 9)
    pdf.set_fill_color(255,255,255)
    pdf.set_text_color(0,0,0)
    pdf.cell(7)
    pdf.cell(25, 5.5, " Accuracy", 1, 0, "L")
    pdf.cell(95, 5.5, "Whether the answer was right or wrong", 1, 0, "C")
    pdf.cell(25, 5.5, str(accu_score)+"% "+str(sum(accuracyl)*accu_weight)+" / "+str(student1.question_count*accu_weight), 1, 0, "C")
    if accu_score < 90:
        pdf.cell(35, 5.5, str("Needs improvement"), 1, 1, "C")
    else:
        pdf.cell(35, 5.5, str("Satisfactory"), 1, 1, "C")
    pdf.cell(7)
    pdf.cell(25, 5.5, " Speed", 1, 0, "L")
    pdf.cell(95, 5.5, "How the long student took to complete", 1, 0, "C")
    pdf.cell(25, 5.5, str(speed)+" minutes", 1, 0, "C")
    if speed < 90:
        pdf.cell(35, 5.5, str("Needs improvement"), 1, 1, "C")
    else:
        pdf.cell(35, 5.5, str("Satisfactory"), 1, 1, "C")
    pdf.cell(7)
    pdf.cell(25, 5.5, " Communication", 1, 0, "L")
    pdf.cell(95, 5.5, "How clean the student shows proof of work and steps", 1, 0, "C")
    pdf.cell(25, 5.5, str(commu_score)+"% "+str(sum(communicationl)*commu_weight)+" / "+str(student1.question_count*commu_weight), 1, 0, "C")
    if commu_score > 90:
        pdf.cell(35, 5.5, str("Satisfactory"), 1, 1, "C")
    else:
        pdf.cell(35, 5.5, str("Needs improvement"), 1, 1, "C")
    pdf.cell(7)
    pdf.cell(25, 5.5, " Understanding", 1, 0, "L")
    pdf.cell(95, 5.5, "How much the student's work demonstrate clear understanding", 1, 0, "C")
    pdf.cell(25, 5.5, str(under_score)+"% "+str(sum(understandingl)*under_weight)+" / "+str(student1.question_count*under_weight), 1, 0, "C")
    if under_score > 90:
        pdf.cell(35, 5.5, str("Satisfactory"), 1, 1, "C")
    else:
        pdf.cell(35, 5.5, str("Needs improvement"), 1, 1, "C")
    pdf.ln(5)
    pdf.cell(7)
    pdf.set_fill_color(91,155,213)
    pdf.set_text_color(255,255,255)
    pdf.set_font('arial', 'B', 9)
    pdf.cell(25, 30, " Result", 1, 0, "L", fill=True)
    pdf.set_fill_color(255,255,255)
    pdf.set_text_color(0,0,0)
    pdf.set_font('arial', '', 9)
    pdf.cell(155, 30, student1.comment, 1, 0, "C")

    for i in range(0,student1.question_count):
        # Download the image
        getImage(imgl[i], i)
            
        pdf.add_page()
        pdf.image(str(i)+".jpg", x=15, y=15, w=150, h=150)


    pdf_data = pdf.output(dest='S').encode('latin1')
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="filename.pdf"'
    # pdf.output(response, 'F')
    return response


@csrf_exempt
def api_view(request):
    if request.method == 'POST':
        try:
            #    data = json.load(f)
            data = json.loads(request.body)
            response = generateReport(data)
            return response 
        except json.decoder.JSONDecodeError as e:
            return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def index(request):
    return HttpResponse("Hello, world. This is my Django app!")
