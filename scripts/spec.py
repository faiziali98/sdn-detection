import os

sum_al = {}
for filename in os.listdir(os.getcwd()):
    if 'csv' in filename:
        print(filename)
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            for l in f.readlines()[1:]:
                if l in sum_al.keys():
                    sum_al[l] += 1
                else:
                    sum_al[l] = 1

print(sum_al)

