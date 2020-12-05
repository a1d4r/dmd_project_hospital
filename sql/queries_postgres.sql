-- 1. A patient claims that she forgot her bag in the room where she had a medical
-- appointment on the last time she came to the hospital. The problem is that she had
-- several appointments on that same day. She believes that the doctor’s name (first or last
-- name, but not both) starts with “M” or “L” - she doesn’t have a good memory either. Find
-- all the possible doctors that match the description.
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

-- 2. The hospital management team wants to get statistics on the appointments per doctors.
-- For each doctor, the report should present the total and average number of
-- appointments in each time slot of the week during the last year. For example, a report
-- generated on 01/12/2019 should consider data since 01/12/2018.
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

-- 3. The hospital wants to retrieve information on the patients who had an appointment
-- during the previous month. However, an information which is relevant for some
-- managers is to find which patients visited the hospital every week, at least twice a week.
-- Such patients probably should receive home visits from doctors.

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

-- 4. Managers want to project the expected monthly income if the hospital start to charge a
-- small value from each patient. The value per appointment would depend on the age and
-- the number of appointments per month. The rules are summarised as follows:
-- # appointments in a month < 3 # appointments in a month >= 3
-- Age < 50 200 Rub 250 Rub
-- Age >= 50 400 Rub 500 Rub
-- Based on the rules above, what would be the income of the hospital in the previous
-- month?
WITH
meetings_num AS (
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

-- 5. The managers want to reward experienced and long serving doctors. For that, they want
-- to find out the doctors who have attended at least five patients per year for the last 10
-- years. Also, such doctors should have had attended a total of at least 100 patients in this
-- period.
WITH sessions AS ( SELECT D.person_id AS person_id, extract(year FROM A.app_time) AS year
        FROM doctor AS D, appointment AS A
        WHERE A.doctor_id = D.person_id
     ),
     amount_overall AS (SELECT S.person_id
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