-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28; --Start by looking for a crime scene report that matches the date and the location of the crime. We found out that interviewers mentioned the word bakery multiple times, as well as that the crime took place at 1015 am.

SELECT transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE '%bakery%'; --Read interviews about what happenned at the bakery that day.

SELECT bakery_security_logs.license_plate, people.name, people.id FROM bakery_security_logs JOIN people ON bakery_security_logs.license_plate = people.license_plate AND year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND minute >= 15 AND activity = 'exit'; --Look at the bakery security logs between 1015 and 1025 in the morning the day of theft(per interview, the theft was exiting parking lot within 10 minutes of the crime) to find out licence plates, names and ids of suspects that were parked by the bakery before the crime happened.
+---------------+---------+--------+
| license_plate |  name   |   id   |
+---------------+---------+--------+
| 5P2BI95       | Vanessa | 221103 |
| 94KL13X       | Bruce   | 686048 |
| 6P58WS2       | Barry   | 243696 |
| 4328GD8       | Luca    | 467400 |
| G412CB7       | Sofia   | 398010 |
| L93JTIZ       | Iman    | 396669 |
| 322W7JE       | Diana   | 514354 |
| 0NTHK55       | Kelsey  | 560886 |
+---------------+---------+--------+
Suspects: Vanessa, Bruce, Barry, Luca, Sofia, Iman, Diana, Kelsey.

SELECT people.name FROM people, bank_accounts, atm_transactions WHERE bank_accounts.person_id = people.id AND atm_transactions.account_number = bank_accounts.account_number AND atm_transactions.year = 2021 AND atm_transactions.month = 7 AND atm_transactions.day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw"; --Find out who made withdrawals from the ATM on Leggett Street that day and compare to suspects.
+---------+
|  name   |
+---------+
| Bruce   |
| Diana   |
| Brooke  |
| Kenny   |
| Iman    |
| Luca    |
| Taylor  |
| Benista |
+---------+
Suspects: Bruce, Luca, Iman, Diana.

SELECT people.name, phone_calls.caller FROM people, phone_calls WHERE people.phone_number = phone_calls.caller AND year = 2021 AND month = 7 AND day = 28 AND duration < 60; --Per one of the interviews, the thief called someone the day of the theft and talked on the phone for less than one minute.
+---------+----------------+
|  name   |     caller     |
+---------+----------------+
| Sofia   | (130) 555-0289 |
| Kelsey  | (499) 555-9472 |
| Bruce   | (367) 555-5533 |
| Kelsey  | (499) 555-9472 |
| Taylor  | (286) 555-6063 |
| Diana   | (770) 555-1861 |
| Carina  | (031) 555-6622 |
| Kenny   | (826) 555-1652 |
| Benista | (338) 555-6650 |
+---------+----------------+
Suspects: Bruce, Diana.

SELECT id, origin_airport_id, destination_airport_id FROM flights WHERE year = 2021 AND month = 7 AND day = 29 ORDER BY hour ASC LIMIT 1; --Per one of the interviews, the thieft wanted to get on the first flight out of the Fiftyville the following day. Look up the earlies fright on July 29.
+----+-------------------+------------------------+
| id | origin_airport_id | destination_airport_id |
+----+-------------------+------------------------+
| 36 | 8                 | 4                      |
+----+-------------------+------------------------+

SELECT passport_number FROM passengers WHERE flight_id = 36; --Look up everyone who bought tickets on the earliest flight out of Fiftyville.

SELECT passport_number FROM people WHERE name = 'Bruce'; --Compare suspect's passport number(matches Bruce).
SELECT passport_number FROM people WHERE name = 'Diana';

SELECT city FROM airports WHERE id = 4; --Find out where Bruce was going by destination airport id(New York).

SELECT people.name FROM people, phone_calls WHERE people.phone_number = phone_calls.receiver AND year = 2021 AND month = 7 AND day = 28 AND duration < 60 AND phone_calls.caller = '(367) 555-5533'; --Find out who helped Bruce by checking who he called that day(Robin).