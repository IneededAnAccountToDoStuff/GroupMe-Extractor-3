import tkinter

root=tkinter.Tk()
root.title('GroupMe Extractor')
tokenholder=tkinter.Frame()
tokenholder.pack(fill='x')
tkinter.Label(tokenholder,text='Token:').pack(side='left',fill='x',expand=1)
tokenask=tkinter.StringVar()
tokenin=tkinter.Entry(tokenholder,textvariable=tokenask);tokenin.pack(side='left',fill='x',expand=1)
QQ=tkinter.BooleanVar(value=1)
attachask=tkinter.Checkbutton(text='Attachments',variable=QQ)
attachask.pack()
tkinter.Button(text='Go!',command=root.destroy).pack(fill='x')
root.mainloop()
getattachmentsflag=QQ.get()
print('Get attachments'if getattachmentsflag else"No Attachments")
GPtoken=tokenask.get()
#If you use this often, I'd recommend replacing this with your token, obfuscated(so can't be stolen at a glance (e.g. bytes((2*40,111-10,11+55+35,99+8,665-568,2*49,37*3*1,3*101-2*96,78+22-67)).decode() )).
def error(text:str):a=tkinter.Tk();a.title('Error');tkinter.Label(text=text).pack(fill='both',expand=1);a.mainloop();raise SystemExit()
if GPtoken.strip()=="":error('You must give a token. Find yours at https://dev.groupme.com/')

import json,urllib.request
def queryURL(url):return json.loads(urllib.request.urlopen(url).read())['response']
try:groups=queryURL(f"https://api.groupme.com/v3/groups?token={GPtoken}")
except urllib.error.HTTPError as err:
    ec=err.code
    if ec==401:C='Unauthorised, probably a token error'
    elif ec==404:C="Something weird's going on"
    else:C="Don't know what's wrong."
    error(f'Something went wrong with the intial fetch - {ec}: {C}')
def parsegroupdata(chat):groupIDnameMap[chat['id']]=chat['name'];return{'name':chat['name'],'subtopics':chat['children_count'],'members':(*(((f'⌊{n}⌋{r[len(n):]}'if R.startswith(N)else f"⌊{n}⌋ AKA ⌊{r}⌋")if N!=R else n,c)for n,r,N,R,c in((a,b,a.casefold(),b.casefold(),c)for a,b,c in((a['nickname'],a['name'],a['id'])for a in chat['members']))),)}
def getGroupFromID(id):return queryURL(f"https://api.groupme.com/v3/groups/{id}?token={GPtoken}")
def querygroupidmessages(groupID):
    a=queryURL(f'https://api.groupme.com/v3/groups/{groupID}/messages?limit=1&token={GPtoken}');total=a['count'];q=a['messages'];count=1
    while count<total:a=queryURL(f'https://api.groupme.com/v3/groups/{groupID}/messages?limit=30&before_id={q[-1]['id']}&token={GPtoken}')['messages'];q.extend(a);count+=len(a)
    q.reverse();return q
def querygroupmessages(group):return querygroupidmessages(group["id"])
groupIDnameMap={}
def querygroupIDmsgWtopics(groupID):
    a=querygroupidmessages(groupID);c={groupID:a}
    for i in a:
        if i['user_id']=='system'and i['event']['type']=='group.subgroup_created':
            i=i['event']['data'];sid=i['subgroup_id'];groupIDnameMap[sid]=nam=i['subgroup_topic']
            try:c.update(querygroupIDmsgWtopics(sid))
            except urllib.error.HTTPError:c[sid]=f'ERROR: subtopic "{nam}" could not be found(probably deleted).'
    return c
def querygroupmsgWtopics(group):return querygroupIDmsgWtopics(group["id"])
def packagegroupdata(group):return(parsegroupdata(group),(*(formattopicmessages(i)for i in querygroupmsgWtopics(group).items()),))
def formattopicmessages(msg):msgn,msg=msg;name=groupIDnameMap[msgn];return(name,msg)if isinstance(msg,str)else(name,(*({'name':'SYSTEM>'if i['user_id']=='system'else i['name'],"id":i['id'],'time':i['created_at'],'text':i['text'],'attachments':i['attachments']}for i in msg),))
def totime(time):import datetime;return datetime.datetime.fromtimestamp(time,datetime.UTC).astimezone().strftime('%H:%M:%S on %Y/%m/%d')
result=[packagegroupdata(group)for group in groups]

def getattachments(jsondat):return(e for i in jsondat for sl in i[1]for s in sl[1]if isinstance(s,dict)for e in s['attachments'])
def saveform(result,outpath='groupme.zip'):
    import zipfile
    with open(outpath,'w'):pass
    with zipfile.ZipFile(outpath,"a",zipfile.ZIP_DEFLATED)as zip_file:
        zip_file.writestr('main.json',json.dumps(result,separators=(',',':')))
        if getattachmentsflag:
            manifest={};count=0
            for attachment in getattachments(result):
                if attachment['type']=='mentions'or attachment['type']=='location'or'reply'==attachment['type']:continue
                if attachment['type']=='charmap':print('\nCharmap - skipping');continue
                if attachment['type']=='emoji':print('\nEmoji attachment - skipping');continue
                if attachment['type']=='split':print('\nMoney Split - skipping');continue
                if'url'not in attachment:print(f'Attachment {repr(attachment)} is not understood');continue
                try:pastr=f'attachment_{count}';zip_file.writestr(pastr,urllib.request.urlopen(attachment['url']).read());manifest[pastr]=attachment;count+=1
                except(urllib.error.URLError,ValueError,urllib.error.HTTPError):print(f'\nError getting {attachment=}')
            zip_file.writestr('attachment_manifest.json',json.dumps(manifest,separators=(',',':')))
import time;path=f'groupme_{int(time.time())}.zip'
print('Generating .zip file to store data.');print('Saving-',end='',flush=1);saveform(result,path);print('\rSaved  ')
print('#TODO: save attachments with proper extensions.')
