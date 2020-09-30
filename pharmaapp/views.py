from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.db import connection
from django.core.mail import EmailMessage
from datetime import date
import json

from django.db import connection
from django.core.files.storage import FileSystemStorage

from datetime import datetime,date

def updatedata(sql):
    try:
        c=connection.cursor()
        c.execute(sql)
        c.close()
        return True
    except:
        return False
    
def getdata(sql,single=False):
    try:
        l=[]
        c=connection.cursor()
        c.execute(sql)
        col=list(i[0] for i in c.description)
        if not single:
            r=c.fetchall()
            if r:
                l=list(dict(zip(col,i))for i in r)
        else:
            r=c.fetchone()
            if r:
                l=dict(zip(col,r))
            print(l)
        c.close()
        return l,''
    except Exception as e:
        print('error.....',str(e))
        return l,str(e)

##def getuser(request):
##    
##    if request.session.has_key('unam'):
##        return request.session['unam']
##    return {}
def getrole(request):
    role=None
    if request.session.has_key('role'):
        role=request.session['role']
    return role

# Create your views here.
def index(request):
    temp1=loader.get_template('index.html')
    role=0
    if request.session.has_key('role'):
        role=request.session['role']
    return HttpResponse(temp1.render({'role':role},request))    
def getuser(request):
    if request.session.has_key('unam'):
        return request.session['unam']
    return {}


def about(request):
    temp1=loader.get_template('about.html')
    
    return HttpResponse(temp1.render({},request))
def contact1(request):
    usr=getuser(request)
    uid=request.session['uid']
    print("uid ",uid)
    d,err=getdata(f"select * from usertab where uid={uid}",True)    
    print("ffffffffffffffff",d)
    if request.method=='POST':
        
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        
        c=connection.cursor()
        c.execute(f"INSERT INTO feedbacktab(fdate,fname,uid,fstatus) VALUES(date('now'),'{name}',{uid},'{message}')")
        

    templ=loader.get_template('contact1.html')
    return HttpResponse(templ.render({"usr":getuser(request),'data':d},request))

def customerlogin(request):
    templ=loader.get_template('customerlogin.html')
    return HttpResponse(templ.render({},request))
def customersignup(request):
    templ=loader.get_template('customersignup.html')
    return HttpResponse(templ.render({},request))
def adminlogin(request):
    stat=""
    role=None
    if request.method=='POST':
        adnam=request.POST['adid']
        pwd=request.POST['adpwd']
        utyp=request.POST['usertype']
        adnam=adnam.replace("'","#'")
       
        #print('user type:',utyp)
        if utyp=='1':
            sql=f"SELECT * FROM admintab where adname='{adnam}' and adpwd='{pwd}'"
        elif utyp=='2':
            sql=f"SELECT * FROM pharmacisttab where pname='{adnam}' and phpwd='{pwd}'"
        else:
            sql=f"SELECT * FROM deliveryboytab where dbname='{adnam}' and dbpwd='{pwd}'"
        
        print(sql)
        r,err=getdata(sql,True)
        idcol='adid' if utyp=='1' else 'pid' if utyp=='2' else 'dbid'
        print('r is:',r)
        if type(r) is str or not r: # is none:
            stat="Login Failed...!"
        else:
            request.session['role'] = utyp
            request.session['uid'] = r[idcol]
           
            print("uid logged:",r[idcol])
            request.session.set_expiry(None)
            stat="welcome"+adnam #"Login Success...!"
            updatelog(adnam,'admin')
            temp1=loader.get_template('index.html')
            return HttpResponse(temp1.render({"usr":stat,'role':utyp},request))

    temp1=loader.get_template('adminlogin.html')
    return HttpResponse(temp1.render({"msg":stat},request))

def adminsignup(request):
    c=connection.cursor()
    adname=d['adname']
    password=d['adpwd']
    email=d['ademadr']
    phone=d['adphone']
    address=d['adadr']
    district=d['addistrict']
    street=d['adstate']
    pin=d['adpin']
    
    
    c.execute(f"INSERT INTO admintab (adname,adpwd,ademadr,adphone,adadr,addistrict,adstate,adpin,)\
VALUES('{name}','{password}','{email}','{phone}','{address}','{district}','{state}','{pin}'")

             


    templ=loader.get_template('adminsignup.html')
    return HttpResponse(templ.render({},request))

