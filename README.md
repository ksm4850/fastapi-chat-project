# FastAPI Chat Project
> FastAPI의 웹소켓 기능을 활용한 간단 채팅서비스 구현

![Static Badge](https://img.shields.io/badge/Python-%233776AB)
![Static Badge](https://img.shields.io/badge/Fastapi-%23009688)
![Static Badge](https://img.shields.io/badge/PostgreSql-%234169E1)
![Static Badge](https://img.shields.io/badge/Sqlalchemy-%23f65855)
![Static Badge](https://img.shields.io/badge/Dependency_Injector-blue)
![Static Badge](https://img.shields.io/badge/Poetry-%2360A5FA)
![Static Badge](https://img.shields.io/badge/Gunicorn-%23499848)
![Static Badge](https://img.shields.io/badge/Docker-%232496ED)
![Static Badge](https://img.shields.io/badge/JwtToken-red)

## 목표
1. 웹소켓에 대한 이해
2. DIP에 대한 이해

##  프로젝트 상세 내용
#### 1. FastAPI 웹소켓 공식문서 URL : https://fastapi.tiangolo.com/ko/advanced/websockets/
#### 2. dependency-injector 공식문서 URL : https://python-dependency-injector.ets-labs.org/
#### 3. Github repo 참고 :
- https://github.com/teamhide/fastapi-layered-architecture
- https://github.com/rumbarum/fastapi-boilerplate-on-di

#### 4. 프론트화면은 Chat-GPT이용해서 간단한 화면 구현

## 실행방법

1. git clone
2. cmd창에서 fastapi-chat-project/src 경로에서 ```docker-compose up``` 실행
3. ```http://localhost:8000``` 접속 -> 로그인페이지 리다이렉트
4. ```http://localhost:8000/docs``` swagger문서

## 실행
### 로그인 페이지
![login](https://github.com/user-attachments/assets/7efc942d-7ce4-43d0-a1aa-783f17f045d4)

### 회원가입 페이지
![join](https://github.com/user-attachments/assets/c1b39214-3107-47d5-9347-416bfc31dcf9)

### 메인 페이지
![main](https://github.com/user-attachments/assets/fe4dc14c-3475-4572-a5e3-f09009340dfc)