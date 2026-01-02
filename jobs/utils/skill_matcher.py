# jobs/utils/skill_matcher.py

import math

def normalize_skills(skills_text):
    """
    Converts comma separated skills to clean list
    """
    return [
        skill.strip().lower()
        for skill in skills_text.split(',')
        if skill.strip()
    ]


def extract_cv_skills(cv_text, job_skills):
    """
    Extract only job-related skills from CV text
    """
    cv_text = cv_text.lower()
    matched_skills = []

    for skill in job_skills:
        if skill in cv_text:
            matched_skills.append(skill)

    return matched_skills


def cosine_similarity(job_skills, cv_skills):
    """
    Apply cosine similarity on skill presence
    """
    if not job_skills:
        return 0

    job_vector = []
    cv_vector = []

    for skill in job_skills:
        job_vector.append(1)
        cv_vector.append(1 if skill in cv_skills else 0)

    dot_product = sum(j * c for j, c in zip(job_vector, cv_vector))
    magnitude_job = math.sqrt(sum(j * j for j in job_vector))
    magnitude_cv = math.sqrt(sum(c * c for c in cv_vector))

    if magnitude_cv == 0:
        return 0

    similarity = dot_product / (magnitude_job * magnitude_cv)
    return round(similarity * 100, 2)