def stafflogin(request):
    stat=""
    if request.method=='POST':
        adnam=request.POST['adid']
        pwd=request.POST['adpwd']
        sql=f"SELECT * FROM admintab where adname='{adnam}' and adpwd='{pwd}'"
        print(sql)
        r,err=getdata(sql,True)
        
        print('r is:',r)
        if type(r) is str or not r: # is none:
            stat="Login Failed...!"
        else:
            request.session['adnam'] = adnam
            request.session['adid'] = r['adid']
           
            print("uid logged:",r['adid'])
            request.session.set_expiry(0)
            stat="welcome"+adnam #"Login Success...!"
            updatelog(adnam,'admin')
            temp1=loader.get_template('index.html')
            return HttpResponse(temp1.render({"usr":stat},request))

    temp1=loader.get_template('adminlogin.html')
    return HttpResponse(temp1.render({"msg":stat},request))

def pharmaregister(request):
    role=getrole(request)
    if not role or role!='1':
        return HttpResponseRedirect("/adminlogin/",request)
    d={}
    stat=''
    c=connection.cursor()
    dl,err=getdata('select * from pharmacisttab')
    if request.method=='GET' and 'pid' in request.GET:
        id=request.GET['pid']
        d,err=getdata(f'select * from pharmacisttab WHERE pid={id}',True)
    if request.method=="POST":
        print("post",request.POST)
       
        name=request.POST['pname']
        password=request.POST['pwd']
        qualification=request.POST['pqlf']
        licence=request.POST['plcno']
        aadhar=request.POST['padrno']
        dateofbirth=request.POST['pdob']
        account=request.POST['pacno']
        address=request.POST['padr']
        phone=request.POST['pphno']
        email=request.POST['pemadr']
        district=request.POST['pdistrict']
        street=request.POST['pstreet']
        pin=request.POST['ppin']
        if 'btnregister' in request.POST:
            
            c.execute(f"INSERT INTO pharmacisttab (pname,phpwd,pqlf,plcno,padrno,pdob,pacno,padr,pphno,pemadr,pstreet,pdistrict,ppin)\
    VALUES('{name}','{password}','{qualification}','{licence}','{aadhar}',\
    '{dateofbirth}','{account}','{address}','{phone}','{email}','{street}','{district}','{pin}')")
        else:
            pid=request.POST['pid']
            c.execute(f"UPDATE  pharmacisttab SET pname='{name}', pqlf='{qualification}',\
plcno='{licence}',padrno='{aadhar}',pdob='{dateofbirth}',pacno='{account}',padr='{address}',\
pphno='{phone}',pemadr='{email}',pstreet='{street}',pdistrict='{district}',ppin='{pin}' WHERE pid={pid}")
      
    templ=loader.get_template('pharmaregister.html')
    return HttpResponse(templ.render({'msg':stat,'dl':dl,'data':d,'role':role},request))

