# Titration Experiments Management Program (TEMP)

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse, quote, unquote
import mysql.connector
import datetime
from datetime import date
import re
import html
import os
import base64

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

# ---------- TEMP DATABASE CONNECTION ---------- #Christina #Sana #Seyoung #Abarnna
def get_connection_temp():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="temp"
    )

# ---------- To save images ---------- #Sana
def save_logo_to_folder(base64_string):
    if not base64_string or "," not in base64_string:
        return None
    try:
        if not os.path.exists('images'):
            os.makedirs('images')

        head, data = base64_string.split(',')
        file_ext = head.split('/')[-1].split(';')[0] 
        
        filename = f"logo_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_ext}"
        filepath = f"images/{filename}"

        with open(filepath, "wb") as f:
            f.write(base64.b64decode(data))
        
        return filepath 
    except:
        return None

# ----------UPDATE HEADER DATA TO THE MYSQL DATABASE ---------- #Christina #Sana
def update_header_in_db(name, logo_path):
    try:
        conn = get_connection_temp()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE header_data_temp 
            SET header_name_temp = %s, header_image_temp = %s 
            WHERE header_id_temp = 1
        """, (name, logo_path))
        
        if cur.rowcount == 0:
            cur.execute("""
                INSERT INTO header_data_temp (header_id_temp, header_name_temp, header_image_temp)
                VALUES (1, %s, %s)
            """, (name, logo_path))
            
        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print(f"SQL Error: {e}")

# ---------- HEADER DATA ---------- #Christina #Sana
def header_data_temp():
    try:
        import time
        conn = get_connection_temp()
        cur = conn.cursor()
        cur.execute("SELECT header_name_temp, header_image_temp FROM header_data_temp WHERE header_id_temp = 1")
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if row:
            title = row[0]
            clean_path = row[1].replace('\\', '/') if row[1] else ""

            if clean_path and not clean_path.startswith('/'):
                clean_path = '/' + clean_path

            logo = f"{clean_path}?v={int(time.time())}" if clean_path else ""
            return title, logo
    except:
        pass
    return "TEMP", ""

# ---------- UPDATE HEADER DATA ---------- #Sana
def update_header_temp(new_name, new_image):
    conn = get_connection_temp()
    cur = conn.cursor()
    cur.execute(
        "UPDATE header_data_temp SET header_name_temp=%s, header_image_temp=%s LIMIT 1",
        (new_name, new_image)
    )
    conn.commit()
    cur.close()
    conn.close()

header_title, header_logo = header_data_temp()

# ============================================================================
# ABOUT PAGE DATABASE FUNCTIONS
# ============================================================================

# ---------- About us title discriptions ---------- #Christina #Abarna
def get_about_hero_content():
    """Get hero section content for about page."""
    conn = get_connection_temp()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS about_hero_temp (
            id INT PRIMARY KEY DEFAULT 1,
            title VARCHAR(255) DEFAULT 'About Us.',
            description TEXT,
            badge_text VARCHAR(255) DEFAULT 'TITRATION EXPERIMENTS MANAGEMENT PROGRAM'
        )
    """)
    conn.commit()
    cur.execute("SELECT title, description, badge_text FROM about_hero_temp WHERE id=1")
    row = cur.fetchone()
    if not row:
        cur.execute("""
            INSERT INTO about_hero_temp (id, title, description, badge_text) VALUES 
            (1, 'About Us.', 'TEMP is a sophisticated solution for modern laboratory data management, bridging the gap between manual records and digital efficiency.', 'TITRATION EXPERIMENTS MANAGEMENT PROGRAM')
        """)
        conn.commit()
        cur.execute("SELECT title, description, badge_text FROM about_hero_temp WHERE id=1")
        row = cur.fetchone()
    cur.close()
    conn.close()
    return {"title": row[0], "description": row[1], "badge_text": row[2]}

# ---------- Update about us title descriptions ---------- #Christina #Abarna
def update_about_hero_content(title, description, badge_text):
    """Update hero section content."""
    conn = get_connection_temp()
    cur = conn.cursor()
    cur.execute("""
        UPDATE about_hero_temp SET title=%s, description=%s, badge_text=%s WHERE id=1
    """, (title, description, badge_text))
    conn.commit()
    cur.close()
    conn.close()

