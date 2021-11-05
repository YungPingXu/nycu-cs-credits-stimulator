"""required function
required_list format:
required_list = {
	"course name1": [credits per semester, number of semesters],
	"course name2": [credits per semester, number of semesters],
	....
}"""
from werkzeug.datastructures import _unicodify_header_value


def required(course, required_credits, required_list, fset):
	result = ""
	finished_list = [] # every element is ["course name", credits per semester, the number of finished semesters]
	not_finished_list = [] # every element is ["course name", credits per semester, the number of finished semesters]
	finished_credits = 0
	not_finished_credits = 0
	for k, v in required_list.items():
		cnt = 0
		for i in course:
			if k in i[4]:
				cnt += 1
				fset.append(i[0])
		tmp = []
		tmp.append(k)
		tmp.append(v[0])
		tmp.append(cnt)
		finished_list.append(tmp)
		finished_credits += v[0] * cnt
		if cnt < v[1]:
			tmp = []
			tmp.append(k)
			tmp.append(v[0])
			tmp.append(v[1] - cnt)
			not_finished_list.append(tmp)
			not_finished_credits += v[0] * (v[1] - cnt)
	result += "必修: " + str(finished_credits) + " / " + str(required_credits) + " 學分 (總共還差 " + str(not_finished_credits) + " 學分)\n\n"
	result += "已通過之課程:"
	for i in finished_list:
		result += i[0] + " : " + str(i[1]) + " 學分 (已修完 " + str(i[2]) + " 個學期)\n"
	if not_finished_list:
		result += "\n未通過之課程:\n"
		for i in not_finished_list:
			result += i[0] + " : " + str(i[1]) + " 學分 (還差 " + str(i[2]) + " 個學期)\n"
	else:
		result += "\n已全數通過\n"
	renderlist = {
		"item": "必修", "finished_credits": finished_credits,
		"required_credits": required_credits,
		"finished_rate": int(round(finished_credits / required_credits, 2) * 100),
		"not_finished_credits": not_finished_credits,
		"finished": finished_list,
		"not_finished": not_finished_list
	}
	return renderlist

"""selective_required function
required_list format:
required_list = {
	"course category1": {
		"course name1": credits,
		"course name2": credits,
		....
	},
	"course category2": {
		"course name1": credits,
		"course name2": credits,
		....
	},
	"course category3": {
		"course name1": credits,
		"course name2": credits,
		....
	},
	....
}"""
def selective_required(course, required_credits, required_list, name, fset):
	result = ""
	resultlist = {}
	for i in required_list:
		resultlist[i] = {
			"finished_credits": 0,
			"finished_list": [], # every element is ["course name", credits]
			"not_finished_list": [], # every element is ["course name", credits]
		}
	for k, v in required_list.items():
		for i in v: # i is the key, i.e. course name
			passed = False
			for j in course:
				if i in j[4]:
					tmp = []
					tmp.append(i)
					tmp.append(int(float(j[6])))
					resultlist[k]["finished_list"].append(tmp)
					resultlist[k]["finished_credits"] += int(float(j[6]))
					passed = True
					fset.append(j[0])
					break
			if not passed:
				tmp = []
				tmp.append(i)
				tmp.append(v[i])
				resultlist[k]["not_finished_list"].append(tmp)
	total_passed = False
	passed_category = ""
	total_finished_credits = 0
	for k, v in resultlist.items():
		if v["finished_credits"] >= required_credits:
			passed_category = k
			total_passed = True
			break
	if total_passed:
		total_finished_credits = required_credits
	else:
		max = 0
		for k, v in resultlist.items():
			if v["finished_credits"] >= max:
				max = v["finished_credits"]
		total_finished_credits = max
	result += name + "必修: " + str(total_finished_credits) + " / " + str(required_credits) + " 學分 (總共還差 " + str(required_credits - total_finished_credits) + " 學分)\n\n"
	result += "已通過之課程:\n"
	for k, v in resultlist.items():
		for i in v["finished_list"]:
			result += i[0] + " : " + str(i[1]) + " 學分 (採計在 \"" + k + "\" 這組課程裡)\n"
	if total_passed:
		result += "\n已全數通過 (以 \"" + passed_category + "\" 這組課程採計)\n"
	else:
		result += "\n尚未通過之課程:\n"
		for k, v in resultlist.items():
			for i in v["not_finished_list"]:
				result += i[0] + " : " + str(i[1]) + " 學分 (採計在 \"" + k + "\" 這組課程裡)\n"
		for k, v in resultlist.items():
			result += "\n若想選擇 \"" + k + "\" 這組課程來採計，則仍需再修以下課程：\n"
			for i in v["not_finished_list"]:
				result += i[0] + " : " + str(i[1]) + " 學分\n"
	renderlist = {
		"item": name, "finished_credits": total_finished_credits,
		"required_credits": required_credits,
		"finished_rate": int(round(total_finished_credits / required_credits, 2) * 100),
		"not_finished_credits": required_credits -  total_finished_credits,
		"total_passed": total_passed,
		"passed_category": passed_category,
		"result": resultlist
	}
	return renderlist