def dvboyregister(request):
    role=getrole(request)
    if not role or role!='1':
        return HttpResponseRedirect("/adminlogin/",request)
    d={}
    stat=''
    c=connection.cursor()
    dl,err=getdata('select * from deliveryboytab')
    if request.method=='GET' and 'dbid' in request.GET:
        id=request.GET['dbid']
        d,err=getdata(f'select * from deliveryboytab WHERE dbid={id}',True)
    if request.method=="POST":
        print("post",request.POST)
        
        name=request.POST['dbname']
        password=request.POST['pwd']
        licence=request.POST['dblcno']
        aadhar=request.POST['dbadrno']
        dateofbirth=request.POST['dbdob']
        account=request.POST['dbacno']
        pancard=request.POST['dbpcno']
        address=request.POST['dbadr']
        phone=request.POST['dbphno']
        email=request.POST['dbemadr']
        district=request.POST['dbdistrict']
        street=request.POST['dbstreet']
        pin=request.POST['dbpin']

        if 'btnregister' in request.POST:
            c.execute(f"INSERT INTO deliveryboytab (dbname,dbpwd,dblcno,dbadrno,dbdob,dbacno,dbpcno,dbadr,dbphno,dbemadr,dbstreet,\
    dbdistrict,dbpin)VALUES('{name}','{password}','{licence}','{aadhar}','{dateofbirth}','{account}','{pancard}','{address}',\
    '{phone}','{email}','{street}','{district}','{pin}')")            

        else:
            dbid=request.POST['dbid']
            c.execute(f"UPDATE  deliveryboytab SET dbname='{name}',\
    dblcno='{licence}',dbadrno='{aadhar}',dbdob='{dateofbirth}',dbacno='{account}',dbpcno='{pancard}',dbadr='{address}',\
    dbphno='{phone}',dbemadr='{email}',dbstreet='{street}',dbdistrict='{district}',dbpin='{pin}' WHERE dbid={dbid}")
                
    templ=loader.get_template('dvboyregister.html')
    return HttpResponse(templ.render({'msg':stat,'dl':dl,'data':d,'role':role},request))         

    



def ordermedicine(request):
    uurl=''
    stat=''
    usr=getuser(request)
    if not usr:
        return HttpResponseRedirect('/',request)
    print('files',request.FILES)
    if request.method == 'POST' and request.FILES['presfile']:
        #insert into prestab
        
        uid=request.session['uid']
        print('uid is:',uid)
##        pdt= datetime.strptime(request.POST['dateinput'],'%Y-%m-%d') #date.today().strftime("%d-%m-%Y")
##        pdt=pdt.date()
        pdt=date.today()
##        oid=request.session['oid']
        c=connection.cursor()
        c.execute(f"INSERT INTO prescriptiontab (uid,prdate) VALUES('{uid}','{pdt}')")
        c.close()
        connection.close()
        pid=c.lastrowid
        fnam=str(pid)+".png"
        prfile = request.FILES['presfile']
        fs = FileSystemStorage()
##        filename = fs.save("pharmaapp/static/pres/"+prfile.name, prfile)
        filename = fs.save("pharmaapp/static/pres/"+fnam, prfile)
        uurl = "/static/pres/"+fnam
        stat=f"Your prescription is qued as no: {pid} for Order..Thank you"
        udata,err=getdata(f'select uemadr from usertab where uid={uid}',True)
        toeml=udata['uemadr']
        email = EmailMessage('Prescription Recieved',stat, to=(toeml,))
        email.send()
    templ=loader.get_template('ordermedicine.html')
    #return HttpResponse(templ.render({"furl":uurl},request))
    return HttpResponse(templ.render({"usr":getuser(request),"furl":uurl,"msg":stat},request))

def pharmorders(request):
    role=getrole(request)
    if not role or role!='2':
        return HttpResponseRedirect("/adminlogin/",request)
    templ=loader.get_template('cart.html')
    d=[]
    stat=''
    c=connection.cursor()
    dl,er=getdata("select prid,prescriptiontab.uid,date(prdate) as prdate,uname,uphone from prescriptiontab \
inner join usertab on prescriptiontab.uid= usertab.uid where oid is null order by prdate")
    ol,e=getdata('select oid,prid,usertab.uname from prescriptiontab \
inner join usertab on prescriptiontab.uid=usertab.uid \
where oid in (select oid from ordermastertab where iid is null)  order by oid desc')
    
    return HttpResponse(templ.render({'prl':dl,'orl':ol,'role':role},request))

