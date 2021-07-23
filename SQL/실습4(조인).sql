/* ========= 실습4 ========= */

--equi join 실습

--사원테이블, 조직테이블 조인
select tb_emp.emp_name, tb_emp.org_cd, tb_org.org_cd, tb_org.org_name
from tb_emp, tb_org
where tb_emp.org_cd = tb_org.org_cd;

--사원이름, 부서코드, 부서명, 직책 출력
select a.emp_no, a.emp_name, a.org_cd, b.org_name, a.position
from tb_emp a, tb_org b 
where a.org_cd = b.org_cd;

--Alias 사용
select a.emp_no ,a.emp_name ,a.org_cd ,b.org_name ,a.position
from tb_emp as a, tb_org as b 
where a.org_cd = b.org_cd and a.position = '팀장'
order by b.org_name;

--계좌번호, 고객명, 상품명, 계약금액, 관리자명 출력
select a.accno , c.cust_name ,p.prod_name ,a.cont_amt ,e.emp_name 
from tb_accnt a, tb_cust c, tb_prod p, tb_emp e 
where a.cust_no = c.cust_no 
	and a.prod_cd =p.prod_cd 
	and a.manager = e.emp_no;

--사원별 급여와 어느 등급에 속하는지 요구사항에 대한 non equi join
select e.emp_name  사원명, e.salary 연봉, s.grade 급여등급
from tb_emp e, tb_grade s 
where e.salary 
	between s.low_sal and s.high_sal;
	
--[예제] 사원번호와 사원이름 수속부서 코드와 소속부서 이름 찾기
--where 절 join 
select emp.emp_no ,emp.emp_name ,org.org_name 
from tb_emp emp, tb_org org
where emp.org_cd = org.org_cd 

--from 절 join 조건
select emp.emp_no ,emp.emp_name ,org.org_name 
from tb_emp emp inner join tb_org org on emp.org_cd = org.org_cd 

--Inner 키워드 생략
select emp.emp_no ,emp.emp_name ,org.org_name 
from tb_emp emp join tb_org org on emp.org_cd = org.org_cd;

--from 절에 join 조건

--[예제] 계좌테이블에서 계좌번호, 고객번ㄹ호, 고객명을 고객테이블과 조인하여 찾아본다.
select acc.accno ,acc.cust_no ,cust.cust_name 
from tb_accnt acc
	inner join tb_cust cust
	on cust.cust_no = acc.cust_no ;
	
--[예제] 조직코드 10인 부서의 소속 사원 이름 및 소속 부서 코드, 부서코드, 부서이름 찾기
select e.emp_name ,e.org_cd ,o.org_cd ,o.org_name 
from tb_emp e 
	join tb_org o
	on e.org_cd = o.org_cd 
where e.org_cd = '10'

--where절 조인조건
select a.accno 계좌번호, c.cust_name 고객명, p.prod_name 상품명,
		a.cont_amt 계약금액, e.emp_name 담당자명
from tb_accnt a, tb_cust c, tb_prod p, tb_emp e 
where a.cust_no =c.cust_no 
	and a.prod_cd = p.prod_cd 
	and a.manager = e.emp_no;

--on절 조인조건
select a.accno 계좌번호, c.cust_name 고객명, p.prod_name 상품명,
		a.cont_amt 계약금액, e.emp_name 담당자명
from tb_accnt a 
	inner join tb_cust c on a.cust_no = c.cust_no 
	inner join tb_prod p on a.prod_cd = p.prod_cd 
	inner join tb_emp e on a.manager = e.emp_no ;

--cross 조인
select count(emp_name)
from tb_emp;

select count(org_name)
from tb_org to2;

select e.emp_name ,o.org_name 
from tb_emp e 
	cross join tb_org o 
order by e.emp_name 

select count(e.emp_name)
from tb_emp e 
	cross join tb_org o;

--left outer join

--[예제] 직원중에 아직 부서배정이 안된 사원도 있다. 사원(TB_EMP)과 조직(TB_ORG)을 JOIN하되 부서배정이안된 사원의 정보도 같이 출력하도록 한다.

select e.emp_no 사번, e.emp_name 사원명, e.position 직책, o.org_name 부서명
from tb_emp e 
	left outer join tb_org o 
	on e.org_cd = o.org_cd 
where e.position = '사원'


--right outer join 
select e.emp_no 사번, e.emp_name 사원명, e.position 직책, o.org_name 부서명
from tb_org o 
	right outer join tb_emp e 
	on e.org_cd = o.org_cd 
where e.position = '사원'

--full outer join 
select a.org_cd ,a.org_name ,b.org_cd ,b.org_name 
from tb_org a
	full outer join tb_org b 
	on a.org_cd = b.org_cd 

select a.org_cd ,a.org_name ,b.org_cd, b.org_name
from tb_org a 
	left outer join tb_org b
	on a.org_cd = b.org_cd
union 
select a.org_cd ,a.org_name ,b.org_cd, b.org_name
from tb_org a 
	right outer join tb_org b
	on a.org_cd = b.org_cd