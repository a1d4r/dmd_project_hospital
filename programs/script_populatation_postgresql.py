from faker import Faker
import psycopg2
import random

con = psycopg2.connect(
    dbname="hospital",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

cur = con.cursor()
fake = Faker()

file_output = open("populate_postgres.sql", "w+")
file_writing = True
number_of_rooms = 20


# cur.execute("DELETE FROM appointment;")
# cur.execute("DELETE FROM person;")

def write_into_file(string_query):
    if file_writing:
        file_output.write(string_query + "\n")


# insert male into table person and return query and id of last added person
def create_person_male():
    ssn, address, name, surname, date_of_birth, sex = \
        fake.itin(), fake.address(), fake.first_name_male(), \
        fake.last_name_male(), fake.date_of_birth(tzinfo=None, minimum_age=15, maximum_age=115), 'm'

    address = address.replace("\n", ", ")
    query_person = "INSERT INTO person (ssn, address, name, surname, date_of_birth, sex) " \
                   "VALUES ('%s', '%s', '%s', '%s', '%s', '%s') RETURNING person_id;" \
                   % (ssn, address, name, surname, date_of_birth, sex)
    cur.execute(query_person)
    write_into_file(query_person.split("RETURNING")[0] + ";")
    person_id = cur.fetchone()[0]
    return [query_person, person_id]


# insert female into table person and return query and id of last added person
def create_person_female():
    ssn, address, name, surname, date_of_birth, sex = \
        fake.itin(), fake.address(), fake.first_name_female(), \
        fake.last_name_female(), fake.date_of_birth(tzinfo=None, minimum_age=15, maximum_age=115), 'm'

    address = address.replace("\n", ", ")
    query_person = "INSERT INTO person (ssn, address, name, surname, date_of_birth, sex) " \
                   "VALUES ('%s', '%s', '%s', '%s', '%s', '%s') RETURNING person_id;" \
                    % (ssn, address, name, surname, date_of_birth, sex)
    cur.execute(query_person)
    write_into_file(query_person.split("RETURNING")[0] + ";")
    person_id = cur.fetchone()[0]
    return [query_person, person_id]


# inserting patients
def inserting_patients():
    # cur.execute("DELETE FROM patient;")
    for i in range(25):
        query_id = create_person_male()
        query_person = query_id[0]
        person_id = query_id[1]
        query_patient = "INSERT INTO patient (person_id) VALUES (%s);" % person_id
        cur.execute(query_patient)
        write_into_file(query_patient)

    for i in range(25):
        query_id = create_person_female()
        query_person = query_id[0]
        person_id = query_id[1]
        query_patient = "INSERT INTO patient (person_id) VALUES (%s);" % person_id
        cur.execute(query_patient)
        write_into_file(query_patient)


# inserting doctors
def inserting_doctors():
    # cur.execute("DELETE FROM doctor;")
    for i in range(12):
        query_id = create_person_male()
        query_person = query_id[0]
        person_id = query_id[1]

        length_of_service = fake.random_int(min=3, max=20, step=1)
        salary = fake.random_int(min=40000, max=80000, step=2000)

        query_doctor = "INSERT INTO doctor (person_id, length_of_service, salary) VALUES (%s, %s, %s);"\
                       % (person_id, length_of_service, salary)
        cur.execute(query_doctor)
        write_into_file(query_doctor)

    for i in range(5):
        query_id = create_person_female()
        query_person = query_id[0]
        person_id = query_id[1]
        length_of_service = fake.random_int(min=3, max=20, step=1)
        salary = fake.random_int(min=40000, max=80000, step=2000)

        query_doctor = "INSERT INTO doctor (person_id, length_of_service, salary) VALUES ('%s', '%s', '%s');"\
                       % (person_id, length_of_service, salary)
        cur.execute(query_doctor)
        write_into_file(query_doctor)


# inserting nurses
def inserting_nurses():
    # cur.execute("DELETE FROM nurse;")
    for i in range(10):
        query_id = create_person_female()
        query_person = query_id[0]
        person_id = query_id[1]

        length_of_service = fake.random_int(min=3, max=20, step=1)
        salary = fake.random_int(min=20000, max=30000, step=2000)

        query_nurse = "INSERT INTO nurse (person_id, length_of_service, salary) VALUES (%s, %s, %s);"\
                      % (person_id, length_of_service, salary)
        cur.execute(query_nurse)
        write_into_file(query_nurse)


# inserting accountants
def inserting_accountants():
    # cur.execute("DELETE FROM accountant;")
    for i in range(4):
        query_id = create_person_female()
        query_person = query_id[0]
        person_id = query_id[1]

        length_of_service = fake.random_int(min=3, max=20, step=1)
        salary = fake.random_int(min=20000, max=40000, step=2000)

        query_accountant = "INSERT INTO accountant (person_id, length_of_service, salary) VALUES (%s, %s, %s);" \
                           % (person_id, length_of_service, salary)
        cur.execute(query_accountant)
        write_into_file(query_accountant)


# inserting receptionists
def inserting_receptionists():
    # cur.execute("DELETE FROM receptionist;")
    for i in range(4):
        query_id = create_person_female()
        query_person = query_id[0]
        person_id = query_id[1]

        length_of_service = fake.random_int(min=3, max=20, step=1)
        salary = fake.random_int(min=20000, max=40000, step=2000)

        query_recept = "INSERT INTO receptionist (person_id, length_of_service, salary) VALUES (%s, %s, %s);"\
                       % (person_id, length_of_service, salary)
        cur.execute(query_recept)
        write_into_file(query_recept)


# inserting storekeepers
def inserting_storekeepers():
    # cur.execute("DELETE FROM storekeeper;")
    for i in range(2):
        query_id = create_person_female()
        query_person = query_id[0]
        person_id = query_id[1]

        length_of_service = fake.random_int(min=3, max=20, step=1)
        salary = fake.random_int(min=20000, max=40000, step=2000)
        query_storekeeper = "INSERT INTO storekeeper (person_id, length_of_service, salary) VALUES (%s, %s, %s);"\
                            % (person_id, length_of_service, salary)
        cur.execute(query_storekeeper)
        write_into_file(query_storekeeper)


# inserting appointments
def inserting_appointments():
    cur.execute("SELECT person_id FROM doctor;")
    doctors_id = cur.fetchall()
    cur.execute("SELECT person_id FROM patient;")
    patients_id = cur.fetchall()
    cur.execute("SELECT person_id FROM nurse;")
    nurses_id = cur.fetchall()
    cur.execute("SELECT person_id FROM receptionist;")
    recs_id = cur.fetchall()

    query = "INSERT INTO appointment(app_time, room, patient_id, doctor_id, nurse_id, rec_id) VALUES "

    for doctor in doctors_id:
        for i in range(101):
            room = fake.random_int(min=1, max=number_of_rooms, step=1)
            app_time = fake.date_time_between(start_date="-10y", end_date="now", tzinfo=None)

            # cur.execute("SELECT person_id FROM patient ORDER BY random() LIMIT 1;")
            # patient_id = int(cur.fetchone()[0])
            patient_id = random.choice(patients_id)[0]
            nurse_id = random.choice(nurses_id)[0]
            rec_id = random.choice(recs_id)[0]
            doctor_id = doctor[0]

            addition = "('%s', %s, %s, %s, %s, %s),\n" % (app_time, room, patient_id, doctor_id, nurse_id, rec_id)
            query += addition

    query = query[0:(len(query)-2)]+";"
    cur.execute(query)
    write_into_file(query)

# inserting medicines
def inserting_medicines():
    medicines = ["Dexmedocet", "Prepapiride", "Aggrerotec", "Eprotide",
                 "Aprevance", "Galanpalene", "Oxyconide Butamectin",
                 "Cleoterol Magnesulin", "Romirabine Marvate", "Kiorate Bexlise"]
    query = "INSERT INTO medicine(price, name, description) VALUES "
    for i in range(len(medicines)):
        medicine = random.choice(medicines)
        medicines.remove(medicine)
        price = fake.random_int(min=100, max=500, step=10)
        descr = fake.sentence()
        add = "(%s, '%s', '%s'),\n" % (price, medicine, descr)
        query += add

    query = query[0:(len(query) - 2)] + ";"
    cur.execute(query)
    write_into_file(query)


# inserting services
def inserting_services():
    services = ["massage", "healing shower", "healing with dirt", "River mud", "Magnetoturbotron", "Prostate massage"]
    query = "INSERT INTO service(name, description, price) VALUES "
    for i in range(len(services)):
        service = random.choice(services)
        services.remove(service)
        price = fake.random_int(min=1000, max=3000, step=500)
        descr = fake.sentence()
        add = "('%s', '%s', %s),\n" % (service, descr, price)
        query += add
    query = query[0:(len(query) - 2)] + ";"
    cur.execute(query)
    write_into_file(query)


def inserting_medical_charts():
    cur.execute("select person_id from patient;")
    persons = cur.fetchall()
    query = "INSERT INTO medical_chart(start_date, chart_id) VALUES "
    for person in persons:
        query_date_of_birth = "select date_of_birth from person where person_id=%s;"
        cur.execute(query_date_of_birth % person[0])
        date_of_birth = cur.fetchone()[0]
        date_chart_create = fake.date_time_between(start_date=date_of_birth, end_date="-10y", tzinfo=None)
        add = "('%s', %s),\n" % (date_chart_create, person[0])
        query += add
    query = query[0:(len(query) - 2)] + ";"
    cur.execute(query)
    write_into_file(query)


def inserting_reports():
    cur.execute("select chart_id, start_date from medical_chart;")
    charts = cur.fetchall()

    cur.execute("SELECT person_id FROM doctor;")
    doctors_id = cur.fetchall()

    cur.execute("SELECT person_id FROM nurse;")
    nurses_id = cur.fetchall()

    query = "INSERT INTO report(create_time, results_of_consultation, chart_id, doctor_id, nurse_id) VALUES "

    for chart in charts:
        for i in range(10):
            chart_id, chart_start_date = chart[0], chart[1]

            cr_time = fake.date_time_between(start_date=chart_start_date, end_date="now", tzinfo=None)

            res_cons = fake.paragraph(nb_sentences=fake.random_int(min=1, max=3, step=1), variable_nb_sentences=True,
                                      ext_word_list=None)

            doctor_id = random.choice(doctors_id)[0]

            nurse_id = random.choice(nurses_id)[0]

            add = "('%s', '%s', %s, %s, %s),\n" % (cr_time, res_cons, chart_id, doctor_id, nurse_id)
            query += add
    query = query[0:(len(query) - 2)] + ";"
    write_into_file(query)
    cur.execute(query)


def inserting_nurse_qual():
    cur.execute("select person_id from nurse;")
    nurses = cur.fetchall()
    quals = ['qual1', 'qual2', 'qual3']
    query = "INSERT INTO nurse_qualifications(descrip, person_id) VALUES "
    for nurse in nurses:
        fake_quals = quals.copy()
        # print(nurse[0], fake_quals)
        for i in range(1, fake.random_int(min=1, max=3, step=1)):
            qual = fake.word(ext_word_list=fake_quals)
            fake_quals.remove(qual)
            add = "('%s', %s),\n" % (qual, nurse[0])
            query += add

    query = query[0:(len(query) - 2)] + ";"
    write_into_file(query)
    cur.execute(query)


def inserting_doctor_qual():
    cur.execute("select person_id from doctor;")
    docs = cur.fetchall()
    quals = ['qual1', 'qual2', 'qual3']
    query = "INSERT INTO doctor_qualifications(descrip, person_id) VALUES "

    for doc in docs:
        fake_quals = quals.copy()
        # print(nurse[0], fake_quals)
        for i in range(1, fake.random_int(min=1, max=3, step=1)):
            qual = fake.word(ext_word_list=fake_quals)
            fake_quals.remove(qual)
            add = "('%s', %s),\n" % (qual, doc[0])
            query += add
    query = query[0:(len(query) - 2)] + ";"
    cur.execute(query)
    write_into_file(query)


def inserting_nurse_assigned():
    cur.execute("select person_id from doctor;")
    doctors = cur.fetchall()
    for doc in doctors:
        doc_id = doc[0]
        cur.execute("select person_id from nurse order by random() limit 1;")
        nurse_id = cur.fetchone()[0]
        query = "INSERT INTO nurse_assigned(doc_id, nurse_id) values ('%s', '%s');" % (doc_id, nurse_id)
        cur.execute(query)
        write_into_file(query)


def inserting_req_med():
    cur.execute("SELECT person_id FROM doctor;")
    doctors_id = cur.fetchall()

    cur.execute("SELECT person_id FROM nurse;")
    nurses_id = cur.fetchall()

    cur.execute("SELECT medicine_id FROM medicine;")
    meds = cur.fetchall()

    for i in range(50):
        doctor_id = random.choice(doctors_id)[0]
        nurse_id = random.choice(nurses_id)[0]
        med_id = random.choice(meds)[0]

        query = "INSERT INTO request_medicine(doctor_id, nurse_id, medicine_id) VALUES (%s, %s, %s);"\
                % (doctor_id, nurse_id, med_id)
        cur.execute(query)
        write_into_file(query)


def inserting_provide_serv():
    cur.execute("SELECT person_id FROM doctor;")
    doctors_id = cur.fetchall()

    cur.execute("SELECT person_id FROM nurse;")
    nurses_id = cur.fetchall()

    cur.execute("SELECT service_id FROM service;")
    sers = cur.fetchall()

    for i in range(50):
        doctor_id = random.choice(doctors_id)[0]
        nurse_id = random.choice(nurses_id)[0]
        ser_id = random.choice(sers)[0]

        query = "INSERT INTO provide_service(doctor_id, nurse_id, ser_id) VALUES (%s, %s, %s);" % (doctor_id, nurse_id, ser_id)
        cur.execute(query)
        write_into_file(query)


def inserting_order():
    cur.execute("SELECT person_id FROM doctor;")
    doctors = cur.fetchall()
    for i in range(50):
        doctor_id = random.choice(doctors)[0]
        query_order = "INSERT INTO \"order\"(doc_id) VALUES (%s);" % doctor_id
        cur.execute(query_order)
        write_into_file(query_order)


def inserting_order_ser():
    cur.execute("select order_id from \"order\";")
    orders = cur.fetchall()

    cur.execute('select service_id from service;')
    sers = cur.fetchall()
    for order in orders:
        order_id = order[0]
        service_id = random.choice(sers)[0]
        query_order_serv = "INSERT INTO order_service(order_id, service) VALUES (%s, %s);" % (order_id, service_id)
        cur.execute(query_order_serv)
        write_into_file(query_order_serv)


def inserting_order_med():
    cur.execute("select order_id from \"order\";")
    orders = cur.fetchall()

    cur.execute('select medicine_id from medicine;')
    meds = cur.fetchall()

    for order in orders:
        order_id = order[0]
        med_id = random.choice(meds)[0]
        query_order_serv = "INSERT INTO order_medicine(order_id, medicine) VALUES (%s, %s);" % (order_id, med_id)
        cur.execute(query_order_serv)
        write_into_file(query_order_serv)


def inserting_invoices():
    cur.execute("select person_id from patient;")
    patients_id = cur.fetchall()
    cur.execute("select order_id from \"order\";")
    orders_id = cur.fetchall()
    for order in orders_id:
        for i in range(1, fake.random_int(min=1, max=1, step=1)):
            patient_id = random.choice(patients_id)[0]
            invoice_date = fake.date_between(start_date="-10y", end_date="today")
            payment_due = fake.date_between(start_date=invoice_date, end_date="today")
            tax_amount = fake.random_int(min=1, max=30, step=1)
            order_id = order[0]
            cur.execute("select order_medicine.medicine "
                        "from \"order\", order_medicine where order_medicine.order_id = %s;" % order_id)
            medicine_id = cur.fetchone()[0]
            cur.execute("select price from medicine where medicine_id = %s" % medicine_id)
            price_med = cur.fetchone()[0]

            cur.execute("select order_service.service "
                        "from \"order\", order_service where order_service.order_id = %s;" % order_id)
            service_id = cur.fetchone()[0]
            cur.execute("select price from service where service.service_id = %s" % service_id)
            price_ser = cur.fetchone()[0]
            total = price_med + price_ser
            query = "INSERT INTO invoice(patient_id, invoice_date, payment_due_date, tax_amount, total_amount, inv_id)"\
                    "VALUES (%s, '%s', '%s', %s, %s, %s);" \
                    % (patient_id, invoice_date, payment_due, tax_amount, total, order_id)
            cur.execute(query)
            write_into_file(query)


def inserting_manage_invoices():
    print("Start manage_invoice")
    cur.execute("select person_id from accountant;")
    accountants = cur.fetchall()

    cur.execute("select inv_id from invoice;")
    invoices = cur.fetchall()

    for invoice in invoices:
        invoice_id = invoice[0]
        accountant_id = random.choice(accountants)[0]
        query = "INSERT INTO manage_invoice(acc_id, inv_id) values (%s, %s);" % (accountant_id, invoice_id)
        cur.execute(query)
        write_into_file(query)


def inserting_complete_order():
    cur.execute("select order_id from \"order\";")
    orders = cur.fetchall()

    cur.execute("select person_id from storekeeper;")
    stks = cur.fetchall()

    for order in orders:
        order_id = order[0]
        stk_id = random.choice(stks)[0]
        query = "INSERT INTO complete_order(order_id, stk_id) values (%s, %s);" % (order_id, stk_id)
        cur.execute(query)
        write_into_file(query)


def inserting_appointments_from_date(start, count_app):
    cur.execute("SELECT person_id FROM doctor;")
    doctors_id = cur.fetchall()
    cur.execute("SELECT person_id FROM patient;")
    patients_id = cur.fetchall()
    cur.execute("SELECT person_id FROM nurse;")
    nurses_id = cur.fetchall()
    cur.execute("SELECT person_id FROM receptionist;")
    recs_id = cur.fetchall()

    query = "INSERT INTO appointment(app_time, room, patient_id, doctor_id, nurse_id, rec_id) VALUES "

    for doctor in doctors_id:
        for i in range(count_app):
            room = fake.random_int(min=1, max=number_of_rooms, step=1)
            app_time = fake.date_time_between(start_date=start, end_date="now", tzinfo=None)

            patient_id = random.choice(patients_id)[0]
            nurse_id = random.choice(nurses_id)[0]
            rec_id = random.choice(recs_id)[0]
            # doctor_id = random.choice(doctors_id)[0]
            doctor_id = doctor[0]

            add = "('%s', %s, %s, %s, %s, %s),\n" % (app_time, room, patient_id, doctor_id, nurse_id, rec_id)
            query += add
    query = query[0:(len(query) - 2)] + ";"
    cur.execute(query)
    write_into_file(query)


inserting_patients()
inserting_doctors()
inserting_nurses()
inserting_accountants()
inserting_receptionists()
inserting_storekeepers()
inserting_medicines()
inserting_services()
inserting_appointments()
inserting_medical_charts()
inserting_reports()
inserting_nurse_qual()
inserting_doctor_qual()
inserting_nurse_assigned()
inserting_req_med()
inserting_provide_serv()
inserting_order()
inserting_order_ser()
inserting_order_med()
inserting_invoices()
inserting_manage_invoices()
inserting_complete_order()
inserting_appointments_from_date("-90d", 60)

# Make the changes to the database persistent
con.commit()

# Close communication with the database
cur.close()
con.close()

# close file
file_output.close()