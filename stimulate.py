course_type_col_num = 10 # 向度

"""
required_list format:
required_list = {
    "course name1": [credits per semester, number of semesters],
    "course name2": [credits per semester, number of semesters],
    ....
}
"""
def required(course, required_credits, required_list, fset):
    result = {
        "item": "必修",
        "finished_credits": 0,
        "not_finished_credits": 0,
        "required_credits": required_credits,
        "finished_rate": 0,
        "finished": [],
        "not_finished": [] # every element is ["course name", credits per semester, the number of finished semesters]
    }
    for k, v in required_list.items():
        cnt = 0
        for i in course:
            if k in i[4]:
                cnt += 1
                result["finished"].append(i)
                fset.append(i[0])
        result["finished_credits"] += v[0] * cnt
        if cnt < v[1]:
            tmp = []
            tmp.append(k)
            tmp.append(v[0])
            tmp.append(v[1] - cnt)
            result["not_finished"].append(tmp)
            result["not_finished_credits"] += v[0] * (v[1] - cnt)
    result["finished_rate"] = int(round(result["finished_credits"] / required_credits, 2) * 100)
    print(result)
    return result

"""
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
}
"""
def selective_required(course, required_credits, required_list, name, fset):
    result = {
        "item": name,
        "finished_credits": 0,
        "not_finished_credits": 0,
        "required_credits": required_credits,
        "finished_rate": 0,
        "passed": False,
        "passed_category": "",
        "result": {}
    }
    for i in required_list:
        result["result"][i] = {
            "finished_credits": 0,
            "finished": [], # every element is ["course name", credits]
            "not_finished": [], # every element is ["course name", credits]
        }
    for k, v in required_list.items():
        for i in v: # i is the key, i.e. course name
            passed = False
            for j in course:
                if i in j[4]:
                    result["result"][k]["finished"].append(j)
                    result["result"][k]["finished_credits"] += int(float(j[6]))
                    passed = True
                    #fset.append(j[0])
                    break
            if not passed:
                tmp = []
                tmp.append(i)
                tmp.append(v[i])
                result["result"][k]["not_finished"].append(tmp)
    for k, v in result["result"].items():
        if v["finished_credits"] >= required_credits:
            result["passed_category"] = k
            result["passed"] = True
            break
    if result["passed"]:
        result["finished_credits"] = required_credits
        for k, v in result["result"].items():
            if k == result["passed_category"]:
                for i in v["finished"]:
                    fset.append(i[0])
            else:
                break
    else:
        max = 0
        for k, v in result["result"].items():
            if v["finished_credits"] >= max:
                max = v["finished_credits"]
        result["finished_credits"] = max
        for k, v in result["result"].items():
            for i in v["finished"]:
                fset.append(i[0])
    result["not_finished_credits"] = required_credits -  result["finished_credits"]
    result["finished_rate"] = int(round(result["finished_credits"] / required_credits, 2) * 100)
    print(result)
    return result

