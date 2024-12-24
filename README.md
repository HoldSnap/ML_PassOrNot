Данные если у определенного предмета будут ставить оценки по посещяемости
```
INSERT INTO exams (student_name, study_hours, avg_grade, attendance_rate, completed_works, passed, subject_id)
SELECT
    CONCAT('Student_', generate_series) AS student_name,
    ROUND(CAST(RANDOM() * 50 AS NUMERIC), 2) AS study_hours, -- Случайное количество часов подготовки
    ROUND(CAST(RANDOM() * 3 + 2 AS NUMERIC), 2) AS avg_grade, -- Средняя оценка (от 2.0 до 5.0)
    1.0 AS attendance_rate, -- 100% посещаемость
    ROUND(CAST(RANDOM() AS NUMERIC), 2) AS completed_works, -- Случайный процент выполненных работ
    TRUE AS passed, -- Экзамен сдан
    5 AS subject_id -- ID предмета 5
FROM
    generate_series(1, 1000);
```
Данные если у 10 предмета внезапно люди начнут сдавать
```
INSERT INTO exams (student_name, study_hours, avg_grade, attendance_rate, completed_works, passed, subject_id)
SELECT
    CONCAT('Student_', generate_series) AS student_name,         -- Уникальное имя студента
    ROUND(CAST(RANDOM() * 50 AS NUMERIC), 2) AS study_hours,     -- Случайное количество часов подготовки (0–50)
    ROUND(CAST(RANDOM() * 3 + 2 AS NUMERIC), 2) AS avg_grade,    -- Средняя оценка (2.0–5.0)
    ROUND(CAST(RANDOM() AS NUMERIC), 2) AS attendance_rate,      -- Случайная посещаемость (0–1)
    ROUND(CAST(RANDOM() AS NUMERIC), 2) AS completed_works,      -- Случайный процент выполненных работ (0–1)
    TRUE AS passed,                                              -- Сданный экзамен
    10 AS subject_id                                             -- ID предмета 10
FROM
    generate_series(1, 300);                                     -- Генерация 300 записей
```
