import os

veri = os.popen("arp -a").read()
veri = veri.split("\n")
cameracon = ""
for x in veri:
    if x.find("8c-f5-a3-70-54-01") == 24:
        a = x[2 : 2 + 15]
        cameracon = "http://" + a + ":8080/shot.jpg"