"""special_required function
required_list format:
required_list = [
	["課名", 每學期幾學分, 學期數, "選別", "向度"],
	["選別", "向度", 每學期幾學分, 學期數],
]"""
def special_required(course, required_credits, required_semesters, required_list, name, fset):
	result = ""
	resultlist = {
		"basic": {
			"name": required_list[0][0],
			"required_credits": required_list[0][1] * required_list[0][2],
			"required_semesters": required_list[0][2],
			"finished_credits": 0,
			"not_finished_credits": 0,
			"finished_semesters": 0,
			"not_finished_semesters": 0,
			"finished_list": [],
			"not_finished_list": [],
		},
		"remain": {
			"name": required_list[1][0],
			"required_credits": required_list[1][1] * required_list[1][2],
			"required_semesters": required_list[1][2],
			"finished_credits": 0,
			"not_finished_credits": 0,
			"finished_semesters": 0,
			"not_finished_semesters": 0,
			"finished_list": [],
		}
	}
	finished_credits = 0
	finished_semesters = 0
	basic_set = set()
	for i in range(1, required_list[0][2] + 1):
		passed = False
		for j in course:
			if required_list[0][0] in j[4] and required_list[0][3] in j[5] and required_list[0][4] in j[12] and i == int(j[1][3]):
				tmp = []
				tmp.append(j[4])
				tmp.append(i)
				tmp.append(int(float(j[6])))
				resultlist["basic"]["finished_list"].append(tmp)
				resultlist["basic"]["finished_credits"] += int(float(j[6]))
				resultlist["basic"]["finished_semesters"] += 1
				finished_credits += int(float(j[6]))
				finished_semesters += 1
				basic_set.add(str(tmp))
				passed = True
				fset.append(j[0])
		if not passed:
			tmp = []
			tmp.append(required_list[0][0])
			tmp.append(i)
			tmp.append(required_list[0][1])
			resultlist["basic"]["not_finished_list"].append(tmp)
			resultlist["basic"]["not_finished_credits"] += required_list[0][1]
			resultlist["basic"]["not_finished_semesters"] += 1
	credits_cnt = 0
	semesters_cnt = 0
	remain_required_semesters = required_list[1][2]
	remain_required_credits = remain_required_semesters * required_list[1][1]
	for i in course:
		tmp = []
		tmp.append(i[4])
		tmp.append(int(i[1][3]))
		tmp.append(int(float(i[6])))
		if str(tmp) not in basic_set and required_list[1][0] == i[5]:
			resultlist["remain"]["finished_list"].append(tmp)
			if resultlist["remain"]["finished_credits"] < remain_required_credits:
				resultlist["remain"]["finished_credits"] += int(float(i[6]))
				finished_credits += int(float(i[6]))
			if resultlist["remain"]["finished_semesters"] < remain_required_semesters:
				resultlist["remain"]["finished_semesters"] += 1
				finished_semesters += 1
			credits_cnt += int(float(i[6]))
			semesters_cnt += 1
			fset.append(i[0])
	if semesters_cnt < remain_required_semesters or credits_cnt < remain_required_credits:
		resultlist["remain"]["not_finished_credits"] += remain_required_credits - credits_cnt
		resultlist["remain"]["not_finished_semesters"] += remain_required_semesters - semesters_cnt
	result += name + "必修: " + str(finished_credits) + " / " + str(required_credits) + " 學分 (" + str(finished_semesters) + " / " + str(required_semesters) + " 學期)\n"
	result += "總共還差 " + str(required_credits - finished_credits) + " 學分 (" + str(required_semesters - finished_semesters) + " / " + str(required_semesters) + " 學期)\n"
	semester = ["上學期", "下學期"]
	for k, v in resultlist.items():
		if k == "basic":
			result += "\n" + v["name"] + "必修: " + str(v["finished_credits"]) + " / " + str(v["required_credits"]) + " 學分 (" + str(v["finished_semesters"]) + " / " + str(v["required_semesters"]) + " 學期)\n"
			result += "還差" + str(v["not_finished_credits"]) + " 學分 (" + str(v["not_finished_semesters"]) + " 學期)\n\n"
			result += "已通過之課程:\n"
			for i in v["finished_list"]:
				result += i[0] + " : " + str(i[2]) + " 學分 (" + str(semester[i[1]-1]) + ")\n"
			if v["not_finished_semesters"]:
				result += "\n未通過之課程:\n"
				for i in v["not_finished_list"]:
					result += i[0] + " : " + str(i[2]) + " 學分 (" + str(semester[i[1]-1]) + ")\n"
			else:
				result += v["name"] + "必修已全數通過\n"
		elif k == "remain":
			result += "\n其餘" + v["name"] + "必修: " + str(v["finished_credits"]) + " / " + str(v["required_credits"]) + " 學分 (" + str(v["finished_semesters"]) + " / " + str(v["required_semesters"]) + "學期)\n"
			result += "還差 " + str(v["not_finished_credits"]) + " 學分 (" + str(v["not_finished_semesters"]) + " 學期)\n\n"
			result += "已通過之課程:\n"
			for i in v["finished_list"]:
				result += i[0] + " : " + str(i[2]) + " 學分\n"
			if v["not_finished_semesters"] == 0:
				result += "其餘" + v["name"] + "必修已全數通過\n"
	renderlist = {
		"item": name,
		"finished_credits": finished_credits,
		"required_credits": required_credits,
		"finished_semesters": finished_semesters,
		"required_semesters": required_semesters,
		"finished_rate": int(round(finished_semesters / required_semesters, 2) * 100),
		"not_finished_semesters": finished_semesters - finished_semesters,
		"result": resultlist
	}
	return renderlist

