import psycopg2
import prettytable

print("Connecting to the database...")
con = psycopg2.connect(
    database="hospital",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)
print("Successfully connected to the database.")

queries = {
    1: '''
with last_meeting_date AS (
    SELECT A.app_time::date, patient_id
    FROM appointment AS A
    WHERE A.patient_id = 28
    ORDER BY A.app_time DESC
    LIMIT 1
),
    possible_appointments AS (
    SELECT nurse_id, doctor_id, A.app_time::date, app_id
    FROM appointment AS A, last_meeting_date AS L
    WHERE A.app_time::date = L.app_time
      AND A.patient_id = L.patient_id
)
SELECT DISTINCT P.person_id, P.name, P.surname
FROM possible_appointments AS P_A, person as P
WHERE
      (P.person_id = P_A.doctor_id OR P.person_id = P_A.nurse_id) AND
      ((P.name LIKE 'M%' OR P.name LIKE 'L%') OR
      (P.surname LIKE 'M%' OR P.surname LIKE 'L%')) AND
      NOT ((P.name LIKE 'M%' OR P.name LIKE 'L%') AND
      (P.surname LIKE 'M%' OR P.surname LIKE 'L%'));
    ''',
    2: '''
WITH
     last_year AS (
         SELECT D.person_id, A.app_time,
                DIV((extract('day' FROM A.app_time) - 1)::INTEGER, 7) + 1 AS week,
                extract('hour' FROM A.app_time)            AS hour
         FROM doctor AS D,
              appointment AS A
         WHERE D.person_id = A.doctor_id
           AND A.app_time >= current_date - interval '1' year
     ),
     time_table AS ( SELECT L.person_id, L.week, L.hour, COUNT(L.person_id) AS count, COUNT(L.person_id)/365.0 AS avg
         FROM last_year AS L
         GROUP BY (L.person_id,L.week, L.hour)
     )
SELECT T.person_id, P.name, P.surname, T.week, T.hour, T.count, T.avg
FROM time_table AS T, person AS P
WHERE P.person_id = T.person_id
ORDER BY (T.person_id, T.week, T.hour);
    ''',
    3: '''
WITH table_of_four AS (SELECT *
        FROM generate_series(0, 3) AS T(num)
     ),
     app_per_week AS (
         SELECT A.patient_id, num, COUNT(A.app_id) as count
         FROM appointment AS A, table_of_four AS T
         WHERE A.app_time >= date_trunc('month', current_date - interval '1' month) + T.num * interval '7' day AND
               A.app_time < date_trunc('month', current_date - interval '1' month) + (T.num+1) * interval '7' day
         GROUP BY (A.patient_id, T.num)
         HAVING COUNT(A.app_id) >= 2
     )
SELECT P.person_id, P.name, P.surname
FROM app_per_week AS A, person AS P
WHERE A.patient_id = P.person_id
GROUP BY (P.person_id)
HAVING COUNT(P.person_id) = 4
ORDER BY P.person_id;
    ''',
    4: '''
WITH
meetings_num AS(
    SELECT A.patient_id, EXTRACT (YEAR FROM age(current_date, PER.date_of_birth)) AS age, COUNT(A.patient_id) AS count
    FROM appointment AS A, person AS PER
    WHERE A.patient_id = PER.person_id AND
          A.app_time >= date_trunc('month', current_date - interval '1' month) AND
          A.app_time < date_trunc('month', current_date)
    GROUP BY A.patient_id, age),
amount AS
        (SELECT M.patient_id,
        CASE
            WHEN M.age < 50 AND M.count < 3 THEN M.count * 200
            WHEN M.age < 50 AND M.count >= 3 THEN M.count * 250
            WHEN M.age >= 50 AND M.count < 3 THEN M.count * 400
            WHEN M.age >= 50 AND M.count >= 3 THEN M.count * 500
            ELSE 0
        END AS sum
        FROM meetings_num AS M)
SELECT SUM(sum) AS SUM
FROM amount
GROUP BY();
    ''',
    5: '''
WITH sessions AS ( SELECT D.person_id AS person_id, extract(year FROM A.app_time) AS year
        FROM doctor AS D, appointment AS A
        WHERE A.doctor_id = D.person_id
     ),
     amount_overall AS(SELECT S.person_id
         FROM sessions AS S
         GROUP BY (S.person_id)
         HAVING count(S.year) >= 100
     ),
     amount_per_year AS (SELECT S.person_id, extract (year FROM current_date) - S.year AS year, COUNT(S.year) AS count
         FROM sessions AS S
         GROUP BY (S.person_id, extract (year FROM current_date) - S.year)
     ),
     perfect_for_ten AS (SELECT A.person_id
         FROM amount_per_year AS A
         WHERE A.year < 10 AND A.count>=5
         GROUP BY (A.person_id)
         HAVING COUNT(A.year) = 10
         )
SELECT P.person_id, P.name, P.surname
FROM person AS P, amount_overall AS O, perfect_for_ten AS perfect
WHERE P.person_id = O.person_id AND O.person_id = perfect.person_id;
    '''
}

while True:
    response = ''
    while response not in ['1', '2', '3', '4', '5', 'q']:
        print("Enter the number of query [1..5] or q to exit: ", end='')
        response = input()

    if response == 'q':
        break

    query_id = int(response)

    cur = con.cursor()
    cur.execute(queries[query_id])

    table = prettytable.from_db_cursor(cur)
    print(table)

con.close()
