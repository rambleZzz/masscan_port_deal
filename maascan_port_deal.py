#coding:utf-8
import json
import re

l = []
ip_mas_port = []
ip_temp_alive = []
FILE_NAME = 'mtest.json'

def rawparse(rawfile):
    #为避免防火墙策略存活所有端口，alive_port_count参数控制超过多少的个开放端口的IP舍去
    alive_port_count = 100
    ipdict = {}
    exclude_port_ip = []
    need_port_ip = []
    fhandle = open(rawfile,'r')
    regexp = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    for line in fhandle:
        result = regexp.findall(line)
        if result and result[0] in ipdict:
            ipdict[result[0]] = ipdict[result[0]] + 1
        elif result:
            ipdict[result[0]] = 1
    print('存活的IP:端口数量：')
    print(ipdict)
    fhandle.close()
    for ip in ipdict:
        if (ipdict[ip]) > alive_port_count:
            exclude_port_ip.append(ip)
        else:
            need_port_ip.append(ip)
    print('存活超过%s个端口的IP：'%(alive_port_count))
    print(exclude_port_ip)
    return need_port_ip,exclude_port_ip

need_port_ip,exclude_port_ip = rawparse(FILE_NAME)
with open(FILE_NAME,'r') as f:
    print('存活的IP:端口信息：')
    for line in f:
        if line.startswith('{ '):
            temp = json.loads(line)
            if temp['ip'] in need_port_ip:
                ip_port = {'ip':temp['ip'],'port':temp['ports'][0]['port']}
                l.append(ip_port)
                #print(temp['ip'],temp['ports'][0]['port'],temp['ports'][0]['proto'],temp['ports'][0]['status'],temp['ports'][0]['reason'])
                print('%s:%d'%(temp['ip'],temp['ports'][0]['port']))
                ip_mas_port.append(temp['ports'][0]['port'])
                ip_temp_alive.append(temp['ip'])
    print('存活端口已去重：')
    print(str(list(set(ip_mas_port))).replace(" ",""))
    print('存活端口的IP已去重：')
    ip_all_alive = '\n'.join(('%s' % id for id in list(set(ip_temp_alive))))
    print(ip_all_alive)

print('单IP当前存活端口：')
c= {}
for i in l:
    c.setdefault(i['ip'],[]).append(i['port'])
print(c)






















