
from decimal import Decimal
import pyodbc
import datetime as dt
from datetime import datetime
from flask import Flask, render_template, request
app = Flask(__name__)

server = 'dheeraj1045.database.windows.net'
database = 'dheerajdb'
username = 'dheeraj'
password = 'Dheer@jkumar1045'
driver = '{ODBC Driver 17 for SQL Server}'

cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server +
                      ';PORT=1443;DATABASE='+database+';UID='+username+';PWD=' + password)
cursor = cnxn.cursor()


@app.route('/')
def main():
    return render_template('index.html')


classl = []


days = {}


@app.route('/students', methods=['POST', 'GET'])
def student():
    global classl
    global days
    dict = {}
    print("asdasd")
    if request.method == "POST":
        id = request.form['id']
        age = request.form['age']
        course = request.form['course']
        section = request.form['section']
        if(int(course) >= 5000):
            query = "SELECT age FROM [dbo].[students] WHERE id ="+id
            cursor.execute(query)
            res = cursor.fetchall()
            print(res[0][0])
            if (res[0][0] > int(age)):
                query2 = "SELECT * FROM [dbo].[class] WHERE Course =" + \
                    course + "And Section="+section+" And Max > 0"
                cursor.execute(query2)
                res2 = cursor.fetchall()
                print(res2)
                d = list(res2[0][2])
                print("dictionary")
                print(days)
                count = 0
                for i in d:
                    if i in days:
                        print(i)
                        if days[i] < 2:
                            days[i] = days[i]+1
                            print(count)
                            count = count+1
                    else:
                        print(i)
                        days[i] = 1
                        count = count+1
                if(count > 0):
                    dict['id'] = id
                    dict['cname'] = res2[0][0]
                    dict['section'] = res2[0][1]
                    dict['days'] = res2[0][2]
                    classl.append(dict)
        if(int(course) < 5000):
            query = "SELECT * FROM [dbo].[students] WHERE id ="+id
            cursor.execute(query)
            res = cursor.fetchall()
            print(res[0][0])
            if (res):
                query2 = "SELECT * FROM [dbo].[class] WHERE Course =" + \
                    course + "And Section="+section+" And Max > 0"
                cursor.execute(query2)
                res2 = cursor.fetchall()
                print(res2)
                d = list(res2[0][2])
                print(d)
                print(days)
                count = 0
                for i in d:
                    if i in days:
                        print(i)
                        if days[i] < 2:
                            days[i] = days[i]+1
                            print(count)
                            count = count+1
                    else:
                        print(i)
                        days[i] = 1
                        count = count+1
                if(count > 0):
                    dict['id'] = id
                    dict['cname'] = res2[0][0]
                    dict['section'] = res2[0][1]
                    dict['days'] = res2[0][2]
                    classl.append(dict)

    return render_template('student.html', data=classl)


courselist = []
di = {}


@app.route('/admin', methods=['POST', 'GET'])
def grade():
    if request.method == "POST":
        course = (request.form["course"])
        section = (request.form["section"])
        for i in range(len(classl)):
            print(classl)
            if(classl[i]['cname'] == course and classl[i]['section'] == section):
                print("true")
                query = "SELECT * FROM [dbo].[students] WHERE id=" + \
                    classl[i]['id']
                cursor.execute(query)
                res = cursor.fetchall()
                if res:
                    di['id'] = res[0][0]
                    di['name'] = res[0][1]
                    di['age'] = res[0][3]
                courselist.append(di)
    return render_template('teacher.html', data=courselist)


if __name__ == "__main__":
    app.run(debug=True)
