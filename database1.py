import sqlite3
import pickle
from pprint import pprint


def read_database(req_value):
    con = sqlite3.connect('Chinook_Sqlite.sqlite')
    cur = con.cursor()
    cur.execute(req_value)
    data = cur.fetchall()
    con.close()
    return data


req_1 = '''
select Customer.CustomerId, Customer.FirstName, Customer.Phone, Customer.Company
from Customer
join Invoice on Invoice.CustomerId = Customer.CustomerId
join InvoiceLine on Invoice.InvoiceId = InvoiceLine.InvoiceId
join Track on InvoiceLine.TrackId = Track.TrackId
join Genre on Track.GenreId = Genre.GenreId
join Employee on Customer.SupportRepId = Employee.EmployeeId
where 
strftime('%Y-%m-%d', Employee.BirthDate) <= strftime('%Y-%m-%d', '1969-05-19')
AND
Genre.Name != 'Rock'
group by Customer.FirstName having count(*) > 1
order by Customer.City asc, Customer.Email desc
limit 10
'''

req_2 = '''
select s.LastName || ' ' || s.FirstName as WorkerName, s.Phone, 
r.LastName || ' ' || r.FirstName as HeadName, r.Phone
from Employee as r
left join Employee as s on r.EmployeeId = s.ReportsTo
where s.ReportsTo is not null
'''

req_3 = '''
select Customer.FirstName, Customer.Phone
from Customer
join Invoice on Invoice.CustomerId = Customer.CustomerId
join InvoiceLine as I on Invoice.InvoiceId = I.InvoiceId
join (select UnitPrice, InvoiceLineId
from InvoiceLine
order by UnitPrice desc
limit 1) as MaxPrice 
on I.UnitPrice = MaxPrice.UnitPrice
group by Customer.FirstName having count(*) > 1
order by Customer.FirstName asc
'''

pprint(read_database(req_1))

pprint(read_database(req_3))

list_employees = {}
pickle_out = open("data.pickle", "wb")
for WorkerName, WorkerPhone, HeadName, HeadPhone in read_database(req_2):
    list_employees[WorkerName] = {"Phone": WorkerPhone, "Head": (HeadName, HeadPhone)}
pickle.dump(list_employees, pickle_out)
pickle_out.close()