# ---------- Update about us main content ---------- #Christina #Abarna
def get_about_project_content():
    """Get project scope content for about page."""
    conn = get_connection_temp()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS about_project_temp (
            id INT PRIMARY KEY DEFAULT 1,
            header_title VARCHAR(255) DEFAULT 'The Project Scope',
            header_tag VARCHAR(100) DEFAULT 'ABOUT TEMP',
            paragraph1 TEXT,
            paragraph2 TEXT,
            paragraph3 TEXT
        )
    """)
    conn.commit()
    cur.execute("SELECT header_title, header_tag, paragraph1, paragraph2, paragraph3 FROM about_project_temp WHERE id=1")
    row = cur.fetchone()
    if not row:
        cur.execute("""
            INSERT INTO about_project_temp (id, header_title, header_tag, paragraph1, paragraph2, paragraph3) VALUES 
            (1, 'The Project Scope', 'ABOUT TEMP',
            'TEMP (Titration Experiments Management Program) is a web-based system designed to help students, researchers, and laboratory users efficiently manage titration experiment data.',
            'This platform allows users to store, search, update, delete, and export titration records in a structured and organized way. By improving accuracy and workflow efficiency, TEMP reduces manual record-keeping errors and enhances accessibility in laboratory environments.',
            'Featuring a secure login system and an intuitive interface, TEMP provides database-driven data management powered by MySQL. Users can easily navigate the system to perform different actions related to experiment handling.')
        """)
        conn.commit()
        cur.execute("SELECT header_title, header_tag, paragraph1, paragraph2, paragraph3 FROM about_project_temp WHERE id=1")
        row = cur.fetchone()
    cur.close()
    conn.close()
    return {"header_title": row[0], "header_tag": row[1], "paragraph1": row[2], "paragraph2": row[3], "paragraph3": row[4]}

# ---------- Update about us project content ---------- #Christina #Abarna
def update_about_project_content(header_title, header_tag, paragraph1, paragraph2, paragraph3):
    """Update project scope content."""
    conn = get_connection_temp()
    cur = conn.cursor()
    cur.execute("""
        UPDATE about_project_temp SET header_title=%s, header_tag=%s, paragraph1=%s, paragraph2=%s, paragraph3=%s WHERE id=1
    """, (header_title, header_tag, paragraph1, paragraph2, paragraph3))
    conn.commit()   
    cur.close()
    conn.close()

# ---------- Update about us team members ---------- #Christina #Abarna
def get_about_team_members():
    """Get team members for about page."""
    conn = get_connection_temp()
    cur = conn.cursor()
    # Updated column to LONGTEXT to store base64 strings
    cur.execute("""
        CREATE TABLE IF NOT EXISTS about_team_temp (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            role VARCHAR(100) DEFAULT 'Developer',
            image_path LONGTEXT
        )
    """)
    conn.commit()
    
    cur.execute("SHOW COLUMNS FROM about_team_temp LIKE 'image_path'")
    column_info = cur.fetchone()
    if column_info and column_info[1].lower() != 'longtext':
        cur.execute("ALTER TABLE about_team_temp MODIFY image_path LONGTEXT")
        conn.commit()

    cur.execute("SELECT id, name, role, image_path FROM about_team_temp ORDER BY id")
    rows = cur.fetchall()
    if not rows:
        default_members = [
            ("Christina", "Developer", "images/Christina.png"),
            ("Sana", "Developer", "images/Sana.png"),
            ("Seyoung", "Developer", "images/Seyoung.png"),
            ("Abarnna", "Developer", "images/Abarnna.png")
        ]
        for name, role, img in default_members:
            cur.execute("INSERT INTO about_team_temp (name, role, image_path) VALUES (%s, %s, %s)", (name, role, img))
        conn.commit()
        cur.execute("SELECT id, name, role, image_path FROM about_team_temp ORDER BY id")
        rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "name": r[1], "role": r[2], "image_path": r[3]} for r in rows]

# ---------- Update about us update team members ---------- #Christina #Abarna
def update_team_member(member_id, name, role, image_path=None):
    """Update a team member and ensure column can handle large image data."""
    conn = get_connection_temp()
    cur = conn.cursor()
    
    # Ensure the column is LONGTEXT to prevent "Data too long" errors
    try:
        cur.execute("ALTER TABLE about_team_temp MODIFY COLUMN image_path LONGTEXT")
        conn.commit()
    except:
        pass

    if image_path:
        cur.execute("UPDATE about_team_temp SET name=%s, role=%s, image_path=%s WHERE id=%s", 
                    (name, role, image_path, member_id))
    else:
        cur.execute("UPDATE about_team_temp SET name=%s, role=%s WHERE id=%s", 
                    (name, role, member_id))
    conn.commit()
    cur.close()
    conn.close()

# ---------- LOGIN CHECK ---------- #Christina & Abarnna
def check_credentials_temp(username_temp, password_temp):
    conn = get_connection_temp()
    cur = conn.cursor()
    cur.execute(
        "SELECT full_name_temp FROM users_temp WHERE username_temp=%s AND password_temp=%s",
        (username_temp, password_temp)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def get_all_users_temp():
    """Fetch all registered users for the Admin panel."""
    conn = get_connection_temp()
    cur = conn.cursor()
    cur.execute("SELECT full_name_temp, username_temp FROM users_temp ORDER BY id_user_temp")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# ---------- CREATE USER ---------- #Christina, Sana, Seyoung & Abarnna
def create_user_temp(full_name_temp, username_temp, password_temp):
    conn = get_connection_temp()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users_temp (full_name_temp, username_temp, password_temp) VALUES (%s, %s, %s)",
        (full_name_temp, username_temp, password_temp)
    )
    conn.commit()
    cur.close()
    conn.close()

# ---------- CALL TABLE (View all the experiments in the table) ---------- #Seyoung
def get_experiments():
    """Fetch all experiments from the table."""
    conn = get_connection_temp()
    cur = conn.cursor()
    cur.execute(
        "SELECT date_temp, titration_id_temp, standard_solution_name_temp, "
        "titrant_solution_name_temp, totaltrial_1_cm3_temp, totaltrial_2_cm3_temp, "
        "totaltrial_3_cm3_temp, totaltrial_average_cm3_temp, pH_temp, observation_temp "
        "FROM Titrations_temp ORDER BY titration_id_temp"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# ---------- ADD FUNCTION (Add New Experiment to the table) ---------- #Sana
def add_experiment(date, titrant, standard, t1, t2, t3, avg, ph, observation):
    conn = get_connection_temp()
    cur = conn.cursor()
    sql = (
        "INSERT INTO Titrations_temp "
        "(date_temp, titrant_solution_name_temp, standard_solution_name_temp, "
        "totaltrial_1_cm3_temp, totaltrial_2_cm3_temp, totaltrial_3_cm3_temp, "
        "totaltrial_average_cm3_temp, pH_temp, observation_temp) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    )
    cur.execute(sql, (date, titrant, standard, t1, t2, t3, avg, ph, observation))
    conn.commit()
    cur.close()
    conn.close()

# ---------- LOAD FUNCTION (Get Experiment by ID from the table) ---------- #Abarnna
def get_experiment_by_id(exp_id):
    """Fetch a single experiment by its titration_id_temp. Returns a dict or None."""
    conn = get_connection_temp()
    cur = conn.cursor()
    cur.execute(
        "SELECT date_temp, titration_id_temp, standard_solution_name_temp, "
        "titrant_solution_name_temp, totaltrial_1_cm3_temp, totaltrial_2_cm3_temp, "
        "totaltrial_3_cm3_temp, totaltrial_average_cm3_temp, pH_temp, observation_temp "
        "FROM Titrations_temp WHERE titration_id_temp = %s",
        (exp_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {
            "date": str(row[0]) if row[0] else "",
            "titration_id": row[1],
            "standard_solution": row[2] or "",
            "titrant_name": row[3] or "",
            "trial1": row[4] if row[4] is not None else "",
            "trial2": row[5] if row[5] is not None else "",
            "trial3": row[6] if row[6] is not None else "",
            "average": row[7] if row[7] is not None else "",
            "ph_temp": row[8] if row[8] is not None else "",
            "observation": row[9] or ""
        }
    return None

# ---------- UPDATE FUNCTION (Updates the existing experiment in the table) ---------- #Abarnna
def update_experiment(exp_id, date, titrant, standard, t1, t2, t3, avg, ph, observation):
    """Update an existing experiment by its titration_id_temp. Returns True if updated."""
    conn = get_connection_temp()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Titrations_temp WHERE titration_id_temp = %s", (exp_id,))
    exists = cur.fetchone()[0]
    if exists == 0:
        cur.close()
        conn.close()
        return False
    sql = (
        "UPDATE Titrations_temp SET "
        "date_temp=%s, titrant_solution_name_temp=%s, standard_solution_name_temp=%s, "
        "totaltrial_1_cm3_temp=%s, totaltrial_2_cm3_temp=%s, totaltrial_3_cm3_temp=%s, "
        "totaltrial_average_cm3_temp=%s, pH_temp=%s, observation_temp=%s "
        "WHERE titration_id_temp=%s"
    )
    cur.execute(sql, (date, titrant, standard, t1, t2, t3, avg, ph, observation, exp_id))
    conn.commit()
    cur.close()
    conn.close()
    return True

# ---------- DELETE FUNCTION (Deletes the experiment from the table, if it exists) ---------- #Sana
def delete_experiment(exp_id):
    """Returns True if a record was deleted, False if not found."""
    conn = get_connection_temp()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Titrations_temp WHERE titration_id_temp = %s", (exp_id,))
    exists = cur.fetchone()[0]
    if exists == 0:
        cur.close()
        conn.close()
        return False
    cur.execute("DELETE FROM Titrations_temp WHERE titration_id_temp = %s", (exp_id,))
    conn.commit()
    cur.close()
    conn.close()
    return True

# ============================================================================
# ALGORITHMS - Bubble Sort and Binary Search
# ============================================================================

# ---------- BUBBLE SORT ---------- #Sana
def bubble_sort_temp(exp, sort_col_index, reverse=False):
    """Sort experiment rows using bubble sort (handles dates, strings, numbers)."""
    sorted_exp = list(exp)
    total_records = len(sorted_exp)

    for pass_num in range(1, total_records):
        swapped = False

        for i in range(0, total_records - pass_num):
            current_value = sorted_exp[i][sort_col_index]
            next_value = sorted_exp[i + 1][sort_col_index]

            # Handle NULL values
            if current_value is None:
                current_value = datetime.date.min if sort_col_index == 0 else ""
            if next_value is None:
                next_value = datetime.date.min if sort_col_index == 0 else ""

            # Convert to lower if string for alphabetical sorting
            if isinstance(current_value, str):
                current_value_lower = current_value.lower()
            elif isinstance(current_value, datetime.date):
                current_value_lower = current_value
            else:
                current_value_lower = current_value

            if isinstance(next_value, str):
                next_value_lower = next_value.lower()
            elif isinstance(next_value, datetime.date):
                next_value_lower = next_value
            else:
                next_value_lower = next_value

            # Compare and swap
            if (current_value_lower > next_value_lower and not reverse) or \
               (current_value_lower < next_value_lower and reverse):
                sorted_exp[i], sorted_exp[i + 1] = sorted_exp[i + 1], sorted_exp[i]
                swapped = True

        if not swapped:
            break

    return sorted_exp

# ---------- BINARY SEARCH ---------- #Seyoung
def binary_search_rows(rows, column_index, target):
    """
    Binary search on sorted rows for partial string match.
    rows: All table data
    column_index: Column index to search
    target: search term (lowercase)
    """
    # String-based sorting (binary search prerequisite)
    rows.sort(key=lambda x: str(x[column_index]).lower())

    result = []
    left, right = 0, len(rows) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_value = str(rows[mid][column_index]).lower()

        if target in mid_value:
            # Collect all matching rows around the midpoint
            i = mid
            while i >= 0 and target in str(rows[i][column_index]).lower():
                result.append(rows[i])
                i -= 1

            i = mid + 1
            while i < len(rows) and target in str(rows[i][column_index]).lower():
                result.append(rows[i])
                i += 1
            break

        elif target < mid_value:
            right = mid - 1
        else:
            left = mid + 1

    return result

# ============================================================================
# COLUMN INDEX MAP (for main page)
# ============================================================================

COLUMN_INDEX_MAP = {
    "date_temp": 0,
    "titration_id_temp": 1,
    "standard_solution_name_temp": 2,
    "titrant_solution_name_temp": 3,
}
# ---------- To highlight the Searched Item ---------- #Seyoung
def highlight(text, col_index, search_column=None, search_value=None):
    escaped = html.escape(str(text))
    if search_column is not None and search_value:
        if COLUMN_INDEX_MAP.get(search_column) == col_index:
            pattern = re.compile(re.escape(html.escape(search_value)), re.IGNORECASE)
            return pattern.sub(
                lambda m: f"<span class='highlight'>{m.group(0)}</span>",
                escaped
            )
    return escaped

# ============================================================================
# PAGE RENDERERS
# ============================================================================

# ---------- ABOUT US PAGE ---------- #Christina #Abarnna #Seyoung
#Christina: Footer, Description(Title, Inserting Images, Footers)
#Abarnna: Create Database, Updating description and Title
#Seyoung: Layout and Buttons

def render_about_page(username="User"):
    # Load content from database
    hero_data = get_about_hero_content()
    project_data = get_about_project_content()
    team_members = get_about_team_members()
    
    # Build team cards HTML
    team_cards_html = ""
    for member in team_members:
        team_cards_html += f'''
                <div class="creator-card">
                    <button type="button" class="edit-btn team-edit-btn" onclick="openTeamModal({member['id']}, '{html.escape(member['name'])}', '{html.escape(member['role'])}', '{html.escape(member['image_path'] or '')}')">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <div class="creator-img-wrap">
                        <img src="{member['image_path'] if member['image_path'] else 'images/default.png'}" class="creator-img" alt="{html.escape(member['name'])}">
                    </div>
                    <div class="name">{html.escape(member['name'])}</div>
                    <div class="role">{html.escape(member['role'])}</div>
                </div>'''
    
    page = f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>About Us – {header_title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400&display=swap');
        :root {{
            --t-green: #002c23;
            --t-gold: #b1d3cb;
            --t-cream: #e8f3f1;
            --radius: 14px;
            --shadow-sm: 0 2px 10px rgba(0,0,0,0.04);
            --shadow-md: 0 8px 30px rgba(0,0,0,0.06);
        }}

        * {{ box-sizing: border-box; }}

        body {{
            background-color: #e8f3f1;
            color: #333;
            font-family: 'Inter', sans-serif;
            margin: 0;
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Inter', sans-serif;
        }}

        /* ═══════════════ EDIT BUTTONS ═══════════════ */ 
        .edit-btn {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: var(--t-green);
            color: white;
            border: none;
            border-radius: 50%;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            opacity: 0;
            transition: all 0.3s;
            z-index: 100;
        }}
        .edit-btn:hover {{
            background: var(--t-gold);
            color: var(--t-green);
            transform: scale(1.1);
        }}
        .hero-section:hover .edit-btn,
        .feature-card:hover .edit-btn,
        .creator-card:hover .edit-btn {{
            opacity: 1;
        }}
        .section-wrapper {{
            position: relative;
        }}
        .team-edit-btn {{
            top: 8px;
            right: 8px;
            width: 30px;
            height: 30px;
            font-size: 0.8rem;
        }}

        /* ═══════════════ MODAL STYLES ═══════════════ */
        .edit-modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 9999;
            align-items: center;
            justify-content: center;
        }}
        .edit-modal.active {{
            display: flex;
        }}
        .modal-content {{
            background: white;
            border-radius: var(--radius);
            padding: 30px;
            max-width: 500px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
        }}
        .modal-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid var(--t-gold);
        }}
        .modal-header h3 {{
            margin: 0;
            color: var(--t-green);
            font-size: 1.3rem;
        }}
        .modal-close {{
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #999;
        }}
        .modal-close:hover {{
            color: var(--t-green);
        }}
        .form-group {{
            margin-bottom: 18px;
        }}
        .form-group label {{
            display: block;
            margin-bottom: 6px;
            font-weight: 600;
            color: var(--t-green);
            font-size: 0.9rem;
        }}
        .form-group input,
        .form-group textarea,
        .form-group select {{
            width: 100%;
            padding: 12px 14px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 0.95rem;
            transition: border-color 0.3s;
        }}
        .form-group input:focus,
        .form-group textarea:focus,
        .form-group select:focus {{
            outline: none;
            border-color: var(--t-gold);
        }}
        .form-group textarea {{
            resize: vertical;
            min-height: 100px;
        }}
        .btn-save {{
            background: var(--t-green);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s;
        }}
        .btn-save:hover {{
            background: #004a3d;
            transform: translateY(-2px);
        }}

        /* ═══════════════ HERO ═══════════════ */
        .hero-section {{
            background: var(--t-green);
            background-image:
                radial-gradient(circle at 20% 80%, rgba(177,211,203,0.06) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255,255,255,0.03) 0%, transparent 50%),
                linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
            background-size: 100%, 100%, 24px 24px, 24px 24px;
            padding: 100px 0 140px;
            color: white;
            position: relative;
            overflow: hidden;
        }}

        .hero-section::after {{
            content: '';
            position: absolute;
            bottom: -60px; left: 0; right: 0;
            height: 120px;
            background: #e8f3f1;
            border-radius: 50% 50% 0 0 / 100% 100% 0 0;
        }}

        .hero-content {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 0 40px;
            text-align: left;
            position: relative;
            z-index: 1;
        }}

        .home-btn {{
            color: var(--t-gold);
            text-decoration: none;
            font-size: 0.82rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 32px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            padding: 8px 18px;
            border: 1px solid rgba(177,211,203,0.25);
            border-radius: 30px;
            transition: all 0.3s;
            backdrop-filter: blur(4px);
            background: rgba(177,211,203,0.06);
        }}
        .home-btn:hover {{
            color: white;
            transform: translateX(-5px);
            background: rgba(255,255,255,0.08);
            border-color: rgba(255,255,255,0.2);
        }}

        .hero-section h1 {{
            font-size: 3.8rem;
            margin: 0;
            line-height: 1.05;
            letter-spacing: -1px;
            font-weight: 700;
        }}

        .title-line {{
            width: 70px;
            height: 4px;
            background: linear-gradient(90deg, var(--t-gold), rgba(177,211,203,0.3));
            margin: 28px 0;
            border-radius: 4px;
        }}

        .hero-section p {{
            font-weight: 300;
            font-size: 1.08rem;
            opacity: 0.7;
            max-width: 480px;
            line-height: 1.7;
        }}

        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(177,211,203,0.1);
            border: 1px solid rgba(177,211,203,0.2);
            color: var(--t-gold);
            padding: 6px 16px;
            border-radius: 30px;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-top: 18px;
        }}

        /* ═══════════════ MAIN CONTENT ═══════════════ */
        .container-custom {{
            max-width: 1000px;
            margin: -60px auto 80px;
            padding: 0 20px;
            position: relative;
            z-index: 10;
        }}

        .feature-card {{
            background: white;
            border-radius: var(--radius);
            padding: 0;
            box-shadow: 0 20px 60px rgba(0,0,0,0.08);
            border: 1px solid rgba(0,0,0,0.04);
            overflow: hidden;
            position: relative;
        }}

        .feature-card-header {{
            background: linear-gradient(135deg, #eef6f4, #e8f0ed);
            padding: 32px 50px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 3px solid var(--t-gold);
        }}

        .feature-card-header h2 {{
            color: var(--t-green);
            font-weight: 700;
            margin: 0;
            font-size: 1.4rem;
        }}

        .feature-card-header .tag {{
            background: var(--t-green);
            color: rgba(255,255,255,0.8);
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 1px;
        }}

        .feature-body {{
            padding: 50px;
        }}

        .feature-text p {{
            margin-bottom: 22px;
            text-align: justify;
            color: #555;
            font-size: 1.02rem;
            line-height: 1.85;
        }}

        .feature-text strong {{
            color: var(--t-green);
        }}

        /* ─── Feature highlights ─── */
        .feature-highlights {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-top: 32px;
            padding-top: 28px;
            border-top: 1px solid #eee;
        }}

        .feature-highlight-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 14px 16px;
            background: #fafaf8;
            border-radius: 12px;
            border: 1px solid rgba(0,0,0,0.04);
            transition: all 0.2s;
        }}

        .feature-highlight-item:hover {{
            background: white;
            box-shadow: var(--shadow-sm);
            transform: translateY(-2px);
        }}

        .fhi-icon {{
            width: 38px; height: 38px;
            background: linear-gradient(135deg, #eef6f4, #d8ebe5);
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            color: var(--t-green);
            font-size: 1rem;
            flex-shrink: 0;
        }}

        .fhi-label {{
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--t-green);
        }}

        @media (max-width: 768px) {{
            .feature-highlights {{
                grid-template-columns: 1fr;
            }}
        }}

        /* ═══════════════ TEAM ═══════════════ */
        .team-section {{ margin-top: 80px; }}

        .team-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 40px;
        }}

        .team-title {{
            color: var(--t-green);
            font-size: 2rem;
            font-weight: 700;
            margin: 0;
        }}

        .team-subtitle {{
            color: #999;
            font-size: 0.85rem;
            font-weight: 500;
        }}

        .creator-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 20px;
        }}

        .creator-card {{
            background: white;
            padding: 36px 20px 30px;
            text-align: center;
            border-radius: var(--radius);
            border: 1px solid rgba(0,0,0,0.04);
            box-shadow: var(--shadow-sm);
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }}

        .creator-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--t-green), var(--t-gold));
            opacity: 0;
            transition: opacity 0.3s;
        }}

        .creator-card:hover {{
            box-shadow: 0 15px 40px rgba(0,0,0,0.08);
            transform: translateY(-6px);
        }}

        .creator-card:hover::before {{ opacity: 1; }}

        .creator-img-wrap {{
            width: 110px; height: 110px;
            margin: 0 auto 18px;
            border-radius: 50%;
            overflow: hidden;
            border: 3px solid #f0f0f0;
            transition: all 0.3s;
            position: relative;
        }}

        .creator-card:hover .creator-img-wrap {{
            border-color: var(--t-gold);
            box-shadow: 0 0 0 4px rgba(177,211,203,0.15);
        }}

        .creator-img {{
            width: 100%; height: 100%;
            object-fit: cover;
            transition: filter 0.4s;
        }}

        .creator-card:hover .creator-img {{ filter: grayscale(0%); }}

        .name {{
            font-weight: 700;
            font-size: 1.05rem;
            color: var(--t-green);
            font-family: 'Inter', san-serif;
        }}

        .role {{
            font-size: 0.72rem;
            color: #bbb;
            text-transform: uppercase;
            margin-top: 6px;
            letter-spacing: 1.5px;
            font-weight: 600;
        }}

        /* ═══════════════ FOOTER ═══════════════ */
        .page-footer {{
            text-align: center;
            padding: 40px 20px 50px;
            color: #bbb;
            font-size: 0.8rem;
        }}

        .page-footer a {{
            color: var(--t-green);
            text-decoration: none;
            font-weight: 600;
        }}

        /* ═══════════════ ANIMATIONS ═══════════════ */
        @keyframes fadeUp {{
            from {{ opacity: 0; transform: translateY(25px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .hero-content {{ animation: fadeUp 0.7s ease-out; }}
        .feature-card {{ animation: fadeUp 0.7s ease-out 0.15s both; }}
        .team-section {{ animation: fadeUp 0.7s ease-out 0.25s both; }}
    </style>
</head>
<body>

    <!-- ═══════════════ HERO ═══════════════ -->
    <section class="hero-section section-wrapper">
        <button type="button" class="edit-btn" onclick="openHeroModal()" style="top: 20px; right: 20px;">
            <i class="bi bi-pencil"></i>
        </button>
        <div class="hero-content">
        <a href="/main?username={quote(username)}" class="home-btn">
            <i class="bi bi-arrow-left"></i> Back to Dashboard
        </a>
        <h1>{html.escape(hero_data['title'])}</h1>
            <div class="title-line"></div>
            <p>{html.escape(hero_data['description'])}</p>
            <div class="hero-badge">
                <i class="bi bi-flask"></i> {html.escape(hero_data['badge_text'])}
            </div>
        </div>
    </section>

    <!-- ═══════════════ PROJECT SCOPE ═══════════════ -->
    <div class="container-custom">
        <div class="feature-card section-wrapper">
            <button type="button" class="edit-btn" onclick="openProjectModal()">
                <i class="bi bi-pencil"></i>
            </button>
            <div class="feature-card-header">
                <h2>{html.escape(project_data['header_title'])}</h2>
                <span class="tag">{html.escape(project_data['header_tag'])}</span>
            </div>
            <div class="feature-body">
                <div class="feature-text">
                    <p>{html.escape(project_data['paragraph1'])}</p>
                    <p>{html.escape(project_data['paragraph2'])}</p>
                    <p>{html.escape(project_data['paragraph3'])}</p>
                </div>

                <div class="feature-highlights">
                    <div class="feature-highlight-item">
                        <div class="fhi-icon"><i class="bi bi-database"></i></div>
                        <span class="fhi-label">MySQL Database</span>
                    </div>
                    <div class="feature-highlight-item">
                        <div class="fhi-icon"><i class="bi bi-shield-lock"></i></div>
                        <span class="fhi-label">Secure Authentication</span>
                    </div>
                    <div class="feature-highlight-item">
                        <div class="fhi-icon"><i class="bi bi-bar-chart"></i></div>
                        <span class="fhi-label">Graph Analytics</span>
                    </div>
                    <div class="feature-highlight-item">
                        <div class="fhi-icon"><i class="bi bi-search"></i></div>
                        <span class="fhi-label">Search & Filter</span>
                    </div>
                    <div class="feature-highlight-item">
                        <div class="fhi-icon"><i class="bi bi-sort-alpha-down"></i></div>
                        <span class="fhi-label">Sorting Algorithm</span>
                    </div>
                    <div class="feature-highlight-item">
                        <div class="fhi-icon"><i class="bi bi-download"></i></div>
                        <span class="fhi-label">Data Export</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- ═══════════════ TEAM ═══════════════ -->
        <div class="team-section">
            <div class="team-header">
                <div>
                    <h2 class="team-title">Our Team</h2>
                    <p class="team-subtitle">Website Designers & Developers</p>
                </div>
            </div>
            <div class="creator-grid">
                {team_cards_html}
            </div>
        </div>
    </div>

    <!-- ═══════════════ FOOTER ═══════════════ -->
    <div class="page-footer">
        <p>TEMP &copy; 2026 &middot; Powered by Python http.server & MySQL • Bootstrap 5</p>
    </div>

    <!-- ═══════════════ EDIT MODALS ═══════════════ -->
    <!-- Hero Edit Modal -->
    <div id="heroModal" class="edit-modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Edit Hero Section</h3>
                <button class="modal-close" onclick="closeModal('heroModal')">&times;</button>
            </div>
            <form method="post" action="/about">
                <input type="hidden" name="action" value="update_hero">
                <input type="hidden" name="username" value="{html.escape(username)}">
                <div class="form-group">
                    <label>Title</label>
                    <input type="text" name="hero_title" value="{html.escape(hero_data['title'])}" required>
                </div>
                <div class="form-group">
                    <label>Description</label>
                    <textarea name="hero_description" rows="4" required>{html.escape(hero_data['description'])}</textarea>
                </div>
                <div class="form-group">
                    <label>Badge Text</label>
                    <input type="text" name="hero_badge" value="{html.escape(hero_data['badge_text'])}">
                </div>
                <button type="submit" class="btn-save">Save Changes</button>
            </form>
        </div>
    </div>

    <!-- Project Edit Modal -->
    <div id="projectModal" class="edit-modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Edit Project Section</h3>
                <button class="modal-close" onclick="closeModal('projectModal')">&times;</button>
            </div>
            <form method="post" action="/about">
                <input type="hidden" name="action" value="update_project">
                <input type="hidden" name="username" value="{html.escape(username)}">
                <div class="form-group">
                    <label>Section Title</label>
                    <input type="text" name="project_title" value="{html.escape(project_data['header_title'])}" required>
                </div>
                <div class="form-group">
                    <label>Tag Text</label>
                    <input type="text" name="project_tag" value="{html.escape(project_data['header_tag'])}">
                </div>
                <div class="form-group">
                    <label>Paragraph 1</label>
                    <textarea name="project_p1" rows="3" required>{html.escape(project_data['paragraph1'])}</textarea>
                </div>
                <div class="form-group">
                    <label>Paragraph 2</label>
                    <textarea name="project_p2" rows="3" required>{html.escape(project_data['paragraph2'])}</textarea>
                </div>
                <div class="form-group">
                    <label>Paragraph 3</label>
                    <textarea name="project_p3" rows="3" required>{html.escape(project_data['paragraph3'])}</textarea>
                </div>
                <button type="submit" class="btn-save">Save Changes</button>
            </form>
        </div>
    </div>

    <!-- Team Member Edit Modal -->
    <div id="teamModal" class="edit-modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Edit Team Member</h3>
                <button class="modal-close" onclick="closeModal('teamModal')">&times;</button>
            </div>
            <form method="post" action="/about" id="teamEditForm">
                <input type="hidden" name="action" value="update_team">
                <input type="hidden" name="username" value="{html.escape(username)}">
                <input type="hidden" name="member_id" id="teamMemberId">
                
                <div class="form-group">
                    <label>Name</label>
                    <input type="text" name="member_name" id="teamMemberName" required>
                </div>
                <div class="form-group">
                    <label>Role</label>
                    <input type="text" name="member_role" id="teamMemberRole" required>
                </div>
                <div class="form-group">
                    <label>Upload Photo from System</label>
                    <input type="file" id="imagePicker" accept="image/*" class="form-control" style="margin-bottom:10px;">
                    <input type="hidden" name="member_image" id="teamMemberImage">
                </div>
                <button type="submit" class="btn-save">Save Changes</button>
            </form>
        </div>
    </div>

    <script>
        function openHeroModal() {{ document.getElementById('heroModal').classList.add('active'); }}
        function openProjectModal() {{ document.getElementById('projectModal').classList.add('active'); }}
        
        function openTeamModal(id, name, role, image) {{
            document.getElementById('teamMemberId').value = id;
            document.getElementById('teamMemberName').value = name;
            document.getElementById('teamMemberRole').value = role;
            document.getElementById('teamMemberImage').value = image;
            document.getElementById('imagePicker').value = ""; // Reset file picker
            document.getElementById('teamModal').classList.add('active');
        }}

        // Handle the "Insert from System" and Resize logic
        document.getElementById('teamEditForm').addEventListener('submit', function(e) {{
            const fileInput = document.getElementById('imagePicker');
            const hiddenInput = document.getElementById('teamMemberImage');
            
            // If a new file was selected from the desktop
            if (fileInput.files && fileInput.files[0]) {{
                e.preventDefault(); // Pause submission to compress image
                
                const reader = new FileReader();
                reader.onload = function(event) {{
                    const img = new Image();
                    img.src = event.target.result;
                    img.onload = function() {{
                        // Create a canvas to resize the image (Prevents 'max_allowed_packet' error)
                        const canvas = document.createElement('canvas');
                        const MAX_WIDTH = 400; // Profile image width
                        const scale = MAX_WIDTH / img.width;
                        canvas.width = MAX_WIDTH;
                        canvas.height = img.height * scale;

                        const ctx = canvas.getContext('2d');
                        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                        
                        // Convert to smaller Base64 and submit
                        hiddenInput.value = canvas.toDataURL('image/jpeg', 0.8);
                        document.getElementById('teamEditForm').submit();
                    }};
                }};
                reader.readAsDataURL(fileInput.files[0]);
            }}
        }});

        function closeModal(modalId) {{ document.getElementById(modalId).classList.remove('active'); }}
        
        document.querySelectorAll('.edit-modal').forEach(modal => {{
            modal.addEventListener('click', function(e) {{ if (e.target === this) this.classList.remove('active'); }});
        }});
        
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') {{
                document.querySelectorAll('.edit-modal.active').forEach(modal => {{ modal.classList.remove('active'); }});
            }}
        }});
    </script>

</body>
</html>"""
    return page

