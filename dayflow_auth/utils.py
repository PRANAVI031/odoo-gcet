from datetime import datetime

def generate_login_id(company, first, last, db):
    cursor = db.cursor()

    # initials
    company_initials = company.strip().replace(" ", "")[:2].upper()
    first_initials = first.strip()[:2].upper()
    last_initials = last.strip()[:2].upper()
    name_initials = first_initials + last_initials

    year = datetime.now().year

    # get last serial of this year
    cursor.execute(
        "SELECT serial FROM yearly_serials WHERE year=%s ORDER BY id DESC LIMIT 1",
        (year,)
    )
    row = cursor.fetchone()

    new_serial = row[0] + 1 if row else 1

    # store new serial
    cursor.execute(
        "INSERT INTO yearly_serials (year, serial) VALUES (%s,%s)",
        (year, new_serial)
    )
    db.commit()
    cursor.close()

    return f"{company_initials}{name_initials}{year}{str(new_serial).zfill(4)}"
