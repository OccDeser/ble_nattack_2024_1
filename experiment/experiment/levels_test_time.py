import re
import os

# 获取所有spthy文件
def get_spthy_files(dir:str):
    files = os.listdir(dir)
    spthy_files = []
    for file in files:
        if file.endswith(".spthy"):
            spthy_files.append(os.path.join(dir, file))
    return spthy_files

# 获取所有spthy文件的内容
def get_spthy_content(spthy_files:list):
    spthy_content = {}
    for file in spthy_files:
        with open(file, "r") as f:
            spthy_content[file] = f.read()
    return spthy_content

# 正则匹配processing time: 后面的所有内容
def get_processing_time(content:str):
    return re.findall(r"processing time: (.*)", content)[0]


spthy_files = get_spthy_files("./experiment/levels_test/proofs")
spthy_content = get_spthy_content(spthy_files)
data = []
for file, content in spthy_content.items():
    name = file.split("/")[-1].split(".")[0]
    dlevel = re.findall(r"d(\d+)", name)[0]
    plevel = re.findall(r"p(\d+)", name)[0]
    data.append([name, dlevel, plevel, get_processing_time(content)])

data.sort(key=lambda x: x[0])
for d in data:
    print(d[0], d[3])

