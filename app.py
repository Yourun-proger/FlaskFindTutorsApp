from json import dumps
from random import randint, shuffle
from flask import Flask, render_template, request
import get_json


app = Flask(__name__)
date = get_json.date
smr = {}
for teach in date["teachers"]:
    smr[teach["id"]] = teach
redays = {"mon": "Понедельник",
          "tue": "Вторник",
          "wed": "Среда",
          "thu": "Четверг",
          "fri": "Пятница",
          "sat": "Суббота",
          "sun": "Воскресение"
          }
books = {}
requests = {}

bi = 0
ri = 0


@app.route("/")
def main():
    gls = date["goals"]
    ml = []
    smr = []
    for i in range(7):
        x = randint(1, 12)
        if x not in ml:
            ml.append(x)
    for te in date["teachers"]:
        if te["id"] in ml:
            smr.append(te)
    return render_template("index.html", goals=gls, list=smr)


@app.route("/all")
def teachers():
    return render_template("all.html", list=date["teachers"])


@app.route("/all/sort/", methods=["POST"])
def sort_all():
    dct = {
        "1": ["price", True],
        "2": ["price", False],
        "3": ["rating", True],
        "4": "random"
    }
    atrs = dct[str(request.form.get("choose"))]
    shuffle(date["teachers"])
    return render_template("all_sort.html", atrs=atrs, teachers=date["teachers"], dct=dct, goals=date["goals"])


@app.route("/goals/<goal>/")
def goals(goal):
    my_list = []
    for teach in date["teachers"]:
        if goal in teach["goals"]:
            my_list.append(teach)
    return render_template("goal.html", smr=my_list, goal=date["goals"][goal])


@app.route("/profiles/<int:id>/")
def get_prof(id):
    table = smr[id]["free"]
    return render_template("profile.html", te=smr[id], goals=date["goals"], days=table, redays=redays)


@app.route("/request/")
def get_req():
    return render_template("request.html", goals=date["goals"])


@app.route("/request_done/", methods=["POST"])
def post_req():
    global ri
    name = request.form.get("clientName")
    phone = request.form.get("clientPhone")
    time = request.form.get("time")
    goal = date["goals"][request.form.get("goal")]
    requests[ri] = {"id": ri, "username": name, "phone": phone, "time": time, "goal": goal}
    ri += 1
    with open("request.json", "w") as f:
        f.write(dumps(requests))
    return render_template("request_done.html", name=name, phone=phone, time=time, goal=goal)


@app.route("/booking/<int:id>/<day>/<time>/")
def get_book(id, day, time):
    te = smr[id]
    return render_template("booking.html", te=te, day=day, time=time, rus=redays, id=id)


@app.route("/booking_done/", methods=["POST"])
def post_book():
    global bi
    name = request.form.get("clientName")
    phone = request.form.get("clientPhone")
    day = request.form.get("clientWeekday")
    time = request.form.get("clientTime")
    rendez_vous = str(redays[day] + ", " + time)
    books[bi] = {"id": bi,
                 "teacher": smr[int(request.form.get("clientTeacher"))],
                 "time": time,
                 "username": name,
                 "phone": phone,
                 "date": rendez_vous
                 }
    smr[int(request.form.get("clientTeacher"))]["free"][day][time] = False
    bi += 1
    with open("booking.json", "w") as f:
        f.write(dumps(books))
    return render_template("booking_done.html", name=name, phone=phone, date=rendez_vous)


if __name__ == '__main__':
    app.run()
