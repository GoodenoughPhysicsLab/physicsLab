'''
    这是我的第一个程序生成的实验的部分代码
    之所以是部分代码，因为当时做了一部分就发现脚本有脚本的缺点
    比如连导线这种精细活对代码的要求稍高
    当时程序生成的电路有问题之后就直接手动改存档与手动做实验了
    就没程序太多事了，除了当时还写了一点小脚本，手动往存档里塞一些原件与导线数据
    这个思路很快就被弃用了
    并且之后我很快就重新制作了physicsLab.py
'''

head = '''{
  "Type": 0,
  "Experiment": {
    "ID": null,
    "Type": 0,
    "Components": 7,
    "Subject": null,
    "StatusSave": "
    {\\\"SimulationSpeed\\\":1.0,\\\"Elements\\\":
      [
'''

# useless #
'''
        {\\\"ModelID\\\":\\\"D Flipflop\\\",\\\"Identifier\\\":\\\"eb6d4a1ac6f9443884d2406410333f96\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"高电平\\\":3.0,\\\"低电平\\\":0.0,\\\"锁定\\\":1.0},\\\"Statistics\\\":{},\\\"Position\\\":\\\"-0.02226322,-3.85046E-05,-0.1915324\\\",\\\"Rotation\\\":\\\"-0.0005059397,179.9991,0.0001571211\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0},
        {\\\"ModelID\\\":\\\"Logic Input\\\",\\\"Identifier\\\":\\\"61573cc9a37a40098d329b784c857fd5\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"高电平\\\":3.0,\\\"低电平\\\":0.0,\\\"锁定\\\":1.0},\\\"Statistics\\\":{\\\"电流\\\":0.0,\\\"电压\\\":0.0,\\\"功率\\\":0.0},\\\"Position\\\":\\\"-0.2088008,-0.0002882481,-0.1764109\\\",\\\"Rotation\\\":\\\"0.3956748,179.9996,0.0003449444\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0},
        {\\\"ModelID\\\":\\\"Logic Output\\\",\\\"Identifier\\\":\\\"a41509a7d0074d249f473770bd42ec14\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"状态\\\":0.0,\\\"高电平\\\":3.0,\\\"低电平\\\":0.0,\\\"锁定\\\":1.0},\\\"Statistics\\\":{\\\"状态\\\":0.0,\\\"电压\\\":0.0},\\\"Position\\\":\\\"0.1671194,-0.0002881885,-0.1914937\\\",\\\"Rotation\\\":\\\"0.3956679,179.9996,0.0003382094\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0},
        {\\\"ModelID\\\":\\\"And Gate\\\",\\\"Identifier\\\":\\\"023a83f9072b4f7fb857c1151e51a8e8\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"高电平\\\":3.0,\\\"低电平\\\":0.0,\\\"最大电流\\\":0.10000000149011612,\\\"锁定\\\":1.0},\\\"Statistics\\\":{\\\"状态\\\":0.0,\\\"输入0\\\":0.0,\\\"输入1\\\":0.0},\\\"Position\\\":\\\"-0.3430932,-0.0002883077,-0.3760597\\\",\\\"Rotation\\\":\\\"359.6043,179.9996,-0.0003266095\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0},
        {\\\"ModelID\\\":\\\"Nor Gate\\\",\\\"Identifier\\\":\\\"bd2aefbe7e9f4c96b3ddd8010d34378c\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"高电平\\\":3.0,\\\"低电平\\\":0.0,\\\"最大电流\\\":0.10000000149011612,\\\"锁定\\\":1.0},\\\"Statistics\\\":{\\\"状态\\\":1.0,\\\"输入0\\\":0.0,\\\"输入1\\\":0.0},\\\"Position\\\":\\\"0.2901083,-0.0002881885,-0.4054283\\\",\\\"Rotation\\\":\\\"359.6043,179.9996,-0.0003242083\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0},
        {\\\"ModelID\\\":\\\"Nimp Gate\\\",\\\"Identifier\\\":\\\"0f4856e0d8774d2285e74a6d763d1f52\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"高电平\\\":3.0,\\\"低电平\\\":0.0,\\\"最大电流\\\":0.10000000149011612,\\\"锁定\\\":1.0},\\\"Statistics\\\":{\\\"状态\\\":0.0,\\\"输入0\\\":0.0,\\\"输入1\\\":0.0},\\\"Position\\\":\\\"-0.01381897,-0.0002883077,-0.3990708\\\",\\\"Rotation\\\":\\\"359.6043,179.9996,-0.0003279969\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0},
        {\\\"ModelID\\\":\\\"Simple Switch\\\",\\\"Identifier\\\":\\\"6cc8760c90304942ad65101f08d58420\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"开关\\\":0.0,\\\"锁定\\\":1.0},\\\"Statistics\\\":{},\\\"Position\\\":\\\"-0.04323891,-0.0002882481,0.04146196\\\",\\\"Rotation\\\":\\\"0.3956634,179.9996,0.0003309827\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0},
        {\\\"ModelID\\\":\\\"Multiplier\\\",\\\"Identifier\\\":\\\"b104620701bc4bf5a386ef5b6d6fa312\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"高电平\\\":3.0,\\\"低电平\\\":0.0,\\\"锁定\\\":1.0},\\\"Statistics\\\":{},\\\"Position\\\":\\\"0.7810758,-3.838539E-05,0.1081042\\\",\\\"Rotation\\\":\\\"-0.0004798342,180.0001,0.0001597951\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0}
'''
# end useless #