def queorder(request):
  
    role=getrole(request)
    if not role or role!='2':
        #pass
        return HttpResponseRedirect("/adminlogin/",request)
    prid=0
    proid=None
    pruid=None
    cnt={'tnos':0}
    if request.method=="GET":
        if 'prid' in request.GET:
            prid=request.GET["prid"]
            
        else:
            return HttpResponseRedirect("/pharmorders/",request)
    else:
        print(request.POST)
        prid=request.POST['prid']
        if 'btninv' in request.POST:
            pruid=request.POST['pruid']
            proid=request.POST['proid']
            tot,er1=getdata(f"select oamt,round(oamt*.12,0) as gst from  ordermastertab where oid={proid}",True)
            if tot:
                gst=tot['gst']
                gtot=tot['oamt']+gst
                idt=date.today().strftime("%Y-%m-%d")
                c=connection.cursor()
                f,er=getdata(f'select iid from invoicetab where oid={proid} LIMIT 1',True)
                if f:
                    invno=f['iid']
                    c.execute(f"UPDATE invoicetab SET tamt={gtot},igst={gst} WHERE iid={invno}")
                else:
                    c.execute(f"INSERT INTO invoicetab (uid,tamt,igst,idate,oid) \
        VALUES({pruid},{gtot},{gst},Date('{idt}'),{proid})")
                    invno=c.lastrowid
                if invno:
                    c.execute(f'update ordermastertab set iid={invno} where oid={proid}')
                    
                    prd,er=getdata(f"select prid,usertab.uname,usertab.uphone,usertab.uemadr from prescriptiontab \
inner join usertab on prescriptiontab.uid= usertab.uid  where prid={prid}",True)
                    if prd:
                        msg=f"Dear{prd['uname']},\nYour invoice [ no:{invno} ] is ready with Amount Rs.{gtot} including 12% gst Rs.{gst}"
                        toeml=prd['uemadr']
                        email = EmailMessage('Invoice Ready No:{invno}',msg, to=(toeml,))
                        email.send()
                        
                return HttpResponseRedirect("/pharmorders/",request)
            else:
                stat="No valuable medicines found for Invoice.."
        elif 'btnnonavail' in request.POST:
            availstat =request.POST['notavail']
            prd,er=getdata(f"select prid,usertab.uname,usertab.uphone,usertab.uemadr from prescriptiontab \
inner join usertab on prescriptiontab.uid= usertab.uid  where prid={prid}",True)
            if prd:
                stat=availstat
                toeml=prd["uemadr"]
                email = EmailMessage('Non availability of medicines',stat, to=(toeml,))
                email.send()
                return HttpResponseRedirect(f"/queorder/?prid={prid}",request)
        
                
            
        pruid=request.POST['pruid']
        proid=request.POST['proid']
        proid =None if proid =='None' else proid
        odt=date.today().strftime("%Y-%m-%d")
        itmid=request.POST['pritid']
        #qty=
        qty=request.POST['oqty']
        amt=request.POST['oamt']
        c=connection.cursor()
        
        if  not proid:
            
            #insert into ordermaster
            c=connection.cursor()
            c.execute(f"INSERT INTO ordermastertab (odate,uid,oamt,ostatus) \
VALUES('{odt}',{pruid},{amt},'order')")
            proid=c.lastrowid
            #f"update prescriptiontab set oid={oid} where prid={prid}"
            c=connection.cursor()
            c.execute(f"UPDATE prescriptiontab SET oid={proid} where prid={prid}")
            
        else :
            c.execute(f"UPDATE ordermastertab SET oamt=oamt+{amt}")

         #insert into orderdetail..oistatus - 'order'
        c=connection.cursor()
        c.execute(f"INSERT INTO orderdetailtab (oid,odate,uid,oqty,oamt,itid,oistatus)\
VALUES({proid},'{odt}',{pruid},{qty},{amt},{itmid},'order')")
        c.close()
        connection.close()
             

    templ=loader.get_template('qordr.html')
    
    d={}
    stat=''
   
    prid=int(prid)
    prd={}
    prd,er=getdata(f"select prid,oid,prescriptiontab.uid,prescriptiontab.oid,date(prdate) as prdate,usertab.uname,usertab.uphone,usertab.uemadr from prescriptiontab \
inner join usertab on prescriptiontab.uid= usertab.uid  where prid={prid}",True)
    print('prd',prd)
    ml,err=getdata("select itemtab.*, companytab.comname,categorytab.catname from itemtab \
left join companytab on itemtab.comid=companytab.comid left join categorytab on itemtab.catid=categorytab.catid")
    cm,cmr=getdata("select * from companytab")
    ct,ctr=getdata("select * from categorytab")
    proid=prd["oid"]      
    prol,err=getdata(f"select b.*,itemtab.itname,\
(select comname from companytab where comid in (select comid from itemtab where itid=b.itid)) as comname,categorytab.catname from orderdetailtab b \
inner join itemtab on b.itid =itemtab.itid \
left join categorytab on itemtab.catid=categorytab.catid \
where oid={proid}")
    tot={}
    if proid:
        tot,er1=getdata(f"select oamt,round(oamt*.12,0) as gst from  ordermastertab where oid={proid}",True)
        if tot:
            tot['Gtot']=tot['oamt']+tot['gst']
        cnt,er2=getdata(f"select count(oid) as tnos from orderdetailtab where  oid={proid}",True)

        stat=f"Your Prescribed medicines are available and placed in order"
        toeml=prd["uemadr"]
   
        email = EmailMessage('Medicines are available',stat,to=(toeml,))
        email.send()
    
    return HttpResponse(templ.render({'prdata':prd,'tot':tot,'ordrcnt':cnt,'medlist':ml,'medcomlist':cm,'medcatlist':ct,'prordr':prol,'role':role,'msg':stat},request))




