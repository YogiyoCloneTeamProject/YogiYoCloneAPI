# YogiYoCloneAPI

<p align="center">
<img width="400" alt="7" src="https://user-images.githubusercontent.com/63357508/95486781-6ce82c00-09ce-11eb-9d6d-08bec966d3d8.jpg"</p>


## Description
음식 배달 서비스 요기요 앱 클론 프로젝트로서 Django, DRF를 활용한 REST API개발 역량을 키우고 iOS팀과 협업하여 커뮤니케이션 능력을 다지는 것을 목표로 했습니다.

## Contributors
- 김주원 [GitHub](https://github.com/Joyykim)
- 최사라 [GitHub](https://github.com/withHappy)

## Features

### 공통
- 요기요 실제 서비스 API를 Requests 라이브러리로 스크랩핑
- 회원가입, 휴대폰 인증 후 유저 활성화
- 토큰을 이용한 로그인
- AWS EC2에 서버 배포
- AWS RDS에 DB 세팅 및 EC2 서버 연결
- AWS S3에 업로드 이미지 저장

### 음식점
- 음식점 목록
	-  필터링
	-  좌표 기준 일정 범위 음식점 반환
	-  추천 매장 목록
- 음식점 검색
- 메뉴, 옵션 선택 및 결제
- 음식점 찜(즐겨찾기)

### 주문
- 메뉴, 옵션 선택하여 주문 생성
- 주문 내역 목록, 상세보기

### 리뷰
- 주문한 메뉴에 한하여 리뷰 생성
- 총점, 맛, 양, 배달 등 다양한 요소에 대한 평가
- 리뷰 생성시 이미지 첨부 기능
- 리뷰에 사장님이 답글 생성

## Requirements

### Language
- Python 3.7

### Framework
- Django 3.1
- Django REST Framework 3.11.1

### Library
- gunicorn - HTTP wsgi server
- requests - crawling
- model-bakery - testcode
- dj-inmemorystorage - testcode
- drf-nested-routers - url form
- boto3 - AWS S3
- drf-yasg - API docs
- django-filter - filter
- django-taggit - tag

## Architecture
![architecture](https://raw.githubusercontent.com/YogiyoCloneTeamProject/YogiYoCloneAPI/develop/readme_image/yogiyo%20architecture.png)

## Document
- [Redoc UI](https://bit.ly/3iD0OHn)

## ERD
- [draw.io](https://drive.google.com/file/d/1ozCishbdkWk1DfW-K6BgQceuMHwHoJWi/view?usp=sharing)

## Tools
- Pycharm - IDE
- Slack - 커뮤니케이션
- Github Projects - 이슈 관리
- Drow.io - ERD 작성
