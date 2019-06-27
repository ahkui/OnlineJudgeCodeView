from django.shortcuts import render
from django.http import JsonResponse
from . import diff2HtmlCode
import numpy as np
import json
import copy

# Create your views here.
def codeView(request):
    return render(request, 'codeView.html')

def analysisView(request):
    return render(request, 'Analysis.html')
    
def getFrustrationData(request):
    def getSubmitAvgStd(oneQuestionJsonData):
        arr = [len(oneQuestionJsonData[user]['code']) for user in oneQuestionJsonData]
        arr = np.array(arr)
        avg = np.mean(arr)
        #std = np.std(arr,ddof=1)
        std = np.std(arr)
        return avg,std
    data = {}
    defaultDict = {}
    for contestID in [23,30,39,48,57,64,74]:
        defaultDict['%d_total'%(contestID)]=0
        defaultDict['%d_use'%(contestID)]=0
        defaultDict['%d_score'%(contestID)]=0
        defaultDict['avg']=0
    
    for contestID in [23,30,39,48,57,64,74]:
        filename = "json/contestData_%d.json"%(contestID)
        with open(filename,mode="r",encoding="utf8") as f:
            contestData = json.load(f)
        maxNumber = len(contestData)*5
        key = '%d_total'%(contestID)
        key_use = '%d_use'%(contestID)
        key_score = '%d_score'%(contestID)
        for Qid in contestData:
            avg,std = getSubmitAvgStd(contestData[Qid])
            
            for nid in contestData[Qid]:
                oneUser = [submit['result'] for submit in contestData[Qid][nid]['code']]
                if nid not in data:
                    data[nid] = copy.deepcopy(defaultDict)
                if len(oneUser)!=0:
                    data[nid][key_use] += 1
                    if 'Accepted' not in oneUser:
                        data[nid][key] += 2
                    else:
                        data[nid][key_score]+= 100/len(contestData)
                    
                    if len(oneUser) > avg + 3*std:
                        data[nid][key] += 3
                    elif len(oneUser) > avg + 2*std:
                        data[nid][key] += 2
                    elif len(oneUser) > avg + 1*std:
                        data[nid][key] += 1
                else:
                    data[nid][key] += 2
        for nid in data:
            if data[nid][key_use]!=0:
                data[nid][key]/=maxNumber
                data[nid][key]*=100
            else:
                data[nid][key]=-1
    
    stuInfo = getStudentInformation()
    needDrop = []
    for nid in data:
        try:
            info = stuInfo[nid]
        except:
            needDrop.append(nid)
            #print("NeedDrop:",nid)
        data[nid]['name'] = info['name']
        data[nid]['major'] = info['major']
        data[nid]['class'] = info['class']
        data[nid]['quit'] = info['quit']
        data[nid]['avg'] = np.mean(np.array([data[nid]['%d_total'%(contestID)] for contestID in [23,30,39,48,57,64,74] if data[nid]['%d_total'%(contestID)]!=-1]))
        data[nid]['avg_score'] = np.mean(np.array([data[nid]['%d_score'%(contestID)] for contestID in [23,30,39,48,57,64,74] if data[nid]['%d_total'%(contestID)]!=-1]))
    for nid in needDrop:
        del data[nid]
    return JsonResponse(data)

def mutiCodeView(request):
    try:
        contest = request.POST["contest_id"]
        question = request.POST["question_id"]
        student = request.POST["student_id"].split(",")
    except:
        return render(request,'mutiCodeView.html')
    studentInfo = getStudentInformation()
    context = {'data': [],'contest_id':contest,'question_id':question,'student_id':student} 
    with open('json/contestData_%s.json'%(contest),encoding='utf8',mode='r') as file:
            data = json.load(file)
    for nid in student:
        user = data[str(question)][str(nid)];
        try:
            info = studentInfo[nid]
        except:
            info={
                'name':'',
                'major':'',
                'class':''
            }
        code1 = user['code'][0]
        if len(user['code'])>1:
            code2 = user['code'][1]
        else:
            code2={'id':"",
                'result':"",
                'time':"",
                'ip':"",
                'code':""}
        with open('codeView/f1.py',mode='w',encoding='utf8')as f:
            f.write(code1['code'])
        with open('codeView/f2.py',mode='w',encoding='utf8')as f:
            f.write(code2['code'])
        paser = diff2HtmlCode.CodeDiff('codeView/f1.py','codeView/f2.py')
        leftCode = []
        for ele in paser.getOneDiff():
            leftCode.append(ele)
        rightCode = []
        for ele in paser.getOneDiff(left=False):
            rightCode.append(ele)
        
        sdata = {'nid':nid,
                'username':info['name'],
                'major':info['major'],
                'class':info['class'],
                'totalSubmit':len(user['code']),
                'leftSubmit':1,
                'leftResult':code1['result'],
                'leftTime':code1['time'],
                'leftCode':leftCode,
                'rightSubmit':2,
                'rightResult':code2['result'],
                'rightTime':code2['time'],
                'rightCode':rightCode
                }
        context['data'].append(sdata)
    return render(request,'mutiCodeView.html',context)

