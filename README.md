# AI-image-serving
AI 모델 서빙 1. 이미지 분류

1. (배포전 개발용)local로 돌릴 때 

unicorn app_img:app --reload --port 9000 
or 
가상환경 만들어서 필요한거 다 깔고난 후
python3.10 -m uvicorn app_img:app --reload --port 9000

2. 배포 아직 안함..