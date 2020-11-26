from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
from flask_cors import CORS
import numpy as np
import random

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

app.config['DBNAME'] = 'INFS740db'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/INFS740db'

mongo = PyMongo(app)

# return true or false depends on whether student satisifes CS530
def satisfiesCS530():
	db_operations_user = mongo.db.students
	sat = any([
		s["cs530_cond"] == "1" or
		s["cs530_cond"] == "2"
		for s in db_operations_user.find({}, {"_id": 0})
		])
	return (sat)

# return true or false depends on whether student satisifes CS531
def satisfiesCS531():
	db_operations_user = mongo.db.students
	sat = any([
		s["cs531_cond"] == "1" or s["cs531_cond"] == "2" 
		for s in db_operations_user.find({}, {"_id": 0})
		])
	return (sat)

# return true or false depends on whether student satisifes CS583
def satisfiesCS583(studyplan_list):
	stu_583 = any([ s["dcode"] == "CS" and s["cno"] == 583 and (s["grade"] == "A" or s["grade"] == "B") for s in studyplan_list])
	return (stu_583)

def satisfiesCS583_2(studyplan_list):
	stu_583 = any([ s["dcode"] == "CS" and s["cno"] == 583 for s in studyplan_list])
	return (stu_583)

def core_course(studyplan_list):
	db_operations_course = mongo.db.course

	list = [l
		for l in studyplan_list
		for c in db_operations_course.find({}, {"_id": 0})
		if l["dcode"] == c["dcode"] and l["cno"] == c["cno"] and c["core"] == 1 and (l["grade"] == "A" or l["grade"] == "B")
	]

	return list

def core_course_2(studyplan_list):
	db_operations_course = mongo.db.course

	list = [l
		for l in studyplan_list
		for c in db_operations_course.find({}, {"_id": 0})
		if l["dcode"] == c["dcode"] and l["cno"] == c["cno"] and c["core"] == 1
	]

	return list

def advanced_course(studyplan_list):
	db_operations_course = mongo.db.course

	list = [l
		for l in studyplan_list
		for c in db_operations_course.find({}, {"_id": 0})
		if l["dcode"] == c["dcode"] and l["cno"] == c["cno"] and c["advanced"] == 1 and (l["grade"] == "A" or l["grade"] == "B")
	]

	return list

def advanced_course_2(studyplan_list):
	db_operations_course = mongo.db.course

	list = [l
		for l in studyplan_list
		for c in db_operations_course.find({}, {"_id": 0})
		if l["dcode"] == c["dcode"] and l["cno"] == c["cno"] and c["advanced"] == 1
	]

	return list

def CS_course(studyplan_list):
	db_operations_course = mongo.db.course

	#return a list of advanced CS courses with grade b or above
	list = [l
		for l in studyplan_list
		for c in db_operations_course.find({}, {"_id": 0})
		if l["dcode"] == c["dcode"] and l["cno"] == c["cno"] and c["dcode"] == "CS" and (l["grade"] == "A" or l["grade"] == "B")
	]

	return list

def CS_course_2(studyplan_list):
	db_operations_course = mongo.db.course

	#return a list of advanced CS courses with grade b or above
	list = [l
		for l in studyplan_list
		for c in db_operations_course.find({}, {"_id": 0})
		if l["dcode"] == c["dcode"] and l["cno"] == c["cno"] and c["dcode"] == "CS"
	]

	return list

#return true or false depends on whether student satisifes core course requirements
def satisfiescorecourse(studyplan_list):
	
	list = core_course(studyplan_list)

	student_core_area = [ s["area"] for s in list ]

	#if core courses from less than three different areas, 
	if len(student_core_area) < 3:
		return False
	elif len(list) < 3:
		return False
	else:
		return True

def satisfiescorecourse_2(studyplan_list):
	
	list = core_course_2(studyplan_list)

	student_core_area = [ s["area"] for s in list ]

	#if core courses from less than three different areas, 
	if len(student_core_area) < 3:
		return False
	elif len(list) < 3:
		return False
	else:
		return True

def satisfiesadvancedcourse(studyplan_list):
	list = advanced_course(studyplan_list)

	student_advanced_cou_area = [ s["area"] for s in list]

	if len(student_advanced_cou_area) < 2:
		return False
	elif len(list) < 4:
		return False
	else:
		return True