linkHead = '''
      ],\\\"Wires\\\":[
'''

# useless #
'''
        {\\\"Source\\\":\\\"eb6d4a1ac6f9443884d2406410333f96\\\",\\\"SourcePin\\\":2,\\\"Target\\\":\\\"eb6d4a1ac6f9443884d2406410333f96\\\",\\\"TargetPin\\\":3,\\\"ColorName\\\":\\\"蓝色导线\\\"}
'''
# end useless #

end = '''
      ]
    }",
    "CameraSave": "{\\\"Mode\\\":0,\\\"Distance\\\":2.7,\\\"VisionCenter\\\":\\\"0.3623461,1.08,-0.4681728\\\",\\\"TargetRotation\\\":\\\"50,0,0\\\"}",
    "Version": 2404,
    "CreationDate": 1673100860436,
    "Paused": false,
    "Summary": null,
    "Plots": null
  },
  "ID": null,
  "Summary": {
    "Type": 0,
    "ParentID": null,
    "ParentName": null,
    "ParentCategory": null,
    "ContentID": null,
    "Editor": null,
    "Coauthors": [],
    "Description": null,
    "LocalizedDescription": null,
    "Tags": [
      "Type-0"
    ],
    "ModelID": null,
    "ModelName": null,
    "ModelTags": [],
    "Version": 0,
    "Language": null,
    "Visits": 0,
    "Stars": 0,
    "Supports": 0,
    "Remixes": 0,
    "Comments": 0,
    "Price": 0,
    "Popularity": 0,
    "CreationDate": 1673086932246,
    "UpdateDate": 0,
    "SortingDate": 0,
    "ID": null,
    "Category": null,
    "Subject": "内存",
    "LocalizedSubject": null,
    "Image": 0,
    "ImageRegion": 0,
    "User": {
      "ID": null,
      "Nickname": null,
      "Signature": null,
      "Avatar": 0,
      "AvatarRegion": 0,
      "Decoration": 0,
      "Verification": null
    },
    "Visibility": 0,
    "Settings": {},
    "Multilingual": false
  },
  "CreationDate": 0,
  "InternalName": "内存",
  "Speed": 1.0,
  "SpeedMinimum": 0.0002,
  "SpeedMaximum": 2.0,
  "SpeedReal": 0.0,
  "Paused": false,
  "Version": 0,
  "CameraSnapshot": null,
  "Plots": [],
  "Widgets": [],
  "WidgetGroups": [],
  "Bookmarks": {},
  "Interfaces": {
    "Play-Expanded": false,
    "Chart-Expanded": false
  }
}
'''

'''
原件引脚编号：

D触发器：
2 0
3 1

逻辑输入、逻辑输出：
0

与门，或门，或非门，蕴含非门：
0
    2
1

二位乘法器：
4  0
5  1
6  2
7  3

原件大小规范：
大原件长宽为0.2
小元件长为0.2，宽为0.1
所有原件高为0.1

'''


