# jobs/utils/skill_matcher.py

import math
import re

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
    if not cv_text:
        return []

    matched_skills = []

    for skill in job_skills:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, cv_text):
            matched_skills.append(skill)

    return matched_skills


def cosine_similarity(job_skills, applicant_skills):
    """
    Calculate cosine similarity between job_skills and applicant_skills.
    Both inputs should be lists of lowercase strings.

    Returns: similarity as percentage
    """

    # normalize: lowercase and strip spaces
    job_skills = [s.strip().lower() for s in job_skills]
    applicant_skills = [s.strip().lower() for s in applicant_skills]

    if not job_skills or not applicant_skills:
        return 0

    # Create simple bag-of-words vectors
    all_skills = list(set(job_skills + applicant_skills))
    job_vector = [1 if skill in job_skills else 0 for skill in all_skills]
    applicant_vector = [1 if skill in applicant_skills else 0 for skill in all_skills]

    # Cosine similarity
    dot_product = sum(j * a for j, a in zip(job_vector, applicant_vector))
    magnitude_job = math.sqrt(sum(j ** 2 for j in job_vector))
    magnitude_applicant = math.sqrt(sum(a ** 2 for a in applicant_vector))

    if magnitude_job == 0 or magnitude_applicant == 0:
        return 0

    similarity = dot_product / (magnitude_job * magnitude_applicant)
    return round(similarity * 100, 2)



# ================= Skill Gap Analysis =================

def analyze_skill_gap(job_skills_text, cv_text):
    """
    Analyze matched, missing and priority skills
    """
    job_skills = normalize_skills(job_skills_text)
    matched_skills = extract_cv_skills(cv_text, job_skills)

    missing_skills = list(set(job_skills) - set(matched_skills))

    match_percentage = cosine_similarity(job_skills, matched_skills)

    # Priority gaps: show top 3 missing skills
    priority_missing = missing_skills[:3]

    explanation = generate_explanation(
        match_percentage,
        matched_skills,
        priority_missing
    )

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "priority_missing": priority_missing,
        "explanation": explanation
    }


def generate_explanation(score, matched, priority_missing):
    """
    Human-readable explanation
    """
    if score >= 80:
        return "Your profile is a strong match for this job."

    if score >= 50:
        if priority_missing:
            return (
                "Your profile partially matches this job. "
                f"Improving skills like {', '.join(priority_missing)} "
                "can significantly increase your match score."
            )
        return "Your profile partially matches this job."

    return (
        "Your profile has a low match for this job. "
        "Consider gaining the required skills before applying."
    )
