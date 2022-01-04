import psycopg2
conn = psycopg2.connect(database='task', user='postgres', password='Sudh!r9899', host='localhost', port= '5432')
sudhir=conn.cursor()
conn.autocommit=True

trigger_func='''create or replace function reg_audit()
returns trigger
as
$$
begin
insert into emp_audit (id,time,reg) values (new.id,current_timestamp,'yes');
return new;
end;
$$
language plpgsql;'''
sudhir.execute(trigger_func)
trigger="create trigger emp_registration after insert on employee for each row execute procedure reg_audit();"
sudhir.execute(trigger)



trigger_func2='''create or replace function update_audit()
returns trigger
as
$$
begin
insert into emp_audit(id,time,update) values (new.id,current_timestamp,'yes');
return new;
end;
$$
language plpgsql;'''
sudhir.execute(trigger_func2)
trigger2="create trigger emp_update after update on employee for each row execute procedure update_audit();"

sudhir.execute(trigger2)

conn.close()