def satisfiesadvancedcourse_2(studyplan_list):
	list = advanced_course_2(studyplan_list)

	student_advanced_cou_area = [ s["area"] for s in list]

	if len(student_advanced_cou_area) < 2:
		return False
	elif len(list) < 4:
		return False
	else:
		return True

def satisfiesCScourse(studyplan_list):
	list = CS_course(studyplan_list)

	list_2 = advanced_course(studyplan_list)

	cs_in_advanced = [ s["dcode"] == "CS" for s in list_2]

	if len(list) < 6:
		return False
	elif len(cs_in_advanced) <2:
		return False
	else:
		return True

def satisfiesCScourse_2(studyplan_list):
	list = CS_course_2(studyplan_list)

	list_2 = advanced_course_2(studyplan_list)

	cs_in_advanced = [ s["dcode"] == "CS" for s in list_2]

	if len(list) < 6:
		return False
	elif len(cs_in_advanced) <2:
		return False
	else:
		return True

def satisfiesPreapprovedcou(studyplan_list):
	if len(studyplan_list) < 8:
		return False
	else:
		return True

def get_course(dcode, cno):
	db_operations_course = mongo.db.course

	cou = [ s
	for s in db_operations_course.find({}, {"_id": 0})
	if s["dcode"] == dcode and s["cno"] == cno 
	]

	return cou

def prereq_cou_list(studyplan_list):
	db_operations_prereq = mongo.db.prereq
	db_operations_course = mongo.db.course

	prereq_list_set = {p["_id"]
		for p in db_operations_prereq.find({})
		for s in studyplan_list
		if s["dcode"] == p["pcode"] and s["cno"] == p["pno"]
	}

	prereq_list = [p
		for p in db_operations_prereq.find({})
		for p_id in prereq_list_set
		if p["_id"] == p_id
	]


	prereq_cou_list_set = {c["_id"]
		for c in db_operations_course.find({})
		for p in prereq_list
		if p["dcode"] == c["dcode"] and p["cno"] == c["cno"]
	}

	prereq_cou_list_id = [c
		for c in db_operations_course.find({})
		for c_id in prereq_cou_list_set
		if c["_id"] == c_id 
	]

	new_list = [{k: v for k, v in d.items() if k != '_id'} for d in prereq_cou_list_id]

	return new_list

def no_prereq_cou_list():
	db_operations_prereq = mongo.db.prereq
	db_operations_course = mongo.db.course
	db_operations_coprereq = mongo.db.coprereq

	co_prereq_list_set = {c["_id"]
		for c in db_operations_course.find({})
		for co in db_operations_coprereq.find({})

		if c["dcode"] == co["dcode"] and c["cno"] == co["cno"]
	}

	co_prereq_list = [c
		for c in db_operations_course.find({})
		for c_id in co_prereq_list_set
		if c["_id"] == c_id
	]

	prereq_list_set = {c["_id"]
		for c in db_operations_course.find({})
		for p in db_operations_prereq.find({})

		if c["dcode"] == p["dcode"] and c["cno"] == p["cno"]
	}

	prereq_list = [c
		for c in db_operations_course.find({})
		for c_id in prereq_list_set
		if c["_id"] == c_id
	]

	total_prereq_list_dup = prereq_list + co_prereq_list

	total_prereq_list = [dict(t) for t in {tuple(d.items()) for d in total_prereq_list_dup}]

	total_course_list = db_operations_course.find({})

	no_prereq_list = [item for item in total_course_list if item not in total_prereq_list]



	new_list = [{k: v for k, v in d.items() if k != '_id'} for d in no_prereq_list]

	return new_list

def studentSatCoursePrereqs(studyplan_list, dcode,cno):
	db_operations_coprereq = mongo.db.coprereq

	prereq_list = [p
		for p in db_operations_coprereq.find({}, {"_id": 0})

		if p["dcode"] == dcode and p["cno"] == cno

	]

	prereqsSatisfied = [s
		for p in prereq_list
		for s in studyplan_list

		if s["dcode"] == p["pcode"] and s["cno"] == p["pno"]
		]

	return prereqsSatisfied


