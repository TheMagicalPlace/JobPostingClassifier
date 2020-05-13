


with open('../ui/qt_gui.py', 'r') as intf:
    hm = intf.read()

import re

z = re.compile(r"(?<=[(|,\b])[0-9]+(?=[|,)])")
groupf = re.compile(r"(\([0-9, ]+\))")

t = """    def __setup_info_tab(self):
        self.Info = QtWidgets.QWidget()
        self.Info.setObjectName("Info")
        self.intro_cont = QtWidgets.QGroupBox(self.Info)
        self.intro_cont.setGeometry(QtCore.QRect(10, 10, 871, 351))
        self.intro_cont.setTitle("")
        self.intro_cont.setObjectName("intro_cont")
        self.intro_info = QtWidgets.QTextBrowser(self.intro_cont)
        self.intro_info.setGeometry(QtCore.QRect(10, 10, 851, 331))
        self.intro_info.setObjectName("intro_info")
        self.MainTab.addTab(self.Info, "")"""



def repl(m):
    print(m.group())
    nums = re.findall('[0-9]+', m.group())

    if len(nums) == 4:
        for j,numm in enumerate(nums):
            nums[j] = re.sub('[0-9]+',f'int({numm}*SCALE_FACTOR)',nums[j])
        else:
            e = f"({nums[0]}, {nums[1]}, {nums[2]}, {nums[3]})"
    else:
        e = "(" +", ".join(nums)+")"
    return e

e =re.sub(groupf,repl,hm)
print(e)



with open('gui_test.py','w') as gut:
    gut.write(e)
print(e)