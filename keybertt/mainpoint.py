from keybert import KeyBERT
import os
from tutorials_soykeyword import bridge

def pointword(filename): #텍스트 전문에서 핵심 단어를 추출
      path_dir = 'C:\\Users\\woojye\\Desktop\\image_manager_usingFlask\\static'
      file_list = os.listdir(path_dir)
      
      f=open("C:\\Users\\woojye\\Desktop\\image_manager_usingFlask\\static\\1{}.txt".format(filename), "r", encoding='utf-8')
      result = open("C:\\Users\\woojye\\Desktop\\image_manager_usingFlask\\static\\{}.txt".format(filename),"w", encoding='UTF-8')
      line=f.readlines()
      doc2=''.join(line)

      kw_model = KeyBERT()
      keywords = kw_model.extract_keywords(doc2, keyphrase_ngram_range=(1,1), stop_words=None)
      f.close()

      for file_name in file_list :
            if file_name == "{}.txt".format(filename):
                continue
            result.write(''.join(map(str, keywords)))
      result.close()
      
def relativeword(filename): #핵심 단어와 연관된 단어를 soykeyword를 통해 얻은 후 텍스트 파일에 추가로 저장한다.      
      #사전에 설정한 단어가 텍스트 파일에 있는지 확인한다.
      target="Ethernet" #키워드 새로 추가시 수정
      with open("C:\\Users\\woojye\\Desktop\\image_manager_usingFlask\\static\\1{}.txt".format(filename),'r',encoding='UTF-8') as file:
        text = file.read()
        if target in text:
            flag = True
        else:
            flag = False
      
      f=open("C:\\Users\\woojye\\Desktop\\image_manager_usingFlask\\static\\{}.txt".format(filename), "a", encoding='utf-8') #텍스트 파일 덮어쓰기

      if flag==True:
            keywords=bridge.bridgefunction()

            #for file_name in file_list :
            #   if file_name == "{}.txt".format(filename):
            #      continue
            f.write(''.join(map(str, keywords)))
            f.close()
      else:
            f.close()
                  
      #전문 텍스트 파일은 키워드 검색 시 중복 우려가 있으므로 삭제한다.
      if os.path.exists("C:\\Users\\woojye\\Desktop\\image_manager_usingFlask\\static\\1{}.txt".format(filename)): 
         os.remove("C:\\Users\\woojye\\Desktop\\image_manager_usingFlask\\static\\1{}.txt".format(filename))