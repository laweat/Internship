/* ========= �ǽ�3 ========= */

--�������� �ǽ�
select count(*) "��ü�Ǽ�",
	count(position) "��å�Ǽ�",
	count(distinct position) "��å����",
	max(salary) "�ִ�",
	min(salary) "�ּ�",
	avg(salary) "���" 
from tb_emp;

--group by ��
select position "��å",
	count(*) "�ο���",
	min(salary) "�ּ�",
	max(salary) "�ִ�",
	avg(salary) "���" 
from tb_emp
group by position;

--Having ��
select org_cd "�μ�",
	count(*) "�ο���",
	avg(salary) "���" 
from tb_emp 
group by org_cd 
having count(*) >= 4; 

select org_cd "�μ�"
from tb_emp
group by org_cd 
having min(salary) <= 40000000;

select org_cd, position, avg(salary) 
from tb_emp
where position in ('����','�븮','���')
group by org_cd, position;

--��ȭ
select org_cd,
	avg(case position when '����' then salary end)"����" , 
	avg(case position when '�븮' then salary end)"�븮" ,
	avg(case position when '���' then salary end)"���"
from tb_emp
where position in ('����','�븮','���')
group by org_cd;

select org_cd,
	sum(coalesce((case position when '����' then 1 else 0 end),0)) "����" ,
	sum(coalesce((case position when '����' then 1 else 0 end),0)) "����" ,
	sum(coalesce((case position when '�븮' then 1 else 0 end),0)) "�븮" ,
	sum(coalesce((case position when '���' then 1 else 0 end),0)) "���"
from tb_emp
group by org_cd;

select org_cd,
	coalesce(sum(case position when '����' then 1 else 0 end),0) "����" ,
	coalesce(sum(case position when '����' then 1 else 0 end),0) "����" ,
	coalesce(sum(case position when '�븮' then 1 else 0 end),0) "�븮" ,
	coalesce(sum(case position when '���' then 1 else 0 end),0) "���"
from tb_emp
group by org_cd


