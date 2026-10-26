from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field


CATEGORY_NAMES = {
    "COD": "Coding",
    "DSA": "Data Structures and Algorithms",
    "OOD": "Object-Oriented Design",
    "APTI": "Aptitude",
    "COMM": "Communication",
    "AI": "Artificial Intelligence",
    "CLOUD": "Cloud",
    "SQL": "SQL and Databases",
    "SWE": "Software Engineering",
    "SYSD": "System Design",
    "NETW": "Networking",
    "OS": "Operating Systems",
    "OTHER": "Other",
}

SKILL_TAXONOMY: dict[str, tuple[str, ...]] = {
    "Python": ("python",),
    "Java": ("java",),
    "JavaScript": ("javascript", "js"),
    "TypeScript": ("typescript",),
    "C#": ("c#", "c sharp"),
    "C++": ("c++",),
    "Go": ("golang", "go"),
    "React": ("react", "reactjs", "react.js"),
    "Node.js": ("node.js", "nodejs"),
    "REST APIs": ("rest api", "rest apis", "restful"),
    "Docker": ("docker",),
    "Kubernetes": ("kubernetes", "k8s"),
    "AWS": ("aws", "amazon web services"),
    "Azure": ("azure",),
    "Google Cloud": ("gcp", "google cloud"),
    "SQL": ("sql",),
    "PostgreSQL": ("postgresql", "postgres"),
    "MySQL": ("mysql",),
    "MongoDB": ("mongodb",),
    "Redis": ("redis",),
    "Machine Learning": ("machine learning",),
    "Artificial Intelligence": ("artificial intelligence", "ai"),
    "TensorFlow": ("tensorflow",),
    "PyTorch": ("pytorch",),
    "Git": ("git",),
    "CI/CD": ("ci/cd", "continuous integration", "continuous delivery"),
    "Linux": ("linux",),
    "TCP/IP": ("tcp/ip",),
    "HTTP": ("http",),
    "System Design": ("system design",),
    "Data Structures": ("data structures",),
    "Algorithms": ("algorithms", "algorithmic problem solving"),
    "Object-Oriented Design": ("object oriented design", "object-oriented design", "oop"),
    "Unit Testing": ("unit testing",),
    "Agile": ("agile",),
    "Communication": ("communication",),
    "Leadership": ("leadership",),
    "Collaboration": ("collaboration", "teamwork"),
    "Problem Solving": ("problem solving",),
}

SKILL_CATEGORIES = {
    "Python": ("COD",),
    "Java": ("COD",),
    "JavaScript": ("COD",),
    "TypeScript": ("COD",),
    "C#": ("COD",),
    "C++": ("COD",),
    "Go": ("COD",),
    "React": ("SWE",),
    "Node.js": ("SWE",),
    "REST APIs": ("SWE",),
    "Docker": ("CLOUD",),
    "Kubernetes": ("CLOUD",),
    "AWS": ("CLOUD",),
    "Azure": ("CLOUD",),
    "Google Cloud": ("CLOUD",),
    "SQL": ("SQL",),
    "PostgreSQL": ("SQL",),
    "MySQL": ("SQL",),
    "MongoDB": ("SQL",),
    "Redis": ("SQL",),
    "Machine Learning": ("AI",),
    "Artificial Intelligence": ("AI",),
    "TensorFlow": ("AI",),
    "PyTorch": ("AI",),
    "Git": ("SWE",),
    "CI/CD": ("SWE",),
    "Linux": ("OS",),
    "TCP/IP": ("NETW",),
    "HTTP": ("NETW",),
    "System Design": ("SYSD",),
    "Data Structures": ("DSA",),
    "Algorithms": ("DSA",),
    "Object-Oriented Design": ("OOD",),
    "Unit Testing": ("SWE",),
    "Agile": ("SWE",),
    "Communication": ("COMM",),
    "Leadership": ("COMM",),
    "Collaboration": ("COMM",),
    "Problem Solving": ("APTI",),
}

SECTION_PATTERNS = (
    "responsibilities",
    "what you'll do",
    "what you will do",
    "key duties",
    "requirements",
    "required qualifications",
    "qualifications",
    "education",
    "skills",
)


@dataclass
class CategoryResult:
    code: str
    name: str
    skills: list[str]


@dataclass
class RequirementResult:
    experience: list[str]
    education: list[str]


@dataclass
class JDAnalysis:
    title: str | None
    company: str | None
    requirements: RequirementResult
    technical_skills: list[str]
    soft_skills: list[str]
    responsibilities: list[str]
    radix_categories: list[CategoryResult] = field(default_factory=list)
    unmatched_skills: list[str] = field(default_factory=list)
    extraction_method: str = "deterministic keyword extraction"


