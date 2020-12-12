data = {"code_type":"3","login_name":"13577777777"}
# data = str(data)
print("data的值",data)

d = {}
if str(data).strip():
    for a in data.items():
        d[str(a[0])] = a[1]
        print(d)




    # print(str(data).strip(),type(str(data).strip()))
    # http_info = data.split('..', 1)
    # print("===========http_info的值是", http_info)
    # for h in http_info:
    #     s = str(h).split('==')
    #     print("===============s的值是", s)
    #     print("===========d[str(s[0])]的值",str(s[0]))
    #     d[str(s[0])] = s[1]

