slt_add1 = {'flow-id': 2, 'trml_port': 2, 'slt_list': [1], 'queue': 2, 'trml_slot': None, 'port': 1}
slt_add2 = {'flow-id': 3, 'trml_port': 21, 'slt_list': [1], 'queue': 2, 'trml_slot': None, 'port': 1}
slt_add3 = {'flow-id': 4, 'trml_port': 22, 'slt_list': [1], 'queue': 2, 'trml_slot': None, 'port': 1}


#for i in a:
#    print i['flow-id']
    


df = pd.DataFrame()

df = df.append(slt_add1, ignore_index=True)
df = df.append(slt_add2, ignore_index=True)
df = df.append(slt_add3, ignore_index=True)


df = df
df= df.drop_duplicates(subset=['flow-id'],  keep='last')
print df

df = df.reset_index(drop=True)
print df

print df[df["flow-id"]==2]
a=  df[df["flow-id"]==2].to_dict('records')[0]
print a 



#df["flow-id"] = [0,2]
#df["rcv-time"] = [0.01,0.081]

#now = 0.10
#CT = 10e-3

#df = df[df["flow-id"]>0].copy()
#df = df[now - df["rcv-time"] < 2*CT]
#print df["flow-id"].tolist()

