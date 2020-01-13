import sys
import win32clipboard 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from PyQt5.QtWidgets import QApplication,QWidget,QLineEdit,QLabel,QVBoxLayout
from PyQt5.Qt import QPushButton, QGridLayout, QComboBox
from PyQt5 import QtGui
from time import sleep
from bs4 import BeautifulSoup

def copy(self,text):
    win32clipboard.OpenClipboard()
    win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    
def number(self,lis):
    number = ''
    for string in lis:
        number = number + str(ord(string)) 
    return number


class search(object):
    def __init__(self):
        pass
        
    def run(self,Cate,Color,Size,whichColor,item):
        #self.option=webdriver.ChromeOptions()
        #self.option.add_argument('headless') 
        #self.browser = webdriver.Chrome(chrome_options=self.option) 
        
        #website url
        self.browser = webdriver.Chrome()
        self.browser.get('https://www.supremenewyork.com/shop/all')
        #item for purchase which should be change every time
        self.category = Cate
        self.name = item
        self.color = Color
        self.whatColor = whichColor

        #main program
        self.browser.implicitly_wait(3)
        while len(self.browser.find_elements_by_link_text(self.category))==0:
            self.browser.refresh()
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_link_text(self.category).click()
        self.browser.implicitly_wait(3)
        while len(self.browser.find_elements_by_link_text(self.name))==0:
            self.browser.refresh()
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_link_text(self.name).click()
        if self.color:
            self.browser.find_element_by_xpath("//a[@data-style-name = '%s']" % self.whatColor).click()
        sleep(0.5)
        self.size = Select(self.browser.find_element_by_id("s"))
        self.size.select_by_visible_text(Size)
        self.browser.find_element_by_name('commit').click()
        
    def purchase(self):
        self.person_name = 'Biyao Li'
        self.email = 'libiyao73@gmail.com'
        self.tel = '8589006126'
        self.address = '2100 NE Whitman Ln'
        self.roomNum = '508'
        self.zipcode = '98195'
        self.month = 2
        self.year = 24
        self.rvv = 812
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_link_text('checkout now').click()
        self.browser.find_element_by_id('order_billing_name').send_keys(self.person_name)
        self.browser.find_element_by_id('order_email').send_keys(self.email)
        copy(self,self.tel)
        self.browser.find_element_by_id('order_tel').send_keys(Keys.CONTROL,'v')
        self.browser.find_element_by_id('bo').send_keys(self.address)
        self.browser.find_element_by_id('oba3').send_keys(self.roomNum)
        self.browser.find_element_by_id('order_billing_zip').send_keys(self.zipcode)
        copy(self,number(self,[',','\x00','\x00','B','Q','.','A','Q','\x00','\x01']))
        self.browser.find_element_by_id('nnaerb').send_keys(Keys.CONTROL,'v')
        date = Select(self.browser.find_element_by_id('credit_card_month'))
        date.select_by_index(self.month-1)
        years = Select(self.browser.find_element_by_id('credit_card_year'))
        years.select_by_index(self.year-19)
        self.browser.find_element_by_id('orcer').send_keys(self.rvv)
        self.browser.find_element_by_xpath('//input[@id = "order_terms"]').send_keys(Keys.SPACE)
        #self.browser.find_element_by_name('commit').click()

class App(QWidget):      
    def __init__(self):
        super().__init__()
        self.title = 'Biyao'
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('headless') 
        self.web = webdriver.Chrome(chrome_options=self.option)
        self.web.get('https://www.supremecommunity.com/season/spring-summer2019/droplists/')
        self.web.find_element_by_id('box-latest').click()
        self.soup = BeautifulSoup(self.web.page_source, 'html5lib')
        self.item_list = ['']
        for items in self.soup.find_all('h2',class_= 'name item-details item-details-title'):
            self.item = items.text.strip()
            self.item_list.append(self.item)
        self.createWindow()
   
                
    def createWindow(self):
        self.status = True
        self.cateStatus = ''
        self.sizes = ''
        self.setWindowTitle(self.title)
        self.item = ''
        self.color = ''
        
        #Button
        self.button1 = QPushButton('Start Running',self)
        self.button1.clicked.connect(lambda: search.run(self,self.cateStatus,self.status,self.sizes,self.color,self.item))
        self.button2 = QPushButton('Purchase',self)
        self.button2.clicked.connect(lambda: search.purchase(self))
        self.button3 = QPushButton('Close',self)
        self.button3.clicked.connect(lambda: self.close())
        self.button4 = QPushButton('Add item',self)
        
        #Dropdown menu
        Options = ['','True','False']
        self.TF = QComboBox(self)
        self.TF.addItems(Options)
        self.TF.activated[str].connect(self.changeOption)
        
        CateOptions = ['','jackets','shirts','tops/sweaters','sweatshirts','pants','shorts','t-shirts','hats','bags','accessories']
        self.cateBox = QComboBox(self)
        self.cateBox.addItems(CateOptions)
        self.cateBox.activated[str].connect(self.changeCateOption)
        
        sizeOption = ['','Small','Medium','Large']
        self.sizeBox = QComboBox(self)
        self.sizeBox.addItems(sizeOption)
        self.sizeBox.activated[str].connect(self.changeSize)
        
        itemList = self.item_list
        self.itemBox = QComboBox(self)
        self.itemBox.addItems(itemList)
        self.itemBox.activated[str].connect(self.changeitem)
        
        #Textbox
        self.EnterColor = QLineEdit(self)
        self.EnterColor.textChanged[str].connect(self.changeColor)
        
        #Label
        self.Name = QLabel('Name: ', self)
        self.Name.setFont(QtGui.QFont('Microsoft YaHei', 9))
        
        self.Category = QLabel('Category: ', self)
        self.Category.setFont(QtGui.QFont('Microsoft YaHei', 9))
 
        self.Sizes = QLabel('Size: ', self)
        self.Sizes.setFont(QtGui.QFont('Microsoft YaHei', 9))
        
        self.color = QLabel('Color(True/False): ', self)
        self.color.setFont(QtGui.QFont('Microsoft YaHei', 9))
        
        self.whatColor = QLabel('Color: ', self)
        self.whatColor.setFont(QtGui.QFont('Microsoft YaHei', 9))
        
        #Vbox 
        Operation = QVBoxLayout()
        Operation.addWidget(self.button4)
        Operation.addWidget(self.button1)
        Operation.addWidget(self.button2)
        Operation.addWidget(self.button3)
        Structure = QGridLayout()
        Structure.addLayout(Operation, 4, 0)
        Structure.addWidget(self.Name, 0, 0)
        Structure.addWidget(self.itemBox, 0, 1)
        Structure.addWidget(self.Category, 1, 0)
        Structure.addWidget(self.cateBox, 1, 1)
        Structure.addWidget(self.Sizes, 2, 0)
        Structure.addWidget(self.sizeBox, 2, 1)
        Structure.addWidget(self.color, 3, 0)
        Structure.addWidget(self.TF, 3, 1)
        Structure.addWidget(self.whatColor, 3, 2)
        Structure.addWidget(self.EnterColor, 3, 3)
        
        #Display
        self.setLayout(Structure)
        self.show()
        
    def changeOption(self, tf):
        if tf == 'True':
            self.status = True
        else:
            self.status = False
            
    def changeColor(self, color):
        self.color = color
    
    def changeCateOption(self, option):
        self.cateStatus = option
        
    def changeSize(self, size):
        self.sizes = size
    
    def changeitem(self, item):
        self.item = item
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())



    
    
