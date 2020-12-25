from json import dumps, loads
import data

goals = data.goals
teachers = data.teachers
objcts = {"goals": goals, "teachers": teachers}

with open("data.json", "w") as f:
    f.write(dumps(objcts))

with open("data.json", "r") as j:
    contents = j.read()

date = loads(contents)
