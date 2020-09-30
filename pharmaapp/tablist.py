#user tab
sqlusertab="CREATE TABLE IF NOT EXISTS usertab\
(uid integer primary key autoincrement,uname varchar(20) not null,upwd varchar(10) not null,\
uphone varchar(20) not null,uemadr varchar(50),uadr varchar(50) not null,ustreet varchar(20) not null,\
udistrict varchar(20) not null,upin varchar(10) not null,uadrno varchar(20) not null,\
sdate text ,sstatus varchar(20))"
#admintab
sqladmintab="CREATE TABLE admintab\
(adid integer primary key autoincrement,adname varchar(10) not null,\
adpwd varchar(10) not null,adphone varchar(20),ademadr varchar(50) not null,\
adadr varchar(50) not null,addistrict varchar(20) not null,\
adstate varchar(20) not null,adpin varchar(20) not null )")
#log tab
sqllogtab="CREATE TABLE logtab\
(id integer primary key autoincrement,uid varchar(20) not null,\
roll varchar(50) not null,logintime TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,logouttime text not null)"

#pharmacist tab
sqlpharmacisttab="CREATE TABLE pharmacisttab\
(pid integer primary key autoincrement,pname varchar(20) not null ,phpwd varchar(10) not null,\
pqlf varchar(50) not null,plcno varchar(50) not null,pdob text not null,padrno varchar(50) not null,\
padr varchar(50) not null,pphno integer not null,pemadr varchar(20),pacno varchar(20) not null,pstreet varchar(20) not null,\
pdistrict varchar(20) not null,ppin varchar(10) not null )")

#deliveryboy tab
sqldeliveryboytab="CREATE TABLE deliveryboytab\
(dbid integer primary key autoincrement,dbname varchar(20) not null ,dbpwd varchar(10) not null,dblcno varchar(20) not null,\
dbdob text not null,dbadrno varchar(20) not null,dbacno varchar(20) not null,dbpcno varchar(50) not null,\
dbadr varchar(50) not null,dbphno integer not null,dbemadr varchar(20) not null,\
dbstreet varchar(20) not null,dbdistrict varchar(20) not null,dbpin varchar(10) not null)")

#prescription tab
sqlprescriptiontab="CREATE TABLE prescriptiontab\
(prid integer primary key autoincrement,uid integer references  usertab ,\
prdate date not null,oid integer references ordermastertab)"

#item tab
sqlitemtab="CREATE TABLE itemtab\
(itid integer primary key autoincrement,itname varchar(50) not null,\
comid integer references companytab,catid integer references category)"

#company tab
sqlcompanytab="CREATE TABLE companytab\
(comid integer primary key autoincrement,comname varchar(50) not null)"

#category tab
sqlcategorytab="CREATE TABLE categorytab\
(catid varchar(20) primary key,catname varchar(50) not null)"

#order master tab
sqlordermastertab="CREATE TABLE ordermastertab\
(oid integer primary key autoincrement,odate text not null,uid varchar(20) references usertab,oamt numeric(8,2) not null,\
iid integer references invoicetab,ostatus varchar(20) not null)"

#order detail tab
sqlorderdetailtab="CREATE TABLE orderdetailtab\
(odid integer primary key autoincrement,oid integer references ordermastertab,odate text not null,\
uid varchar(20) references usertab,oqty integer not null,oamt numeric(8,2) not null,\
itid varchar(20) references itemtab,iqty integer null,oistatus varchar(20) not null)"

#payment tab
sqlpaymenttab="CREATE TABLE paymenttab\
(pyid integer primary key autoincrement,oid integer references ordermastertab,uid varchar(20)not null,\
pytype varchar(20) not null,vno integer not null, vtype varchar(1),pystatus boolean not null)"

#invoice tab
sqlinvoicetab="CREATE TABLE invoicetab\
(iid integer primary key autoincrement,uid integer references usertab,\
tamt varchar(20) not null,tdisc varcahar(20) not null)"

#user transaction tab
sqlusertransactiontab="CREATE TABLE usertransactiontab\
(tid integer primary key autoincrement,tdate text not null,iid integer references invoicetab,\
oid integer references ordermastertab,itype varchar(20) not null,tamt varchar(20)not null)"

#receipt tab
sqlreceipttab="CREATE TABLE receipttab\
(rid integer primary key autoincrement,rdate text not null,iid integer references invoicetab,\
uid varchar(20) references usertab,ramt varchar(20)not null)"

#notification tab
sqlnotificationtab="CREATE TABLE notificationtab\
(nid integer primary key autoincrement,\
ntittle varchar(20) not null,ndescription varchar(20) not null)"

#feedback tab
sqlfeedbacktab="CREATE TABLE feedbacktab\
(fid integer primary key autoincrement,uid varchar(20) not null references usertab,\
fstatus varchar(50) not null)"