label = -1 # 每个原件都有一个独特的序列号，原本Unix时间戳
component, link = '', '' # 原件，导线


class physicsLab:
    def __init__(self):
        pass

    def crt_D_Flipflop(self, x, y, z):
        global label, component
        label += 1
        component += "        {\\\"ModelID\\\":\\\"D Flipflop\\\",\\\"Identifier\\\":\\\"" + str(label) + "\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"高电平\\\":3.0,\\\"低电平\\\":0.0,\\\"锁定\\\":1.0},\\\"Statistics\\\":{},\\\"Position\\\":\\\"" + str(x) + "," + str(z) + "," + str(y) + "\\\",\\\"Rotation\\\":\\\"0,180,0\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0},\n"
        return label

    def crt_Logic_Input(self, x, y, z, heading = 180):
        global label, component
        label += 1
        component += "        {\\\"ModelID\\\":\\\"Logic Input\\\",\\\"Identifier\\\":\\\"" + str(label) + "\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"高电平\\\":3.0,\\\"低电平\\\":0.0,\\\"锁定\\\":1.0},\\\"Statistics\\\":{\\\"电流\\\":0.0,\\\"电压\\\":0.0,\\\"功率\\\":0.0},\\\"Position\\\":\\\"" + str(x) + "," + str(z) + "," + str(y) + "\\\",\\\"Rotation\\\":\\\"0," + str(heading) + ",0\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0},\n"
        return label

    def crt_Logic_Output(self, x, y, z):
        global label, component
        label += 1
        component += "        {\\\"ModelID\\\":\\\"Logic Output\\\",\\\"Identifier\\\":\\\"" + str(label) + "\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"状态\\\":0.0,\\\"高电平\\\":3.0,\\\"低电平\\\":0.0,\\\"锁定\\\":1.0},\\\"Statistics\\\":{\\\"状态\\\":0.0,\\\"电压\\\":0.0},\\\"Position\\\":\\\"" + str(x) + "," + str(z) + "," + str(y) + "\\\",\\\"Rotation\\\":\\\"0,180,0\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0},\n"
        return label

    def crt_AndGate(self, x, y, z):
        global label, component
        label += 1
        component += "        {\\\"ModelID\\\":\\\"And Gate\\\",\\\"Identifier\\\":\\\"" + str(label) + "\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"高电平\\\":3.0,\\\"低电平\\\":0.0,\\\"最大电流\\\":0.10000000149011612,\\\"锁定\\\":1.0},\\\"Statistics\\\":{\\\"状态\\\":0.0,\\\"输入0\\\":0.0,\\\"输入1\\\":0.0},\\\"Position\\\":\\\"" + str(x) + "," + str(z) + "," + str(y) + "\\\",\\\"Rotation\\\":\\\"0,180,0\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0},\n"
        return label

    def crt_OrGate(self, x, y, z):
        global label, component
        label += 1
        component += "        {\\\"ModelID\\\":\\\"Or Gate\\\",\\\"Identifier\\\":\\\"" + str(label) + "\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"高电平\\\":3.0,\\\"低电平\\\":0.0,\\\"最大电流\\\":0.10000000149011612,\\\"锁定\\\":1.0},\\\"Statistics\\\":{\\\"状态\\\":0.0,\\\"输入0\\\":0.0,\\\"输入1\\\":0.0},\\\"Position\\\":\\\"" + str(x) + "," + str(z) + "," + str(y) + "\\\",\\\"Rotation\\\":\\\"0,180,0\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0},\n"
        return label

    def crt_NoGate(self, x, y, z):
        global label, component
        label += 1
        component += "        {\\\"ModelID\\\":\\\"No Gate\\\",\\\"Identifier\\\":\\\"" + str(label) + "\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"高电平\\\":3.0,\\\"低电平\\\":0.0,\\\"最大电流\\\":0.10000000149011612,\\\"锁定\\\":1.0},\\\"Statistics\\\":{},\\\"Position\\\":\\\"" + str(x) + "," + str(z) + "," + str(y) + "\\\",\\\"Rotation\\\":\\\"359.6043,179.9996,-0.0003245904\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0},\n"
        return label

    def crt_NorGate(self, x, y, z):
        global label, component
        label += 1
        component += "        {\\\"ModelID\\\":\\\"Nor Gate\\\",\\\"Identifier\\\":\\\"" + str(label) + "\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"高电平\\\":3.0,\\\"低电平\\\":0.0,\\\"最大电流\\\":0.10000000149011612,\\\"锁定\\\":1.0},\\\"Statistics\\\":{\\\"状态\\\":1.0,\\\"输入0\\\":0.0,\\\"输入1\\\":0.0},\\\"Position\\\":\\\"" + str(x) + "," + str(z) + "," + str(y) + "\\\",\\\"Rotation\\\":\\\"0,180,0\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0},\n"
        return label

    def crt_NimpGate(self, x, y, z):
        global label, component
        label += 1
        component += "        {\\\"ModelID\\\":\\\"Nimp Gate\\\",\\\"Identifier\\\":\\\"" + str(label) + "\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"高电平\\\":3.0,\\\"低电平\\\":0.0,\\\"最大电流\\\":0.10000000149011612,\\\"锁定\\\":1.0},\\\"Statistics\\\":{\\\"状态\\\":0.0,\\\"输入0\\\":0.0,\\\"输入1\\\":0.0},\\\"Position\\\":\\\"" + str(x) + "," + str(z) + "," + str(y) + "\\\",\\\"Rotation\\\":\\\"0,180,0\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0},\n"
        return label

    def crt_SimpleSwitch(self, x, y, z):
        global label, component
        label += 1
        component += "        {\\\"ModelID\\\":\\\"Simple Switch\\\",\\\"Identifier\\\":\\\"" + str(label) + "\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"开关\\\":0.0,\\\"锁定\\\":1.0},\\\"Statistics\\\":{},\\\"Position\\\":\\\"" + str(x) + "," + str(z) + "," + str(y) + "\\\",\\\"Rotation\\\":\\\"0,180,0\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0},\n"
        return label

    def crt_Multiplier(self, x, y, z):
        global label, component
        label += 1
        component += "        {\\\"ModelID\\\":\\\"Multiplier\\\",\\\"Identifier\\\":\\\"" + str(label) + "\\\",\\\"IsBroken\\\":false,\\\"IsLocked\\\":false,\\\"Properties\\\":{\\\"高电平\\\":3.0,\\\"低电平\\\":0.0,\\\"锁定\\\":1.0},\\\"Statistics\\\":{},\\\"Position\\\":\\\"" + str(x) + "," + str(z) + "," + str(y) + "\\\",\\\"Rotation\\\":\\\"0,180,0\\\",\\\"DiagramCached\\\":false,\\\"DiagramPosition\\\":{\\\"X\\\":0,\\\"Y\\\":0,\\\"Magnitude\\\":0.0},\\\"DiagramRotation\\\":0},\n"
        return label

    def crt_link(self, SourceLabel, SourcePin, TargetLabel, TargetPin):
        global link
        link += "        {\\\"Source\\\":\\\"" + str(SourceLabel) + "\\\",\\\"SourcePin\\\":" + str(SourcePin) + ",\\\"Target\\\":\\\"" + str(TargetLabel) + "\\\",\\\"TargetPin\\\":" + str(TargetPin) + ",\\\"ColorName\\\":\\\"蓝色导线\\\"},\n"

    def write(self, file):
        artical = head + component[:len(component) - 2:] + linkHead + link[:len(link) - 2:] + end
        with open(file, "w", encoding = "UTF-8") as f:
            f.write(artical)

