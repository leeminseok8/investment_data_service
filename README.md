# Investment Service
유저의 투자 계좌 데이터 조회 및 검증을 통한 입금 서비스의 백엔드 API를 개발하여 제공합니다.

---
## 목차
1. [사용법](#사용법)
2. [사용 기술 스택](#사용-기술-스택)
3. [MVP Service](#MVP-Service)
4. [ERD](#ERD)
5. [API 명세서](#API-명세서)
6. [기능 명세서 및 분석](#기능-명세서-및-분석)

<br>

---

## 사용법
- [가상 환경 설치](#가상-환경-설치)부터는 프로젝트 최상위 디렉토리(investment_service)에서 명령어를 입력하셔야 합니다.

### 프로젝트 로컬 설치
```
> git clone https://github.com/leeminseok8/investment_data_service.git

> cd --project_name
```

### 가상 환경 설치
> pipenv를 사용하였습니다.
```
프로젝트 최상위 디렉토리(Pipfile)에서 실행)
> pwd
~/.../investment_service


pipenv가 없으시다면)
> pip install pipenv

> pipenv shell


pipenv가 있으시다면)
> pipenv shell
```

### DB 생성
```
프로젝트 최상위 디렉토리(manage.py)에서 실행)
> pwd
~/.../investment_service

> python manage.py makemigrations

> python manage.py migrate
```

### Batch 파일로 데이터 삽입
```
프로젝트 최상위 디렉토리에서 실행)
> pwd
~/.../investment_service

> python uploader.py
```

### 로컬(개발용) 서버 실행
```
> python manage.py runserver
```

### Schedule 설정
> Batch 파일을 특정 시간마다 실행시키기 위한 스케쥴러 설정입니다. <br>
매일 00시 00분 기준으로 데이터를 업데이트 합니다.
```
> crontab -e
vim 에디터 화면으로 전환 (i 누르면 insert 모드)

[시간 설정] [파이썬이 설치된 절대경로] [실행할 파이썬의 절대경로] 입력
> 0 0 * * * [파이썬 절대경로] [실행 파일 절대경로]

주의)
숫자와 '*" 사이는 모두 뛰어쓰기 1칸 입니다.

실행 중인 스케줄링을 확인할 수 있습니다.
> crontab -l

```

<br>

---

## 사용 기술 스택
- back-end : Python, Django, DjangoRestFramework

- DataBase : MySQL

- formater : black

<br>

---

## MVP Service
> 회원가입 없이 로그인 후 데이터 호출할 수 있도록 구현하였습니다.<br>
유저 이름(ID) : 류영길<br>
비밀번호 : 0 [ 비밀번호는 임의 0으로 통일 ]
### 계정
- 로그인
    - 유저 이름(ID)와 비밀번호를 입력하여 로그인할 수 있습니다.
### 계좌
> 조회 권한 : 로그인 된 본인의 계좌만 확인할 수 있습니다.
- 투자 화면 조회
    - 투자 화면을 조회할 수 있습니다.
        - 계좌명, 증권사, 계좌번호, 계좌 총 자산
- 투자 상세 화면 조회
    - 투자 상세 화면을 조회할 수 있합니다.
        - 계좌명, 증권사, 계좌번호, 계좌 총 자산, 투자 원금, 총 수익금, 수익률
- 보유 종목 화면 조회
    - 현재 유저가 보유한 종목을 조회할 수 있습니다.
        - 보유 종목명, 보유 종목 자산군, 보유 종목 평가 금액, ISIN
### 입금
> 2단계로 나누어 입금을 진행합니다.
- 입금 계좌 검증
    - 기존 계좌와 요청 계좌의 진위여부를 검증합니다.
- 입금 계좌 업데이트
    - 검증이 완료되면 계좌를 업데이트합니다.

<br>

---

## ERD
<img width="1085" alt="스크린샷 2022-09-28 오후 5 37 49" src="https://user-images.githubusercontent.com/93478318/192731558-03bb7332-518b-44b1-ae62-085325566026.png">

<br>

---

## API 명세서
| Domain | endpoint | Method | 기능 | 권한 |
| --- | --- | --- | --- | --- |
| **Users** | accounts/signin/ | POST | 로그인 | - |
| - |  |  |  |  |
| **Products** |accounts/ | GET | 투자 화면 조회 | 로그인 |
|  | accounts/detail | GET | 투자 상세 화면 조회 | 로그인 |
|  | accounts/own | GET | 보유 종목 화면 조회 | 로그인 |
| - |  |  |  |  |
| **Orders** | accounts/deposit/p1/ | POST | 입금 계좌 검증 | 로그인 |
|  | accounts/deposit/p2/ | POST | 계좌 자산 업데이트 | 로그인 |

<br>

---

## 기능 명세서 및 분석

### 로그인
<img width="960" alt="스크린샷 2022-09-28 오후 6 34 17" src="https://user-images.githubusercontent.com/93478318/192744859-ea81d353-72f4-43f8-bca5-1433db86de98.png">

- simple-jwt를 사용하여 로그인을 구현하였습니다.
- 주식 계좌 조회/입금 서비스를 제공하므로 회원가입은 구현하지 않았습니다.

### 투자 화면 조회
<img width="957" alt="스크린샷 2022-09-28 오후 6 36 11" src="https://user-images.githubusercontent.com/93478318/192745160-8a6eb188-ced0-472b-a2b3-81931fc9b9c7.png">

- 총 자산(total_asset)은 테이블 컬럼이 아닌 함수로 구현하여 return에 담아 응답하였습니다.

- 총 자산을 구현할 때 보유 종목(Stock 테이블)의 현금 컬럼을 어떻게 정의해야 하는지 고민했습니다. 현재는 보유 종목 테이블에 정의했지만, 이후 계좌(Account) 테이블 컬럼으로 마이그레이션할 예정입니다.
(**입금 시 현금으로 추가하여 자산을 계산해야 하기 때문**)

- 하루의 특정 시간( 예를 들어, 24시 ~ 24시 30분 )을 선정하여 한 번에 처리할 수 있도록 캐싱(redis)하는 방법으로 추가 구현을 예상하고 있습니다.

### 투자 상세 화면 조회
<img width="963" alt="스크린샷 2022-09-28 오후 6 35 39" src="https://user-images.githubusercontent.com/93478318/192745057-ee297af0-999e-4d92-b694-4a0367635ae7.png">

- 총 자산(total_asset)과 같이 총 수익(Total_proceed), 수익률(yeild)은 함수로 구현하였습니다.

### 보유 종목 화면 조회
<img width="965" alt="스크린샷 2022-09-28 오후 6 37 20" src="https://user-images.githubusercontent.com/93478318/192745399-13b0c17d-6e72-44e9-9839-34466254f1da.png">

- 로그인 유저 인증 후 참조하는(fk) 계좌의 보유 종목을 호출합니다.

### 입금 계좌 검증
<img width="964" alt="스크린샷 2022-09-28 오후 6 38 23" src="https://user-images.githubusercontent.com/93478318/192745653-7a751223-5a46-4716-8c70-f7ebb04b727a.png">

- 유저, 계좌 검증을 구현하였습니다.

- 기존 요청 예시값으로는 [유저 이름, 계좌 번호, 입금 금액]을 JSON으로 받았습니다. 하지만 이 경우, http method를 POST로 받아야 하여 테이블 컬럼이 중복되는 상황, 즉 정규화가 필요합니다. 이 부분에서 **역정규화하여 진행할 지 정규화하여 진행할 지 고민끝에 개명할 경우를 대비하여 정규화하여 진행하였습니다.**

### 계좌 자산 업데이트
<img width="961" alt="스크린샷 2022-09-28 오후 6 39 37" src="https://user-images.githubusercontent.com/93478318/192745904-ee349ae0-774e-437e-b9fc-ce3a5855c740.png">

- 검증 완료 후 검증된 데이터로 hashing하고 클라이언트에서 요청하면 DB의 데이터와 대조하여 실제 계좌를 업데이트합니다.

- [투자 화면 조회](#투자-화면-조회)의 총 자산을 구현할 때 고민한 것처럼 Stock 테이블의 현금 컬럼을 업데이트하는 방향으로 구현할 예정입니다. 총 자산뿐만 아닌 현금 자산과 함께 업데이트하도록 분석하였습니다.