def coprereq_list(studyplan_list):
	db_operations_coprereq = mongo.db.coprereq
	db_operations_course = mongo.db.course

	co_prereq_dup = [s
	for s in db_operations_coprereq.find({}, {"dcode": 1, "cno": 1, "_id": 0})]

	#list of all elements in coprereq collection
	co_prereq = [s
	for s in db_operations_coprereq.find({}, {"_id": 0})]

	# list of non dup coprereq course list
	co_prereq_list = [dict(t) for t in {tuple(d.items()) for d in co_prereq_dup}]

	co_prereq_cou = [c
		for c in co_prereq_list
		if len(studentSatCoursePrereqs(studyplan_list, c["dcode"], c["cno"])) == 2
	]

	co_prereq_cou_list = [co
		for c in co_prereq_cou
		for co in db_operations_course.find({}, {"_id": 0})

		if c["dcode"] == co["dcode"] and c["cno"] == co["cno"]
	]


	return co_prereq_cou_list

def total_prereq_list(studyplan_list):
	list_1 = prereq_cou_list(studyplan_list)
	list_2 = no_prereq_cou_list()
	list_3 = coprereq_list(studyplan_list)

	new_list = list_1 + list_2 + list_3

	return new_list


def get_core_course_by_area(area):
	db_operations_course = mongo.db.course

	list = [s
		for s in db_operations_course.find({}, {"_id": 0})
		if s["area"] == area and s["core"] == 1
	]

	return list

def get_CS_course_satisfies_prereq(studyplan_list):
	list_prereq = total_prereq_list(studyplan_list)

	list = [s
		for s in list_prereq
		if s["dcode"] == "CS"
	]

	return list

def get_advanced_course_satisfies_prereq(studyplan_list):
	list_prereq = total_prereq_list(studyplan_list)

	list = [s
		for s in list_prereq
		if s["advanced"] == 1
	]

	return list

def get_advanced_course_by_dcode_satisfies_prereq(studyplan_list, dcode):
	list_prereq = total_prereq_list(studyplan_list)

	list = [s
		for s in list_prereq
		if s["dcode"] == dcode and s["advanced"] == 1
	]

	return list

def get_advanced_course_by_area_satisfies_prereq(studyplan_list, area):
	list_prereq = total_prereq_list(studyplan_list)

	list = [s
		for s in list_prereq
		if s["area"] == area and s["advanced"] == 1
	]

	return list

def get_advanced_course_by_area_dcode_satisfies_prereq(studyplan_list, area, dcode):
	list_prereq = total_prereq_list(studyplan_list)

	list = [s
		for s in list_prereq
		if s["area"] == area and s["advanced"] == 1 and s["dcode"] == dcode
	]

	return list

def getallpassedcourse(studyplan_list):
	db_operations_course = mongo.db.course

	passed_list_set = {c["_id"]
		for s in studyplan_list
		for c in db_operations_course.find({})
		if s["dcode"] == c["dcode"] and s["cno"] == c["cno"] and (s["grade"] == "A" or s["grade"] == "B")
	}

	passed_list = [c
		for c in db_operations_course.find({})
		for c_id in passed_list_set
		if c["_id"] == c_id
	]

	new_list = [{k: v for k, v in d.items() if k != '_id'} for d in passed_list]

	return new_list


@app.route('/create', methods=['POST'])
def add_studyplan():
	db_operations_user = mongo.db.students
	data = request.get_json()
	db_operations_user.insert_one(data)
	res = jsonify('Successfully')
	return res


@app.route('/getallSP')
def getallStudyPlan():
	db_operations_user = mongo.db.students
	result = db_operations_user.distinct('studyPlans')
	res = dumps(result)
	return res

@app.route('/deleteallSP', methods=['DELETE'])
def deleteAllStudyPlan():
	db_operations_user = mongo.db.students
	db_operations_user.remove({})
	result = jsonify('Successfully')
	return result


