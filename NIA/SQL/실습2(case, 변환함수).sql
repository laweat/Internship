/* ========= 실습2 ========= */

--주수 구하기
select emp_name, to_char((current_timestamp - ent_date),'w') as WEEKS 
from tb_emp
where org_cd = '10';

--to_char 구문
select emp_name ,ent_date ,
		to_char(ent_date,'yyyy') 입사년,
		to_char(ent_date,'MM') 입사월,
		to_char(ent_date,'DD') 입사일 
from tb_emp;

--변환함수(명시적 데이터 유형 변환)
select to_date('05 Dec 2000', 'DD Mon YYYY');

select to_number('12,454.8-','99G999D9S');

select to_timestamp('05 Dec 2000', 'DD Mon YYYY');

--Case 변환함수
select CAST(123.4 AS VARCHAR(10))
	, CAST('123.5' AS NUMERIC)
	, CAST(1234.5678 AS DEC(6,2))
	, CAST(CURRENT_TIMESTAMP AS DATE)
	, TO_CHAR(CURRENT_TIMESTAMP, 'YYYY-MM-DD HH24:MI:SS')
	, TO_CHAR(1234.56, 'L9,999.99')
	, TO_NUMBER('$12,345', '$99,999')
	, TO_DATE('2014/03/01 21:30:18','YYYY/MM/DD HH24:MI:SS')
	, TO_TIMESTAMP('2014/03/01 21:30:18','YYYY/MM/DD HH24:MI:SS');

--case 표현 예제
select emp_name,
	case when salary > 50000000
	then salary 
	else 50000000
	end as revised_salary
from tb_emp;

select org_name,
	case org_name
		when '영업1팀' then '지사'
		when '영업2팀' then '지사'
		when '영업3팀' then '지사'
		when '경영관리팀' then '본사'
		else '지점'
	end as AREA
from tb_org;

select emp_name,
	case
		when salary >= 90000000 then 'HIGH'
		when salary >= 60000000 then 'MID'
		else 'LOW'
	end as Salary_grade
from tb_emp

--중첩 case문
select emp_name, salary,
	case 
		when salary  >= 50000000 then 20000000
		else(case
				when salary >= 20000000 then 10000000
				else salary * 0.5
			end)
	end as Bonus
from tb_emp;

--null 관련 함수

--coalesce 함수
select emp_name, position,coalesce(position,'없음')
from tb_emp;

--case 함수
select emp_name, position,
	case when position is null then '없음'
	else position
	end as 직책
from tb_emp;

--null, 공집합
select coalesce (salary, 0) SAL
from tb_emp 
where emp_name = '김태진';

select MAX (salary) SAL
from tb_emp 
where emp_name = '김태진';

select coalesce (MAX(salary), 9999) SAL
from tb_emp 
where emp_name = '김태진';