def medicine(request):
    stat=""
    role=None
    d=''
    
    if request.method=='GET' and 'itid' in request.GET:
        id=request.GET['itmid']
        d,err=getdata(f'select * from itemtab WHERE itid={id}',True)
        
    if request.method=="POST":
        print("post",request.POST)
        
        
        itmnam=request.POST['itname']
        d,err=getdata(f"select * from itemtab WHERE upper(trim(replace(itname,' ','')))=\
upper(trim(replace('{itmnam}',' ','')))",True)
        
        if d:
            stat="This medicine already exists"
        else:
            cmid=request.POST['comid']
            ctid=request.POST['catid']
            print('cmd',cmid)
            print(ctid)
            ctid='null' if ctid =='None' else ctid
            cmid='null' if cmid =='None' else cmid
            c=connection.cursor()
            c.execute(f"INSERT INTO itemtab (itname,comid,catid) \
VALUES(trim(replace(replace(replace('{itmnam}',' ','<>'),'><',''),'<>',' ')),{cmid},{ctid})")
            c.close()
            connection.close()
        
    dl,err=getdata("SELECT * FROM itemtab")
    cml,err=getdata("SELECT * FROM companytab")
    cgl,err=getdata("SELECT * FROM categorytab")
            
    templ=loader.get_template('medicine.html')
    return HttpResponse(templ.render({"usr":stat,"msg":stat,'dl':dl,'cml':cml,'cgl':cgl,'data':d},request))


def mcompany(request):
    stat=""
    role=None
    d=''
    
    if request.method=='GET' and 'comid' in request.GET:
        id=request.GET['comid']
        d,err=getdata(f'select * from companytab WHERE comid={id}',True)
        
    if request.method=="POST":
        print("post",request.POST)
        
        
        cmnam=request.POST['comname']
        d,err=getdata(f"select * from companytab WHERE upper(trim(replace(comname,' ','')))=\
upper(trim(replace('{cmnam}',' ','')))",True)
        if d:
            stat="This company already exists"
        
            
            c=connection.cursor()
            c.execute(f"INSERT INTO companytab (comname) VALUES(trim(replace(replace(replace('{cmnam}',' ','<>'),'><',''),'<>',' ')),'{cmid}','{ctid}')")
            c.close()
            connection.close()
        
    dl,err=getdata("SELECT * FROM companytab")

    templ=loader.get_template('mcompany.html')
    return HttpResponse(templ.render({"usr":stat,"msg":stat,'dl':dl,'data':d},request))
