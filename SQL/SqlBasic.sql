/* where�� ����1 */

select emp_name ����̸�, org_cd �Ҽ�, position ����, salary ����
from cslee.tb_emp
where position ='�븮';

/* where�� ����2 */

select count(*) 
from cslee.tb_emp;


/* where�� ����3  */

select emp_name ����̸�, org_cd �Ҽ�, position ��å, salary ����
from cslee.tb_emp
where (org_cd = '08' or org_cd = '09' or org_cd = '10')
and position = '���'
and salary >= 40000000
and salary <= 50000000;

/* where��  ����4 */

select emp_name ����̸�, org_cd �Ҽ�, position ��å, salary ����
from cslee.tb_emp
where org_cd in ('08','09','10')
and position = '���'
and salary between 40000000 and 50000000;


/* where�� ����5 */

select emp_name ,org_cd ,position
from cslee.tb_emp
where org_cd in ('06','07')
and position in ('����','����');


/* where�� ����6 */

select emp_name ����̸�, org_cd ���ڵ�, position ��å,ent_date �Ի�����
from cslee.tb_emp
where emp_name like '��%';


/* where�� ����7 */

select emp_name ����̸�, org_cd �Ҽ�, position ��å, gender ����
from cslee.tb_emp
where gender = null;

/* where�� ����8 */

select emp_name ����̸�, org_cd �Ҽ�, position ��å
from cslee.tb_emp
where org_cd = '10'
and not position = '����';

/* where�� ����9 */

select org_cd �μ�, emp_name ����̸�, ent_date �Ի���
from cslee.tb_emp
order by org_cd ,ent_date desc;


select emp_name, emp_no, org_cd 
from cslee.tb_emp
order by emp_name asc, emp_no asc , emp_no desc;


select emp_name ����̸�, emp_no �����ȣ, org_cd �μ��ڵ�
from cslee.tb_emp
order by ����̸�, �����ȣ, �μ��ڵ� desc;

select emp_name ,emp_no ,org_cd 
from cslee.tb_emp
order by 1 asc ,2 asc ,3 desc 


select emp_name ����̸�, emp_no �����ȣ, org_cd �μ��ڵ�
from cslee.tb_emp
order by emp_name ,2,�μ��ڵ� desc;