"""general_required function
required_list format:
required_list = {
	"general course category1": [required credits, {empty if no}],
	"general course category2": [required credits, {
		"course type1": required semesters,
		"course type2": required semesters,
		....
	}],
	"general course category3": [required credits, {empty if no}],
	....
}"""
def general_required(course, required_credits, required_list, fset):
	result = ""
	resultlist = {}
	for k, v in required_list.items():
		resultlist[k] = [{
			"required_credits": v[0],
			"finished_credits": 0,
			"not_finished_credits": 0,
			"finished_list": [], # every element is ["course name", credits]
		}, {}]
	for k, v in required_list.items():
		if v[1]:
			for course_type, credits in v[1].items():
				resultlist[k][1][course_type] = {
					"required_semesters": v[1][course_type],
					"finished_semesters": 0,
					"not_finished_semesters": 0,
					"finished_list": [], # every element is ["course name", credits]
			}
	finished_credits = 0
	for k, v in required_list.items():
		cnt = 0
		for i in course:
			if k in i[12]:
				credits = int(float(i[6]))
				tmp = []
				tmp.append(i[4])
				tmp.append(credits)
				resultlist[k][0]["finished_list"].append(tmp)
				resultlist[k][0]["finished_credits"] += credits
				cnt += credits
				finished_credits += credits
				if v[1]:
					for course_type, credits in v[1].items():
						if course_type in i[12]:
							resultlist[k][1][course_type]["finished_list"].append(tmp)
							resultlist[k][1][course_type]["finished_semesters"] += 1
				fset.append(i[0])
		if cnt < v[0]:
			resultlist[k][0]["not_finished_credits"] = v[0] - cnt
		if resultlist[k][0]["finished_credits"] > v[0]:
			resultlist[k][0]["finished_credits"] = v[0]
		if v[1]:
			for course_type, info in resultlist[k][1].items():
				if info["finished_semesters"] < v[1][course_type]:
					info["not_finished_semesters"] = v[1][course_type] - info["finished_semesters"]
				if info["finished_semesters"] > info["required_semesters"]:
					info["finished_semesters"] = info["required_semesters"]
	result += "通識必修: " + str(finished_credits) + " / " + str(required_credits) + " 學分 (總共還差 " + str(required_credits - finished_credits) + " 學分)\n"
	for k, v in resultlist.items():
		result += "\n" + k + ": " + str(v[0]["finished_credits"]) + " / " + str(v[0]["required_credits"]) + " 學分 (還差" + str(v[0]["not_finished_credits"]) + " 學分)\n\n"
		if v[0]["finished_credits"] > 0:
			if v[1]:
				for course_type, info in v[1].items():
					result += course_type + " : " + str(info["finished_semesters"]) + " / " + str(info["required_semesters"]) + " 門 (還差 " + str(info["not_finished_semesters"]) + " 門)\n"
					for i in info["finished_list"]:
						result += i[0] + " : " + str(i[1]) + " 學分\n"
					result += "\n"
			else:
				for i in v[0]["finished_list"]:
					result += i[0] + " : " + str(i[1]) + " 學分\n"
				result += "\n"
		result += k
		if v[0]["not_finished_credits"] == 0:
			result += "已全數通過\n"
		else:
			result += "還差 " + str(v[0]["not_finished_credits"]) + " 學分\n"
	renderlist = {
		"item": "通識必修", "finished_credits": finished_credits,
		"required_credits": required_credits,
		"finished_rate": int(round(finished_credits / required_credits, 2) * 100),
		"not_finished_credits": required_credits - finished_credits,
		"result": resultlist
	}
	return renderlist