def mcategory(request):
    stat=""
    role=None
    d=''
    
    if request.method=='GET' and 'catid' in request.GET:
        id=request.GET['catid']
        d,err=getdata(f'select * from categorytab WHERE catid={id}',True)
        
    if request.method=="POST":
        print("post",request.POST)
        
        
        ctnam=request.POST['catname']
        d,err=getdata(f"select * from categorytab WHERE upper(trim(replace(catname,' ','')))=\
upper(trim(replace('{ctnam}',' ','')))",True)
        if d:
            stat="This category already exists"
        
            
            c=connection.cursor()
            c.execute(f"INSERT INTO categorytab (catname) VALUES(trim(replace(replace(replace('{ctnam}',' ','<>'),'><',''),'<>',' ')),'{cmid}','{ctid}')")
            c.close()
            connection.close()
        
    dl,err=getdata("SELECT * FROM categorytab")

    templ=loader.get_template('mcategory.html')
    return HttpResponse(templ.render({"usr":stat,"msg":stat,'dl':dl,'data':d},request))

def invoice(request):
    usr=getuser(request)
    if not usr:
        return HttpResponseRedirect('/',request)
    uid=request.session['uid']
    dl,err=getdata(f"select a.*,(select ifnull(sum(paidamt),0) from paymenttab where vno=a.iid) as paid from invoicetab a where uid={uid} \
 ORDER BY iid DESC")
    stat='' if dl else 'No pending invoice found'
    
    templ=loader.get_template('invoice.html')
    return HttpResponse(templ.render({'invlist':dl,'msg':stat},request))
    
def cart(request):
    templ=loader.get_template('cart.html')
    return HttpResponse(templ.render({},request))
def shop(request):
    templ=loader.get_template('shop.html')
    return HttpResponse(templ.render({},request))

def checkout(request,iid):
    usr=getuser(request)
    if not usr or iid<=0:
        return HttpResponseRedirect('/',request)
    
    d,err=getdata(f'select a.*,(select ifnull(sum(paidamt),0) from paymenttab \
where vno=a.iid) as paid,a.tamt-(select ifnull(sum(paidamt),0) from paymenttab \
where vno=a.iid) as bal from invoicetab a where  iid={iid}',True)
    if request.method=="POST" and d:
        print(request.POST)
        oid=d["oid"]
        uid=d['uid']
        pytyp='chq' if 'chkpy' in request.POST else 'cash'
        vno=iid
        amt=request.POST["paidamt"]
        #c=connection.cursor()
        #c.execute("
        c=connection.cursor()
        c.execute(f"INSERT INTO paymenttab (oid,uid,pytype,vno,paidamt)\
VALUES({oid},{uid},'{pytyp}',{vno},{amt})")
        c.close()
        connection.close()
        
    templ=loader.get_template('checkout.html')
    return HttpResponse(templ.render({'data':d},request))

def delivery(request):
    role=getrole(request)
    invno=0
    if not role or role!='3':
        #pass
        return HttpResponseRedirect("/adminlogin/",request)
    uid=request.session['uid']
    d=pd={}
    iid=None
    if request.method=="POST":
        if 'btninv' in request.POST:
            iid=request.POST['invno']
           
            d,err=getdata(f'select a.*,(select ifnull(sum(paidamt),0) from paymenttab \
where vno=a.iid) as paid,a.tamt-(select ifnull(sum(paidamt),0) from paymenttab \
where vno=a.iid) as bal from invoicetab a where  iid={iid}',True)
            pd,err=getdata(f"select * from paymenttab where vno=={iid} and pystatus is null")
        elif 'btnrect' in request.POST:
            iid=request.POST['recdfor']
            d,err=getdata(f'select a.*,(select ifnull(sum(paidamt),0) from paymenttab \
            where vno=a.iid) as paid,a.tamt-(select ifnull(sum(paidamt),0) from paymenttab \
            where vno=a.iid) as bal from invoicetab a where  iid={iid}',True)
            c=connection.cursor()
            c.execute(f"update paymenttab set pystatus=true,dbid={uid},dbdate=Date('now') where vno=={iid} and pystatus is null")
            em,err=getdata(f'select uname,uemadr from usertab where uid={d["uid"]}',True)
            print("jjkkkk",em)
            toeml=em['uemadr']
            if toeml:
                dt=d['idate'].strftime("%d-%m-%Y")
                stat=f"Dear d['uname'],\nThis is to inform that the payment for\n \
Invoice : {iid} Amount Rs.: {d['tamt']} incl. IGST 12% Rs. {d['igst']} \n \
is received \n regards,\n for NetPharma\nAdministrator.\n \n \
all queries can be addressed netpharma003@gmail.com\n +91 9567501626"
                email = EmailMessage(f'Receieved payment for inv:{iid}',stat, to=(toeml,))
                email.send()
            return HttpResponseRedirect("/delivery/",request)
            
    templ=loader.get_template('delivery.html')
    return HttpResponse(templ.render({'data':d,'pdata':pd,'invno':iid},request))