# main #
experiment = physicsLab()

  # 生成D触，编号为[0, 127]
for z in [k / 10 for k in range(4)]:
    for y in [j / 10 for j in range(0, 16, 2)]:
        for x in [-1.8, -1.6, -1.4, -1.2]:
            experiment.crt_D_Flipflop(x, y, z)

  # D触clk引脚连线
for SourceLabel in [x + z for z in range(0, label, 32) for x in range(4)]:
    for TargetLabel in [SourceLabel + 4 * y for y in range(1, 8)]:
        experiment.crt_link(SourceLabel, 3, TargetLabel, 3)

  # 逻辑输入与逻辑输出，编号为[128, 149]
for x in [-1, -0.8]:
    for y in [i / 10 for i in range(11)]:
        if (x == -0.8 and y > 0.2):
            experiment.crt_Logic_Output(x, y, 0)
            continue
        if (y != 0.2):
            experiment.crt_Logic_Input(x, y, 0)
        else:
            experiment.crt_Logic_Input(x, y, 0, 0)

  # D触D引脚连线
for i in range(131, 139):
    for d in [z * 32 + x for z in range(4) for x in range(4)]:
        y = i - 131
        experiment.crt_link(i, 0, d + y * 4, 2)

  # 译码器，编号[150, 169]
