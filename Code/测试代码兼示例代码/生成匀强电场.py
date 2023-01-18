'''
    这是我对物实程序化的第一次尝试
    写得很简陋，因为为了赶工（）
    类似的思路也被用于实现我的第一个程序化电学实验
    最终刺激我写了现在的那个玩意（physicsLab.py）
'''

head = '''{
  "Type": 4,
  "Experiment": {
    "ID": null,
    "Type": 4,
    "Components": 3,
    "Subject": null,
    "StatusSave": "{\\\"SimulationSpeed\\\":1.0,\\\"Elements\\\":
    ['''
############################
end =  '''    ]}",
    "CameraSave": "{\\\"Mode\\\":1,\\\"Distance\\\":2.0,\\\"VisionCenter\\\":\\\"0,0.88,0\\\",\\\"TargetRotation\\\":\\\"90,0,0\\\"}",
    "Version": 2404,
    "CreationDate": 1673014816541,
    "Paused": true,
    "Summary": null,
    "Plots": null
  },
  "ID": null,
  "Summary": {
    "Type": 4,
    "ParentID": null,
    "ParentName": null,
    "ParentCategory": null,
    "ContentID": null,
    "Editor": null,
    "Coauthors": [],
    "Description": null,
    "LocalizedDescription": null,
    "Tags": [
      "Type-4"
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
    "CreationDate": 1673014667293,
    "UpdateDate": 0,
    "SortingDate": 0,
    "ID": null,
    "Category": null,
    "Subject": "匀强电场",
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
  "InternalName": "匀强电场",
  "Speed": 1.0,
  "SpeedMinimum": 0.1,
  "SpeedMaximum": 2.0,
  "SpeedReal": 0.0,
  "Paused": true,
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

def crt_pCharge(x, y, z = 0): # 正电荷
    return "      {\\\"ModelID\\\":\\\"Positive Charge\\\",\\\"Identifier\\\":\\\"d854643b21b54bf0a72fed4df1283731\\\",\\\"Properties\\\":{\\\"锁定\\\":1.0,\\\"强度\\\":1E-07,\\\"质量\\\":0.1},\\\"Position\\\":\\\""+str(x)+","+str(z)+","+str(y)+"\\\",\\\"Rotation\\\":\\\"0,0,0\\\",\\\"Velocity\\\":\\\"0,0,0\\\",\\\"AngularVelocity\\\":\\\"0,0,0\\\"},\n"

def crt_nCharge(x, y, z = 0): # 负电荷
    return "      {\\\"ModelID\\\":\\\"Negative Charge\\\",\\\"Identifier\\\":\\\"ca7b921ed3b143608b78b934926bfb2d\\\",\\\"Properties\\\":{\\\"锁定\\\":1.0,\\\"强度\\\":-1E-07,\\\"质量\\\":0.1},\\\"Position\\\":\\\""+str(x)+","+str(z)+","+str(y)+"\\\",\\\"Rotation\\\":\\\"0,0,0\\\",\\\"Velocity\\\":\\\"0,0,0\\\",\\\"AngularVelocity\\\":\\\"0,0,0\\\"},\n"

def main():
    print(head)

    # write body
    body = ""
    startNum = -4.0
    endNum = 4.0
    increase = 0.03125 # increase num of 'x'
    y_pCharge = 1
    y_nCharge = -1

    x_pCharge = startNum
    while (x_pCharge <= endNum):
        body += crt_pCharge(x_pCharge, y_pCharge)
        x_pCharge += increase
    x_nCharge = startNum
    while (x_nCharge <= endNum):
        body += crt_nCharge(x_nCharge, y_nCharge)
        x_nCharge += increase

    print(body[:len(body) - 2:])
    # end write body

    print(end)

main()