def _alias_pattern(alias: str) -> re.Pattern[str]:
    escaped = re.escape(alias)
    escaped = escaped.replace(r"\ ", r"\s+")
    return re.compile(rf"(?<![A-Za-z0-9])(?:{escaped})(?![A-Za-z0-9])", re.IGNORECASE)


def _clean_lines(text: str) -> list[str]:
    return [re.sub(r"\s+", " ", line).strip(" -*\t") for line in text.splitlines() if line.strip(" -*\t")]


def _extract_title(lines: list[str]) -> str | None:
    for line in lines[:12]:
        match = re.match(r"^(?:job\s+)?title\s*[:\-]\s*(.+)$", line, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def _extract_company(lines: list[str]) -> str | None:
    for line in lines[:12]:
        match = re.match(r"^(?:company|organization|employer)\s*[:\-]\s*(.+)$", line, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def _extract_bullets(lines: list[str], section_names: tuple[str, ...]) -> list[str]:
    results: list[str] = []
    active = False
    for line in lines:
        normalized = line.lower().rstrip(":")
        is_heading = normalized in section_names or any(normalized.startswith(f"{name}:") for name in section_names)
        if is_heading:
            active = True
            continue
        if active and normalized in ("requirements", "required qualifications", "qualifications", "skills", "education"):
            break
        if active and line:
            results.append(line)
    return results[:20]


def _extract_experience(text: str) -> list[str]:
    pattern = re.compile(r"(?i)(?:\b\d+(?:\+)?(?:-|–| to )\d+\s*years?|\b(?:at least |minimum )?\d+\+?\s*years?\b[^.\n]{0,35}|at least \d+\s*years?\b)")
    values = []
    for match in pattern.finditer(text):
        value = match.group(0).strip()
        value = re.sub(r"\s+(?:of\s+)?(?:experience|background|exposure).*", "", value, flags=re.IGNORECASE)
        values.append(value)
    return list(dict.fromkeys(values))


def _extract_education(text: str) -> list[str]:
    pattern = re.compile(
        r"(?i)(?<![A-Za-z])(?:Bachelor(?:'s)?|Master(?:'s)?|PhD|Doctorate|associate(?:'s)? degree)[^.\n]*"
    )
    return list(dict.fromkeys(match.group(0).strip() for match in pattern.finditer(text)))


def _find_skills(text: str) -> tuple[list[str], list[str], list[str]]:
    found: list[str] = []
    soft: list[str] = []
    unmatched: list[str] = []
    for skill, aliases in SKILL_TAXONOMY.items():
        if any(_alias_pattern(alias).search(text) for alias in aliases):
            category = SKILL_CATEGORIES[skill]
            if category == ("COMM",):
                soft.append(skill)
            else:
                found.append(skill)

    known_aliases = [alias for aliases in SKILL_TAXONOMY.values() for alias in aliases]
    candidate_pattern = re.compile(r"(?<![A-Za-z])([A-Z][A-Za-z0+#.]{1,12}(?:[- ][A-Z]?[A-Za-z0+#.]{1,12})*)(?![A-Za-z])")
    common_non_skills = {
        "Job", "Title", "Company", "Responsibilities", "Requirements", "Requirements", "Qualifications",
        "Education", "Skills", "Strong", "Bachelor", "Master", "REST", "APIs",
    }
    for candidate in candidate_pattern.findall(text):
        if candidate.lower() in {alias.lower() for alias in known_aliases}:
            continue
        if candidate in common_non_skills:
            continue
        if candidate.lower() in {word.lower() for word in CATEGORY_NAMES.values()}:
            continue
        if len(candidate) >= 3:
            unmatched.append(candidate)

    return found, soft, list(dict.fromkeys(unmatched))[:10]


def analyze_job_description(text: str) -> JDAnalysis:
    normalized = text.strip()
    lines = _clean_lines(normalized)

    technical, soft, unmatched = _find_skills(normalized)
    grouped: dict[str, list[str]] = {}
    for skill in technical + soft:
        for code in SKILL_CATEGORIES[skill]:
            grouped.setdefault(code, []).append(skill)

    categories = [
        CategoryResult(code=code, name=CATEGORY_NAMES[code], skills=skills)
        for code, skills in grouped.items()
    ]

    responsibilities = _extract_bullets(lines, (
        "responsibilities", "what you'll do", "what you will do", "key duties"
    ))
    return JDAnalysis(
        title=_extract_title(lines),
        company=_extract_company(lines),
        requirements=RequirementResult(
            experience=_extract_experience(normalized),
            education=_extract_education(normalized),
        ),
        technical_skills=technical,
        soft_skills=soft,
        responsibilities=responsibilities,
        radix_categories=categories,
        unmatched_skills=unmatched,
    )


def analysis_to_dict(analysis: JDAnalysis) -> dict:
    return asdict(analysis)