for y in [-i / 10 - 0.1 for i in range(4)]:
    experiment.crt_AndGate(-1.8, y, 0)
experiment.crt_AndGate(-1.6, -0.5, 0)
experiment.crt_NimpGate(-1.6, -0.6, 0)
experiment.crt_NimpGate(-1.6, -0.7, 0)
experiment.crt_NorGate(-1.6, -0.8, 0)
experiment.crt_AndGate(-1.6, -0.1, 0)
experiment.crt_NimpGate(-1.6, -0.2, 0)
experiment.crt_NimpGate(-1.6, -0.3, 0)
experiment.crt_NorGate(-1.6, -0.4, 0)

for x in [-1.4, -1.2]:
    for y in [-i / 5 - 0.2 for i in range(4)]:
        experiment.crt_Multiplier(x, y, 0)

  # 或门，编号[170, 265]
for z in [-0.4, -0.3, -0.2, -0.1]:
    for y in [i / 5 for i in range(8)]:
        for x in [-1.8, -1.6, -1.4]:
            experiment.crt_OrGate(x, y, z)

  # D触Q引脚连线，连接到或门上
for z in range(4):
    for y in range(8):
        for x in range(4):
            experiment.crt_link(x + 4 * y + 32 * z, 0, int(x / 2) + 3 * y + 24 * z + 170, x % 2)

  # 或门输出引脚连线
for z in range(4):
    for y in range(8):
        for x in range(2):
            experiment.crt_link(170 + x + 3 * y + 24 * z, 2, 172 + 3 * y + 24 * z, x % 2)

  # 生成或门并使或门连接或门，原件编号[266, 281]
for y in range(8):
    for z in [-0.4, -0.3]:
        sign = experiment.crt_OrGate(-1.1, y / 5, z)
        if (z == -0.4):
            experiment.crt_link(172 + 3 * y, 2, sign, 0)
            experiment.crt_link(172 + 3 * y + 24 * 1, 2, sign, 1)
        else:
            experiment.crt_link(172 + 3 * y + 24 * 2, 2, sign, 0)
            experiment.crt_link(172 + 3 * y + 24 * 3, 2, sign, 1)

  # 生成或门并把刚才的或门的输出引脚连接上，编号[282, 289]
for y in range(8):
    sign = experiment.crt_OrGate(-1.1, y / 5, -0.2)
    experiment.crt_link(sign, 0, 266 + 2 * y, 2)
    experiment.crt_link(sign, 1, 267 + 2 * y, 2)

  # 生成输出寄存器，并连线，编号[290, 297]
for y in range(8):
    sign = experiment.crt_D_Flipflop(-1.1, y / 5, -0.1)
    experiment.crt_link(282 + y, 2, sign, 2)

  # 输出寄存器clk连线
for i in range(1, 8):
    experiment.crt_link(290, 3, 290 + i, 3)

  # 输出寄存器Q引脚连线
for i in range(8):
    experiment.crt_link(290 + i, 0, 142 + i, 0)
  # 输出寄存器clk连线
experiment.crt_link(290, 3, 141, 0)

  # 译码器剩余部分
experiment.crt_NoGate(-1.8, -0.5, 0)
experiment.crt_AndGate(-1.8, -0.6, 0)
experiment.crt_OrGate(-1.8, -0.7, 0)
experiment.crt_OrGate(-1.8, -0.8, 0)
experiment.crt_NorGate(-1.8, -0.9, 0)
experiment.crt_AndGate(-1.6, -0.9, 0)

''' 译码器部分的电路的导线由人工完成 '''
''' 程序自动生成的电路部分还有bug……不得不手动改存档了 '''
  # 与门label：[304, 431]

experiment.write("42763c41-14a7-41d2-9780-1310ede42f1e.sav")
# end main #