"""
required_list format:
required_list = [
    ["課名", 每學期幾學分, 學期數, "選別", "向度"],
    ["選別", "向度", 每學期幾學分, 學期數],
]
"""
def special_required(course, required_credits, required_semesters, required_list, name, fset):
    result = {
        "item": name,
        "finished_credits": 0,
        "required_credits": required_credits,
        "finished_semesters": 0,
        "required_semesters": required_semesters,
        "finished_rate": 0,
        "not_finished_semesters": 0,
        "result": {
            "basic": {
                "name": required_list[0][0],
                "required_credits": required_list[0][1] * required_list[0][2],
                "required_semesters": required_list[0][2],
                "finished_credits": 0,
                "not_finished_credits": 0,
                "finished_semesters": 0,
                "not_finished_semesters": 0,
                "finished": [],
                "not_finished": [],
            },
            "remain": {
                "name": required_list[1][0],
                "required_credits": required_list[1][1] * required_list[1][2],
                "required_semesters": required_list[1][2],
                "finished_credits": 0,
                "not_finished_credits": 0,
                "finished_semesters": 0,
                "not_finished_semesters": 0,
                "finished": [],
            }
        }
    }
    basic_set = set()
    for i in range(1, required_list[0][2] + 1):
        passed = False
        for j in course:
            if required_list[0][0] in j[4] and required_list[0][3] in j[5] and required_list[0][4] in j[course_type_col_num] and i == int(j[1][3]):
                result["result"]["basic"]["finished"].append(j)
                result["result"]["basic"]["finished_credits"] += int(float(j[6]))
                result["result"]["basic"]["finished_semesters"] += 1
                result["finished_credits"] += int(float(j[6]))
                result["finished_semesters"] += 1
                tmp = []
                tmp.append(j[4])
                tmp.append(i)
                tmp.append(int(float(j[6])))
                basic_set.add(str(tmp))
                passed = True
                fset.append(j[0])
        if not passed:
            tmp = []
            tmp.append(required_list[0][0])
            tmp.append(i)
            tmp.append(required_list[0][1])
            result["result"]["basic"]["not_finished"].append(tmp)
            result["result"]["basic"]["not_finished_credits"] += required_list[0][1]
            result["result"]["basic"]["not_finished_semesters"] += 1
    credits_cnt = 0
    semesters_cnt = 0
    remain_required_semesters = required_list[1][2]
    remain_required_credits = remain_required_semesters * required_list[1][1]
    for i in course:
        tmp = []
        tmp.append(i[4])
        tmp.append(int(i[1][3]))
        tmp.append(int(float(i[6])))
        if str(tmp) not in basic_set and required_list[1][0] == i[5] \
        and result["result"]["remain"]["finished_semesters"] < result["result"]["remain"]["required_semesters"]:
            result["result"]["remain"]["finished"].append(i)
            if result["result"]["remain"]["finished_credits"] < remain_required_credits:
                result["result"]["remain"]["finished_credits"] += int(float(i[6]))
                result["finished_credits"] += int(float(i[6]))
            if result["result"]["remain"]["finished_semesters"] < remain_required_semesters:
                result["result"]["remain"]["finished_semesters"] += 1
                result["finished_semesters"] += 1
            credits_cnt += int(float(i[6]))
            semesters_cnt += 1
            fset.append(i[0])
    if semesters_cnt < remain_required_semesters or credits_cnt < remain_required_credits:
        result["result"]["remain"]["not_finished_credits"] += remain_required_credits - credits_cnt
        result["result"]["remain"]["not_finished_semesters"] += remain_required_semesters - semesters_cnt
    result["finished_rate"] = int(round(result["finished_semesters"] / required_semesters, 2) * 100)
    result["not_finished_semesters"] = required_semesters - result["finished_semesters"]
    print(result)
    return result

