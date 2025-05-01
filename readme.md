# 의존성 주입 문제 해결
> 비동기 프로그래밍으로 외부 DI 라이브러리 없이 의존성 주입 구현
1. Sub-dependency로 모든 계층의 생성자 주입 구현
2. fastapi-utils 라이브러리로 라우터 계층에서의 의존성 주입 반복 코드 제거

## 정상 작동 확인
1. 요청별 DB 트랜잭션 처리
2. 동시 요청 처리
3. 독립적인 테스트 실행

## 서버 실행 (루트 디렉토리 기준)
- `uvicorn app.main:app [--reload]`
- `localhost:8000/docs`에서 API 문서 확인

## 테스트 실행 (루트 디렉토리 기준)
- 전체 테스트: `python -m unittest discover -s tests -p "*.py"`
- 개별 파일 단위: `python -m unittest tests/<테스트 파일>`

## 참고
https://devocean.sk.com/blog/techBoardDetail.do?ID=167025&boardType=techBlog

## TODO
- HTTP 예외 처리
- 동기 작업과의 성능 비교