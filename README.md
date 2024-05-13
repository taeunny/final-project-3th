# Mentos



## 1. 프로젝트 배경 및 목표

### 배경

​	현대 사회에서 스트레스와 정신적 고민은 누구나 겪을 수 있는 일상적인 문제가 되었습니다.  

​	이러한 문제를 해결하기 위해 많은 사람들이 심리 상담을 찾지만, 시간과 비용, 접근성 문제, 사회적 편견 등으로 인해 실제 상담을 받는 게 쉽지 않은 경우가 많습니다.  

​	위 문제들을 해결하기 위해 심리상담 챗봇 서비스가 시행되고 있습니다. 

​	그러나 사람들 개성과 상황에 따라 선호하는 소통 방식이 다르기 때문에 다소 말투가 차갑게 느껴질 수 있고, 사용자는 상담 말투에 따라 만족도나 개선 효과가 달라질 수 있습니다.

​	실제 심리 상담에서도 이러한 개인의 선호를 반영하여 상담을 진행함에 따라 만족도나 개선 효과가 달라지는 것처럼 말이죠

### 목표

​	위와 같은 문제를 해결하고자 저희 Mentos는 __다양한 말투를 사용하여 사용자에게 맞춤형 상담을 제공하는 심리상담 챗봇__ 을 주제로 프로젝트를 진행하였습니다.





## 2. 서비스 Flow & ERD
<img src="https://i.ibb.co/sHqDC0t/mentos-flow-1.png" alt="mentos-flow-1" border="0">  

**1. project에 사용할 모델 분석 및 선정** 
   1) meta-llama/Meta-Llama-3-8B-Instruct
   2) microsoft/Phi-3-mini-4k-instruct
   3) yanolja/EEVE-Korean-Instruct-10.8B-v1.0  
**=>세 모델 중에서 실용적 측면 및 이미 한국어 단어장이 추가 된 EEVE 모델을 프로젝트 모델로 선정** 

**2. HuggingFace의 trl 라이브러리를 활용한 SFT 진행**
   - Smoked-Salmon-s/empathetic_dialogues_ko 데이터 활용하여 singgleturn으로 SFT 학습 진행  
   - 진행시 다양한 하이퍼 파라미터를 선정하여 출력을 비교

**3. HuggingFace의 trl 라이브러리를 활용한 DPO 진행**
   - Naver ClovaX를 활용하여 DPO의 chosen과 rejected 칼럼을 생성(약 1만개)
   - 해당 chosen, rejected 데이터를 활용하여 DPO 진행

**4. LangChain을 활용하여 RAG 구현**
   - 허깅페이스의 HuggingFaceEmbeddings, 랭체인의 VectorStore, FAISS 등등 활용하여
   - RAG를 구현하고 해당 RAG를 프로젝트 모델에 적용시켜 멀티턴을 구현
 
**5. 최종 모델 평가 및 실제 인퍼런스용 모델 선정**
   - G-eval 및 실제 사용 후기를 통한 성능 평가 진행 

**6. inference**
   - FastAPI 및 Gradio를 활용하여 모듈화 및 실제 시연 준비
   - 구체적인 UI 및 유저 편의성 고려하여 조정
<img src="https://i.ibb.co/dpk7Xjz/mentalcare-erd-6.png" alt="mentalcare-erd-6" border="0">

## 3. 프로젝트 일정
<img src="https://i.ibb.co/hBPQzcP/image.png" />

## 4. 프로젝트 구성 및 담당자

### 홍성균

<img src="https://i.ibb.co/ydy5G3H/Kakao-Talk-20240510-182343911.png" alt="Kakao-Talk-20240510-182343911" border="0" height="150" width="120"/>

1. **개발 환경 설정**
   - GCP, AWS 등 GPU사용 환경 설정

2. **모델 선정 및 분석** 
   - meta-llama/Meta-Llama-3-8B-Instruct
   - microsoft/Phi-3-mini-4k-instruct
   - yanolja/EEVE-Korean-Instruct-10.8B-v1.0
  
3. **huggingface trl 라이브러리 활용하여 SFT, DPO 진행**
   - 하이퍼 파라미터를 다양하게 설정하여 모델 출력 비교 분석
   - DPO 관련 데이터셋 준비 (naver-clovaX활용) 후 DPO 실시


### 박태은

