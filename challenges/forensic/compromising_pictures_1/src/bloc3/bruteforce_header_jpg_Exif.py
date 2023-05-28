import os

with open("meetingplace.jpg", "rb") as image:
  f = image.read()
  b = bytearray(f)

path = "bruteforce_out"
os.mkdir(path)

for x in range(0,256):
    for y in range(0,256):
        b[4] = x
        b[5] = y
        f2 = bytes(b)
        filename = path + "/meetingplace_" + str(x) + str(y) + ".jpg"
        with open(filename, 'wb') as image:
            image.write(f2)
print("END")