# ----------ADMIN LOGIN PAGE ---------- #Christina, Sana, Seyoung & Abarnna
#All: Create Database, Layout
#Christina: Footer
#Sana: Updating header title and logo
#Abarnna: Password Eye icon
#Seyoung: Logo design and Button design

def render_admin_login_page(message="", error=""):
    curr_title, curr_logo = header_data_temp()
    print(f"DEBUG CHECK: Title is '{curr_title}', Logo path is '{curr_logo}'")
    # to check if the changed title and logo is seen on the wepage
    
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Admin Login – TEMP</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400&display=swap');
  *{{ box-sizing: border-box; }}

  @keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(25px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}
  @keyframes slideInRight {{
    from {{ opacity: 0; transform: translateX(40px); }}
    to {{ opacity: 1; transform: translateX(0); }}
  }}
  @keyframes float {{
    0%,100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-8px); }}
  }}
  @keyframes pulse-glow {{
    0%,100% {{ filter: drop-shadow(0 0 12px rgba(177,211,203,0.4)); }}
    50% {{ filter: drop-shadow(0 0 25px rgba(177,211,203,0.7)); }}
  }}

  body, html {{ height: 100%; margin: 0; font-family: 'Inter', sans-serif; overflow: hidden; background-color: #002c23; }}

  /* ─── Navbar ─── */
  .navbar-custom {{
    position: absolute; top: 0; width: 100%; z-index: 1000;
    padding: 18px 30px;
    display: flex; align-items: center; gap: 12px;
    background: linear-gradient(180deg, rgba(0,26,21,0.6) 0%, transparent 100%);
  }}
  .navbar-custom img {{ width: 32px; filter: drop-shadow(0 0 6px rgba(177,211,203,0.3)); }}
  .navbar-custom span {{
    color: #b1d3cb; font-weight: 700; font-size: 1.05rem;
    font-family: 'Outfit', sans-serif; letter-spacing: 0.5px;
  }}

  /* ─── Split Layout ─── */
  .split-container {{ display: flex; height: 100vh; width: 100%; }}

  .image-side {{
    flex: 1.3;
    background-image: url("images/bg.jpg");
    background-size: cover; background-position: center;
    position: relative; display: flex; align-items: flex-end; padding: 70px;
  }}
  .image-overlay {{
    position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(0,44,35,0.7) 0%, rgba(0,44,35,0.2) 50%, transparent 100%);
  }}

  /* ─── Form Panel ─── */
  .form-side-panel {{
    flex: 0.7;
    background: linear-gradient(165deg, rgba(0,44,35,0.92) 0%, rgba(0,26,21,0.97) 100%);
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    padding: 60px; position: relative; overflow: hidden;
    animation: slideInRight 0.7s ease-out;
  }}
  .form-side-panel::before {{
    content: ''; position: absolute; top: -50%; right: -50%;
    width: 100%; height: 100%;
    background: radial-gradient(circle, rgba(177,211,203,0.04) 0%, transparent 70%);
    pointer-events: none;
  }}

  .login-content {{ width: 100%; max-width: 340px; color: white; position: relative; z-index: 2; }}

  .glowing-logo {{
    width: 100px; margin-bottom: 20px;
    animation: pulse-glow 3s ease-in-out infinite, float 4s ease-in-out infinite;
  }}

  .form-subtitle {{
    font-size: 0.85rem; opacity: 0.5; margin-bottom: 32px;
    letter-spacing: 0.3px;
  }}

  /* ─── Inputs ─── */
  .input-wrapper {{ position: relative; margin-bottom: 22px; }}
  .input-wrapper label {{
    display: block; font-size: 0.72rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 1.5px;
    color: rgba(177,211,203,0.7); margin-bottom: 8px;
  }}
  .input-wrapper .form-control {{
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(177,211,203,0.15) !important;
    color: #fff !important; padding: 13px 16px;
    border-radius: 10px; font-size: 0.92rem;
    transition: all 0.3s ease;
  }}
  .input-wrapper .form-control:focus {{
    background: rgba(255,255,255,0.1) !important;
    border-color: rgba(177,211,203,0.45) !important;
    box-shadow: 0 0 0 3px rgba(177,211,203,0.08) !important;
  }}
  .input-wrapper .form-control::placeholder {{ color: rgba(255,255,255,0.2); }}

  .eye-btn {{
    position: absolute; right: 12px; bottom: 10px;
    background: none !important; border: none !important;
    color: rgba(177,211,203,0.6) !important; cursor: pointer;
    transition: color 0.2s;
  }}
  .eye-btn:hover {{ color: #b1d3cb !important; }}

  /* ─── Button ─── */
  .login-btn {{
    background: linear-gradient(135deg, #b1d3cb 0%, #8fbdaf 100%);
    color: #002c23; font-weight: 700; border: none;
    padding: 14px; border-radius: 12px; font-size: 0.95rem;
    letter-spacing: 0.5px; transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(177,211,203,0.25);
    margin-top: 8px;
  }}
  .login-btn:hover {{
    background: linear-gradient(135deg, #d4ece5 0%, #b1d3cb 100%);
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(177,211,203,0.35);
    color: #002c23;
  }}
  .login-btn:active {{ transform: translateY(0); }}

    /* ═══════════════════ AUTH FOOTER (LOGIN) ═══════════════════ */
  .auth-footer {{
    position: fixed;
    bottom: 20px;
    right: 85px;

    font-family: "Inter", sans-serif;
    font-size: 0.85rem;
    font-weight: 400;
    letter-spacing: 0.3px;

    color: rgba(255, 255, 255, 0.3);

    z-index: 9999;   
  }}

  /* ─── Links ─── */
  .bottom-links {{ 
    margin-top: 30px; 
    text-align: center; 
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }}
  .register-link {{
    color: #b1d3cb; text-decoration: none; font-weight: 600;
    font-size: 0.95rem; transition: 0.2s;
    border-bottom: 1px solid transparent;
  }}
  .register-link:hover {{ border-bottom-color: #b1d3cb; color: #fff; }}

  /* ─── Divider ─── */
  .divider {{
    display: flex; align-items: center; gap: 14px;
    width: 100%; opacity: 0.3;
  }}
  .divider::before, .divider::after {{
    content: ''; flex: 1; height: 1px; background: #b1d3cb;
  }}
  .divider span {{ font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; color: #fff; }}

  /* ─── Alerts ─── */
  .alert {{ border-radius: 10px; font-size: 0.85rem; border: none; }}

  @media (max-width: 992px) {{
    .image-side {{ display: none; }}
    .form-side-panel {{
      flex: 1;
      background: #002c23;
    }}
  }}
</style>
</head>

<div class="auth-footer">
    TEMP &copy; 2026 &middot; Powered by Python http.server & MySQL • Bootstrap 5
</div>

<body>

<nav class="navbar-custom">
    <img src="{curr_logo}" style="width:35px; margin-right:8px;" onerror="this.style.display='none'">
    <span style="color:#b1d3cb; font-weight:700; font-family:'Outfit', serif;">{curr_title}</span>
</nav>

<div class="split-container">
  <div class="image-side">
    <div class="image-overlay"></div>
  </div>

  <div class="form-side-panel">
    <div class="login-content text-center">
      <img src="images/Login.png" class="glowing-logo" alt="TEMP Logo">
      <h4 style="font-weight:700; margin-bottom:4px; font-family:'Inter',sans-serif; color:#b1d3cb; font-size:1.6rem;">
        Admin Login - TEMP
      </h4>
      <p class="form-subtitle">Access your laboratory workspace</p>

      {error}
      {message}

      <form method="post" class="text-start">
        <input type="hidden" name="action" value="login">

        <div class="input-wrapper">
          <label>Username_temp</label>
          <input type="text" name="username_temp" class="form-control" placeholder="Enter your username_temp" required autocomplete="username">
        </div>

        <div class="input-wrapper" style="position:relative;">
          <label>Password_temp</label>
          <input type="password" name="password_temp" id="loginPassword" class="form-control" placeholder="Enter your password_temp" required autocomplete="current-password">
          <button class="eye-btn" type="button" onclick="togglePassword('loginPassword', this)">
            <i class="bi bi-eye-slash" style="font-size:1.1rem;"></i>
          </button>
        </div>

        <button type="submit" class="btn login-btn w-100">LOGIN</button>
      </form>
      
      <div class="bottom-links">
        <div class="divider"><span>Don't have an account?</span></div>
        <a href="/signup" class="register-link">Register here &rarr;</a>
      </div>
    </div>
  </div>
</div>

<script>
function togglePassword(inputId, btn) {{
    const input = document.getElementById(inputId);
    const icon = btn.querySelector("i");
    if (input.type === "password") {{
        input.type = "text";
        icon.classList.replace("bi-eye-slash", "bi-eye");
    }} else {{
        input.type = "password";
        icon.classList.replace("bi-eye", "bi-eye-slash");
    }}
}}
</script>

</body>
</html>"""
    return page

# ---------- ADMIN SIGNUP PAGE ---------- #Christina, Sana, Seyoung & Abarnna
#All: Create Database, Layout
#Christina: Footer, Unique Password Characters
#Sana: Updating header title and logo
#Abarnna: Password Eye icon
#Seyoung: Logo design and Button design

def render_signup_page(message="", error=""):
    curr_title, curr_logo = header_data_temp()
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Admin Signup – TEMP</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400&display=swap');
  * {{ box-sizing: border-box; }}

  @keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(25px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}
  @keyframes slideInRight {{
    from {{ opacity: 0; transform: translateX(40px); }}
    to {{ opacity: 1; transform: translateX(0); }}
  }}
  @keyframes float {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-8px); }}
  }}
  @keyframes pulse-glow {{
    0%,100% {{ filter: drop-shadow(0 0 12px rgba(177,211,203,0.4)); }}
    50% {{ filter: drop-shadow(0 0 25px rgba(177,211,203,0.7)); }}
  }}

  body, html {{ height: 100%; margin: 0; font-family: 'Inter', sans-serif; overflow: hidden; background-color: #002c23; }}

  /* ─── Navbar ─── */
  .navbar-custom {{
    position: absolute; top: 0; width: 100%; z-index: 1000;
    padding: 18px 30px;
    display: flex; align-items: center; gap: 12px;
    background: linear-gradient(180deg, rgba(0,26,21,0.6) 0%, transparent 100%);
  }}
  .navbar-custom img {{ width: 32px; filter: drop-shadow(0 0 6px rgba(177,211,203,0.3)); }}
  .navbar-custom span {{
    color: #b1d3cb; font-weight: 700; font-size: 1.05rem;
    font-family: 'Outfit', sans-serif; letter-spacing: 0.5px;
  }}

  /* ─── Split Layout ─── */
  .split-container {{ display: flex; height: 100vh; width: 100%; }}

  .image-side {{
    flex: 1.3;
    background-image: url("images/bg.jpg");
    background-size: cover; background-position: center;
    position: relative; display: flex; align-items: flex-end; padding: 70px;
  }}
  .image-overlay {{
    position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(0,44,35,0.7) 0%, rgba(0,44,35,0.2) 50%, transparent 100%);
  }}


  /* ─── Form Panel ─── */
  .form-side-panel {{
    flex: 0.7;
    background: linear-gradient(165deg, rgba(0,44,35,0.92) 0%, rgba(0,26,21,0.97) 100%);
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    padding: 40px 55px; position: relative; overflow: hidden;
    animation: slideInRight 0.7s ease-out;
  }}

  .signup-content {{ width: 100%; max-width: 340px; color: white; position: relative; z-index: 2; }}

  .glowing-logo {{
    width: 80px; margin-bottom: 12px;
    animation: pulse-glow 3s ease-in-out infinite, float 4s ease-in-out infinite;
  }}

  .form-subtitle {{
    font-size: 0.82rem; opacity: 0.5; margin-bottom: 24px;
    letter-spacing: 0.3px;
  }}

  /* ─── Inputs ─── */
  .input-wrapper {{ position: relative; margin-bottom: 16px; }}
  .input-wrapper label {{
    display: block; font-size: 0.7rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 1.5px;
    color: rgba(177,211,203,0.7); margin-bottom: 6px;
  }}
  .input-wrapper .form-control {{
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(177,211,203,0.15) !important;
    color: #fff !important; padding: 12px 14px;
    border-radius: 10px; font-size: 0.9rem;
    transition: all 0.3s ease;
  }}
  .input-wrapper .form-control:focus {{
    background: rgba(255,255,255,0.1) !important;
    border-color: rgba(177,211,203,0.45) !important;
    box-shadow: 0 0 0 3px rgba(177,211,203,0.08) !important;
  }}
  
  /* --- Fixed Placeholder Color here --- */
  .input-wrapper .form-control::placeholder {{ color: rgba(255,255,255,0.2) !important; }}

  .eye-btn {{
    position: absolute; 
    right: 10px; 
    /* Changed from bottom to top with a transform to stay centered on the input */
    top: 36px; 
    background: none !important; border: none !important;
    color: rgba(177,211,203,0.6) !important; cursor: pointer;
    transition: color 0.2s;
    z-index: 10;
    padding: 0;
  }}
  .eye-btn:hover {{ color: #b1d3cb !important; }}

  /* Add this to prevent text from going under the icon */
  .input-wrapper input[type="password"],
  .input-wrapper input[type="text"] {{
    padding-right: 40px !important;
  }}

  /* ─── Strength Meter ─── */
  .strength-meter {{
    height: 4px; width: 100%;
    background: rgba(255,255,255,0.08);
    margin-top: 8px; border-radius: 4px;
    overflow: hidden; display: flex;
  }}
  .strength-bar {{
    height: 100%; width: 0%;
    transition: width 0.4s ease, background-color 0.4s ease;
    border-radius: 4px;
  }}
  .requirement-list {{
    font-size: 0.68rem; text-align: left;
    margin-top: 10px; padding-left: 0;
    list-style: none; columns: 2; gap: 6px;
  }}
  .req-item {{
    color: rgba(255,255,255,0.3); transition: 0.3s;
    margin-bottom: 4px; display: flex; align-items: center; gap: 5px;
  }}
  .req-item.met {{ color: #b1d3cb; }}

  /* ─── Button ─── */
  .register-btn {{
    background: linear-gradient(135deg, #b1d3cb 0%, #8fbdaf 100%);
    color: #002c23; font-weight: 700; border: none;
    padding: 13px; border-radius: 12px; font-size: 0.95rem;
    letter-spacing: 0.5px; transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(177,211,203,0.25);
    margin-top: 6px;
  }}
  .register-btn:hover {{
    background: linear-gradient(135deg, #d4ece5 0%, #b1d3cb 100%);
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(177,211,203,0.35);
    color: #002c23;
  }}

    /* ═══════════════════ AUTH FOOTER (SIGNUP) ═══════════════════ */
  .auth-footer {{
    position: fixed;
    bottom: 20px;
    right: 85px;

    font-family: "Inter", sans-serif;
    font-size: 0.85rem;
    font-weight: 400;
    letter-spacing: 0.3px;

    color: rgba(255, 255, 255, 0.3);

    z-index: 9999;   
  }}

  /* ─── Links ─── */
  .back-link {{
    display: inline-flex; align-items: center; gap: 6px; margin-top: 24px;
    color: rgba(177,211,203,0.8); text-decoration: none;
    font-size: 0.9rem; font-weight: 500; transition: 0.2s;
    border-bottom: 1px solid transparent;
  }}
  .back-link:hover {{ color: #b1d3cb; border-bottom-color: #b1d3cb; }}

  @media (max-width: 992px) {{
    .image-side {{ display: none; }}
    .form-side-panel {{
      flex: 1; padding: 40px 30px;
      background: #002c23;
    }}
  }}
</style>
</head>

<div class="auth-footer">
    TEMP &copy; 2026 &middot; Powered by Python http.server & MySQL • Bootstrap 5
</div>

<body>

<nav class="navbar-custom">
    <img src="{curr_logo}" style="width:35px; margin-right:8px;" onerror="this.style.display='none'">
    <span style="color:#b1d3cb; font-weight:700; font-family:'Outfit', sans-serif;">{curr_title}</span>
</nav>

<div class="split-container">
  <div class="image-side">
    <div class="image-overlay"></div>
  </div>

  <div class="form-side-panel">
    <div class="signup-content text-center">
      <img src="images/Login.png" class="glowing-logo" alt="TEMP Logo">
      <h4 style="color:#b1d3cb; font-weight:700; margin-bottom:4px; font-family:'Inter',sans-serif; font-size:1.5rem;">
        Join the Admin Lab
      </h4>
      <p class="form-subtitle">Set up your laboratory credentials</p>

      {error}
      {message}

      <form method="post" class="text-start">
        <input type="hidden" name="action" value="signup">

        <div class="input-wrapper">
          <label>Full Name_temp</label>
          <input type="text" name="full_name_temp" class="form-control" placeholder="Enter your full name_temp" required>
        </div>

        <div class="input-wrapper">
          <label>Username_temp</label>
          <input type="text" name="username_temp" class="form-control" placeholder="Create a username_temp" required>
        </div>

        <div class="input-wrapper" style="position:relative;">
          <label>Password_temp</label>
          <input type="password" name="password_temp" id="signupPassword" class="form-control" placeholder="Create a password_temp" required oninput="checkStrength(this.value)">
          <button class="eye-btn" type="button" onclick="togglePassword('signupPassword', this)">
            <i class="bi bi-eye-slash" style="font-size:1.05rem;"></i>
          </button>

          <div class="strength-meter">
            <div id="strength-bar" class="strength-bar"></div>
          </div>

          <ul class="requirement-list">
            <li id="req-len" class="req-item"><i class="bi bi-circle" style="font-size:0.55rem;"></i> 8+ Characters</li>
            <li id="req-num" class="req-item"><i class="bi bi-circle" style="font-size:0.55rem;"></i> 1+ Number</li>
            <li id="req-cap" class="req-item"><i class="bi bi-circle" style="font-size:0.55rem;"></i> 1+ Capital</li>
            <li id="req-sym" class="req-item"><i class="bi bi-circle" style="font-size:0.55rem;"></i> 1+ Symbol</li>
          </ul>
        </div>

        <div class="input-wrapper" style="position:relative;">
          <label>Confirm Password_temp</label>
          <input type="password" name="confirm_password_temp" id="ConfirmPassword" class="form-control" placeholder="Re-enter your password_temp" required>
          <button class="eye-btn" type="button" onclick="togglePassword('ConfirmPassword', this)">
            <i class="bi bi-eye-slash" style="font-size:1.05rem;"></i>
          </button>
        </div>

        <button type="submit" id="submitBtn" class="btn register-btn w-100">JOIN THE ADMIN LAB</button>
      </form>

      <a href="/" class="back-link">
        <i class="bi bi-arrow-left"></i> Back to Login
      </a>
    </div>
  </div>
</div>

<script>
function togglePassword(inputId, btn) {{
    const input = document.getElementById(inputId);
    const icon = btn.querySelector("i");
    if (input.type === "password") {{
        input.type = "text";
        icon.classList.replace("bi-eye-slash", "bi-eye");
    }} else {{
        input.type = "password";
        icon.classList.replace("bi-eye", "bi-eye-slash");
    }}
}}

function checkStrength(pw) {{
    let strength = 0;
    const bar = document.getElementById('strength-bar');

    const requirements = {{
        "req-len": pw.length >= 8,
        "req-num": /[0-9]/.test(pw),
        "req-cap": /[A-Z]/.test(pw),
        "req-sym": /[^A-Za-z0-9]/.test(pw)
    }};

    for (const [id, met] of Object.entries(requirements)) {{
        const el = document.getElementById(id);
        if (met) {{
            strength++;
            el.classList.add('met');
            el.querySelector('i').classList.replace('bi-circle', 'bi-check-circle-fill');
        }} else {{
            el.classList.remove('met');
            el.querySelector('i').classList.replace('bi-check-circle-fill', 'bi-circle');
        }}
    }}

    const colors = ['#ef4444', '#f59e0b', '#22c55e', '#b1d3cb'];
    bar.style.width = (strength * 25) + '%';
    bar.style.backgroundColor = strength > 0 ? colors[strength - 1] : 'transparent';
}}
</script>

</body>
</html>"""
    return page

# ============================================================================
# MAIN PAGE RENDERER
# ============================================================================

# ---------- COLUMN INDEX MAP ----------
COLUMN_INDEX_MAP = {
    "date_temp": 0,
    "titration_id_temp": 1,
    "standard_solution_name_temp": 2,
    "titrant_solution_name_temp": 3,
}

# ---------- HIGHLIGHT ITEM (highlights the searched item in the table) ---------- #Seyoung
def highlight(text, col_index, search_column=None, search_value=None):
    escaped = html.escape(str(text))
    if search_column is not None and search_value:
        if COLUMN_INDEX_MAP.get(search_column) == col_index:
            pattern = re.compile(re.escape(html.escape(search_value)), re.IGNORECASE)
            return pattern.sub(
                lambda m: f"<span class='highlight'>{m.group(0)}</span>",
                escaped
            )
    return escaped
# ---------- Render Main Page #Christina, Sana, Seyoung & Abarnna
#All: Create Database, Layout
#Christina: Footer, About us, Dash Board, User Icon, edit header data
#Sana: Add, Sort, Graph, Delete, Logout Button, edit header data
#Seyoung: Table, Mobile view, Search, Sidebar, About us, Header
#Abarnna: Load/update, About us, Dashboard

def render_main_page(
    username="",
    message="",
    error="",
    show_add_form=False,
    show_delete_form=False,
    form_data=None,
    search_column=None,
    search_value=None,
    search_rows=None,
    show_graph_form=False,
    show_load_form=False,
    show_header_form=False,
    load_record_data=None
):
    curr_title, curr_logo = header_data_temp()
    today = date.today().strftime('%Y-%m-%d')
    if form_data is None:
        form_data = {}

    username = html.escape(username)

    selected_sort = form_data.get("sort_column", "")
    selected_order = form_data.get("sort_order", "asc")

    try:
        if search_rows is not None:
            rows = search_rows
        else:
            rows = get_experiments()

        # -------- SORTING (Bubble Sort) -------- #Sana
        if form_data and "sort_column" in form_data:
            sort_column = form_data.get("sort_column")
            sort_order = form_data.get("sort_order", "asc")

            column_map = {
                "date": 0,
                "standard": 2,
                "titrant": 3,
                "average": 7
            }

            if sort_column in column_map:
                rows = bubble_sort_temp(
                    rows,
                    column_map[sort_column],
                    reverse=(sort_order == "desc")
                )

    except Exception as e:
        rows = []
        error = error + f"<div class='alert alert-danger mt-3'><pre>{html.escape(str(e))}</pre></div>"

    # Build table rows #Seyoung
    html_rows = ""
    for r in rows:
        dt, tid, ssn, tsn, t1, t2, t3, ta, ph, ob = r
        t1_str = "" if t1 is None else str(t1)
        t2_str = "" if t2 is None else str(t2)
        t3_str = "" if t3 is None else str(t3)
        ta_str = "" if ta is None else str(ta)
        ph_str = "" if ph is None else str(ph)
        ob_str = "" if ob is None else str(ob)

        html_rows += (
            "<tr>"
            f"<td>{highlight(dt, 0, search_column, search_value)}</td>"
            f"<td class='titration-id-cell fw-bold'>{highlight(tid, 1, search_column, search_value)}</td>"
            f"<td>{highlight(ssn, 2, search_column, search_value)}</td>"
            f"<td><span class='badge-titrant'>{highlight(tsn, 3, search_column, search_value)}</span></td>"
            f"<td>{highlight(t1_str, 4, search_column, search_value)}</td>"
            f"<td>{highlight(t2_str, 5, search_column, search_value)}</td>"
            f"<td>{highlight(t3_str, 6, search_column, search_value)}</td>"
            f"<td class='fw-bold text-success'>{ta if ta is not None else ''}</td>"
            f"<td><span class='ph-value'>{ph if ph is not None else ''}</span></td>"
            f"<td class='text-muted small'>{highlight(ob, 9, search_column, search_value)}</td>"
            "</tr>"
        )

    page = f"""<!doctype html>
<html lang="en">
<head>

<meta charset="utf-8">
<title>Main Page – TEMP</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400&display=swap');
:root {{
    --t-green: #002c23;
    --t-gold: #b1d3cb;
    --t-cream: #e8f3f1;
    --radius: 14px;
    --shadow-sm: 0 2px 10px rgba(0,0,0,0.04);
    --shadow-md: 0 8px 30px rgba(0,0,0,0.06);
}}

* {{ box-sizing: border-box; }}

body {{
    background-color: #e8f3f1;
    color: #333;
    font-family: 'Inter', sans-serif;
    margin: 0;
}}

h1, h2, h3, h4, h5, .header-title, .section-title {{
    font-family: 'Inter', sans-serif;
}}

/* ═══════════════════ SIDEBAR (LEFT) ═══════════════════ */
:root {{
    --sidebar-width-collapsed: 70px;
    --sidebar-width-expanded: 240px;
}}

body {{
    margin: 0;
    padding-left: var(--sidebar-width-collapsed); 
    transition: padding-left 0.3s ease;
}}

.sidebar-main {{
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: var(--sidebar-width-collapsed);
    background: var(--t-green);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    z-index: 1000;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 2px 0 20px rgba(0,44,35,0.15);
}}

/* Expand on mouse hover */
.sidebar-main:hover {{
    width: var(--sidebar-width-expanded);
}}
/* Logo area */
.nav-brand {{
    display: flex;
    align-items: center;
    padding: 20px 20px;
    text-decoration: none;
    height: 80px;
    overflow: hidden;
    white-space: nowrap;
}}
.nav-brand img {{ 
    width: 30px; 
    min-width: 30px; 
    filter: drop-shadow(0 0 6px rgba(177,211,203,0.3)); 
}}
.nav-brand .brand-text {{
    color: var(--t-gold);
    font-family: 'Inter', serif;
    font-weight: 700;
    font-size: 0.9rem;
    margin-left: 15px;
    opacity: 0;
    transition: opacity 0.2s;
}}

.header-new {{
    font-family: 'Outfit', sans-serif;
    font-size: 1.5rem;
    font-weight: 500;         
    color: var(--t-green);
    
    letter-spacing: 0.2rem;
    text-transform: uppercase;  

    text-shadow: 
        -1px -1px 0 #fff,  1px -1px 0 #fff,
        -1px  1px 0 #fff,  1px  1px 0 #fff,
         0px -1px 0 #fff,  0px  1px 0 #fff,
        -1px  0px 0 #fff,  1px  0px 0 #fff;

    display: inline-block;
    padding: 15px 20px;
    transition: all 0.4s ease; 
}}

.sidebar-main:hover .brand-text {{ opacity: 1; }}

/* Menu link area */
.nav-links {{
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 30px 10px;
    flex-grow: 1;
    justify-content: center;
}}

.nav-link-item {{
    width: 100%;
    color: rgba(255,255,255,0.6);
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 500;
    padding: 12px 15px;
    border-radius: 8px;
    transition: all 0.2s;
    background: none;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    white-space: nowrap;
}}

.nav-link-item i {{
    font-size: 1.2rem;
    min-width: 30px;
    text-align: center;
    align-items: center;
}}

.nav-link-item span {{
    margin-left: 10px;
    opacity: 0;
    transition: opacity 0.2s;
}}
.sidebar-main:hover .nav-link-item span {{ opacity: 1; }}

.nav-link-item:hover {{ color: rgba(255,255,255,0.95); background: rgba(255,255,255,0.08); }}
.nav-link-item.active {{ color: var(--t-gold); background: rgba(177,211,203,0.1); }}

/* Bottom user information area */
.nav-bottom {{
    padding: 20px 10px;
    border-top: 1px solid rgba(255,255,255,0.1);
}}
.welcome-tag {{
    display: flex;
    align-items: center;
    padding: 10px 15px;
    color: rgba(255,255,255,0.7);
    font-size: 0.8rem;
    white-space: nowrap;
}}
.welcome-tag b {{ margin-left: 5px; opacity: 0; transition: opacity 0.2s; }}
.sidebar-main:hover .welcome-tag b {{ opacity: 1; }}

.logout-btn {{
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--t-gold);
    color: var(--t-green);
    border-radius: 8px;
    padding: 10px;
    margin-top: 10px;
    font-weight: 700;
    font-size: 0.82rem;
    text-decoration: none;
    transition: all 0.2s;
}}
.logout-btn span {{ display: none; margin-left: 5px; }}
.sidebar-main:hover .logout-btn span {{ display: inline; }}
.logout-btn:hover {{ background: #d4ece5; transform: translateY(-1px); }}

/* ═══════════════════ SEARCH BAR ═══════════════════ */
.search-bar {{
    background: none; padding: 14px 35px;
    margin-bottom: -20px;
    border-bottom: 0px solid rgba(0,0,0,0.05);
    display: flex; justify-content: flex-end;
}}
.search-bar .form-select {{
    border-radius: 20px 0 0 20px; border: 1px solid #ddd;
    font-size: 0.85rem; padding: 8px 14px;
    max-width: 160px; border-right: none;
    background-color: #fafafa;
}}
.search-bar .form-control {{
    border-radius: 0; border: 1px solid #ddd;
    font-size: 0.85rem; padding: 8px 14px;
    max-width: 250px; border-right: none;
}}
.search-bar .search-btn {{
    border-radius: 0 20px 20px 0;
    background: var(--t-green); color: white;
    border: 1px solid var(--t-green); padding: 8px 18px;
    font-size: 0.85rem; transition: 0.2s;
}}
.search-bar .search-btn:hover {{ background: #004d3d; }}

/* ═══════════════════ HIGHLIGHT ═══════════════════ */
.highlight {{
    background: linear-gradient(135deg, #fff9db, #fff3a0);
    padding: 1px 5px; border-radius: 4px; font-weight: 600;
}}

/* ═══════════════════ TABLE CARD ═══════════════════ */
.table-card {{
    background: white; border-radius: var(--radius);
    overflow: hidden; box-shadow: var(--shadow-md);
    border: 1px solid rgba(0,0,0,0.04);
}}
.table-card-header {{
    background: var(--t-green); color: white;
    padding: 18px 22px;
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 3px solid var(--t-gold);
}}
.table-card-header h5 {{
    margin: 0; font-size: 1.1rem; font-weight: 700;
    font-family: 'Inter', sans-serif;
}}
.table-card-header .badge-tech {{
    background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.7);
    padding: 5px 12px; border-radius: 20px; font-size: 0.72rem;
    font-weight: 500; border: 1px solid rgba(255,255,255,0.1);
}}

/* ─── Sort Bar ─── */
.sort-bar {{
    background: #eef6f4; padding: 12px 22px;
    display: flex; align-items: center; gap: 12px;
    border-bottom: 1px solid rgba(0,0,0,0.04);
}}
.sort-bar label {{
    font-weight: 600; color: var(--t-green);
    font-size: 0.82rem; white-space: nowrap;
}}
.sort-bar .form-select {{
    border-radius: 10px; font-size: 0.82rem;
    padding: 7px 14px; border: 1px solid #ddd;
    max-width: 180px;
}}


CSS
/* ─── Table ─── */
.table {{ 
    margin-bottom: 0;
    table-layout: fixed; /* Layout Algorithm Fixed */
    width: 1298px !important; 
    min-width: 1298px!important;
    max-width: 1298px!important;
    border-collapse: collapse;
}}

.table thead th {{
    background: #fafafa; color: #999;
    font-weight: 600; text-transform: uppercase;
    font-size: 0.7rem; letter-spacing: 0.8px;
    padding: 13px 13px; border-bottom: 2px solid #eee;
    
   /* Create scrollbar when screen becomes narrow */
    white-space: normal; 
    word-break: break-all; 
    overflow-wrap: break-word;
    vertical-align: top;
}}

.table tbody td {{
    padding: 12px; vertical-align: middle;
    font-size: 0.88rem; border-bottom: 1px solid #f5f5f5;
    
/* If the main text exceeds the width, it will wrap to the next line */
    white-space: normal; 
    word-break: break-all; 
}}

.table thead th, .table tbody td {{
   /* Prevent internal width from changing due to padding */
    box-sizing: border-box; 
    
   /* Prevent text from pushing out the width */
    word-break: break-all;
    overflow: hidden;
}}

.table th:nth-child(1), .table td:nth-child(1) {{ width: 120px !important; min-width: 120px !important; max-width: 120px !important; }}
.table th:nth-child(2), .table td:nth-child(2) {{ width: 95px !important;  min-width: 95px !important;  max-width: 95px !important;  }}
.table th:nth-child(3), .table td:nth-child(3) {{ width: 165px !important; min-width: 165px !important; max-width: 165px !important; }}
.table th:nth-child(4), .table td:nth-child(4) {{ width: 155px !important; min-width: 155px !important; max-width: 155px !important; }}
.table th:nth-child(5), .table td:nth-child(5) {{ width: 115px !important; min-width: 115px !important; max-width: 115px !important; }}
.table th:nth-child(6), .table td:nth-child(6) {{ width: 118px !important; min-width: 118px !important; max-width: 118px !important; }}
.table th:nth-child(7), .table td:nth-child(7) {{ width: 118px !important; min-width: 118px !important; max-width: 118px !important; }}
.table th:nth-child(8), .table td:nth-child(8) {{ width: 175px !important; min-width: 175px !important; max-width: 175px !important; }}
.table th:nth-child(9), .table td:nth-child(9) {{ width: 85px !important;  min-width: 85px !important;  max-width: 85px !important;  }}
.table th:nth-child(10), .table td:nth-child(10) {{ width: 145px !important; min-width: 145px !important; max-width: 145px !important; }}
.badge-titrant {{
  background: rgba(0, 44, 35, 0.05);
  color: #002c23;
  padding: 4px 10px;
  border-radius: 6px;
  font-weight: 500;
}}
.ph-value {{
   background: #f1f3f5;
   padding: 2px 6px;
  border-radius: 4px;
        }} 

/* ═══════════════════ FORM BOXES ═══════════════════ */
.form-box {{
    background: white; border-radius: var(--radius);
    padding: 32px; box-shadow: var(--shadow-md);
    border: 1px solid rgba(0,0,0,0.04);
}}
.form-box .form-header {{
    display: flex; justify-content: space-between;
    align-items: center; margin-bottom: 20px;
}}
.form-box .form-header h4 {{
    color: var(--t-green); font-weight: 800; margin: 0;
    font-size: 1.15rem;
}}
.form-box .form-header .tag {{
    background: #eef6f4; padding: 5px 14px; border-radius: 20px;
    color: #11676a; font-weight: 700; font-size: 0.72rem;
    letter-spacing: 0.5px;
}}

.section-title {{
    text-align: center; font-weight: 700;
    font-size: 1.15rem; color: var(--t-green);
    background: linear-gradient(135deg, #dceee9, #c8e0da);
    padding: 12px; border-radius: 10px;
    margin-bottom: 16px;
}}

.main-footer {{
    background-color: #e8f3f1;
    color: #bbb; 
    text-align: center;
    padding: 10px 0;
    font-size: 0.8rem;
    border-top: 1px solid #b1d3cc;
    width: 100%;
    position: fixed; /* This locks it to the screen */
    bottom: 0;
    left: 0;
    z-index: 999; /* Keeps it above other elements */
}}

/* ═══════════════════ ALERTS ═══════════════════ */
.alert.compact-alert {{
    padding: 4px 10px;
    font-size: 0.8rem;
    border-radius: 8px;
    margin-bottom: 6px;
}}
/* ─── Buttons ─── */
.btn-primary-custom {{
    background: var(--t-green); color: white; font-weight: 700;
    border: none; border-radius: 10px; padding: 10px 24px;
    font-size: 0.88rem; transition: all 0.2s;
}}
.btn-primary-custom:hover {{ background: #004d3d; transform: translateY(-1px); color: white; }}

.btn-danger-custom {{
    background: #7c1515; color: white; font-weight: 700;
    border: none; border-radius: 10px; padding: 10px 24px;
    font-size: 0.88rem; transition: all 0.2s;
}}
.btn-danger-custom:hover {{ background: #a01c1c; transform: translateY(-1px); color: white; }}

.btn-outline-custom {{
    background: none; border: 1px solid #ccc; color: #666;
    border-radius: 10px; padding: 10px 24px; font-size: 0.88rem;
    font-weight: 600; transition: all 0.2s;
}}
.btn-outline-custom:hover {{ border-color: var(--t-green); color: var(--t-green); }}

/* ═══════════════════ TOP RIGHT USER ICON ═══════════════════ */
.top-user-box {{
    position: fixed;
    top: 20px;
    right: 25px;
    background: white;
    border-radius: 50px;
    padding: 8px 18px;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 6px 25px rgba(0,0,0,0.08);
    z-index: 2000;
    transition: all 0.2s ease;
}}

.top-user-box:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
}}

.top-user-box i {{
    font-size: 1.2rem;
    color: var(--t-green);
}}

.top-user-box span {{
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--t-green);
}}

#addExperimentBtn:disabled {{
    background-color: #cccccc !important;
    border-color: #bbbbbb !important;
    color: #666666 !important;
    cursor: not-allowed;
    opacity: 0.6;
}}

</style>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
<div class="top-user-box">
    <i class="bi bi-person-circle"></i>
    <span>{username}</span>
</div>
<!-- ═══════════════════ SIDEBAR (LEFT) ═══════════════════ -->
<nav class="sidebar-main">
<a href="http://localhost:8080/" class="nav-brand" style="margin-right: 12px; display: flex; align-items: center;">
  <img src="{curr_logo}" style="width:35px; margin-right:12px;" onerror="this.style.display='none'">
  <span class="brand-text" style="color:#b1d3cb; font-size:1.6rem; font-weight:700;">ADMIN</span>
</a>

  <div class="nav-links">

    <button type="button" class="nav-link-item" data-bs-toggle="modal" data-bs-target="#dashboardModal">
      <i class="bi bi-grid-1x2-fill"></i> <span>Dashboard</span>
    </button>

    <form method="post">
      <input type="hidden" name="action" value="toggle_add_form">
      <input type="hidden" name="show_add_form" value="{1 if not show_add_form else 0}">
      <input type="hidden" name="username" value="{username}">
      <button type="submit" class="nav-link-item {'active' if show_add_form else ''}">
        <i class="bi bi-plus-circle"></i> <span>Add</span>
      </button>
    </form>

    <form method="post">
      <input type="hidden" name="action" value="toggle_load_form">
      <input type="hidden" name="show_load_form" value="{1 if not show_load_form else 0}">
      <input type="hidden" name="username" value="{username}">
      <button type="submit" class="nav-link-item {'active' if show_load_form else ''}">
        <i class="bi bi-arrow-repeat"></i> <span>Load / Update</span>
      </button>
    </form>

    <form method="post">
      <input type="hidden" name="action" value="toggle_delete_form">
      <input type="hidden" name="show_delete_form" value="{1 if not show_delete_form else 0}">
      <input type="hidden" name="username" value="{username}">
      <button type="submit" class="nav-link-item {'active' if show_delete_form else ''}">
        <i class="bi bi-trash3"></i> <span>Delete</span>
      </button>
    </form>

    <form method="post">
      <input type="hidden" name="action" value="toggle_graph_form">
      <input type="hidden" name="show_graph_form" value="{'0' if show_graph_form else '1'}">
      <input type="hidden" name="username" value="{username}">
      <button type="submit" class="nav-link-item {'active' if show_graph_form else ''}">
        <i class="bi bi-bar-chart-line"></i> <span>Graph</span>
      </button>
    </form>

    <form method="post">
        <input type="hidden" name="action" value="toggle_header_form">
        <input type="hidden" name="show_header_form" value="{'0' if show_header_form else '1'}">
        <input type="hidden" name="username" value="{username}">
        <button type="button" class="nav-link-item" data-bs-toggle="modal" data-bs-target="#editHeaderModal">
            <i class="bi bi-pencil-square"></i> <span>Edit Header & Logo</span>
        </button>
    </form>

    <a href="/about" class="nav-link-item">
      <i class="bi bi-info-circle"></i> <span>About Us</span>
    </a>
  </div>

  
  <div class="nav-bottom">
    <div class="welcome-tag">
      <i class="bi bi-person-circle"></i> <b>{username}</b>
    </div>
    <a href="/logout"" class="logout-btn">
      <i class="bi bi-box-arrow-left"></i> <span>Logout</span>
    </a>
  </div>
</nav>

<!-- ═══════════════════ HEADER NAME ═══════════════════ -->
<div class="container-fluid py-2" style="background:#e8f3f1; margin-bottom: 18px;">
    <div class="d-flex justify-content-center align-items-center">
    <span class="header-new">
            <a href="http://localhost:8080/" style="text-decoration: none; color: inherit;">
                {curr_title}
            </a>
        </span>
    </div>
</div>

<!-- ═══════════════════ SEARCH BAR ═══════════════════ -->
<div class="search-bar">
    <form method="post" class="d-flex align-items-center">
        <input type="hidden" name="action" value="search">
        <select name="search_column" class="form-select">
            <option value="date_temp" {"selected" if search_column == "date_temp" else ""}>Date</option>
            <option value="titration_id_temp" {"selected" if search_column == "titration_id_temp" else ""}>ID</option>
            <option value="standard_solution_name_temp" {"selected" if search_column == "standard_solution_name_temp" else ""}>Standard</option>
            <option value="titrant_solution_name_temp" {"selected" if search_column == "titrant_solution_name_temp" else ""}>Titrant</option>
        </select>
        <input type="text" name="search_value" class="form-control" placeholder="Search experiments..." value="{html.escape(search_value or '')}">
        <button class="btn search-btn" type="submit"><i class="bi bi-search"></i></button>
    </form>
</div>

<!-- ═══════════════════ TABLE ═══════════════════ -->
<div class="container-fluid px-4 py-4">
    {"<div class='alert alert-success'>" + message + "</div>" if message else ""}
    {"<div class='alert alert-danger'>" + error + "</div>" if error else ""}

    <div class="table-card">
        <div class="table-card-header">
            <h5>Titrations_temp</h5>
        </div>

        <!-- Sort Bar -->
        <div class="sort-bar">
            <form method="post" class="d-flex align-items-center gap-3">
                <input type="hidden" name="action" value="sort">
                <input type="hidden" name="username" value="{username}">
                <label>Sort by:</label>
                <select name="sort_column" class="form-select" onchange="this.form.submit()">
                    <option value="" disabled selected hidden>Choose field</option>
                    <option value="date" {"selected" if selected_sort=="date" else ""}>Date</option>
                    <option value="standard" {"selected" if selected_sort=="standard" else ""}>Standard Solution</option>
                    <option value="titrant" {"selected" if selected_sort=="titrant" else ""}>Titrant</option>
                    <option value="average" {"selected" if selected_sort=="average" else ""}>Average Volume</option>
                </select>
                <select name="sort_order" class="form-select" onchange="this.form.submit()">
                    <option value="asc" {"selected" if selected_order=="asc" else ""}>&#8593; Ascending</option>
                    <option value="desc" {"selected" if selected_order=="desc" else ""}>&#8595; Descending</option>
                </select>
            </form>
        </div>

        <!-- Data Table -->
        <div style="overflow-x: auto;">
            <table class="table table-hover align-middle table-fixed">
                <thead>
                    <tr>
                        <th>date_temp</th>
                        <th>titration_id_temp</th>
                        <th>standard_solution_name_temp</th>
                        <th>titrant_solution_name_temp</th>
                        <th>totaltrial_1_cm3_temp</th>
                        <th>totaltrial_2_cm3_temp</th>
                        <th>totaltrial_3_cm3_temp</th>
                        <th>totaltrial_average_cm3_temp</th>
                        <th>pH_temp</th>
                        <th>observation_temp</th>
                    </tr>
                </thead>
                <tbody>
                    {html_rows}
                </tbody>
            </table>
        </div>

    </div>
</div>
"""
    # -------- The Header Modal ---------
    edit_header_modal = f"""
        <div class="modal fade" id="editHeaderModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content" style="border-radius: 24px; border: none; overflow: hidden; box-shadow: 0 25px 50px rgba(0,0,0,0.3);">
                    
                    <div class="modal-header px-4 py-4" style="background: var(--t-green); border: none;">
                        <div class="d-flex align-items-center">
                            <div style="background: rgba(177,211,203,0.2); padding: 12px; border-radius: 15px; margin-right: 15px;">
                                <i class="bi bi-magic" style="color: var(--t-gold); font-size: 1.5rem;"></i>
                            </div>
                            <div>
                                <h5 class="modal-title fw-bold text-white mb-0" style="font-family: 'Inter', sans-serif;">Edit Header System</h5>
                                <p class="text-white-50 small mb-0">Live preview your changes before applying the new changes.</p>
                            </div>
                        </div>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <form method="POST" action="/admin-dashboard" id="brandingForm">
                        <div class="modal-body p-0">
                            <div class="row g-0">
                                
                                <div class="col-md-7 p-4 border-end bg-white">
                                    <input type="hidden" name="action" value="update_header">
                                    <input type="hidden" name="logo_base64" id="logo_base64">
                                    
                                    <div class="mb-4">
                                        <label class="form-label fw-bold small text-muted text-uppercase" style="letter-spacing: 1px;">Header Name_Temp</label>
                                        <input type="text" id="nameInput" name="new_header_name" class="form-control form-control-lg" value="{curr_title}" style="border-radius: 12px; background: #f8f9fa; border: 1px solid #eee; font-size: 1rem;" placeholder="Enter new header name...">
                                    </div>

                                    <div class="mb-2">
                                        <label class="form-label fw-bold small text-muted text-uppercase" style="letter-spacing: 1px;">Header Logo_Temp</label>
                                        <input type="file" id="filePicker" class="form-control" accept="image/*" style="border-radius: 12px; background: #f8f9fa; border: 1px solid #eee;">
                                        <div class="form-text mt-3 p-2 rounded" style="background: #eef6f4; color: var(--t-green); font-size: 0.75rem;">
                                        </div>
                                    </div>
                                </div>

                                <div class="col-md-5 p-4 d-flex flex-column justify-content-center align-items-center" style="background-color: #fafafa;">
                                    <div id="previewCard" class="preview-card p-4 bg-white text-center" style="border-radius: 20px; width: 100%; border: 1px dashed #ced4da; transition: all 0.3s ease;">
                                        <p class="small text-muted fw-bold mb-3" style="font-size: 0.6rem; letter-spacing: 2px;">LIVE PREVIEW</p>
                                        
                                        <div class="mb-3" style="min-height: 60px; display: flex; align-items: center; justify-content: center;">
                                            <img id="imagePreview" src="{curr_logo}" alt="Logo" style="max-height: 55px; width: auto; transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);" onerror="this.src='https://cdn-icons-png.flaticon.com/512/1048/1048944.png'">
                                        </div>
                                        
                                        <h6 id="namePreview" class="fw-bold m-0" style="color: var(--t-green); font-family: 'Outfit', serif; font-size: 1rem; word-break: break-all;">{curr_title}</h6>
                                        
                                        <div class="mt-3 py-1 px-3 rounded-pill d-inline-block">
                                            HEADER VIEW
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="modal-footer p-4 bg-white border-0">
                            <button type="submit" class="btn w-100 py-3 fw-bold" style="background: var(--t-gold); color: var(--t-green); border-radius: 14px; box-shadow: 0 4px 15px rgba(177,211,203,0.4); border: none; transition: transform 0.2s;">
                                UPDATE HEADER SYSTEM
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <script>
        (function() {{
            // Elements
            const nameInput = document.getElementById('nameInput');
            const namePreview = document.getElementById('namePreview');
            const filePicker = document.getElementById('filePicker');
            const imagePreview = document.getElementById('imagePreview');
            const base64Input = document.getElementById('logo_base64');

            // 1. Live Typing Preview
            nameInput.addEventListener('input', function(e) {{
                namePreview.textContent = e.target.value || "Untitled Lab";
            }});

            // 2. Live File Preview + Base64 Conversion
            filePicker.addEventListener('change', function(e) {{
                const file = e.target.files[0];
                if (file) {{
                    const reader = new FileReader();
                    reader.onload = function(event) {{
                        // Update the image src in the preview
                        imagePreview.src = event.target.result;
                        // Put the Base64 string into the hidden field for Python
                        base64Input.value = event.target.result;
                        
                        // Small "pop" animation
                        imagePreview.style.transform = "scale(1.15)";
                        setTimeout(() => imagePreview.style.transform = "scale(1)", 250);
                    }};
                    reader.readAsDataURL(file);
                }}
            }});
        }})();
        </script>
        """
    page += edit_header_modal

# ─── Dashboard Modal ───
    try:
        all_exps = get_experiments()
        all_users = get_all_users_temp()
    except:
        all_exps = []
        all_users = []

    total_titrations = len(all_exps)
    total_users = len(all_users)

    # 1. Recent Users (last 3) 
    recent_users = all_users[-3:][::-1]
    recent_users_html = ""
    for u in recent_users:
        name_val = html.escape(str(u[0] or 'User')) 
        first_letter = name_val[0].upper() if name_val else "?"
        recent_users_html += f"""
        <div style="display:flex; align-items:center; gap:14px; padding:12px 16px; margin-bottom:8px; border-radius:14px; background:#f0f7f4; border:1px solid rgba(0,44,35,0.05);">
            <div style="width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,var(--t-green),#004d3d);color:white;display:flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0;">
                {first_letter}
            </div>
            <div style="flex-grow:1;">
                <div style="font-weight:600; color:var(--t-green); font-size:0.9rem;">{name_val}</div>
                <small style="color:#22c55e; font-weight:600; font-size:0.75rem;">Recently Joined</small>
            </div>
        </div>"""

    # 2. Recent experiments (last 3)
    recent_exps = all_exps[-3:][::-1]
    activity_feed_html = ""
    for exp in recent_exps:
        activity_feed_html += f"""
        <div style="display:flex; align-items:center; gap:14px; padding:12px 16px; margin-bottom:8px; border-radius:14px; background:#eef6f4; border-left:4px solid var(--t-gold);">
            <div style="width:40px;height:40px;border-radius:12px;background:rgba(0,44,35,0.05);display:flex;align-items:center;justify-content:center;color:var(--t-green);flex-shrink:0;">
                <i class="bi bi-droplet-half"></i>
            </div>
            <div style="flex-grow:1;">
                <div style="font-weight:600; color:var(--t-green); font-size:0.9rem;">{html.escape(str(exp[3] or ''))} &middot; ID {exp[1]}</div>
                <small style="color:#888;">Vol: <b>{exp[7]} cm&sup3;</b> &middot; {exp[0]}</small>
            </div>
        </div>"""

    dashboard_modal = f"""
    <div class="modal fade" id="dashboardModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content" style="border-radius:24px; border:none; overflow:hidden; box-shadow:0 25px 50px rgba(0,0,0,0.25);">

          <div class="modal-header px-4 py-4" style="background:var(--t-green); border:none;">
            <div class="d-flex align-items-center">
              <div style="background:rgba(177,211,203,0.2); padding:12px; border-radius:15px; margin-right:15px;">
                <i class="bi bi-grid-1x2-fill" style="color:var(--t-gold); font-size:1.5rem;"></i>
              </div>
              <div>
                <h5 class="modal-title fw-bold text-white mb-0">TEMP Dashboard</h5>
                <p class="text-white-50 small mb-0">Live Overview of Users and Experiments</p>
              </div>
            </div>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body p-4" style="background:#e8f3f1; max-height:75vh; overflow-y:auto;">
            <div class="row g-3">
              
              <div class="col-md-6">
                <div style="border-radius:18px; padding:25px; background:linear-gradient(135deg,#b1d3cb,#8fbdaf); color:var(--t-green); position:relative; overflow:hidden; margin-bottom:15px;">
                  <i class="bi bi-people-fill" style="position:absolute; right:15px; bottom:-10px; font-size:4rem; opacity:0.1;"></i>
                  <div style="font-size:0.7rem; font-weight:600; text-transform:uppercase; opacity:0.7;">Lab Users</div>
                  <div style="font-size:2.2rem; font-weight:800;">{total_users}</div>
                </div>
                <div style="background:white; border-radius:18px; padding:25px; border:1px solid rgba(0,0,0,0.04); min-height:250px;">
                  <h6 style="font-weight:700; color:var(--t-green); margin-bottom:15px;">Newest Members</h6>
                  {recent_users_html if recent_users_html else "<p class='text-muted small'>None.</p>"}
                </div>
              </div>

              <div class="col-md-6">
                <div style="border-radius:18px; padding:25px; background:linear-gradient(135deg,#b1d3cb,#8fbdaf); color:var(--t-green); position:relative; overflow:hidden; margin-bottom:15px;">
                  <i class="bi bi-flask-fill" style="position:absolute; right:15px; bottom:-10px; font-size:4rem; opacity:0.05;"></i>
                  <div style="font-size:0.7rem; font-weight:600; text-transform:uppercase; opacity:0.7;">Total Experiments</div>
                  <div style="font-size:2.2rem; font-weight:800;">{total_titrations}</div>
                </div>
                <div style="background:white; border-radius:18px; padding:25px; border:1px solid rgba(0,0,0,0.04); min-height:250px;">
                  <h6 style="font-weight:700; color:var(--t-green); margin-bottom:15px;">Recent Activity</h6>
                  {activity_feed_html if activity_feed_html else "<p class='text-muted small'>None.</p>"}
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
    """
    page += dashboard_modal
    
    # ===================== ADD FORM ===================== #Sana
    if show_add_form:
        titrant_name = html.escape(str(form_data.get("titrant_name", "")))
        standard_solution = html.escape(str(form_data.get("standard_solution", "")))
        exp_date = html.escape(str(form_data.get("exp_date", "")))
        trial1 = html.escape(str(form_data.get("trial1", "")))
        trial2 = html.escape(str(form_data.get("trial2", "")))
        trial3 = html.escape(str(form_data.get("trial3", "")))
        observation = html.escape(str(form_data.get("observation", "")))
        ph_value = html.escape(str(form_data.get("ph_temp", "")))
        average = html.escape(str(form_data.get("average", "")))
        today = date.today().isoformat()
        
        is_calculated = "disabled" if not average or average == "0.00" else ""

        page += f"""
<div class="container-fluid px-4 pb-4" style="max-width: 1300px;">
  <div class="form-box" style="border-top: 4px solid var(--t-green);">
    <div class="form-header">
        <div>
            <h4><i class="bi bi-plus-circle-fill" style="color:var(--t-gold); margin-right:8px;"></i>New Titration Entry</h4>
            <p class="text-muted mb-0" style="font-family:'Inter'; font-size:0.85rem;">Enter your titration details to log and track experiment results.</p>
        </div>
        <div class="tag">EXPERIMENT ENTRY</div>
    </div>

    <div class="alert" style="background: #eef6f4; border-left: 4px solid var(--t-green); color: var(--t-green);">
        <h6 class="fw-bold mb-1" style="font-size:0.85rem;"><i class="bi bi-info-circle me-1"></i> How to Add</h6>
        <ul class="small mb-0" style="padding-left: 18px;">
            <li>All fields marked with <span class="text-danger">*</span> are <strong>required</strong>.</li>
            <li>Click <strong>'Calculate Average'</strong> before adding your experiment.</li>
            <li>Records are safely stored and can be reviewed anytime.</li>
        </ul>
    </div>

    <form method="post" id="addExperimentForm">
      <input type="hidden" name="action" value="add_experiment">
      <input type="hidden" name="username" value="{username}">
      
      <div class="row g-3 mb-3">
        <div class="col-md-4">
          <label class="form-label small fw-semibold" style="color:#666;">Titrant Name<span class="text-danger">*</span></label>
          <input type="text" name="titrant_name" class="form-control" style="border-radius:10px;" placeholder="e.g. HCl" value="{titrant_name}" required>
        </div>
        <div class="col-md-4">
          <label class="form-label small fw-semibold" style="color:#666;">Standard Solution<span class="text-danger">*</span></label>
          <input type="text" name="standard_solution" class="form-control" style="border-radius:10px;" placeholder="e.g. NaOH" value="{standard_solution}" required>
        </div>
        <div class="col-md-4">
          <label class="form-label small fw-semibold" style="color:#666;">Experiment Date<span class="text-danger">*</span></label>
          <input type="date" name="exp_date" id="exp_date" max="{today}" class="form-control" style="border-radius:10px;" value="{exp_date}" oninput="validateDate()" required>
          <div id="date-alert" class="text-danger small mt-1" style="display:none; font-size: 0.75rem;">
            <i class="bi bi-exclamation-circle"></i> Future dates are not allowed.
          </div>
        </div>
      </div>

      <div class="row g-3 mb-3">
        <div class="col-md-2">
          <label class="form-label small fw-semibold" style="color:#666;">Trial 1 (cm&sup3;)<span class="text-danger">*</span></label>
          <input type="number" step="0.01" name="trial1" class="form-control" style="border-radius:10px;" placeholder="e.g. 12.23" value="{trial1}" required>
        </div>
        <div class="col-md-2">
          <label class="form-label small fw-semibold" style="color:#666;">Trial 2 (cm&sup3;)<span class="text-danger">*</span></label>
          <input type="number" step="0.01" name="trial2" class="form-control" style="border-radius:10px;" value="{trial2}" required>
        </div>
        <div class="col-md-2">
          <label class="form-label small fw-semibold" style="color:#666;">Trial 3 (cm&sup3;)<span class="text-danger">*</span></label>
          <input type="number" step="0.01" name="trial3" class="form-control" style="border-radius:10px;" value="{trial3}" required>
        </div>
        <div class="col-md-3">
          <label class="form-label small fw-semibold" style="color:#666;">Average Volume<span class="text-danger">*</span></label>
          <input type="text" name="average" class="form-control fw-bold" style="border-radius:10px; background:#f8f9fa;" readonly value="{average}" required>
        </div>
        <div class="col-md-3">
            <label class="form-label small fw-semibold" style="color:#666;">
                Measured pH <span style="font-size: 0.7rem; color: #999;">(Range: 0-14)</span><span class="text-danger">*</span>
            </label>
            <input type="number" 
                step="0.01" 
                min="0" 
                max="14" 
                name="ph_temp" 
                class="form-control" 
                style="border-radius:10px;" 
                placeholder="0.00" 
                value="{ph_value}" 
                oninvalid="this.setCustomValidity('pH must be between 0 and 14')" 
                oninput="this.setCustomValidity('')"
                required>
        </div>
      </div>

      <div class="mb-4">
        <label class="form-label small fw-semibold" style="color:#666;">Observations<span class="text-danger">*</span></label>
        <textarea name="observation" class="form-control" style="border-radius:10px;" rows="2" placeholder="e.g. Color changed from colorless to faint pink..." required>{observation}</textarea>
      </div>

      <div class="d-flex justify-content-end gap-3 pt-3 border-top">
            <button type="submit" name="calculate" value="1" id="calcAverageBtn" class="btn btn-outline-custom">
                <i class="bi bi-calculator me-1"></i> Calculate Average
            </button>
            
            <button type="submit" name="add" value="1" id="addExperimentBtn" class="btn btn-primary-custom" {is_calculated}>
                <i class="bi bi-plus-lg me-1"></i> Add Experiment
            </button>
      </div>
    </form>
  </div>
</div>
"""

    # ===================== DELETE FORM =====================
    if show_delete_form:
        page += f"""
    <div class="container-fluid px-4 pb-4" style="max-width: 1000px;">
        <div class="form-box mx-auto" style="max-width: 550px; border-top: 4px solid #7c1515;">
            <div class="d-flex align-items-center gap-3 mb-3">
                <div style="width:42px;height:42px;background:#fdf2f2;border-radius:12px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                    <i class="bi bi-trash3-fill" style="color:#7c1515; font-size:1.1rem;"></i>
                </div>
                <div>
                    <h4 class="fw-bold mb-0" style="color:#7c1515; font-size:1.1rem;">Delete Experiment</h4>
                    <p class="text-muted mb-0" style="font-size:0.8rem;">Remove a titration record permanently</p>
                </div>
            </div>

            <form method="post" onsubmit="return confirm('Are you sure you want to permanently delete this experiment?');">
                <input type="hidden" name="action" value="delete_experiment">
                <input type="hidden" name="username" value="{username}">

                <div class="row align-items-center g-2 mb-2">
                    <div class="col-md-8">
                        <div class="input-group">
                            <span class="input-group-text fw-bold" style="border-radius:10px 0 0 10px; background:#fdf2f2; color:#7c1515; border-color:#eee;">ID#</span>
                            <input type="number" name="id_to_delete" class="form-control" style="border-radius:0 10px 10px 0;"
                                  placeholder="Enter Titration ID" required oninput="checkExperimentExistsJS(this.value)">
                        </div>
                    </div>
                    <div class="col-md-4">
                        <button type="submit" class="btn btn-danger-custom w-100">
                            <i class="bi bi-trash3 me-1"></i> REMOVE
                        </button>
                    </div>
                </div>

                <p class="small text-danger mb-0" style="font-size:0.78rem;">
                    * This permanently removes the experiment from records.
                </p>
                <div id="deleteFeedback" class="mt-1 small fw-bold" style="height:20px;"></div>
            </form>

            <div class="mt-3 pt-2 border-top text-center">
                <p class="small text-muted mb-0">
                    Need to change data instead?
                    <a href="#" onclick="event.preventDefault(); document.getElementById('loadToggleForm').submit();" style="color:#7c1515; text-decoration:none; font-weight:600;">Use the Load / Update feature</a>
                </p>
            </div>
            <form id="loadToggleForm" method="post" style="display:none;">
                <input type="hidden" name="action" value="toggle_load_form">
                <input type="hidden" name="show_load_form" value="1">
                <input type="hidden" name="username" value="{username}">
            </form>
        </div>
    </div>
    """

    # ===================== LOAD / UPDATE FORM =====================
    if show_load_form:
        if load_record_data:
            ld = load_record_data
            load_id = html.escape(str(ld.get("titration_id", "")))
            load_date = html.escape(str(ld.get("date", "")))
            load_titrant = html.escape(str(ld.get("titrant_name", "")))
            load_standard = html.escape(str(ld.get("standard_solution", "")))
            load_t1 = html.escape(str(ld.get("trial1", "")))
            load_t2 = html.escape(str(ld.get("trial2", "")))
            load_t3 = html.escape(str(ld.get("trial3", "")))
            load_avg = html.escape(str(ld.get("average", "")))
            load_ph = html.escape(str(ld.get("ph_temp", "")))
            load_obs = html.escape(str(ld.get("observation", "")))
        else:
            load_id = load_date = load_titrant = load_standard = ""
            load_t1 = load_t2 = load_t3 = load_avg = load_ph = load_obs = ""

        has_record = "block" if load_record_data else "none"
        no_record = "none" if load_record_data else "block"

        page += f"""
    <div class="container-fluid px-4 pb-4" style="max-width: 1300px;">
      <div class="form-box" style="border-top: 4px solid var(--t-green);">
        <div class="form-header">
            <div>
                <h4><i class="bi bi-arrow-repeat" style="color:var(--t-gold); margin-right:8px;"></i>Load / Update Record</h4>
                <p class="text-muted mb-0" style="font-family:'Inter'; font-size:0.85rem;">Search for a record by ID, review details and update fields.</p>
            </div>
            <div class="tag">LOAD &amp; EDIT</div>
        </div>

        <!-- Search by ID -->
        <form method="post" class="mb-4">
            <input type="hidden" name="action" value="load_experiment">
            <input type="hidden" name="username" value="{username}">
            <div class="row align-items-end g-2">
                <div class="col-md-6">
                    <label class="form-label small fw-semibold" style="color:#666;">Enter Titration ID to load</label>
                    <div class="input-group">
                        <span class="input-group-text fw-bold" style="border-radius:10px 0 0 10px; background:#eef6f4; color:var(--t-green); border-color:#ddd;">ID#</span>
                        <input type="number" name="load_id" class="form-control" style="border-radius:0 10px 10px 0;" placeholder="Enter Titration ID" value="{load_id}" required oninput="checkLoadIdExistsJS(this.value)">
                    </div>
                    <div id="loadFeedback" class="mt-1 small fw-bold" style="height:20px;"></div>
                </div>
                <div class="col-md-3" style="margin-bottom:20px;">
                    <button type="submit" class="btn btn-primary-custom w-100" style="padding:10px 24px; font-size:0.88rem;">
                        <i class="bi bi-search me-1"></i> Load Record
                    </button>
                </div>
            </div>
        </form>

        <!-- Placeholder when no record loaded -->
        <div id="load-placeholder" style="display:{no_record}; text-align:center; padding:40px 20px; color:#ccc;">
            <i class="bi bi-folder2-open" style="font-size:3rem; display:block; margin-bottom:12px; opacity:0.3;"></i>
            <p class="fw-semibold" style="font-size:0.95rem; color:#aaa;">No record loaded</p>
            <p class="small" style="opacity:0.6;">Enter a Titration ID above and click Load Record</p>
        </div>

        <!-- Editable record form -->
        <div id="load-record-form" style="display:{has_record};">
          <div class="alert" style="background: #eef6f4; border-left: 4px solid var(--t-green); color: var(--t-green);">
              <h6 class="fw-bold mb-1" style="font-size:0.85rem;"><i class="bi bi-pencil-square me-1"></i> Editing Record #{load_id}</h6>
              <p class="small mb-0">Modify any field below and click <strong>Update Experiment</strong> to save changes. Click <strong>Recalculate Average</strong> if you change trial values.</p>
          </div>

          <form method="post">
            <input type="hidden" name="action" value="update_experiment">
            <input type="hidden" name="username" value="{username}">
            <input type="hidden" name="update_id" value="{load_id}">

            <div class="row g-3 mb-3">
              <div class="col-md-4">
                <label class="form-label small fw-semibold" style="color:#666;">Titrant Name<span class="text-danger">*</span></label>
                <input type="text" name="titrant_name" class="form-control" style="border-radius:10px;" value="{load_titrant}">
              </div>
              <div class="col-md-4">
                <label class="form-label small fw-semibold" style="color:#666;">Standard Solution<span class="text-danger">*</span></label>
                <input type="text" name="standard_solution" class="form-control" style="border-radius:10px;" value="{load_standard}">
              </div>
              <div class="col-md-4">
                <label class="form-label small fw-semibold" style="color:#666;">Experiment Date<span class="text-danger">*</span></label>
                <input type="date" name="exp_date" id="exp_date" max="{today}" class="form-control" style="border-radius:10px;" value="{load_date}" oninput="validateDate()" required>
                <div id="date-alert" class="text-danger small mt-1" style="display:none; font-size: 0.75rem;">
                    <i class="bi bi-exclamation-circle"></i> Future dates are not allowed.
                </div>
              </div>
            </div>

            <div class="row g-3 mb-3">
              <div class="col-md-2">
                <label class="form-label small fw-semibold" style="color:#666;">Trial 1 (cm&sup3;)<span class="text-danger">*</span></label>
                <input type="number" step="0.01" name="trial1" class="form-control" style="border-radius:10px;" value="{load_t1}">
              </div>
              <div class="col-md-2">
                <label class="form-label small fw-semibold" style="color:#666;">Trial 2 (cm&sup3;)<span class="text-danger">*</span></label>
                <input type="number" step="0.01" name="trial2" class="form-control" style="border-radius:10px;" value="{load_t2}">
              </div>
              <div class="col-md-2">
                <label class="form-label small fw-semibold" style="color:#666;">Trial 3 (cm&sup3;)<span class="text-danger">*</span></label>
                <input type="number" step="0.01" name="trial3" class="form-control" style="border-radius:10px;" value="{load_t3}">
              </div>
              <div class="col-md-3">
                <label class="form-label small fw-semibold" style="color:#666;">Average Volume</label>
                <input type="text" name="average" class="form-control fw-bold" style="border-radius:10px; background:#f8f9fa;" readonly value="{load_avg}">
              </div>
              <div class="col-md-3">
                <label class="form-label small fw-semibold" style="color:#666;">
                    Measured pH <span style="font-size: 0.7rem; color: #999;">(Range: 0-14)</span><span class="text-danger">*</span>
                </label>
                <input type="number" 
                    step="0.01" 
                    min="0" 
                    max="14" 
                    name="ph_temp" 
                    class="form-control" 
                    style="border-radius:10px;" 
                    placeholder="0.00" 
                    value="{load_ph}" 
                    oninvalid="this.setCustomValidity('pH must be between 0 and 14')" 
                    oninput="this.setCustomValidity('')"
                    required>
              </div>
            </div>

            <div class="mb-4">
              <label class="form-label small fw-semibold" style="color:#666;">Observations<span class="text-danger">*</span></label>
              <textarea name="observation" class="form-control" style="border-radius:10px;" rows="2">{load_obs}</textarea>
            </div>

            <div class="d-flex justify-content-end gap-3 pt-3 border-top">
              <button type="submit" name="recalculate" value="1" class="btn btn-outline-custom">
                  <i class="bi bi-calculator me-1"></i> Recalculate Average
              </button>
              <button type="submit" name="save_update" value="1" class="btn btn-primary-custom">
                  <i class="bi bi-check-lg me-1"></i> Update Experiment
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    """

    # ===================== GRAPH SECTION =====================
    if show_graph_form:
        page += """
    <div class="container-fluid px-4 pb-5" style="max-width: 1300px;">
        <div id="graph-dashboard" class="form-box p-0" style="display:flex; gap:0; overflow:hidden; border-top:4px solid var(--t-green); min-height:480px;">
            <!-- Sidebar -->
            <div id="graph-sidebar" style="flex:0 0 320px; padding:32px; border-right:1px solid #eee;">
                <div class="d-flex align-items-center gap-3 mb-4">
                    <div style="width:42px;height:42px;background:#eef6f4;border-radius:12px;display:flex;align-items:center;justify-content:center;">
                        <i class="bi bi-bar-chart-line-fill" style="color:var(--t-green); font-size:1.1rem;"></i>
                    </div>
                    <div>
                        <h5 class="fw-bold mb-0" style="color:var(--t-green); font-size:1.05rem;">Graph Analysis</h5>
                        <p class="text-muted mb-0" style="font-size:0.78rem;">Visualize titration data</p>
                    </div>
                </div>

                <div class="mb-3">
                    <label class="form-label small fw-semibold" style="color:#666;">Titration ID</label>
                    <div class="input-group">
                        <span class="input-group-text fw-bold" style="border-radius:10px 0 0 10px; background:#eef6f4; color:var(--t-green); border-color:#ddd;">ID#</span>
                        <input type="number" id="graph-id-input" class="form-control" style="border-radius:0 10px 10px 0;" placeholder="Enter ID" oninput="checkGraphIdExistsJS(this.value)">
                    </div>
                    <div id="graphFeedback" class="mt-2 small fw-bold" style="height:20px;"></div>
                </div>
                <button onclick="generateGraph()" class="btn btn-primary-custom w-100" style="padding:12px;">
                    <i class="bi bi-play-fill me-1"></i> UPDATE PLOT
                </button>
            </div>
            <!-- Chart Area -->
            <div id="chart-view" style="flex:1; padding:32px; background:#fafaf8; position:relative;">
                <div id="clear-btn-container" style="display:none; position:absolute; top:18px; right:22px; z-index:10;">
                    <button onclick="resetGraphView()" class="btn btn-sm" style="border:1px solid #ddd; color:#888; font-size:0.75rem; background:white; border-radius:8px; padding:4px 12px;">
                        <i class="bi bi-x-lg me-1"></i>Clear
                    </button>
                </div>
                <div id="placeholder-text" style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); text-align:center; color:#ccc;">
                    <i class="bi bi-graph-up" style="font-size:3.5rem; display:block; margin-bottom:12px; opacity:0.3;"></i>
                    <p class="fw-semibold" style="font-size:0.95rem;">Awaiting Data...</p>
                    <p class="small" style="opacity:0.6;">Enter an ID to generate a graph</p>
                </div>
                <div id="actual-content" style="display:none;">
                    <div style="background:white; border:1px solid #eee; border-radius:12px; padding:25px;">
                        <canvas id="titrationChart" style="height:420px; width:100%;"></canvas>
                    </div>
                    <div id="reaction-result" class="mt-4"></div>
                </div>
            </div>
        </div>
    </div>
    """

    # ===================== JAVASCRIPT =====================
    page += """
<script>
    function toggleMobileMenu() {
        document.getElementById('mobileMenu').classList.toggle('show');
    }
    document.addEventListener('click', function(e) {
        const menu = document.getElementById('mobileMenu');
        const toggle = document.querySelector('.menu-toggle');
        if (menu && !menu.contains(e.target) && !toggle.contains(e.target)) {
            menu.classList.remove('show');
        }
    });

    function getExistingIds() {
        let ids = [];
        document.querySelectorAll(".titration-id-cell").forEach(cell => {
            ids.push(cell.textContent.trim());
        });
        return ids;
    }

    function checkIdExists(value, feedbackId, foundMsg, notFoundMsg) {
        const feedback = document.getElementById(feedbackId);
        if (!feedback) return;
        const searchId = value ? value.toString().trim() : "";
        if (!searchId) { feedback.textContent = ""; return; }
        if (getExistingIds().includes(searchId)) {
            feedback.textContent = foundMsg;
            feedback.style.color = "#16a34a";
        } else {
            feedback.textContent = notFoundMsg;
            feedback.style.color = "#dc2626";
        }
    }

    function checkExperimentExistsJS(value) {
        checkIdExists(value, "deleteFeedback", "✔ Record found", "✖ No record found with this ID");
    }
    function checkGraphIdExistsJS(value) {
        checkIdExists(value, "graphFeedback", "✔ Record found — ready to graph", "✖ ID not in table");
    }
    function checkLoadIdExistsJS(value) {
        checkIdExists(value, "loadFeedback", "✔ Record found — ready to load", "✖ ID not in table");
    }

    // ---- Client-side Calculate Average ----
    (function() {
        const form = document.getElementById('addExperimentForm');
        if (!form) return;

        const calcBtn = document.getElementById('calcAverageBtn');
        const addBtn = document.getElementById('addExperimentBtn');
        const avgField = form.querySelector('input[name="average"]');

        if (calcBtn) {
            calcBtn.addEventListener('click', function() {
                const t1 = parseFloat(form.querySelector('input[name="trial1"]').value) || 0;
                const t2 = parseFloat(form.querySelector('input[name="trial2"]').value) || 0;
                const t3 = parseFloat(form.querySelector('input[name="trial3"]').value) || 0;
                const avg = ((t1 + t2 + t3) / 3).toFixed(2);
                avgField.value = avg;
                if (addBtn) addBtn.disabled = false;
            });
        }

        // ---- Unsaved changes warning ----
        let formDirty = false;
        const fields = form.querySelectorAll('input:not([type="hidden"]):not([readonly]), textarea');
        fields.forEach(function(el) {
            el.addEventListener('input', function() { formDirty = true; });
        });
        form.addEventListener('submit', function() { formDirty = false; });
        window.addEventListener('beforeunload', function(e) {
            if (formDirty) {
                e.preventDefault();
                e.returnValue = '';
            }
        });
    })();

    let myChart = null; 

    function resetGraphView() {
        document.getElementById('placeholder-text').style.display = 'block';
        document.getElementById('actual-content').style.display = 'none';
        document.getElementById('clear-btn-container').style.display = 'none';
        document.getElementById('graph-id-input').value = "";
        document.getElementById('graphFeedback').textContent = "";
        if(myChart) { myChart.destroy(); myChart = null; }
    }

    function generateGraph() {
        const targetId = document.getElementById('graph-id-input').value;
        let t1, t2, t3, avgVol, phValue, titrantName, standardName, observation;

        document.querySelectorAll("tbody tr").forEach(row => {
            const idCell = row.querySelector(".titration-id-cell");
            if (idCell && idCell.textContent.trim() === targetId) {
                const cells = row.querySelectorAll("td");
                standardName = cells[2].textContent;
                titrantName = cells[3].textContent;
                t1 = parseFloat(cells[4].textContent);
                t2 = parseFloat(cells[5].textContent);
                t3 = parseFloat(cells[6].textContent);
                avgVol = parseFloat(cells[7].textContent); 
                phValue = parseFloat(cells[8].textContent); 
                observation = cells[9].textContent;
            }
        });

        if (isNaN(phValue)) {
            alert("ID not found! Please check the table for the correct Titration ID.");
            return;
        }

        document.getElementById('placeholder-text').style.display = 'none';
        document.getElementById('actual-content').style.display = 'block';
        document.getElementById('clear-btn-container').style.display = 'block';

        const resultDiv = document.getElementById('reaction-result');
        let themeColor, bgColor, statusText;

        if (phValue < 7) {
            themeColor = "#b02a37"; bgColor = "#fdf2f2"; statusText = "ACIDIC";
        } else if (phValue > 7) {
            themeColor = "#0a58ca"; bgColor = "#f0f7ff"; statusText = "BASIC";
        } else {
            themeColor = "#146c43"; bgColor = "#f0fdf4"; statusText = "NEUTRAL";
        }

        resultDiv.style.all = "unset"; 
        resultDiv.style.display = "block";
        resultDiv.style.marginTop = "25px";
        resultDiv.style.padding = "24px";
        resultDiv.style.borderRadius = "14px";
        resultDiv.style.backgroundColor = bgColor;
        resultDiv.style.border = `1px solid ${themeColor}22`;
        resultDiv.style.borderLeft = `5px solid ${themeColor}`;

        resultDiv.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid ${themeColor}22; padding-bottom:12px; margin-bottom:18px;">
                <h5 style="margin:0; color:${themeColor}; font-weight:800; letter-spacing:1px; font-family:'Outfit',sans-serif; font-size:1rem;">ANALYTICAL REPORT</h5>
                <span style="font-size:0.78rem; background:white; padding:4px 10px; border-radius:6px; border:1px solid #eee; color:#888;">Lab ID: #00${targetId}</span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:20px;">
                <div style="border-right:1px solid #eee; padding-right:16px;">
                    <label style="font-size:0.68rem; text-transform:uppercase; color:#999; font-weight:700; letter-spacing:1px;">Final State</label>
                    <div style="font-size:1.8rem; font-weight:900; color:#222; margin-top:4px;">${statusText}</div>
                    <div style="font-size:1.05rem; color:${themeColor}; font-weight:600;">pH ${phValue.toFixed(2)}</div>
                </div>
                <div style="border-right:1px solid #eee; padding-right:16px;">
                    <label style="font-size:0.68rem; text-transform:uppercase; color:#999; font-weight:700; letter-spacing:1px;">Reagents</label>
                    <div style="font-size:0.88rem; margin-top:6px;"><strong>Standard:</strong> ${standardName}</div>
                    <div style="font-size:0.88rem;"><strong>Titrant:</strong> ${titrantName}</div>
                    <div style="font-size:0.88rem;"><strong>Avg Vol:</strong> ${avgVol.toFixed(2)} cm³</div>
                </div>
                <div>
                    <label style="font-size:0.68rem; text-transform:uppercase; color:#999; font-weight:700; letter-spacing:1px;">Observations</label>
                    <p style="font-size:0.85rem; font-style:italic; color:#666; margin-top:6px; line-height:1.5;">"${observation || "Equivalence reached with visible color change."}"</p>
                </div>
            </div>
            <div style="margin-top:16px; padding-top:12px; border-top:1px dashed #ddd; font-size:0.78rem; color:#999;">
                <strong>Note:</strong> pH ${phValue < 7 ? '< 7 indicates acidic' : phValue > 7 ? '> 7 indicates basic' : '= 7 indicates neutral'} solution characteristics.
            </div>`;

        const ctx = document.getElementById('titrationChart').getContext('2d');
        if(myChart) { myChart.destroy(); }

        myChart = new Chart(ctx, {
          type: 'line',
          data: {
              labels: ['Trial 1', 'Trial 2', 'Trial 3', 'Average'],
              datasets: [{
                  label: 'Volume (cm³)',
                  data: [t1, t2, t3, avgVol],
                  borderColor: themeColor, 
                  backgroundColor: themeColor + '15',
                  fill: true,
                  tension: 0.35,
                  pointRadius: 8,
                  pointHoverRadius: 12,
                  pointBackgroundColor: '#b1d3cb',
                  pointBorderColor: themeColor,
                  pointBorderWidth: 3,
                  borderWidth: 3
              }]
          },
          options: {
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                  y: {
                      title: { display: true, text: 'Measured Volume (cm³)', font: { size: 13, weight: '600' }, color: '#999' },
                      ticks: { font: { size: 12 }, color: '#999' },
                      grid: { color: 'rgba(0,0,0,0.04)', drawBorder: false }
                  },
                  x: {
                      title: { display: true, text: 'Experimental Iterations', font: { size: 13, weight: '600' }, color: '#999' },
                      ticks: { font: { size: 12 }, color: '#999' },
                      grid: { display: false }
                  }
              },
              plugins: {
                  title: {
                      display: true,
                      text: 'Volumetric Analysis: ' + standardName,
                      font: { size: 16, weight: '700', family: "'Outfit', sans-serif" },
                      color: themeColor,
                      padding: { bottom: 20 }
                  },
                  legend: { display: false },
                  tooltip: {
                      backgroundColor: '#002c23',
                      titleColor: '#b1d3cb',
                      bodyColor: '#fff',
                      cornerRadius: 10,
                      padding: 12
                  }
              }
          }
      });
    }
</script>

<script>
function validateDate() {
    const dateInput = document.getElementById('exp_date');
    const dateAlert = document.getElementById('date-alert');
    const addBtn = document.getElementById('addExperimentBtn');
    
    if (!dateInput.value) return;

    // 1. Get Today's date but strip the time (set to midnight)
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    // 2. Get Selected date (JavaScript Date objects from inputs are UTC midnight by default)
    // We split the string to ensure it doesn't shift timezones
    const [year, month, day] = dateInput.value.split('-');
    const selectedDate = new Date(year, month - 1, day);

    // 3. Compare: Only show alert if selectedDate is STRICTLY after today
    if (selectedDate > today) {
        dateAlert.style.display = 'block';
        dateInput.style.borderColor = '#dc3545'; // Red border
    } else {
        dateAlert.style.display = 'none';
        dateInput.style.borderColor = '#b1d3cc'; // Normal border
    }
}
</script>

<script>
document.getElementById('calcAverageBtn').addEventListener('click', function() {
    // Get the three trial values
    let t1 = parseFloat(document.getElementsByName('trial1')[0].value) || 0;
    let t2 = parseFloat(document.getElementsByName('trial2')[0].value) || 0;
    let t3 = parseFloat(document.getElementsByName('trial3')[0].value) || 0;

    if (t1 > 0 && t2 > 0 && t3 > 0) {
        // Calculate the average
        let avg = ((t1 + t2 + t3) / 3).toFixed(2);
        
        // Put the result in the Average Volume box
        document.getElementsByName('average')[0].value = avg;
        
        // --- THE MAGIC LINE ---
        // This removes the 'disabled' attribute from your Add Experiment button
        document.getElementById('addExperimentBtn').removeAttribute('disabled');
        
        // Optional: Make the button look 'active'
        document.getElementById('addExperimentBtn').style.opacity = "1";
    } else {
        alert("Please enter all 3 trial volumes first!");
    }
});
</script>

<footer class="main-footer">
        <p>TEMP &copy; 2026 &middot; Powered by Python http.server & MySQL • Bootstrap 5</p>
</footer>

</body></html>
"""
    # ---The Header Modal HTML ---
    edit_header_modal = f"""
        <div class="modal fade" id="editHeaderModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content" style="border-radius: 24px; border: none; overflow: hidden; box-shadow: 0 25px 50px rgba(0,0,0,0.3);">
                        
                    <div class="modal-header px-4 py-4" style="background: var(--t-green); border: none;">
                        <div class="d-flex align-items-center">
                            <div style="background: rgba(177,211,203,0.2); padding: 12px; border-radius: 15px; margin-right: 15px;">
                                <i class="bi bi-magic" style="color: var(--t-gold); font-size: 1.5rem;"></i>
                            </div>
                            <div>
                                <h5 class="modal-title fw-bold text-white mb-0" style="font-family: 'Inter',sans-serif;"> Edit Header Name & Logo </h5>
                                <p class="text-white-50 small mb-0">Live preview your changes before applying the new changes.</p>
                            </div>
                        </div>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <form method="POST" action="/admin-dashboard" id="brandingForm">
                        <div class="modal-body p-0">
                            <div class="row g-0">
                                    
                                <div class="col-md-7 p-4 border-end bg-white">
                                    <input type="hidden" name="action" value="update_header">
                                    <input type="hidden" name="logo_base64" id="logo_base64">
                                        
                                    <div class="mb-4">
                                        <label class="form-label fw-bold small text-muted text-uppercase" style="letter-spacing: 1px;">Header Name_Temp</label>
                                        <input type="text" id="nameInput" name="new_header_name" class="form-control form-control-lg" value="{curr_title}" style="border-radius: 12px; background: #f8f9fa; border: 1px solid #eee; font-size: 1rem;" placeholder="Enter new header name...">
                                    </div>

                                    <div class="mb-2">
                                        <label class="form-label fw-bold small text-muted text-uppercase" style="letter-spacing: 1px;">Header Logo_Temp</label>
                                        <input type="file" id="filePicker" class="form-control" accept="image/*" style="border-radius: 12px; background: #f8f9fa; border: 1px solid #eee;">
                                        <div class="form-text mt-3 p-2 rounded" style="background: #eef6f4; color: var(--t-green); font-size: 0.75rem;">
                                        </div>
                                    </div>
                                </div>

                                <div class="col-md-5 p-4 d-flex flex-column justify-content-center align-items-center" style="background-color: #fafafa;">
                                    <div id="previewCard" class="preview-card p-4 bg-white text-center" style="border-radius: 20px; width: 100%; border: 1px dashed #ced4da; transition: all 0.3s ease;">
                                        <p class="small text-muted fw-bold mb-3" style="font-size: 0.6rem; letter-spacing: 2px;">LIVE PREVIEW</p>
                                            
                                        <div class="mb-3" style="min-height: 60px; display: flex; align-items: center; justify-content: center;">
                                            <img id="imagePreview" src="{curr_logo}" alt="Logo" style="max-height: 55px; width: auto; transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);" onerror="this.src='https://cdn-icons-png.flaticon.com/512/1048/1048944.png'">
                                        </div>
                                            
                                        <h6 id="namePreview" class="fw-bold m-0" style="color: var(--t-green); font-family: 'Inter', sans-serif; font-size: 1.15rem; word-break: break-all;">{curr_title}</h6>
                                            
                                        <div class="mt-3 py-1 px-3 rounded-pill d-inline-block" style="background: var(--t-cream); color: var(--t-green); font-size: 0.6rem; font-weight: 700; letter-spacing: 0.5px;">
                                            DASHBOARD VIEW
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="modal-footer p-4 bg-white border-0">
                            <button type="submit" class="btn w-100 py-3 fw-bold" style="background: var(--t-gold); color: var(--t-green); border-radius: 14px; box-shadow: 0 4px 15px rgba(177,211,203,0.4); border: none; transition: transform 0.2s;">
                                UPDATE HEADER SYSTEM
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <script>
        (function() {{
            // Elements
            const nameInput = document.getElementById('nameInput');
            const namePreview = document.getElementById('namePreview');            const filePicker = document.getElementById('filePicker');
            const imagePreview = document.getElementById('imagePreview');
            const base64Input = document.getElementById('logo_base64');

            // 1. Live Typing Preview
            nameInput.addEventListener('input', function(e) {{
                namePreview.textContent = e.target.value || "Untitled Lab";
            }});

            // 2. Live File Preview + Base64 Conversion
            filePicker.addEventListener('change', function(e) {{
                const file = e.target.files[0];
                if (file) {{
                    const reader = new FileReader();
                    reader.onload = function(event) {{
                        // Update the image src in the preview
                        imagePreview.src = event.target.result;
                        // Put the Base64 string into the hidden field for Python
                        base64Input.value = event.target.result;
                        
                        // Small "pop" animation
                        imagePreview.style.transform = "scale(1.15)";
                        setTimeout(() => imagePreview.style.transform = "scale(1)", 250);
                    }};
                    reader.readAsDataURL(file);
                }}
            }});
        }})();
        </script>
        """
    page += edit_header_modal
    return page

# ============================================================================
# HTTP HANDLER AND SERVER
# ============================================================================

CONTENT_TYPE_HTML = "text/html"
CONTENT_TYPE_IMAGE = "image/png"
# ---------- Apphandler------- #Christina, Sana, Seyoung & Abarnna
class AppHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        username = "User"
        cookie = self.headers.get("Cookie")

        if cookie:
            parts = cookie.split(";")
            for part in parts:
                if "username=" in part:
                    raw_username = part.strip().split("=")[1]
                    username = unquote(raw_username)
                if "username" in query_params:
                    username = query_params["username"][0]
        if path == "/":
            page = render_main_page(username=username)

        if path == "/logout":
            self.send_response(303)
            self.send_header("Location", "/?logged_out=true")
            self.end_headers()
            return

        if path == "/":
            logout_msg = ""
            if "logged_out" in query_params:
                logout_msg = """
                <div class='alert alert-success py-2 small text-center mb-4' 
                     style='border-radius:12px; background:rgba(25, 135, 84, 0.1); border:1px solid rgba(25, 135, 84, 0.2); color:#198754;'>
                    <i class='bi bi-check-circle-fill me-2'></i>You have been successfully logged out.
                </div>"""
            
            # Make sure render_login_page accepts 'message' as an argument
            page = render_admin_login_page(message=logout_msg)
            self._send_html(page)

        # --- About Page ---#Christina #Seyoung #Abarnna
        if path == '/about':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            response = render_about_page(username=username) 
            self.wfile.write(response.encode('utf-8'))
            return
        
        # --- Serve Images --- #Sana
        if path.startswith("/images/"):
            try:
                with open("." + path, "rb") as f:
                    self.send_response(200)
                    self.send_header("Content-Type", CONTENT_TYPE_IMAGE)
                    self.end_headers()
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_error(404)
            return

        # --- THE IMAGE SERVER ---#Sana
        if self.path.startswith("/images/"):
            try:
                clean_path = self.path.split('?')[0].lstrip('/')
                clean_path = clean_path.replace('\\', '/')

                if os.path.exists(clean_path):
                    self.send_response(200)
                    if clean_path.lower().endswith(".png"):
                        self.send_header("Content-Type", "image/png")
                    elif clean_path.lower().endswith((".jpg", ".jpeg")):
                        self.send_header("Content-Type", "image/jpeg")
                    self.end_headers()
                    
                    with open(clean_path, "rb") as f:
                        self.wfile.write(f.read())
                    return 
            except Exception as e:
                print(f"Image Error: {e}")
                self.send_error(404)
                return
        
        # FETCH HEADER DATA (Title and Logo variables)#Sana
        curr_title, curr_logo = header_data_temp()

        # --- Page Routing ---
        if path == "/signup":
            page = render_signup_page()
        elif path == "/main":
            username = query_params.get("username", [""])[0]
            show_add_form = query_params.get("show_add_form", ["0"])[0] == "1"
            show_delete_form = query_params.get("show_delete_form", ["0"])[0] == "1"
            show_graph_form = query_params.get("show_graph_form", ["0"])[0] == "1"
            show_load_form = query_params.get("show_load_form", ["0"])[0] == "1"
            page = render_main_page(
                username=username,
                show_add_form=show_add_form,
                show_delete_form=show_delete_form,
                show_graph_form=show_graph_form,
                show_load_form=show_load_form
            )
        else:
            page = render_admin_login_page()

        self.send_response(200)
        self.send_header("Content-Type", CONTENT_TYPE_HTML)
        self.end_headers()
        self.wfile.write(page.encode())

    def get_username_from_cookie(self):
        cookie = self.headers.get("Cookie")
        if not cookie:
            return "User"

        for part in cookie.split(";"):
            if part.strip().startswith("username="):
                return unquote(part.strip().split("=", 1)[1])
        return "User"

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = parse_qs(self.rfile.read(length).decode())
        action = data.get("action", [""])[0]
        username_temp = self.get_username_from_cookie()

        # ==================== UPDATE HEADER ====================#Sana #Christina
        if action == "update_header":
            new_name = data.get("new_header_name", [""])[0]
            logo_data = data.get("logo_base64", [""])[0]
            
            saved_path = save_logo_to_folder(logo_data)
            
            if not saved_path:
                conn = get_connection_temp()
                cur = conn.cursor()
                cur.execute("SELECT header_image_temp FROM header_data_temp WHERE header_id_temp = 1")
                row = cur.fetchone()
                saved_path = row[0] if row else ""
                cur.close()
                conn.close()
                
            update_header_in_db(new_name, saved_path)
            
            message = """
            <div class="alert alert-success" style="padding: 5px 15px; font-size: 1rem;">
                <i class="bi bi-check2-circle"></i> Header Name and Logo updated successfully!
            </div>
            """

            page = render_main_page(username=username_temp, message=message) 
            self._send_html(page)
            return

        # ==================== SEARCH (BINARY) ==================== #Seyoung
        if action == "search":
            column = data.get("search_column", [""])[0]
            value = data.get("search_value", [""])[0].lower()

            all_rows = get_experiments()
            col_index = COLUMN_INDEX_MAP.get(column)

            if col_index is not None and value:
                all_rows.sort(key=lambda row: str(row[col_index]).lower())
                filtered_rows = binary_search_rows(all_rows, col_index, value)
            else:
                filtered_rows = all_rows

            page = render_main_page(
                username=username_temp,
                search_column=column,
                search_value=value,
                search_rows=filtered_rows
            )
            self._send_html(page)
            return

        # ==================== UPDATE ABOUT HERO ==================== #Christina #Abarnna
        if action == "update_hero":
            hero_title = data.get("hero_title", ["About Us."])[0]
            hero_description = data.get("hero_description", [""])[0]
            hero_badge = data.get("hero_badge", [""])[0]
            update_about_hero_content(hero_title, hero_description, hero_badge)
            self.send_response(302)
            self.send_header("Location", f"/about?username={quote(username_temp)}")
            self.end_headers()
            return

        # ==================== UPDATE ABOUT PROJECT ==================== #Christina #Abarnna
        if action == "update_project":
            project_title = data.get("project_title", ["The Project Scope"])[0]
            project_tag = data.get("project_tag", ["ABOUT TEMP"])[0]
            project_p1 = data.get("project_p1", [""])[0]
            project_p2 = data.get("project_p2", [""])[0]
            project_p3 = data.get("project_p3", [""])[0]
            update_about_project_content(project_title, project_tag, project_p1, project_p2, project_p3)
            self.send_response(302)
            self.send_header("Location", f"/about?username={quote(username_temp)}")
            self.end_headers()
            return

        # ==================== UPDATE ABOUT TEAM MEMBER ==================== #Christina #Abarnna
        if action == "update_team":
            member_id = data.get("member_id", [""])[0]
            member_name = data.get("member_name", [""])[0]
            member_role = data.get("member_role", ["Developer"])[0]
            member_image = data.get("member_image", [""])[0]
            if member_id.isdigit():
                update_team_member(int(member_id), member_name, member_role, member_image if member_image else None)
            self.send_response(302)
            self.send_header("Location", f"/about?username={quote(username_temp)}")
            self.end_headers()
            return


        # ==================== TOGGLE ADD FORM ==================== #Sana
        if action == "toggle_add_form":
            show_val = data.get("show_add_form", ["0"])[0]
            self.send_response(302)
            self.send_header("Location", f"/main?show_add_form={show_val}&username={quote(username_temp)}")
            self.end_headers()
            return

        # ==================== TOGGLE DELETE FORM ==================== #Sana
        if action == "toggle_delete_form":
            show_val = data.get("show_delete_form", ["0"])[0]
            self.send_response(302)
            self.send_header("Location", f"/main?show_delete_form={show_val}&username={quote(username_temp)}")
            self.end_headers()
            return

        # ==================== TOGGLE GRAPH FORM ==================== #Sana
        if action == "toggle_graph_form":
            show_val = data.get("show_graph_form", ["0"])[0]
            self.send_response(302)
            self.send_header("Location", f"/main?show_graph_form={show_val}&username={quote(username_temp)}")
            self.end_headers()
            return

        # ==================== TOGGLE LOAD/UPDATE FORM ==================== #Abarnna
        if action == "toggle_load_form":
            show_val = data.get("show_load_form", ["0"])[0]
            self.send_response(302)
            self.send_header("Location", f"/main?show_load_form={show_val}&username={quote(username_temp)}")
            self.end_headers()
            return

        # ==================== LOAD EXPERIMENT (by ID) ==================== #Abarnna
        if action == "load_experiment":
            load_id = data.get("load_id", [""])[0].strip()
            if load_id.isdigit():
                record = get_experiment_by_id(int(load_id))
                if record:
                    page = render_main_page(
                        username=username_temp,
                        show_load_form=True,
                        load_record_data=record
                    )
                else:
                    page = render_main_page(
                        username=username_temp,
                        show_load_form=True,
                        error="<div class='alert alert-danger'>No experiment found with that ID.</div>"
                    )
            else:
                page = render_main_page(
                    username=username_temp,
                    show_load_form=True,
                    error="<div class='alert alert-danger'>Please enter a valid numeric ID.</div>"
                )
            self._send_html(page)
            return

        # ==================== UPDATE EXPERIMENT ==================== #Abarnna
        if action == "update_experiment":
            update_id = data.get("update_id", [""])[0].strip()
            titrant_name = data.get("titrant_name", [""])[0]
            standard_solution = data.get("standard_solution", [""])[0]
            exp_date = data.get("exp_date", [""])[0]
            trial1 = data.get("trial1", ["0"])[0]
            trial2 = data.get("trial2", ["0"])[0]
            trial3 = data.get("trial3", ["0"])[0]
            ph_value_input = data.get("ph_temp", ["0.00"])[0] 
            observation = data.get("observation", [""])[0]

            try:
                t1, t2, t3 = float(trial1), float(trial2), float(trial3)
                average = round((t1 + t2 + t3) / 3, 2)
            except (ValueError, TypeError):
                average = "0.00"

            record_data = {
                "titration_id": update_id, 
                "date": exp_date,
                "titrant_name": titrant_name, 
                "standard_solution": standard_solution,
                "trial1": trial1, 
                "trial2": trial2, 
                "trial3": trial3,
                "average": average, 
                "ph_temp": ph_value_input, 
                "observation": observation
            }

            if "recalculate" in data:
                page = render_main_page(username=username_temp, show_load_form=True, load_record_data=record_data)
                self._send_html(page)
                return

            if "save_update" in data and update_id.isdigit():
                try:
                    ph_final = float(ph_value_input)
                    
                    if ph_final < 0 or ph_final > 14:
                        error_msg = "<div class='alert alert-danger'>⚠ <strong>pH Error:</strong> Value must be between 0.00 and 14.00!</div>"
                        page = render_main_page(
                            username=username_temp, 
                            error=error_msg, 
                            show_load_form=True, 
                            load_record_data=record_data
                        )
                        self._send_html(page)
                        return 

                    success = update_experiment(int(update_id), exp_date, titrant_name, standard_solution, t1, t2, t3, average, ph_final, observation)
                    
                    if success:
                        msg = "<div class='alert alert-success'>✔ Experiment updated successfully!</div>"

                        updated_record = get_experiment_by_id(int(update_id))
                        page = render_main_page(username=username_temp, message=msg, show_load_form=True, load_record_data=updated_record)
                    else:
                        page = render_main_page(username=username_temp, error="<div class='alert alert-danger'>ID not found.</div>", show_load_form=True)
                
                except Exception as e:
                    page = render_main_page(username=username_temp, error=f"<div class='alert alert-danger'>Error: {e}</div>", show_load_form=True, load_record_data=record_data)
                
                self._send_html(page)
                return
        # ==================== ADMIN SIGNUP ==================== #Christina, Sana, Seyoung & Abarnna
        if action == "signup":
            full_name_temp = data["full_name_temp"][0]
            username_temp = data["username_temp"][0]
            password_temp = data["password_temp"][0]
            confirm_password_temp = data["confirm_password_temp"][0]

            if password_temp != confirm_password_temp:
                error = "<div class='alert alert-danger'>Passwords do not match</div>"
                page = render_signup_page("", error)
            else:
                create_user_temp(full_name_temp, username_temp, password_temp)
                message = "<div class='alert alert-success'>Signup successful! Please login.</div>"
                page = render_admin_login_page(message, "")

 
        # ==================== ADMIN LOGIN ==================== #Christina, Sana, Seyoung & Abarnna
        elif action == "login":
            username_temp = data["username_temp"][0]
            password_temp = data["password_temp"][0]
            row = check_credentials_temp(username_temp, password_temp)

            if row:

                logged_in_user = row[0]
                self.send_response(302)
                self.send_header("Location", f"/main?username={quote(logged_in_user)}")
                self.send_header("Set-Cookie", f"username={quote(logged_in_user)}; Path=/; HttpOnly; Max-Age=3600")
                self.end_headers()
                return 
            else:
                page = render_admin_login_page("", "<div class='alert alert-danger'>Invalid login</div>")

        # ==================== LOGOUT ==================== #Sana #Seyoung
        elif action == "logout":
                message = "<div class='alert alert-info mt-3'>You have been logged out.</div>"
                page = render_admin_login_page(message, "")
            
        # ==================== ADD EXPERIMENT ==================== #Sana
        elif action == "add_experiment":
            message = ""
            titrant_name = data.get("titrant_name", [""])[0]
            standard_solution = data.get("standard_solution", [""])[0]
            exp_date = data.get("exp_date", [""])[0]
            trial1 = data.get("trial1", ["0"])[0]
            trial2 = data.get("trial2", ["0"])[0]
            trial3 = data.get("trial3", ["0"])[0]
            ph_value = data.get("ph_temp", ["0.00"])[0]
            observation = data.get("observation", [""])[0]

            try:
                t1, t2, t3 = float(trial1), float(trial2), float(trial3)
                average = round((t1 + t2 + t3) / 3, 2)
            except (ValueError, TypeError):
                average = ""

            form_data = {
                "titrant_name": titrant_name, "standard_solution": standard_solution,
                "exp_date": exp_date, "trial1": trial1, "trial2": trial2, "trial3": trial3,
                "observation": observation, "ph_temp": ph_value, "average": average
            }

            # --- USER CLICKED CALCULATE ---
            if "calculate" in data:
                page = render_main_page(username=username_temp, message="", show_add_form=True, form_data=form_data)
                self._send_html(page)
                return

            # --- USER CLICKED ADD ---
            elif "add" in data:
                if not titrant_name.strip() or not standard_solution.strip() or not exp_date.strip():
                    message = "<div class='alert alert-warning'>⚠ Please fill in all required fields (*) before saving.</div>"
                    page = render_main_page(username=username_temp, message=message, show_add_form=True, form_data=form_data)
                    self._send_html(page)
                    return 

                try:
                    ph_final = float(ph_value)
                    if ph_final < 0 or ph_final > 14:
                        message = "<div class='alert alert-danger'>⚠ <strong>pH Error:</strong> Value must be between 0.00 and 14.00!</div>"
                        page = render_main_page(username=username_temp, message=message, show_add_form=True, form_data=form_data)
                        self._send_html(page)
                        return 
                except (ValueError, TypeError):
                    ph_final = 0.0

                try:
                    add_experiment(exp_date, titrant_name, standard_solution, t1, t2, t3, average, ph_final, observation)
                    message = "<div class='alert alert-success'>✔ Experiment added successfully!</div>"
                    page = render_main_page(username=username_temp, message=message, show_add_form=False)
                except Exception as e:
                    message = f"<div class='alert alert-danger'>Error adding experiment: {e}</div>"
                    page = render_main_page(username=username_temp, message=message, show_add_form=True, form_data=form_data)
                
                self._send_html(page)
                return

        # ==================== SORT (BUBBLE) ==================== #Sana
        elif action == "sort":
            sort_column = data.get("sort_column", [""])[0]
            sort_order = data.get("sort_order", ["asc"])[0]
            form_data = {"sort_column": sort_column, "sort_order": sort_order}
            page = render_main_page(username=username_temp, show_add_form=False, form_data=form_data)

        # ==================== DELETE EXPERIMENT ==================== #Sana
        elif action == "delete_experiment":
            raw_id = data.get("id_to_delete", [""])[0].strip()
            if not raw_id.isdigit():
                page = render_main_page(
                    username=username_temp,
                    error="<div class='small text-danger'>Invalid ID</div>",
                    show_delete_form=True
                )
                self._send_html(page)
                return

            exp_id = int(raw_id)
            message = ""
            error = ""

            try:
                if delete_experiment(exp_id):
                    message = "<div class='alert alert-success'>Experiment deleted successfully.</div>"
                else:
                    error = "<div class='small text-danger'>Experiment ID does not exist.</div>"
            except Exception as e:
                error = f"<div class='small text-danger text-center'>Error: {e}</div>"

            page = render_main_page(
                username=username_temp,
                message=message,
                error=error,
                show_delete_form=True
            )

        else:
            page = render_main_page(username=username_temp)

        self._send_html(page)

    def _send_html(self, page):
        """Helper to send an HTML response."""
        self.send_response(200)
        self.send_header("Content-Type", CONTENT_TYPE_HTML)
        self.end_headers()
        self.wfile.write(page.encode())

# ---------- RUN ---------- #Christina, Sana, Seyoung & Abarnna
def run_temp():
    server = HTTPServer(("", 8080), AppHandler)
    print("Running on http://localhost:8080")
    server.serve_forever()

if __name__ == "__main__":
    run_temp()