import os

def searcher(uid): #검색한 키워드가 포함된 사진의 이름을 확장자와 함께 반환한다.
    searchstring=uid
    c=[]
    for (path, dir, files) in os.walk("C:\\Users\\woojye\\Desktop\\image_manager_usingFlask\\static"):
        for filename in files:
            with open(path+os.sep+filename, 'r', encoding='utf-8') as f:
                try:
                    if searchstring in f.read():
                        a=filename
                        b=a.rsplit('.')[0]+".{}".format("jpg")
                        c.append(b)
                    else:
                        pass
                except:
                    pass
    return c