@app.route('/getrecommendcourse')
def getrecommendedcou():
	db_operations_user = mongo.db.students
	sp = db_operations_user.distinct('studyPlans')
	cur_sp = getallpassedcourse(sp)
	recommend_list = []
	if not satisfiesCS530():
		cur_sp.extend(get_course("CS", 530))
		recommend_list.extend(get_course("CS", 530))

	if not satisfiesCS531():
		cur_sp.extend(get_course("CS", 531))
		recommend_list.extend(get_course("CS", 531))

	if not (satisfiesCS583_2(cur_sp) and satisfiesCS583(sp)):
		cur_sp.extend(get_course("CS", 583))
		recommend_list.extend(get_course("CS", 583))

	if not (satisfiescorecourse(sp) and satisfiescorecourse_2(cur_sp)):
		area =  [ s["area"] for s in core_course_2(cur_sp) ]
		i_area = db_operations_user.distinct('interestedArea')
		n_area = np.setdiff1d(i_area, area)
		course = []
		if len(n_area) == 2:
			course.append(random.choice(get_core_course_by_area(n_area[0])))
			course.append(random.choice(get_core_course_by_area(n_area[1])))
			cur_sp.extend(course)
			recommend_list.extend(course)
		else:
			course.append(random.choice(get_core_course_by_area(n_area[0])))
			cur_sp.extend(course)
			recommend_list.extend(course)

	
	if not (satisfiesadvancedcourse_2(cur_sp) and satisfiesadvancedcourse(sp)):
		area =  [ s["area"] for s in advanced_course_2(cur_sp) ]
		i_area = db_operations_user.distinct('interestedArea')
		n_area = np.setdiff1d(i_area, area)
		course = []
		new_course = []
		list_2 = advanced_course_2(cur_sp)
		cs_in_advanced = [ s["dcode"] == "CS" for s in list_2]

		if len(n_area) == 3:
			if len(cs_in_advanced) == 0:
				course.append(random.choice(get_advanced_course_by_area_dcode_satisfies_prereq(cur_sp, n_area[0], "CS")))
			else:
				course.append(random.choice(get_advanced_course_by_area_satisfies_prereq(cur_sp, n_area[0])))
			course.append(random.choice(get_advanced_course_by_area_satisfies_prereq(cur_sp, n_area[1])))
			course.append(random.choice(get_advanced_course_by_area_satisfies_prereq(cur_sp, n_area[2])))
			cur_sp.extend(course)
		elif len(n_area) == 2:
			if len(cs_in_advanced) == 0:
				course.append(random.choice(get_advanced_course_by_area_dcode_satisfies_prereq(cur_sp, n_area[0], "CS")))
			else:
				course.append(random.choice(get_advanced_course_by_area_satisfies_prereq(cur_sp, n_area[0])))
			course.append(random.choice(get_advanced_course_by_area_satisfies_prereq(cur_sp, n_area[1])))
			cur_sp.extend(course)
		else:
			if len(cs_in_advanced) == 0:
				course.append(random.choice(get_advanced_course_by_area_dcode_satisfies_prereq(cur_sp, n_area[0], "CS")))
			else:
				course.append(random.choice(get_advanced_course_by_area_satisfies_prereq(cur_sp, n_area[0])))
			cur_sp.extend(course)

		list_3 = advanced_course_2(cur_sp)

		while len(list_3) < 4:
			cou = random.choice(get_advanced_course_by_area_satisfies_prereq(cur_sp, n_area[0]))
			course.append(cou)
			cur_sp.append(cou)
			list_3 = advanced_course_2(cur_sp)
					
		recommend_list.extend(course)
		

	if not (satisfiesCScourse(sp) and satisfiesCScourse_2(cur_sp)):
		list_2 = advanced_course_2(cur_sp)
		cs_in_advanced = [ s["dcode"] == "CS" for s in list_2]
		course = []

		if len(cs_in_advanced) == 1:
			course.append(random.choice(get_advanced_course_by_dcode_satisfies_prereq(cur_sp, "CS")))
			cur_sp.extend(course)
			recommend_list.extend(course)
		elif len(cs_in_advanced) == 0:
			cou = random.choice(get_advanced_course_by_dcode_satisfies_prereq(cur_sp, "CS"))
			course.append(cou)
			cur_sp.extend(cou)
			cou_1 = random.choice(get_advanced_course_by_dcode_satisfies_prereq(cur_sp, "CS"))
			course.append(cou_1)
			cur_sp.extend(cou_1)
			recommend_list.extend(course)

		list_3 = CS_course_2(cur_sp)

		while len(list_3) < 6:
			cou = random.choice(get_CS_course_satisfies_prereq(cur_sp))
			course.append(cou)
			cur_sp.append(cou)

		recommend_list.extend(course)

	if not satisfiesPreapprovedcou(cur_sp):
		course = []
		while len(cur_sp) < 8:
			cou = random.choice(total_prereq_list(cur_sp))
			course.append(cou)
			cur_sp.extend(cou)

		recommend_list.extend(course)

	return dumps(recommend_list)



if __name__ == '__main__':
	app.run(debug=True)
