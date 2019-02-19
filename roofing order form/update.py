from flask import Flask, request
import fileinput

app = Flask(__name__)

@app.route('/',methods=['GET'])
def base():
  if request.method=='GET':
    return app.send_static_file('index.html')
  else: pass
  
@app.route('/quote',methods=['POST'])
def quote():
  if request.method=='POST':
    if request.form['email'] and request.form['password']:
      if (True):
        return app.send_static_file('quote.html')
      else: return app.send_static_file('index.html')
  else: return app.send_static_file('index.html')
      
#display quote
@app.route('/result',methods=['POST'])
def result():
  if request.method=='POST':
    #init
    pdict={'0':1,
           '1':1.01,
           '2':1.02,
           '3':1.03,
           '4':1.05,
           '5':1.08,
           '6':1.12,
           '7':1.16,
           '8':1.2,
           '9':1.25,
          '10':1.3,
          '11':1.36,
          '12':1.41}
    #elementary error detection
    errors=''
    if request.form['sqft1']:
      sqft1=float(request.form['sqft1'])
    else:
      errors+='Square Feet (1st Entry)

'
    if request.form['pitch1']:
      pitch1=request.form['pitch1']
    else:
      errors+='Pitch (2nd Entry)

'
    if request.form['sqft2']:
      sqft2=float(request.form['sqft2'])
    else:
      errors+='Square Feet (3rd Entry)

'
    if request.form['pitch2']:
      pitch2=request.form['pitch2']
    else:
      errors+='Pitch (4th Entry)

'
    if request.form['osb']:
      osb=float(request.form['osb'])
    else:
      errors+='OSB (5th Entry)

'
    if request.form['fas']:
      fas=request.form['fas']
    else:
      errors+='Fascia (6th Entry)

'
    if request.form['hips']:
      hips=request.form['hips']
    else:
      errors+='Hips (5th Entry)

'
    if request.form['mats']:
      mats=request.form['mats']
    else:
      errors+='Panels (6th Entry)

'
    if request.form['under']:
      under=request.form['under']
    else:
      errors+='Underlayment (7th Entry)

'
    if request.form['roof']:
      roof=request.form['roof']
    else:
      errors+='Reroof/Roofover (8th Entry)

'
    #if no errors, calculate quote
    if errors=='':
      calc1='%.2f'%sqft1
      calc1=float(calc1)
      #by the bundle
      if calc1%.5!=0:
        if calc1/.5%2==0:
          calc1=float(int(calc1)+.5)
        else: calc1=float(int(calc1)+1)
      calc1*=pdict[pitch1]
      calc2='%.2f'%sqft2
      calc2=float(calc2)
      #by the bundle
      if calc2%.5!=0:
        if calc2/.5%2==0: calc2=float(int(calc2)+.5)
        else: calc2=float(int(calc2)+1)
      calc2*=pdict[pitch2]
      calc=calc1+calc2
      ppsq=0
      if hips=='gable':
        calc*=1.1
        ppsq+=125
      elif hips=='hips':
        calc*=1.05
        ppsq+=150
      elif hips=='hipsp':
        calc*=1.15
        ppsq+=200
      if mats=='tcm': ppsq+=700
      elif mats=='five': ppsq+=600
      elif mats=='ult': ppsq+=500
      if under=='rad': ppsq+=100
      elif under=='stk': ppsq+=50
      if roof=='reroof': ppsq+=100
      cost=calc*ppsq/100
      cost+=osb*80
      cost+=fas*5.5
      cost='%.2f'%(cost)
      with open('static/resultbase.html', 'r') as f:
        tempdata = f.read()
      tempdata = tempdata.replace('0', str(cost))
      print(str(cost))
      with open('static/result.html', 'w') as f:
        f.write(tempdata)
      return app.send_static_file('result.html')
    #if there are any errors
    else:
      print('Please fill out the following:/n/n'+errors)
      return app.send_static_file('index.html')

if __name__ == '__main__':
  app.run(host='50.193.164.153', port=80)
