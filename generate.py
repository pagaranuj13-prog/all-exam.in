#!/usr/bin/env python3
"""
all-exam.in - सर्व बोर्ड व इयत्तांची पाने आपोआप बनवणारी script.

वापर:
    python generate.py            # फक्त नसलेल्या फाईल्स बनवते (आधीच्या फाईल्स सुरक्षित)
    python generate.py --force    # सर्व फाईल्स पुन्हा बनवते (जुन्या बदलल्या जातील!)

तयार होणाऱ्या फाईल्स: state1.html ... state12.html,
                      cbse1.html  ... cbse12.html,
                      icse1.html  ... icse12.html
"""

import sys
from pathlib import Path

# ============================================================
# 1) बोर्डची माहिती (नाव + रंग)
# ============================================================
BOARDS = {
    "state": {"name": "State Board", "color": "#0066cc", "dark": "#004b99"},
    "cbse":  {"name": "CBSE Board",  "color": "#d35400", "dark": "#a84300"},
    "icse":  {"name": "ICSE Board",  "color": "#27ae60", "dark": "#1e8449"},
}

# ============================================================
# 2) इयत्ता क्रमांक -> मराठी नाव
# ============================================================
CLASS_NAMES = {
    1: "१ ली", 2: "२ री", 3: "३ री", 4: "४ थी", 5: "५ वी", 6: "६ वी",
    7: "७ वी", 8: "८ वी", 9: "९ वी", 10: "१० वी", 11: "११ वी", 12: "१२ वी",
}


# ============================================================
# 3) विषयांची यादी  -- येथे हवे ते बदला / जोडा
#    (विषय नाव, टेस्ट पानाची लिंक)  लिंक नसेल तर "#" ठेवा
# ============================================================
def subjects_for(board: str, cls: int):
    if board == "state":
        if cls <= 2:
            names = ["मराठी", "गणित", "इंग्रजी"]
        elif cls <= 4:
            names = ["मराठी", "गणित", "इंग्रजी", "परिसर अभ्यास"]
        elif cls == 5:
            names = ["मराठी", "हिंदी", "इंग्रजी", "गणित", "परिसर अभ्यास भाग १", "परिसर अभ्यास भाग २"]
        elif cls <= 8:
            names = ["मराठी", "हिंदी", "इंग्रजी", "गणित", "सामान्य विज्ञान",
                     "इतिहास व नागरिकशास्त्र", "भूगोल"]
        elif cls <= 10:
            names = ["मराठी", "हिंदी", "इंग्रजी", "गणित भाग १", "गणित भाग २",
                     "विज्ञान व तंत्रज्ञान", "इतिहास व राज्यशास्त्र", "भूगोल"]
        else:  # 11-12
            names = ["मराठी", "इंग्रजी", "भौतिकशास्त्र", "रसायनशास्त्र", "जीवशास्त्र",
                     "गणित", "अर्थशास्त्र", "लेखाकर्म", "वाणिज्य संघटन", "इतिहास",
                     "भूगोल", "राज्यशास्त्र"]
    elif board == "cbse":
        if cls <= 2:
            names = ["English", "Hindi", "Mathematics"]
        elif cls <= 5:
            names = ["English", "Hindi", "Mathematics", "Environmental Studies (EVS)"]
        elif cls <= 8:
            names = ["English", "Hindi", "Sanskrit", "Mathematics", "Science", "Social Science"]
        elif cls <= 10:
            names = ["English", "Hindi", "Mathematics", "Science", "Social Science",
                     "Information Technology"]
        else:
            names = ["English", "Physics", "Chemistry", "Mathematics", "Biology",
                     "Computer Science", "Accountancy", "Business Studies", "Economics",
                     "History", "Geography", "Political Science"]
    else:  # icse
        if cls <= 5:
            names = ["English", "Hindi", "Mathematics", "Environmental Studies (EVS)"]
        elif cls <= 10:
            names = ["English", "Hindi", "Mathematics", "Physics", "Chemistry", "Biology",
                     "History & Civics", "Geography", "Computer Applications"]
        else:  # ISC
            names = ["English", "Physics", "Chemistry", "Mathematics", "Biology",
                     "Computer Science", "Accountancy", "Commerce", "Economics", "History",
                     "Geography", "Political Science"]

    # लिंक उदा.: state8-maths.html  (आता "#" ठेवली आहे, नंतर बदलता येईल)
    return [(n, "#") for n in names]


