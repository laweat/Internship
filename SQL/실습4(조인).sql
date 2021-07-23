/* ========= �ǽ�4 ========= */

--equi join �ǽ�

--������̺�, �������̺� ����
select tb_emp.emp_name, tb_emp.org_cd, tb_org.org_cd, tb_org.org_name
from tb_emp, tb_org
where tb_emp.org_cd = tb_org.org_cd;

--����̸�, �μ��ڵ�, �μ���, ��å ���
select a.emp_no, a.emp_name, a.org_cd, b.org_name, a.position
from tb_emp a, tb_org b 
where a.org_cd = b.org_cd;

--Alias ���
select a.emp_no ,a.emp_name ,a.org_cd ,b.org_name ,a.position
from tb_emp as a, tb_org as b 
where a.org_cd = b.org_cd and a.position = '����'
order by b.org_name;

--���¹�ȣ, ����, ��ǰ��, ���ݾ�, �����ڸ� ���
select a.accno , c.cust_name ,p.prod_name ,a.cont_amt ,e.emp_name 
from tb_accnt a, tb_cust c, tb_prod p, tb_emp e 
where a.cust_no = c.cust_no 
	and a.prod_cd =p.prod_cd 
	and a.manager = e.emp_no;

--����� �޿��� ��� ��޿� ���ϴ��� �䱸���׿� ���� non equi join
select e.emp_name  �����, e.salary ����, s.grade �޿����
from tb_emp e, tb_grade s 
where e.salary 
	between s.low_sal and s.high_sal;
	
--[����] �����ȣ�� ����̸� ���Ӻμ� �ڵ�� �ҼӺμ� �̸� ã��
--where �� join 
select emp.emp_no ,emp.emp_name ,org.org_name 
from tb_emp emp, tb_org org
where emp.org_cd = org.org_cd 

--from �� join ����
select emp.emp_no ,emp.emp_name ,org.org_name 
from tb_emp emp inner join tb_org org on emp.org_cd = org.org_cd 

--Inner Ű���� ����
select emp.emp_no ,emp.emp_name ,org.org_name 
from tb_emp emp join tb_org org on emp.org_cd = org.org_cd;

--from ���� join ����

--[����] �������̺��� ���¹�ȣ, ������ȣ, ������ �����̺�� �����Ͽ� ã�ƺ���.
select acc.accno ,acc.cust_no ,cust.cust_name 
from tb_accnt acc
	inner join tb_cust cust
	on cust.cust_no = acc.cust_no ;
	
--[����] �����ڵ� 10�� �μ��� �Ҽ� ��� �̸� �� �Ҽ� �μ� �ڵ�, �μ��ڵ�, �μ��̸� ã��
select e.emp_name ,e.org_cd ,o.org_cd ,o.org_name 
from tb_emp e 
	join tb_org o
	on e.org_cd = o.org_cd 
where e.org_cd = '10'

--where�� ��������
select a.accno ���¹�ȣ, c.cust_name ����, p.prod_name ��ǰ��,
		a.cont_amt ���ݾ�, e.emp_name ����ڸ�
from tb_accnt a, tb_cust c, tb_prod p, tb_emp e 
where a.cust_no =c.cust_no 
	and a.prod_cd = p.prod_cd 
	and a.manager = e.emp_no;

--on�� ��������
select a.accno ���¹�ȣ, c.cust_name ����, p.prod_name ��ǰ��,
		a.cont_amt ���ݾ�, e.emp_name ����ڸ�
from tb_accnt a 
	inner join tb_cust c on a.cust_no = c.cust_no 
	inner join tb_prod p on a.prod_cd = p.prod_cd 
	inner join tb_emp e on a.manager = e.emp_no ;

--cross ����
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

--[����] �����߿� ���� �μ������� �ȵ� ����� �ִ�. ���(TB_EMP)�� ����(TB_ORG)�� JOIN�ϵ� �μ������̾ȵ� ����� ������ ���� ����ϵ��� �Ѵ�.

select e.emp_no ���, e.emp_name �����, e.position ��å, o.org_name �μ���
from tb_emp e 
	left outer join tb_org o 
	on e.org_cd = o.org_cd 
where e.position = '���'


--right outer join 
select e.emp_no ���, e.emp_name �����, e.position ��å, o.org_name �μ���
from tb_org o 
	right outer join tb_emp e 
	on e.org_cd = o.org_cd 
where e.position = '���'

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