"""
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
}
"""
def general_required(course, required_credits, required_list, fset):
    result = {
        "item": "通識必修",
        "finished_credits": 0,
        "required_credits": required_credits,
        "finished_rate": 0,
        "not_finished_credits": 0,
        "result": {}
    }
    for k, v in required_list.items():
        result["result"][k] = [{
            "required_credits": v[0],
            "finished_credits": 0,
            "not_finished_credits": 0,
            "finished": [],
        }, {}]
    for k, v in required_list.items():
        if v[1]:
            for course_type, credits in v[1].items():
                result["result"][k][1][course_type] = {
                    "required_semesters": v[1][course_type],
                    "finished_semesters": 0,
                    "not_finished_semesters": 0,
                    "finished": [],
                }
    for k, v in required_list.items():
        cnt = 0
        for i in course:
            if k in i[course_type_col_num]:
                credits = int(float(i[6]))
                result["result"][k][0]["finished"].append(i)
                result["result"][k][0]["finished_credits"] += credits
                cnt += credits
                result["finished_credits"] += credits
                if v[1]:
                    for course_type, credits in v[1].items():
                        if course_type in i[course_type_col_num]:
                            result["result"][k][1][course_type]["finished"].append(i)
                            result["result"][k][1][course_type]["finished_semesters"] += 1
                fset.append(i[0])
        if cnt < v[0]:
            result["result"][k][0]["not_finished_credits"] = v[0] - cnt
        if result["result"][k][0]["finished_credits"] > v[0]:
            result["result"][k][0]["finished_credits"] = v[0]
        if v[1]:
            for course_type, info in result["result"][k][1].items():
                if info["finished_semesters"] < v[1][course_type]:
                    info["not_finished_semesters"] = v[1][course_type] - info["finished_semesters"]
                if info["finished_semesters"] > info["required_semesters"]:
                    info["finished_semesters"] = info["required_semesters"]
    result["finished_rate"] = int(round(result["finished_credits"] / required_credits, 2) * 100)
    result["not_finished_credits"] = required_credits - result["finished_credits"]
    print(result)
    return result

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
            if len(i) == 11 and i[7] != "" and i[8] != "" and (i[7] == "通過" or i[7] in ("A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-")):
                credits = int(float(i[6]))
                i[6] = credits
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
    if student_class == "C":
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
        result["field_required"] = selective_required(course, 9, field_list, "領域專業課程", fset)
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
    PE = [ # 體育6學期
        ["大一體育", 0, 2, "體育", "體育必修"], # 0學分 2學期
        ["體育", 0, 4], # 向度: 體育必修 0學分 4學期
    ]
    result["PE"] = special_required(course, 0, 6, PE, "體育", fset)
    foreign = [ # 外語
        ["大一英文", 2, 2, "外語", "基礎"], # 2學分 2學期
        ["外語", 2, 2], # 向度: 進階 2學分 2學期
    ]
    result["english"] = special_required(course, 8, 4, foreign, "外語", fset)
    
    credits_replace = False
    physics_first = False
    physics_second = False
    for i in course:
        if "物理(一)" in i[4]:
            physics_first = True
        if "物理(二)" in i[4]:
            physics_second = True
    if physics_first and physics_second:
        credits_replace = True

    fset = set(fset)
    # 專業選修30學分
    result["selective"] = {
        "finished_credits": 0,
        "not_finished_credits": 0,
        "required_credits": 30,
        "finished_rate": 0,
        "finished": [],
        "passed": False
    }
    # 自由選修11學分
    result["free"] = {
        "finished_credits": 0,
        "not_finished_credits": 0,
        "required_credits": 11,
        "finished_rate": 0,
        "finished": [],
        "passed": False
    }
    # 若選修物理(一)(二)，共計 8 學分，則可減少專業選修或自由選修學分 2 學分
    if credits_replace:
        result["free"]["finished_credits"] += 2
        result["free"]["finished"].append(["", "", "", "", "物理(一)(二) 抵免", "", "2", "", "", "", "", "", ""])
    # 其他選修4學分
    result["other_free"] = {
        "finished_credits": 0,
        "not_finished_credits": 0,
        "required_credits": 4,
        "finished_rate": 0,
        "finished": [],
        "passed": False
    }

    for i in course:
        if i[0] not in fset:
            # 專業選修30學分
            if result["selective"]["finished_credits"] < result["selective"]["required_credits"] \
            and ((i[3] == "資工系") or (i[5] == "大學部修研究所課程" and (i[3] in ("網工所", "數據所", "多媒體所", "資科工碩", "資科工博")))) \
            and result["selective"]["finished_credits"] < result["selective"]["required_credits"]:
                result["selective"]["finished"].append(i)
                result["selective"]["finished_credits"] += i[6]
            else:
                if "軍訓" not in i[5] and "護理" not in i[5] and "體育" not in i[5]:
                    if "通識" not in i[5] and result["free"]["finished_credits"] < result["free"]["required_credits"]: # 自由選修11學分
                        result["free"]["finished"].append(i)
                        result["free"]["finished_credits"] += i[6]
                    else: # 其他選修4學分
                        result["other_free"]["finished"].append(i)
                        result["other_free"]["finished_credits"] += i[6]
    result["selective"]["not_finished_credits"] = result["selective"]["required_credits"] - result["selective"]["finished_credits"]
    result["free"]["not_finished_credits"] = result["free"]["required_credits"] - result["free"]["finished_credits"]
    result["other_free"]["not_finished_credits"] = result["other_free"]["required_credits"] - result["other_free"]["finished_credits"]
    
    result["selective"]["finished_rate"] = int(round(result["selective"]["finished_credits"] / result["selective"]["required_credits"], 2) * 100)
    result["free"]["finished_rate"] = int(round(result["free"]["finished_credits"] / result["free"]["required_credits"], 2) * 100)
    result["other_free"]["finished_rate"] = int(round(result["other_free"]["finished_credits"] / result["other_free"]["required_credits"], 2) * 100)
    
    if result["selective"]["required_credits"] <= result["selective"]["finished_credits"]:
        result["selective"]["passed"] = True
        result["selective"]["finished_credits"] = result["selective"]["required_credits"]
        result["selective"]["not_finished_credits"] = 0
        result["selective"]["finished_rate"] = 100
    
    if result["free"]["required_credits"] <= result["free"]["finished_credits"]:
        result["free"]["passed"] = True
        result["free"]["finished_credits"] = result["free"]["required_credits"]
        result["free"]["not_finished_credits"] = 0
        result["free"]["finished_rate"] = 100
    
    if result["other_free"]["required_credits"] <= result["other_free"]["finished_credits"]:
        result["other_free"]["passed"] = True
        result["other_free"]["finished_credits"] = result["other_free"]["required_credits"]
        result["other_free"]["not_finished_credits"] = 0
        result["other_free"]["finished_rate"] = 100
    return result