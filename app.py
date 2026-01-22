from flask import Flask, request, make_response, render_template
import mysql.connector as sql
from mysql.connector import Error
import html

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "nimish",
    "database": "ccms",
}

app = Flask(__name__, template_folder="templates")

def connect_db():
    return sql.connect(**DB_CONFIG)

def create_tables():
    conn = connect_db()
    c1 = conn.cursor()
    c1.execute("""
        CREATE TABLE IF NOT EXISTS Add_new_customer (
            Customer_ID INT AUTO_INCREMENT PRIMARY KEY,
            Customer_name VARCHAR(50) NOT NULL,
            Age INT,
            Address VARCHAR(150),
            Phone_no VARCHAR(20) UNIQUE,
            Email_ID VARCHAR(80)
        )
    """)
    c1.execute("""
        CREATE TABLE IF NOT EXISTS Bill (
            Bill_ID INT AUTO_INCREMENT PRIMARY KEY,
            Customer_ID INT NOT NULL,
            Time_accessed_in_min INT NOT NULL,
            Total_charges DECIMAL(10,2) NOT NULL,
            Bill_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (Customer_ID) REFERENCES Add_new_customer(Customer_ID)
                ON DELETE CASCADE ON UPDATE CASCADE
        )
    """)
    c1.execute("""
        CREATE TABLE IF NOT EXISTS Time_charges (
            id INT AUTO_INCREMENT PRIMARY KEY,
            label VARCHAR(30) DEFAULT 'current',
            Amount_charged DECIMAL(10,2) NOT NULL,
            set_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c1.execute("""
        CREATE TABLE IF NOT EXISTS Admins (
            Admin_ID INT AUTO_INCREMENT PRIMARY KEY,
            Username VARCHAR(30) UNIQUE,
            Password VARCHAR(100)
        )
    """)
    conn.commit()

    # Ensure Password column exists in Add_new_customer
    c1.execute("SHOW COLUMNS FROM Add_new_customer LIKE 'Password'")
    if not c1.fetchone():
        try:
            c1.execute("ALTER TABLE Add_new_customer ADD COLUMN Password VARCHAR(100) AFTER Email_ID")
            conn.commit()
        except Exception:
            pass

    # Insert default admin if missing
    try:
        c1.execute("SELECT Admin_ID FROM Admins WHERE Username=%s", ("admin",))
        if not c1.fetchone():
            c1.execute("INSERT INTO Admins (Username, Password) VALUES (%s, %s)", ("admin", "admin123"))
            conn.commit()
    except Exception:
        pass

    c1.close()
    conn.close()

create_tables()

BLUE_CSS = """
<style>
  :root{
    --bg:#07101a; --panel:#08131a; --muted:#9aa7b7; --text:#e6eef6;
    --blue:#22d3ee; --blue2:#38bdf8; --danger:#ef4444;
  }
  html,body{height:100%;margin:0;background:linear-gradient(180deg,#020617,#051022);color:var(--text);font-family:Inter,system-ui,Segoe UI,Roboto,Arial;}
  .wrap{max-width:1100px;margin:36px auto;padding:18px;}
  .card{background:linear-gradient(180deg,rgba(255,255,255,0.02),transparent);border-radius:12px;padding:18px;border:1px solid rgba(34,211,238,0.06);box-shadow:0 10px 40px rgba(2,6,23,0.6);}
  h1{margin:0 0 12px 0;color:var(--blue);}
  table{width:100%;border-collapse:collapse;margin-top:12px;box-shadow:0 6px 30px rgba(2,6,23,0.6);}
  th,td{padding:10px 12px;border:1px solid rgba(34,211,238,0.08);text-align:left;background:linear-gradient(180deg,rgba(255,255,255,0.01),transparent);}
  th{border-bottom:2px solid rgba(34,211,238,0.12);color:var(--blue);font-weight:600}
  .ok { box-shadow: 0 0 30px rgba(34,211,238,0.06); border-left:4px solid var(--blue2); }
  .err { box-shadow: 0 0 30px rgba(239,68,68,0.06); border-left:4px solid var(--danger); }
  pre{white-space:pre-wrap;color:var(--muted);font-size:13px;padding:8px;background:rgba(0,0,0,0.12);border-radius:6px;}
  .meta{color:var(--muted);font-size:13px;margin-top:8px;}
  a.link{color:var(--blue);text-decoration:none}
</style>
"""

def make_plain_response(title, data=None, ok=True, message=None, status=200):
    content = title + "\n"
    if message:
        content += message + "\n"
    if data is None:
        pass
    elif isinstance(data, dict):
        for k, v in data.items():
            content += f"{k}\n{'' if v is None else str(v)}\n"
    elif isinstance(data, list):
        if not data:
            content += "No rows\n"
        else:
            for r in data:
                for k, v in r.items():
                    content += f"{k}\n{'' if v is None else str(v)}\n"
    else:
        content += str(data) + "\n"
    content += "Back to UI\n"
    resp = make_response(content, status)
    resp.headers["Content-Type"] = "text/plain; charset=utf-8"
    return resp

def make_html_response(title, data=None, ok=True, message=None, status=200):
    cls = "ok" if ok else "err"
    content = "<div class='wrap'><div class='card {cls}'>".format(cls=cls)
    content += f"<h1>{html.escape(title)}</h1>"
    if message:
        content += f"<div class='meta'>{html.escape(message)}</div>"
    if data is None:
        pass
    elif isinstance(data, dict):
        content += dict_to_table(data)
    elif isinstance(data, list):
        content += rows_to_table(data)
    else:
        content += f"<pre>{html.escape(str(data))}</pre>"
    content += "<div style='margin-top:14px' class='meta'><a class='link' href='/'>Back to UI</a></div>"
    content += "</div></div>"
    full = "<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
    full += BLUE_CSS + "</head><body>" + content + "</body></html>"
    resp = make_response(full, status)
    resp.headers["Content-Type"] = "text/html; charset=utf-8"
    return resp

def dict_to_table(data):
    keys = list(data.keys())
    header = "".join(f"<th>{html.escape(str(k))}</th>" for k in keys)
    row = "".join(f"<td>{html.escape('' if v is None else str(v))}</td>" for v in (data[k] for k in keys))
    return f"<table><thead><tr>{header}</tr></thead><tbody><tr>{row}</tr></tbody></table>"

def rows_to_table(rows):
    if not rows:
        return "<div class='meta'>No rows</div>"
    keys = list(rows[0].keys())
    header = "".join(f"<th>{html.escape(str(k))}</th>" for k in keys)
    body = ""
    for r in rows:
        row = "".join(f"<td>{html.escape('' if v is None else str(v))}</td>" for v in (r[k] for k in keys))
        body += f"<tr>{row}</tr>"
    return f"<table><thead><tr>{header}</tr></thead><tbody>{body}</tbody></table>"

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/customers")
def add_customer():
    data = request.get_json(silent=True) or {}
    required = ["Customer_name", "Age", "Address", "Phone_no", "Email_ID", "Password"]
    missing = [k for k in required if k not in data or str(data[k]).strip() == ""]
    if missing:
        return make_html_response("Add Customer — Error", {"error": f"Missing fields: {', '.join(missing)}"}, ok=False, status=400)
    try:
        conn = connect_db()
        c1 = conn.cursor(dictionary=True)
        q = ("INSERT INTO Add_new_customer (Customer_name, Age, Address, Phone_no, Email_ID, Password) "
             "VALUES (%s, %s, %s, %s, %s, %s)")
        c1.execute(q, (
            data["Customer_name"].strip(),
            int(data["Age"]),
            data["Address"].strip(),
            data["Phone_no"].strip(),
            data["Email_ID"].strip(),
            data["Password"].strip(),
        ))
        conn.commit()
        customer_id = c1.lastrowid
        return make_plain_response("Add Customer — Success", {"Customer_ID": customer_id}, ok=True, status=201)
    except Error as e:
        msg = str(e)
        code = 409 if "Duplicate" in msg or "UNIQUE" in msg else 500
        return make_html_response("Add Customer — Error", {"error": msg}, ok=False, status=code)
    finally:
        try:
            c1.close(); conn.close()
        except Exception:
            pass

@app.post("/api/rate")
def set_rate():
    data = request.get_json(silent=True) or {}
    try:
        rate = float(data.get("rate", ""))
        if rate <= 0:
            raise ValueError
    except Exception:
        return make_html_response("Set Rate — Error", {"error": "Invalid rate. Provide a positive number."}, ok=False, status=400)
    try:
        conn = connect_db()
        c1 = conn.cursor()
        c1.execute("INSERT INTO Time_charges (label, Amount_charged) VALUES (%s, %s)", ("current", rate))
        conn.commit()
        return make_html_response("Set Rate — Success", {"rate": rate}, ok=True, status=201)
    except Error as e:
        return make_html_response("Set Rate — Error", {"error": str(e)}, ok=False, status=500)
    finally:
        try:
            c1.close(); conn.close()
        except Exception:
            pass

@app.post("/api/bill")
def generate_bill():
    data = request.get_json(silent=True) or {}
    phone = (data.get("Phone_no") or "").strip()
    try:
        minutes = int(data.get("Time_accessed_in_min"))
        if minutes <= 0:
            raise ValueError
    except Exception:
        return make_html_response("Generate Bill — Error", {"error": "Invalid minutes. Must be a positive integer."}, ok=False, status=400)
    if not phone:
        return make_html_response("Generate Bill — Error", {"error": "Phone_no is required."}, ok=False, status=400)
    try:
        conn = connect_db()
        c1 = conn.cursor(dictionary=True)
        c1.execute("SELECT Customer_ID FROM Add_new_customer WHERE Phone_no=%s", (phone,))
        cust = c1.fetchone()
        if not cust:
            return make_html_response("Generate Bill — Error", {"error": "Customer not found."}, ok=False, status=404)
        customer_id = cust["Customer_ID"]
        c1.execute("SELECT Amount_charged FROM Time_charges ORDER BY set_at DESC, id DESC LIMIT 1")
        row = c1.fetchone()
        rate = float(row["Amount_charged"]) if row else 1.0
        total = round(minutes * rate, 2)
        c1.execute("INSERT INTO Bill (Customer_ID, Time_accessed_in_min, Total_charges) VALUES (%s, %s, %s)",
                   (customer_id, minutes, total))
        conn.commit()
        bill_id = c1.lastrowid
        return make_html_response("Generate Bill — Success", {"Bill_ID": bill_id, "Customer_ID": customer_id, "Rate": rate, "Minutes": minutes, "Total": total}, ok=True, status=201)
    except Error as e:
        return make_html_response("Generate Bill — Error", {"error": str(e)}, ok=False, status=500)
    finally:
        try:
            c1.close(); conn.close()
        except Exception:
            pass

@app.get("/api/customers")
def view_customer():
    phone = (request.args.get("phone") or "").strip()
    if not phone:
        return make_html_response("View Customer — Error", {"error": "Query param 'phone' is required."}, ok=False, status=400)
    try:
        conn = connect_db()
        c1 = conn.cursor(dictionary=True)
        c1.execute("SELECT Customer_ID, Customer_name, Age, Address, Phone_no, Email_ID FROM Add_new_customer WHERE Phone_no=%s", (phone,))
        row = c1.fetchone()
        if not row:
            return make_html_response("View Customer — Error", {"error": "Phone number not in system."}, ok=False, status=404)
        return make_html_response("Customer Details", row, ok=True, status=200)
    except Error as e:
        return make_html_response("View Customer — Error", {"error": str(e)}, ok=False, status=500)
    finally:
        try:
            c1.close(); conn.close()
        except Exception:
            pass

@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    role = (data.get("role") or "").strip().lower()
    if role not in ("admin", "customer"):
        return make_html_response("Login — Error", {"error": "role must be 'admin' or 'customer'"}, ok=False, status=400)
    try:
        conn = connect_db()
        c1 = conn.cursor(dictionary=True)
        if role == "admin":
            username = (data.get("username") or "").strip()
            password = (data.get("password") or "").strip()
            if not username or not password:
                return make_html_response("Login — Error", {"error": "username and password required"}, ok=False, status=400)
            c1.execute("SELECT Admin_ID, Username FROM Admins WHERE Username=%s AND Password=%s", (username, password))
            row = c1.fetchone()
            if not row:
                return make_html_response("Login — Error", {"error": "Invalid admin credentials"}, ok=False, status=401)
            return make_html_response("Login — Admin Success", {"username": row["Username"]}, ok=True, status=200)
        else:
            phone = (data.get("phone") or "").strip()
            password = (data.get("password") or "").strip()
            if not phone or not password:
                return make_html_response("Login — Error", {"error": "phone and password required"}, ok=False, status=400)
            c1.execute("SELECT Customer_ID, Customer_name, Phone_no FROM Add_new_customer WHERE Phone_no=%s AND Password=%s", (phone, password))
            row = c1.fetchone()
            if not row:
                return make_html_response("Login — Error", {"error": "Invalid customer credentials"}, ok=False, status=401)
            return make_html_response("Login — Customer Success", {"phone": row["Phone_no"], "name": row["Customer_name"]}, ok=True, status=200)
    except Error as e:
        return make_html_response("Login — Error", {"error": str(e)}, ok=False, status=500)
    finally:
        try:
            c1.close(); conn.close()
        except Exception:
            pass

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
