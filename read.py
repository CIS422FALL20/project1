with open("resultado.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

list=[]
for i in content:
    temp = (i.replace(']', ''))
    temp1 = (temp.replace('[', ''))
    # parte = (temp1.replace(',', ''))
    # print(parte)
    numero = temp1.split(" ")
    list.append(numero[0])



for i in list:
    print("{0}".format(i),end=" ")
