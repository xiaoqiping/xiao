import datetime
for i in range(1,1000):
    nf = open("log.txt", "w")
    nf.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    nf.close()
    print(i)
