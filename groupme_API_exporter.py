import json,urllib.request
GPtoken=input('GroupMe API Token(find at https://dev.groupme.com/)>')#No, you don't get my token. I'd recommend replacing this with your token, obfuscated(so can't be stolen at a glance (e.g. bytes((2*40,111-10,11+55+35,99+8,665-568,2*49,37*3*1,3*101-2*96,78+22-67)).decode() )).
def queryURL(url):return json.loads(urllib.request.urlopen(url).read())['response']
groups=queryURL(f"https://api.groupme.com/v3/groups?token={GPtoken}")
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
def displaygroupmessages(msg):
    name,msg=msg;print(f'\tGroup/Topic Name: {name}\n\tCount: {len(msg)}')
    if isinstance(msg,str):print(msg);return
    for i in msg:
        print(f'\t\t{i['name']} at {totime(i['time'])}: {i["text"]}')
        if i['attachments']:print(f'\t\t\t⎙ Attachments:{i['attachments']}')
        print()
result=[]
for group in groups:
    gdata=packagegroupdata(group);result.append(gdata);print(gdata[0])
    for j in gdata[1]:displaygroupmessages(j)
    print();print()

def getattachments(jsondat):return(e for i in jsondat for sl in i[1]for s in sl[1]if isinstance(s,dict)for e in s['attachments'])
def saveform(result,outpath='groupme.zip'):
    import zipfile#,io
    with open(outpath,'w'):pass#zip_buffer=io.BytesIO()
    with zipfile.ZipFile(outpath,"a",zipfile.ZIP_DEFLATED)as zip_file:
        zip_file.writestr('main.json',json.dumps(result,separators=(',',':')));manifest={};count=0
        for attachment in getattachments(result):
            if attachment['type']=='mentions'or'reply'==attachment['type']:continue
            pastr=f'attachment_{count}';zip_file.writestr(pastr,urllib.request.urlopen(attachment['url']).read());manifest[pastr]=attachment;count+=1
        zip_file.writestr('attachment_manifest.json',json.dumps(manifest,separators=(',',':')))
    #with open(outpath,'bw')as f:f.write(zip_buffer.getbuffer())
path=f'groupme_{int(time.time())}.zip';import time
print('Generating .zip file to store data.');print('Saving-',end='',flush=1);saveform(result,path);print('\rSaved  ')
print('#TODO: save attachments with proper extensions.')
