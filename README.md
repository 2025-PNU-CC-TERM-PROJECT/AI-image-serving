# AI-image-serving  
**AI 모델 서빙 1. 이미지 분류**

이미지 분류 모델을 마이크로서비스 형태로 서빙하는 프로젝트
FastAPI 기반으로 개발되었으며, TorchServe로 모델 추론을 처리하고 Kubernetes 기반 인프라에 배포되어 운영될 수 있도록 구성

---

## 프로젝트 개요

- 입력 이미지를 분류하여 사전 학습된 모델을 통해 해당 클래스 정보 예측
- RESTful API 형태로 이미지를 전달하면, 분류 결과를 JSON으로 반환
- TorchServe로 모델을 서빙하고, KServe + Istio 기반의 마이크로서비스 아키텍처에 통합

---

## 로컬 실행 (FastAPI 개발 서버)

### 1. FastAPI 서버 실행

```bash
# (선택) 가상환경 생성 및 활성화
python3.10 -m venv venv
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 서버 실행
uvicorn app_img:app --reload --port 9000 '''