# ============================================================
# 4) HTML टेम्पलेट
# ============================================================
TEMPLATE = """<!DOCTYPE html>
<html lang="mr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>इयत्ता {cls_name} - {board_name} विषय</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        body {{ background-color: #f4f7f6; color: #333; line-height: 1.6; }}
        nav {{ background-color: #00264d; color: white; display: flex; justify-content: space-between; align-items: center; padding: 0.8rem 2rem; }}
        .logo {{ font-size: 1.5rem; font-weight: bold; }}
        .back-btn {{ background: #ff9900; color: white; padding: 0.4rem 1rem; border-radius: 4px; text-decoration: none; font-weight: bold; }}
        header {{ background: linear-gradient(135deg, {color}, #00264d); color: white; padding: 2.5rem 1rem; text-align: center; }}
        .container {{ max-width: 1000px; margin: 3rem auto; padding: 0 1rem; }}
        h2.section-title {{ text-align: center; margin-bottom: 2rem; color: #00264d; font-size: 1.8rem; }}
        .subject-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; }}
        .subject-card {{ background: white; padding: 1.8rem 1rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; border-top: 5px solid {color}; transition: transform 0.3s ease; }}
        .subject-card:hover {{ transform: translateY(-5px); }}
        .subject-card h3 {{ color: {color}; margin-bottom: 1rem; font-size: 1.3rem; }}
        .subject-btn {{ display: inline-block; background: {color}; color: white; padding: 0.5rem 1.2rem; border-radius: 4px; text-decoration: none; font-weight: bold; }}
        .subject-btn:hover {{ background: {dark}; }}
        footer {{ text-align: center; padding: 1.5rem; background: #222; color: white; margin-top: 5rem; }}
    </style>
</head>
<body>
    <nav>
        <div class="logo">All Exam - इयत्ता {cls_name}</div>
        <a href="class{cls}.html" class="back-btn">मागे (Back)</a>
    </nav>

    <header>
        <h1>इयत्ता {cls_name} - {board_name}</h1>
        <p>तुमचा विषय निवडा</p>
    </header>

    <div class="container">
        <h2 class="section-title">सर्व विषय</h2>
        <div class="subject-grid">
{cards}
        </div>
    </div>

    <footer><p>&copy; 2026 all-exam.in | सर्व हक्क सुरक्षित.</p></footer>
</body>
</html>
"""

CARD = """            <div class="subject-card"><h3>{name}</h3><a href="{link}" class="subject-btn">टेस्ट सुरू करा</a></div>"""


# ============================================================
# 5) फाईल्स तयार करणे
# ============================================================
def main():
    force = "--force" in sys.argv
    out_dir = Path(__file__).resolve().parent
    created, skipped = 0, 0

    for key, b in BOARDS.items():
        for cls in range(1, 13):
            path = out_dir / f"{key}{cls}.html"
            if path.exists() and not force:
                skipped += 1
                continue

            cards = "\n".join(
                CARD.format(name=n, link=l) for n, l in subjects_for(key, cls)
            )
            html = TEMPLATE.format(
                cls=cls, cls_name=CLASS_NAMES[cls], board_name=b["name"],
                color=b["color"], dark=b["dark"], cards=cards,
            )
            path.write_text(html, encoding="utf-8")
            created += 1

    print(f"तयार झाल्या: {created} | वगळल्या (आधीच आहेत): {skipped}")
    if skipped:
        print("सर्व पुन्हा बनवायच्या असतील तर:  python generate.py --force")


if __name__ == "__main__":
    main()