<img src="https://i.ibb.co/K9jXHcM/image.png"  height="160" width="130"/>

1. 





### 이희성

<img src="https://i.ibb.co/NtvvgzH/image.png" alt="image" border="0" height="150" width="120"/>

1. 





### 이현지


<img src="https://i.ibb.co/RvKVd8v/image.png" alt="image" border="0" height="165" width="120"/>  



1. **데이터베이스 설계 및 구현**
   - AWS RDS를 활용한 MySQL 데이터베이스 설계 및 구현. 
   - pymysql 라이브러리를 사용하여 데이터베이스 연결 및 데이터 흐름 검증.
2.  **데이터 수집**
     - selenium을 이용하여 웹 사이트 데이터 정보 크롤링 및 스크랩핑.
3. **데이터 분석 및 시각화**
   - pandas를 이용한 데이터 전처리 및 분석, matplotlib 및 seaborn을 사용한 통계적 데이터 시각화, plotly를 활용한 인터랙티브 데이터 시각화 작업 수행.





##  5. 사용 툴

| Category | Techs                                                        |
| -------- | ------------------------------------------------------------ |
| 🖥️ 개발   | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=white) ![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)  ![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white) ![OpenAI](https://img.shields.io/badge/openai-412991?style=for-the-badge&logo=openai&logoColor=white)  ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![VisualStudioCode](https://img.shields.io/badge/visualstudiocode-007ACC?style=for-the-badge&logo=mysql&logoColor=white) ![MYSQL](https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white) |
| ☁️ 환경   | ![nVIDIA](https://img.shields.io/badge/nVIDIA-%2376B900.svg?style=for-the-badge&logo=nVIDIA&logoColor=white) ![Anaconda](https://img.shields.io/badge/Anaconda-%2344A833.svg?style=for-the-badge&logo=anaconda&logoColor=white) ![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white) |
| 📋 협업   | ![Notion](https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![GitHub]( https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=Discord&logoColor=white) |





## 6. 데이터 셋

#### uine/single-practice-dataset

![uine/single-practice-dataset](https://i.ibb.co/LzMbHD5/image.png)

- 원본 데이터인 **Smoked-Salmon-s/empathetic_dialogues_ko**에서 **single turn** 데이터만 정제
- **약 8천개 학습 데이터 셋 사용**


## 7. 모델학습 및 기능구현 flow
**1. project에 사용할 모델 분석 및 선정** 
   1) meta-llama/Meta-Llama-3-8B-Instruct
   2) microsoft/Phi-3-mini-4k-instruct
   3) yanolja/EEVE-Korean-Instruct-10.8B-v1.0  
**=>세 모델 중에서 실용적 측면 및 이미 한국어 단어장이 추가 된 EEVE 모델을 프로젝트 모델로 선정** 

**2. HuggingFace의 trl 라이브러리를 활용한 SFT 진행**
   - Smoked-Salmon-s/empathetic_dialogues_ko 데이터 활용하여 singgleturn으로 SFT 학습 진행  
   - 진행시 다양한 하이퍼 파라미터를 선정하여 출력을 비교

**3. HuggingFace의 trl 라이브러리를 활용한 DPO 진행**
   - Naver ClovaX를 활용하여 DPO의 chosen과 rejected 칼럼을 생성(약 1만개)
   - 해당 chosen, rejected 데이터를 활용하여 DPO 진행

**4. LangChain을 활용하여 RAG 구현**
   - 허깅페이스의 HuggingFaceEmbeddings, 랭체인의 VectorStore, FAISS 등등 활용하여
   - RAG를 구현하고 해당 RAG를 프로젝트 모델에 적용시켜 멀티턴을 구현
 
**5. 최종 모델 평가 및 실제 인퍼런스용 모델 선정**
   - G-eval 및 실제 사용 후기를 통한 성능 평가 진행 

**6. inference**
   - FastAPI 및 Gradio를 활용하여 모듈화 및 실제 시연 준비
   - 구체적인 UI 및 유저 편의성 고려하여 조정


## 8. 결과  
<img src="https://i.ibb.co/nk8FH4d/result.png" alt="result" border="0">
- 질문에 대한 모델1, 2, 3, 4의 답변들  
  
  
<img src="https://i.ibb.co/ZB5HpWG/result.png" alt="result" border="0">
- 모델1, 2, 3, 4 평가 지표
- 모델3이 가장 좋은 평가를 보임
