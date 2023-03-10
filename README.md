# 파이썬을 활용한 "디지털 이미지 관리 어플리케이션 설계 및 구현"

## 개요

본 프로젝트는 수많은 사진들 중에 찾고자 하는 사진을 보다 쉽게 찾도록 도와주는 서비스입니다. 사용자가 이미지를 업로드하면, 이미지 속 특징들(텍스트)이 로컬 디렉토리에 저장됩니다. 이후 사용자는 특정 이미지를 찾을 때 키워드 검색을 통해 간편하게 해당 사진을 찾을 수 있습니다.
프로젝트에서는 python, flask 라이브러리를 이용한 웹서비스를 제공하고 있습니다.

## 주요 기능

- 이미지 속 텍스트 원문을 텍스트 파일로 변환하고 keybert 모델을 통해 핵심 단어를 추출 및 저장합니다.
- 원문 파일에 특정 주제의 키워드(예. celebrity, 사용자 지정 가능)가 있다면 해당 키워드와 연관된 단어들 또한 텍스트 파일에 저장됩니다.
- 웹페이지 검색 창을 통해 이미지와 관련된 단어를 입력하면, 새 페이지에서 해당 이미지를 보여줍니다. 찾고자 하는 이미지가 없다면 찾지 못했다는 문구를 출력합니다.
- 전문 텍스트 파일은 메모리 효율과 검색 정확도를 위해 키워드 추출이 끝나면 삭제됩니다.

## 이용 안내

- 본 서비스는 텍스트가 포함된 이미지를 대상으로 합니다. (예. 유튜브 댓글 스크린샷)
- 이미지 속 텍스트는 영어어야 하며, 일부 문자/기호의 경우 오류가 발생할 수 있습니다.
- tokenized 폴더에 학습시키고자 하는 텍스트 데이터가 저장되어 있다면, 별도의 학습 과정 필요 없이 바로 웹서비스를 이용할 수 있습니다.
- 기본 노트북 사양으로도 작동 가능합니다.
- 코드를 처음 사용할 경우, 이미지가 저장될 경로를 모두 바꿔주어야 합니다.
- 업로드한 이미지와 핵심 키워드 텍스트 파일은 프로젝트폴더/static 폴더에 저장됩니다.
- 이름이 중복된 사진 파일은 자동으로 삭제됩니다.

## 사용자 맞춤 추가 키워드 학습시키기

-사용자 맞춤 연관 키워드를 학습시킬 수 있습니다.

1) tokenized 폴더에 학습시키고자 하는 데이터를 xxx.txt 파일 하나로 저장합니다. .txt 파일 작성시 각 줄이 하나의 데이터 셋을 나타내게 됩니다.
2) bridge.py 파일에서 def bridgefunction() 함수에서 문자열에 해당하는 부분을 새로 추가한 텍스트 파일 이름, 새로 추가한 키워드로 각각 수정합니다.
3) keybertt 폴더 속 mainpoint.py의 relativeword() 함수에서 target 변수를 새로운 키워드로 변경합니다.
4) bridge.py bridgefuction() 함수에서 min_score, min_frequency 변수를 조정하여 키워드 추출 기준을 설정할 수 있습니다.

## 슬라이드 

![poster](/slide/슬라이드3.JPG)
![poster](/slide/슬라이드4.JPG)
![poster](/slide/슬라이드5.JPG)
![poster](/slide/슬라이드6.JPG)
![poster](/slide/슬라이드7.JPG)
![poster](/slide/슬라이드8.JPG)
![poster](/slide/슬라이드9.JPG)

## 사용한 도구

### 텍스트 에디터

-Visual Studio Code

### 파이썬 라이브러리

- 파이썬 버전: 3.8.6
- 라이브러리: soykeyword, numpy, scikit-learn, psutil, flask, pillow, gevent, gunicorn, pytesseract, tesseract, keybert, cv2

## 참고 자료

<https://github.com/lovit/soykeyword>
<https://github.com/bboe/flask-image-uploader>
<https://github.com/MaartenGr/KeyBERT>