def notification(request):
    
    usr=getuser(request)
    if not usr:
        return HttpResponseRedirect('/',request)    
    uid=request.session['uid']
    d,err=getdata(f"select * from prescriptiontab,ordermastertab where ordermastertab.uid and prescriptiontab.uid ={uid}")
    
    print("dddd",d)
    templ=loader.get_template('notification.html')
    return HttpResponse(templ.render({'list':d},request))

def feedback(request):

    usr=getuser(request)
    if not usr:
        return HttpResponseRedirect('/',request)    
    uid=request.session['uid']
    d,err=getdata(f"select * from feedbacktab",False)
    
    print("dddd",d)
    
    templ=loader.get_template('feedback.html')
    return HttpResponse(templ.render({'list':d},request))
    
def thankyou(request):
    templ=loader.get_template('thankyou.html')
    return HttpResponse(templ.render({},request))






catlist=[{'Id':1,'catname':'stationary'},
         {'Id':2,'catname':'provision'},
         {'Id':3,'catname':'vegetable'}]

    

def category(request):
    
##    s='<ul>'
##    for i in catlist:
##        s+=f'<li><a href="/details/{i["Id"]}/">{i["catname"]}</a></li>'
##    s+='</ul><a href="/"home</a>'
    print(catlist)
    temp1=loader.get_template('cat.html')
    return HttpResponse(temp1.render({'cat':catlist},request))

def details(request,cid):
    l=[i for i in catlist if i['Id']==cid]
    s=''
    if l:
        s=f"<h3>{l[0]['catname']}</h3>"
    else:
        s='Invalid id no such category..!!'
        
    s+="<br/><a href=/category/>back to category list</a>"

    return HttpResponse(s)

def updatelog(uid,role,logout=None):
    if not logout: # new login- log entry
        return updatedata(f"INSERT INTO logtab (uid,roll) VALUES('{uid}','{role}')")
     
    
    
def login(request):
    stat=""
    if request.method=='POST':
        unam=request.POST['uid']
        pwd=request.POST['pwd']
        unam=unam.replace("'","#'")
        sql=f"SELECT * FROM usertab where uname='{unam}' and upwd='{pwd}'"
        print(sql)
        r,err=getdata(sql,True)
        
        
        print('r is:',r)
        if type(r) is str or not r: # is none:
            stat="Login Failed...!"
        else:
            request.session['unam'] = unam
            request.session['uid'] = r['uid']
           
            print("uid logged:",r['uid'])
            request.session.set_expiry(0)
            stat="welcome"+unam #"Login Success...!"
            updatelog(unam,'customer')
            temp1=loader.get_template('index.html')
            return HttpResponse(temp1.render({"usr":stat},request))

    temp1=loader.get_template('customerlogin.html')
    return HttpResponse(temp1.render({"msg":stat},request))

def logout(request):
    try:
        del request.session['unam']
    except:
        pass

    temp1=loader.get_template('index.html')
    return HttpResponse(temp1.render({},request))

