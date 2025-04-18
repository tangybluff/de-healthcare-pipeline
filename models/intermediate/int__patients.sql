WITH summary AS (
    SELECT
        patient_type,
        COUNT(*) AS patient_count,
        AVG(age) AS avg_age,
        SUM(CASE WHEN pneumonia = 1 THEN 1 ELSE 0 END) AS pneumonia_cases,
        SUM(CASE WHEN icu = 1 THEN 1 ELSE 0 END) AS icu_admissions
    FROM staging_healthcare
    GROUP BY patient_type
)
SELECT * FROM summary;