def calculate(inputdata, student_class):
	result = {}
	rawdata = inputdata
	table = []
	tmp = rawdata.replace("（", "(").replace("）", ")").split("\n")
	for i in tmp:
		row = i.split("\t")
		table.append(row)
	course = []
	for i in table:
		try:
			if len(i) == 13 and i[7] != "" and i[8] != "" and i[10] != "" and (i[7] == "通過" or float(i[7]) >= 60.0):
				course.append(i)
		except ValueError:
			pass
	fset = []
	if student_class == "AB": # 資工組
		# 資訊工程組必修57學分:
		# 必修51學分 + 自然科學三組擇一必修6學分
		repeated_required_list = {
			"微積分甲(一)": [4, 1],
			"微積分甲(二)": [4, 1],
			"線性代數": [3, 1],
			"計算機概論與程式設計": [3, 1],
			"資料結構與物件導向程式設計": [3, 1],
			"離散數學": [3, 1],
			"數位電路設計": [3, 1],
			"機率": [3, 1],
			"演算法概論": [3, 1],
			"作業系統概論": [3, 1],
			"正規語言概論": [3, 1],
			"計算機組織": [3, 1],
			"資訊工程專題(一)": [2, 1],
			"資訊工程專題(二)": [2, 1],
			"生涯規劃及導師時間": [0, 2], # 0學分 2學期
			"服務學習(一)": [0, 1],
			"服務學習(二)": [0, 1],
			"資訊工程研討": [0, 1],
			"基礎程式設計": [0, 1],
			"藝文賞析教育": [0, 2], # 0學分 2學期
			"計算機網路概論": [3, 1],
			"微處理機系統實驗": [3, 1],
			"編譯器設計概論": [3, 1],
		}
		result["required"] = required(course, 51, repeated_required_list, fset)
		#result += required(course, 51, repeated_required_list, fset)
	elif student_class == "C": # 網多組
		# 網路與多媒體工程組必修57學分:
		# 必修42學分 + 領域專業課程兩組擇一必修9學分 + 自然科學三組擇一必修6學分
		repeated_required_list = {
			"微積分甲(一)": [4, 1],
			"微積分甲(二)": [4, 1],
			"線性代數": [3, 1],
			"計算機概論與程式設計": [3, 1],
			"資料結構與物件導向程式設計": [3, 1],
			"離散數學": [3, 1],
			"數位電路設計": [3, 1],
			"機率": [3, 1],
			"演算法概論": [3, 1],
			"作業系統概論": [3, 1],
			"正規語言概論": [3, 1],
			"計算機組織": [3, 1],
			"資訊工程專題(一)": [2, 1],
			"資訊工程專題(二)": [2, 1],
			"生涯規劃及導師時間": [0, 2], # 0學分 2學期
			"服務學習(一)": [0, 1],
			"服務學習(二)": [0, 1],
			"資訊工程研討": [0, 1],
			"基礎程式設計": [0, 1],
			"藝文賞析教育" : [0, 2], # 0學分 2學期
		}
		result["required"] = required(course, 42, repeated_required_list, fset)
		# result += required(course, 42, repeated_required_list, fset)
	elif student_class == "D": # 資電組
		# 資電工程組必修60學分:
		# 必修54學分 + 自然科學三組擇一必修6學分
		repeated_required_list = {
			"微積分甲(一)": [4, 1],
			"微積分甲(二)": [4, 1],
			"線性代數": [3, 1],
			"計算機概論與程式設計": [3, 1],
			"資料結構與物件導向程式設計": [3, 1],
			"離散數學": [3, 1],
			"數位電路設計": [3, 1],
			"演算法概論": [3, 1],
			"作業系統概論": [3, 1],
			"正規語言概論": [3, 1],
			"計算機組織": [3, 1],
			"資訊工程專題(一)": [2, 1],
			"資訊工程專題(二)": [2, 1],
			"生涯規劃及導師時間": [0, 2], # 0學分 2學期
			"服務學習(一)": [0, 1],
			"服務學習(二)": [0, 1],
			"資訊工程研討": [0, 1],
			"基礎程式設計": [0, 1],
			"藝文賞析教育" : [0, 2], # 0學分 2學期
			"微處理機系統實驗": [3, 1],
			"電路與電子學(一)": [3, 1],
			"編譯器設計概論": [3, 1],
			"訊號與系統": [3, 1],
			"嵌入式系統設計概論與實作": [3, 1],
			"編譯器設計概論": [3, 1],
			"數位電路實驗": [3, 1],
		}
		result["required"] = required(course, 54, repeated_required_list, fset)
		#result += required(course, 54, repeated_required_list, fset)
	#result += "--------------------------------------------\n"
	science_list = { # 擇一
		"物理": {
			"物理(一)": 3,
			"物理(二)": 3,
		},
		"普通生物": {
			"普通生物(一)": 3,
			"普通生物(二)": 3,
		},
		"化學": {
			"化學(一)": 3,
			"化學(二)": 3,
		},
	}
	result["science"] = selective_required(course, 6, science_list, "自然科學必修", fset)
	#result += selective_required(course, 6, science_list, "自然科學", fset)
	if student_class == "C":
		#result += "--------------------------------------------\n"
		field_list = { # 擇一
			"網路": {
				"計算機網路概論": 3,
				"網路程式設計概論": 3,
				"通訊原理與無線網路": 3,
			},
			"多媒體": {
				"數值方法": 3,
				"計算機圖學概論": 3,
				"影像處理概論": 3,
			}
		}
		#result += selective_required(course, 9, field_list, "領域專業課程", fset)
		result["field_required"] = selective_required(course, 9, field_list, "領域專業課程", fset)
	#result += "--------------------------------------------\n"
	# 通識
	general = {
		"校基本素養": [6, {}],
		"核心": [6, {
			"人文": 1, # 至少一門(2學分)
			"社會": 1, # 至少一門(2學分)
		}],
		"跨院基本素養": [2, {}],
	}
	result["general_required"] = general_required(course, 18, general, fset)
	#result += general_required(course, 18, general, fset)
	#result += "--------------------------------------------\n"
	PE = [ # 體育6學期
		["大一體育", 0, 2, "體育", "體育必修"], # 0學分 2學期
		["體育", 0, 4], # 向度: 體育必修 0學分 4學期
	]
	result["PE"] = special_required(course, 0, 6, PE, "體育", fset)
	#result += special_required(course, 0, 6, PE, "體育", fset)
	#result += "--------------------------------------------\n"
	foreign = [ # 外語
		["大一英文", 2, 2, "外語", "基礎"], # 2學分 2學期
		["外語", 2, 2], # 向度: 進階 2學分 2學期
	]
	result["english"] = special_required(course, 8, 4, foreign, "外語", fset)
	#result += special_required(course, 8, 4, foreign, "外語", fset)
	#result += "--------------------------------------------\n"
	fset = set(fset)
	# 專業選修30學分
	selective_required_credits = 30
	selective_finished = []
	selective_finished_credits = 0
	# 自由選修15學分
	free_required_credits = 15
	free_finished = []
	free_finished_credits = 0
	for i in course:
		if i[0] not in fset:
			if "軍訓" not in i[12]:
				if selective_finished_credits < selective_required_credits and ((i[3] == "資工系") or (i[5] == "大學部修研究所課程" and (i[3] in ("網工所", "數據所", "多媒體所", "資科工碩", "資科工博")))):
					tmp = []
					tmp.append(i[4])
					tmp.append(int(float(i[6])))
					selective_finished.append(tmp)
					selective_finished_credits += int(float(i[6]))
				else:
					tmp = []
					tmp.append(i[4])
					tmp.append(int(float(i[6])))
					free_finished.append(tmp)
					free_finished_credits += int(float(i[6]))
	#result += "專業選修: " + str(selective_finished_credits) + " / " + str(selective_required_credits) + "學分\n"
	#result += "已通過之課程:\n"
	result["selective"] = {
		"finished_credits": selective_finished_credits,
		"not_finished_credits": selective_required_credits - selective_finished_credits,
		"required_credits": selective_required_credits,
		"finished_rate": int(round(selective_finished_credits / selective_required_credits, 2) * 100),
		"finished": free_finished,
		"passed": False
	}
	if selective_required_credits <= selective_finished_credits:
		result["selective"]["passed"] = True
		result["selective"]["not_finished_credits"] = 0
		result["selective"]["finished_rate"] = 100
	result["free"] = {
		"finished_credits": free_finished_credits,
		"not_finished_credits": free_required_credits - free_finished_credits,
		"required_credits": free_required_credits,
		"finished_rate": int(round(free_finished_credits / free_required_credits, 2) * 100),
		"finished": free_finished,
		"passed": False
	}
	if free_required_credits <= free_finished_credits:
		result["free"]["passed"] = True
		result["free"]["not_finished_credits"] = 0
		result["free"]["finished_rate"] = 100
	'''for i in selective_finished:
		result += i[0] + " : " + str(i[1]) + " 學分\n"
	if selective_required_credits - selective_finished_credits > 0:
		result += "仍須再修 " + str(selective_required_credits - selective_finished_credits) + " 學分\n"
	else:
		result += "已符合專業選修30學分門檻\n"
	result += "--------------------------------------------\n"
	result += "自由選修: " + str(free_finished_credits) + " / " + str(free_required) + " 學分\n"
	result += "已通過之課程:\n"
	for i in free_finished:
		result += i[0] + " : " + str(i[1]) + " 學分\n"
	if free_required - free_finished_credits > 0:
		result += "仍須再修" + str(free_required - free_finished_credits) + " 學分\n"
	else:
		result += "已符合自由選修15學分門檻\n""'''
	return result