import uuid
def customersignup(request):
    stat=""
    showreg=False
    dl={}

    if request.method=='POST':
       
        if request.session.has_key('ky') and request.POST.get('Confirm'):
            ky=request.POST['verify']
            print('to verify')
            if ky==request.session['ky']:
                print('ok')
                ds=request.POST['hidn']
                d=json.loads(ds)
                print("posted",d)
                #insert command
                c=connection.cursor()
                name=d['uname']
                password=d['upwd']
                email=d['uemadr']
                phone=d['uphone']
                address=d['uadr']
                district=d['udistrict']
                street=d['ustreet']
                pin=d['upin']
                aadhar=d['uadrno']
                
                c.execute(f"INSERT INTO usertab (uname,upwd,uemadr,uphone,uadr,udistrict,ustreet,upin,uadrno)\
VALUES('{name}','{password}','{email}','{phone}','{address}','{district}','{street}','{pin}','{aadhar}')")

                c.close()
                connection.close()
                del request.session['ky']
                return HttpResponseRedirect("/customerlogin",request)

##                templ=loader.get_template('login.html')
##                return HttpResponse(templ.render({"msg":stat},request))

            else:
                stat="Invalid key..please Retry or click verify To send OTP Again"
                showreg=True

        else:
            toeml=request.POST['email']
            name=request.POST['uname']
            password=request.POST['password']
            email=request.POST['email']
            phone=request.POST['phonenum']
            address=request.POST['address']
            district=request.POST['district']
            street=request.POST['street']
            pin=request.POST['pinnum']
            aadhar=request.POST['aadharnum']
            #we need to send a verification link
            try:

                ky=uuid.uuid4().hex[:6].upper()
                request.session['ky']=ky

                msg="Your OTP is " +ky +" please enter it on OTP box..Donot reply to this"
                email = EmailMessage('OTP for site regn',msg, to=(toeml,))
                email.send()
                stat="new key to send to your regn.email id...plz enter it here"
                showreg=True
           
            except:
                stat='unable to verify email... please check your internet connection..RETRY...!!'
            if showreg:
                dl={'uname':name,'upwd':password,'uemadr':toeml,'uphone':phone,'uadr':address,'udistrict':district,'ustreet':street,'upin':pin,'uadrno':aadhar} 
    print(dl)
 ##         r=getdata(f"SELECT * FROM usertab where userid='{unam}'and pwd='{pwd}'",True)   

    templ=loader.get_template('customersignup.html')
   
    return HttpResponse(templ.render({"stat":stat,'showreg':showreg,'data':json.dumps(dl)},request))
          
def register(request):

    stat=""
    showreg=False
    dl={}

    if request.method=='POST':
        toeml=request.POST['email']

        name=request.POST['name']
        dob=request.POST['dob']
        address=request.POST['addressname']
        phone=request.POST['phonenumber']
        email=request.POST['email']
        pin=request.POST['pinnumber']
        if request.session.has_key('ky') and request.POST.get('register'):
            ky=request.POST['verify']
            print('to verify')
            if ky==request.session['ky']:
                print('ok')

                #insert command
                c=connection.cursor()
                c.execute(f"INSERT INTO registation (regname,dob,address,phone,email,pincode) VALUES('{name}','{dob}','{address}','{phone}','{email}','{pin}')")

                c.close()
                connection.close()
                del request.session['ky']

                temp1=loader.get_template('login.html')
                return HttpResponse(temp1.render({"msg":stat},request))

            else:
                stat="Invalid key..please Retry or click verify To send OTP Again"
                showreg=True

        else:
            #we need to send a verification link
            try:

                ky=uuid.uuid4().hex[:6].upper()
                request.session['ky']=ky

                msg="Your OTP is " +ky +" please enter it on OTP box..Donot reply to this"
                email = EmailMessage('OTP for site regn',msg, to=(toeml,))
                email.send()
                stat="new key to send to your regn.email id...plz enter it here"
                showreg=True
            except:
                stat='unable to verify email... please check your internet connection..RETRY...!!'
    if showreg:
        dl={'name':name,'email':toeml} #should complete
    ##         r=getdata(f"SELECT * FROM usertab where userid='{unam}'and pwd='{pwd}'",True)   

    temp1=loader.get_template('register.html')
    return HttpResponse(temp1.render({"stat":stat,'showreg':showreg,'data':dl},request))
            