def bad_request(request, exception, template_name='errors/page_400.html'):
    return render(request, template_name)
    
def server_error(request, template_name='errors/page_400.html'):
    return render(request, template_name)
    
def getFiles(path):
    pass

def getcode(request):
    contest = str(request.POST.get('contest'))
    qid = str(request.POST.get('qid'))
    lnid = str(request.POST.get('lnid'))
    lidx = int(request.POST.get('lidx'))-1
    rnid = str(request.POST.get('rnid'))
    ridx = int(request.POST.get('ridx'))-1
    with open('json/contestData_%s.json'%(contest),encoding='utf8',mode='r') as file:
        data = json.load(file)
    try:
        user1 = data[qid][lnid]
        code1 = user1['code'][lidx]
    except IndexError as e:
        code1={'id':"",
            'result':"",
            'time':"",
            'ip':"",
            'code':""}
        print(e," : code1")
    try:
        user2 = data[qid][rnid]
        code2 = user2['code'][ridx]
    except IndexError as e:
        code2={'id':"",
            'result':"",
            'time':"",
            'ip':"",
            'code':""}
        print(e," : code2")
        
    with open('codeView/f1.py',mode='w',encoding='utf8')as f:
        f.write(code1['code'])
    with open('codeView/f2.py',mode='w',encoding='utf8')as f:
        f.write(code2['code'])
    paser = diff2HtmlCode.CodeDiff('codeView/f1.py','codeView/f2.py')
    leftHtml = ""
    for ele in paser.getOneHtml():
        leftHtml+=ele
    rightHtml = ""
    for ele in paser.getOneHtml(left=False):
        rightHtml+=ele
    left = {'id':code1['id'],
            'result':code1['result'],
            'time':code1['time'],
            'ip':code1['ip'],
            'code':leftHtml
            }
    right = {'id':code2['id'],
            'result':code2['result'],
            'time':code2['time'],
            'ip':code2['ip'],
            'code':rightHtml
            }
    return JsonResponse({'left':left,'right':right})
 
def getAllStudent(request):
    contest = str(request.POST.get('contest'))
    pid = str(request.POST.get('pid'))
    with open('json/contestData_%s.json'%(contest),encoding='utf8',mode='r') as file:
        data = json.load(file)
    try:
        ret = {}
        userlist = sorted(data[pid].keys())
        inClassStudent = getStudentInformation()
        wantDelStudent = []
        for user in userlist:
            ret[user] = [ele['result'] for ele in data[pid][user]['code']]
            if user not in inClassStudent:
                wantDelStudent.append(user)
        for user in wantDelStudent:
            del ret[user]
    except e:
        print(e)
    return JsonResponse(ret)
    
def getProblemList(request):
    with open('json/contestProblem.json',encoding='utf8',mode='r') as file:
        data = json.load(file)
    return JsonResponse(data)
    
def getStudentInformation():
    student={}
    with open("json/1072Python_name.csv",encoding="utf8",mode="r") as f:
        for line in f:
            line = line.split(',')
            student[line[0].lower()] = {'name':line[1],'class':line[2],'major':line[5],'quit':"X"}
    with open("json/quit.csv",encoding="utf8",mode="r") as f:
        for line in f:
            line = line.split(',')
            if line[0] in student:
                student[line[0]]['quit'] = '第 %02d 週'%(int(line[1]))
    #print(student)
    return student
