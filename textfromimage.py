import pytesseract

def tdi(filename):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    result = open("C:\\Users\\woojye\\Desktop\\image_manager_usingFlask\\static\\1{}.txt".format(filename),"w", encoding='UTF-8')

    file_name="{}.jpg".format(filename)
    result.write(pytesseract.image_to_string('C:\\Users\\woojye\\Desktop\\image_manager_usingFlask\\static\\{}'.format(file_name))+'\n') #lang='ENG' 삭제함.
    result.close()