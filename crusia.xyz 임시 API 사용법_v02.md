# crusia.xyz API 사용법
### 박윤식, 김영광
#### Version : v02
--

## User list
* URL : crusia.xyz/apis/user/
* Request : GET

> 정상 Response : 유저 리스트 JSON 반환

## User 정보 한개만 조회
* URL : crusia.xyz/apis/user/{PK}/
* Request : GET

> 정상 Response : 개별 유저정보 JSON 반환

## User signup
* URL : crusia.xyz/apis/user/
* Request : POST
* Body
	* email - 아이디 대신 이메일 주소 사용 (필수)
	* password1 - 비밀번호 (필수)
	* password2 - 확인용 비밀번호(password1과 동일한 값) (필수)
	* first_name - (선택), text
	* last_name - (선택), text
	* birthday - (선택), 날짜형식, 기본값: 1990-01-01
	* agreement - (선택), Boolean, 기본값: True

> 정상 Response : 가입을 시도한 email 반환

## User login
* URL : crusia.xyz/apis/user/login/
* Request : POST
* Body
	* email - 가입한 이메일 (필수)
	* password - 비밀번호 (필수)

> 정상 Response : User Token 반환

## User logout
* URL : crusia.xyz/apis/user/logout/
* Request : GET
* Headers
	* Authorization : Token 67b53cd02~~~~ (필수)

> 정상 Response : "Logout Completed" (해더의 토큰이 서버에서 삭제됨)


## User 정보 수정
* URL : crusia.xyz/apis/user/{PK}/  
* Request : PATCH
* Headers
	* Authorization : Token 67b53cd02~~~~ (필수)
* Body (아래 항목을 자유롭게 사용 가능)
	* img_profile - 프로필 이미지 (한장만 가능), 이미지 파일
	* gender - 성별, OTHER(기본값, 기타성별)/MALE(남자)/FEMALE(여자) 중 택1, 영어로 입력해야하고 대소문자 구분해서 입력해야 함, 위 3가지 단어중 한가지만 입력
	* birthday - 생일, 날짜형식만 입력 가능(기본값:1990-01-01)
	* phone_num - 연락처, text 20자 제한
	* preference_language - 선호 언어, text 20자 제한
	* preference_currency - 선호 통화, text 20자 제한
	* living_site - 거주지, text 100자 제한
	* introduce - 자기소개, text 300자 제한

> 정상 Response : 수정 시도한 User의 JSON 반환


## User 회원탈퇴(User 삭제)
* URL : crusia.xyz/apis/user/{PK}/  
* Request : DELETE
* Headers
	* Authorization : Token 67b53cd02~~~~ (필수)

> 정상 Response : 아무것도 오지 않음, status 확인 > status 204 No Content 보이면 정상

<br>

---

<br>

## House list
* URL : crusia.xyz/apis/house/
* Request : GET

> 정상 Response : House list JSON 반환

## House 한개만 접근하는 방법
* URL : crusia.xyz/apis/house/{PK}/  
* Request : GET

ex) http://crusia.xyz/apis/house/1/ 에 GET요청을 보내면 pk=1인 하우스의 JSON이 반환됨

> 정상 Response : House JSON 반환

## House create
* URL : crusia.xyz/apis/house/
* Request : POST
* Headers
	* Authorization : Token 67b53cd02~~~~ (필수)
* Body
	* title - 숙소 제목, text 300자 제한 (필수)
	* address - 주소, text 200자 제한
	* introduce - 숙소 소개, text 1000자 제한
	* space\_info - 숙소 부연 설명, text 1000자 제한
	* guest\_access - 숙소 내 비품 설명, text 1000자 제한
	* price\_per\_day - 1박 비용, 양의 정수형 숫자 (필수)
	* extra\_people\_fee - 추가인원에 대한 비용, 양의 정수형 숫자(필수) 
	* cleaning\_fee - 청소비, 양의 정수형 숫자 (필수)
	* weekly\_discount - 일주일이상 장기 투숙시 할인률, 양의 정수형 숫자 (필수)
	* accommodates - 기본 숙박가능 인원수, 양의 정수형 숫자 (필수)
	* bathrooms - 화장실 개수, 양의 정수형 숫자 (필수)
	* bedrooms - 침실 개수, 양의 정수형 숫자 (필수)
	* beds - 챔대 개수, 양의 정수형 숫자 (필수)
	* room_type - 숙소의 형태, House(집 전체 임대)/Individual(개인실)/Shared\_Room(다인실) 중 택1, 영어로 입력해야하고 대소문자 구분해서 입력해야 함, 위 3가지 단어중 한가지만 입력 (필수)
	* house_images - 숙소 이미지, 이미지 파일은 갯수 제한없고 Key의 이름도 사실상 제한 없음. 본 요청에서 들어오는 모든 이미지 파일을 자동으로 파싱해서 업로드 해줌.
	* amenities - 숙소 내 편의시설 및 이용안내 사항, text 입력이나 들어갈 수 있는 단어가 제한 됨. 단어는 쉼표(,)로 구분되고, 공백은 아무리 넣어도 상관없음.(공백은 구분자로서 기능을 안함) 잘못된 단어를 넣을 경우 오류를 반환함. 허용되는 단어는 아래와 같음. 대소문자를 구분하므로 정확히 입력해야 함. ex) TV, Internet, Breakfast
		* Pets_allowed
		* Elevator
		* Gym
		* Indoor_fireplace
		* Internet
		* Doorman
		* Kitchen
		* Pool
		* Smoking_allowed
		* Wheelchair_accessible
		* Wireless_Internet
		* Free_parking
		* Breakfast
		* Dryer
		* Cable_TV
		* Hangers
		* Washer
		* Shampoo
		* Essentials
		* Heating
		* TV
		* Air_conditioning
	* latitude - 위도, 실수형 숫자 (필수)
	* longitude - 경도, 실수형 숫자 (필수) 

> 정상 Response : 새로 만들어진 House의 JSON 반환

## House 정보 수정
* URL : crusia.xyz/apis/house/{PK}/
* Request : PATCH
* Headers
	* Authorization : Token 67b53cd02~~~~ (필수)
* Body(위의 모든 정보 수정 가능).  
**단, 이미지는 추가만 되고 현재 삭제는 안됨**

> 정상 Response : 수정 시도한 House의 JSON 반환


## House 삭제
* URL : crusia.xyz/apis/house/{PK}/
* Request : DELETE
* Headers
	* Authorization : Token 67b53cd02~~~~ (필수)

> 정상 Response : 아무것도 오지 않음, status 확인 > status 204 No Content 보이면 정상


