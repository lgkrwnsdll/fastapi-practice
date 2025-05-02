# FastAPI Practice
> 비동기 패러다임에서 외부 DI 라이브러리 없이 의존성 주입 구현
1. Sub-dependency로 모든 계층의 생성자 주입 구현
2. fastapi-utils 라이브러리로 라우터 계층에서의 의존성 주입 반복 코드 제거

## 정상 작동 확인
### 1. 요청별 DB 트랜잭션 처리
> pycharm 디버깅 툴 활용
```mermaid
---
config:
  theme: neo-dark
---
sequenceDiagram
  participant inject_session as inject_session
  participant Router as Router
  participant @Transactional as @Transactional
  inject_session ->> Router: 세션 생성, 컨텍스트 설정
  Router ->> @Transactional: 요청 전달
  @Transactional ->> @Transactional: DB 작업 수행
  @Transactional ->> Router: 세션 커밋/롤백 및 종료
  Router ->> inject_session: (세션 종료), 컨텍스트 해제
```

### 2. 동시 요청 처리
> apache benchmark 활용
- `ab -n 1000 -c 100 http://localhost:8000/v2/data`
```
Server Software:        uvicorn
Server Hostname:        localhost
Server Port:            8000

Document Path:          /v2/data
Document Length:        204 bytes

Concurrency Level:      100
Time taken for tests:   5.165 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      349000 bytes
HTML transferred:       204000 bytes
Requests per second:    193.61 [#/sec] (mean)
Time per request:       516.510 [ms] (mean)
Time per request:       5.165 [ms] (mean, across all concurrent requests)
Transfer rate:          65.99 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.4      0       2
Processing:    66  278  32.5    278     429
Waiting:       63  271  32.1    271     418
Total:         67  278  32.5    278     429

Percentage of the requests served within a certain time (ms)
  50%    278
  66%    287
  75%    296
  80%    303
  90%    317
  95%    325
  98%    349
  99%    358
 100%    429 (longest request)
```
- `ab -n 1000 -c 10 http://localhost:8000/v2/data`

```
Server Software:        uvicorn
Server Hostname:        localhost
Server Port:            8000

Document Path:          /v2/data
Document Length:        204 bytes

Concurrency Level:      10
Time taken for tests:   4.764 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      349000 bytes
HTML transferred:       204000 bytes
Requests per second:    209.92 [#/sec] (mean)
Time per request:       47.637 [ms] (mean)
Time per request:       4.764 [ms] (mean, across all concurrent requests)
Transfer rate:          71.54 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.4      0       2
Processing:    17   27   5.8     26      72
Waiting:       14   26   5.7     25      71
Total:         17   27   5.8     26      72

Percentage of the requests served within a certain time (ms)
  50%     26
  66%     27
  75%     28
  80%     28
  90%     29
  95%     32
  98%     47
  99%     60
 100%     72 (longest request)
```

### 3. 독립적인 테스트 실행
> unittest로 클래스 기반 테스트 코드 작성

> ⚠️ 주의
> - `unittest.IsolatedAsyncioTestCase`는 테스트마다 event loop을 생성한다
>   - https://docs.python.org/3/library/unittest.html#unittest.IsolatedAsyncioTestCase.run
> - 테스트 환경의 DB 세션 설정이 프로덕션과 동일하지 않다
>   - 각 테스트마다 하나의 DB 트랜잭션만을 사용한다
>   - 대부분의 경우 프로덕션에서도 하나의 트랜잭션으로 모든 작업을 처리하겠지만, 그렇지 않은 경우 주의 필요

- unittest의 setUp, tearDown을 테스트 클래스 및 메서드 별로 적절히 설정하여 테스트 간 영향이 없도록 처리
- AsyncMock 사용 시 테스트 메서드 별로 제공
- AsyncClient는 (중간에 종료하지 않으면) 재사용 가능
- AsyncClient 사용 시 `dependency_overrides`로 적절히 의존성 교체


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
- 로깅, 모니터링