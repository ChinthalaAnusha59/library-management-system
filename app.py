from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret123'  # for flash messages

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

admin_books = [
        {"sno": 1, "title": "Swamy's Complete Manual on Establishment and Administration for Central Government Office", "author": "Muthuswamy and Brinda", "publisher": "Swamy Publishers (P) LTD.", "acc_no": "11"},
        {"sno": 2, "title": "Swamy's Compilation of General Financial Rules", "author": "Muthuswamy and Brinda", "publisher": "Swamy Publishers (P) LTD.", "acc_no": "10"},
        {"sno": 3, "title": "Swamy's Compilation on Group Insurance Schemes", "author": "Muthuswamy and Brinda", "publisher": "Swamy Publishers (P) LTD.", "acc_no": "16"},
        {"sno": 4, "title": "Swamy's Compilation of General Provident Fund Rules", "author": "Muthuswamy and Brinda", "publisher": "Swamy Publishers (P) LTD.", "acc_no": "13"},
        {"sno": 5, "title": "T.A Rules Made Easy", "author": "Muthuswamy and Brinda", "publisher": "Swamy Publishers (P) LTD.", "acc_no": "15"},
        {"sno": 6, "title": "Swamy's Compilation on Advances to Central Government Staff", "author": "Muthuswamy and Brinda", "publisher": "Swamy Publishers (P) LTD.", "acc_no": "14"},
        {"sno": 7, "title": "Swamy's Manual on e-Office Procedure", "author": "Muthuswamy and Brinda", "publisher": "Swamy Publishers (P) LTD.", "acc_no": "12"},
        {"sno": 8, "title": "Swamy's Manual on Office Procedure", "author": "Muthuswamy and Brinda", "publisher": "Swamy Publishers (P) LTD.", "acc_no": "17"},
        {"sno": 9, "title": "Swamy's Hand Book 2016", "author": "Muthuswamy and Brinda", "publisher": "Swamy Publishers (P) LTD.", "acc_no": "18"},
        {"sno": 10, "title": "Swamy's Handbook 2018", "author": "Muthuswamy, Brinda Sanjeev", "publisher": "Swamy Publishers (P) LTD.", "acc_no": "19"},
        {"sno": 11, "title": "Swamy's Handbook 2012", "author": "Muthuswamy and Brinda", "publisher": "Swamy Publishers (P) LTD.", "acc_no": "20"},
        {"sno": 12, "title": "Swamy's Compilation of FRSR Part 2", "author": "Muthuswamy and Brinda", "publisher": "Swamy Publishers (P) LTD.", "acc_no": "21"},
        {"sno": 13, "title": "Swamy's Compilation of FRSR Part 3", "author": "Muthuswamy and Brinda", "publisher": "Swamy Publishers (P) LTD.", "acc_no": "22"},
        {"sno": 14, "title": "Swamy's Leave Rules Made Objective", "author": "Muthuswamy and Brinda", "publisher": "Swamy Publishers (P) LTD.", "acc_no": "23"},
        {"sno": 15, "title": "Swamy's Income Tax on Salaries 2016-17", "author": "Muthuswamy, Brinda Sanjeev", "publisher": "Swamy Publishers (P) LTD.", "acc_no": "24"},
        {"sno": 16, "title": "Swamy's Compilation of FRSR Part 1", "author": "Muthuswamy and Brinda", "publisher": "Swamy Publishers (P) LTD.", "acc_no": "30"},
    
        ]
# ---------------- MODELS ---------------- #

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sno = db.Column(db.String(50))
    date = db.Column(db.String(50))
    title = db.Column(db.String(200))
    author = db.Column(db.String(200))
    publisher = db.Column(db.String(200))
    edition = db.Column(db.String(50))
    isbn = db.Column(db.String(100))
    acc_no = db.Column(db.String(100))
    remark = db.Column(db.String(200))
    category = db.Column(db.String(50))


class Viewer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String(100))
    candidate_id = db.Column(db.String(50))
    department = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    borrowed_book = db.Column(db.String(100))
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))


class IssueBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String(100))
    book_title = db.Column(db.String(100))
    date_issued = db.Column(db.DateTime, default=datetime.now)
class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


# ---------------- ROUTES ---------------- #


@app.route('/')
def home():
    return render_template('login.html')


# LOGIN FIXED
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        role = request.form['role']
        username = request.form['username']


        # ---------------- ADMIN LOGIN ----------------
        if role == "admin":

            password = request.form['password']

            if username == "sameerce3" and password == "sameer":

                session["role"] = "admin"
                return redirect('/dashboard')

            else:
                return render_template(
                    'login.html',
                    error="Invalid Admin Credentials!"
                )


        # ---------------- USER LOGIN ----------------
        elif role == "user":

            department = request.form['department']


            viewer = Viewer.query.filter_by(
                username=username,
                department=department,
                role="user"
            ).first()


            # Existing User
            if viewer:

                session["role"] = "user"
                session["username"] = username

                return redirect('/dashboard')


            # New User Auto Register
            else:

                new_user = Viewer(
                    candidate_name=username,
                    username=username,
                    department=department,
                    role="user"
                )

                db.session.add(new_user)
                db.session.commit()


                session["role"] = "user"
                session["username"] = username

                return redirect('/dashboard')


    return render_template('login.html')

@app.route('/dashboard')
def dashboard():

    books = Book.query.all()
    viewers = Viewer.query.all()
    issued_books = IssueBook.query.all()

    # COUNTS
    total_books = Book.query.count()
    technical_books = Book.query.filter_by(category="Technical").count()
    administrative_books = Book.query.filter_by(category="Administrative").count()

    issued_count = IssueBook.query.count()
    available_count = total_books - issued_count
    viewers_count = Viewer.query.count()

    return render_template(
        'dashboard.html',

        books=books,
        viewers=viewers,
        issued_books=issued_books,

        admin_books=admin_books,

        total_books=total_books,
        technical_books=technical_books,
        administrative_books=administrative_books,
        issued_count=issued_count,
        available_count=available_count,
        viewers_count=viewers_count
    )

@app.route('/available_books')
def available_books():
    technical_books = Book.query.filter_by(category="Technical").all()
    administrative_books = Book.query.filter_by(category="Administrative").all()

    return render_template(
        'available_books.html',
        technical_books=technical_books,
        administrative_books=administrative_books
    )
                                                                                 
                                                                                 
@app.route('/issued_books')
def view_issued_books():

    issues = IssueBook.query.all()
    books = Book.query.all()

    candidates = Candidate.query.all()

    return render_template(
        'issued_books.html',
        issued_books=issues,
        books=books,
        candidates=candidates,
        admin_books=admin_books
    )
@app.route('/add_candidate', methods=['POST'])
def add_candidate():

    candidate_name = request.form['candidate_name'].strip()

    if candidate_name:

        existing = Candidate.query.filter_by(
            name=candidate_name
        ).first()

        if not existing:

            db.session.add(
                Candidate(name=candidate_name)
            )

            db.session.commit()

            flash("Candidate added successfully!")

        else:
            flash("Candidate already exists!")

    return redirect(url_for('view_issued_books'))



# 👉 ADD BOOK (POST)
@app.route('/add_issue', methods=['POST'])
def add_issue():

    candidate_name = request.form['candidate_name']
    book_title = request.form['book_title']

    # CHECK IF BOOK ALREADY ISSUED
    existing_issue = IssueBook.query.filter_by(book_title=book_title).first()

    if existing_issue:
        flash("Book already issued!")
        return redirect(url_for('view_issued_books'))

    # ISSUE BOOK
    new_issue = IssueBook(
        candidate_name=candidate_name,
        book_title=book_title
    )

    db.session.add(new_issue)
    db.session.commit()

    flash("Book issued successfully!")

    return redirect(url_for('view_issued_books'))
@app.route('/load_candidates')
def load_candidates():

    names = [
        "Shri Suresh Kumar",
        "Shri B.V.Ramana",
        "Shri A.Vinod Kumar",
        "Shri E Ashok",
        "Shri M.Bala Krishna",
        "Suguna-RS",
        "Siddartha-RS",
        "Suchitra-RS",
        "Niharika-RS",
        "Sravani-PA",
        "Varshini-PA",
        "Tejaswini-PA",
        "Bhagya Sri-PA",
        "Boloka-PA"
    ]

    for name in names:
        existing = Candidate.query.filter_by(name=name).first()

        if not existing:
            db.session.add(Candidate(name=name))

    db.session.commit()

    return "Candidates Loaded Successfully!"
@app.route('/show_candidates')
def show_candidates():

    candidates = Candidate.query.all()

    result = ""

    for c in candidates:
        result += c.name + "<br>"

    return result

@app.route('/delete_issue/<int:id>')
def delete_issue(id):
    issue = IssueBook.query.get_or_404(id)
    
    db.session.delete(issue)
    db.session.commit()
    
    return redirect(url_for('view_issued_books'))


@app.route('/delete_admin_book/<int:sno>')
def delete_admin_book(sno):

    global admin_books

    admin_books = [book for book in admin_books if book['sno'] != sno]

    flash("Administrative book deleted successfully!")

    return redirect(url_for('dashboard'))

# ADD BOOK
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():

    if request.method == 'POST':

        category = request.form['category']

        # TECHNICAL BOOK → DATABASE
        if category == "Technical":

            new_book = Book(
                sno=request.form['sno'],
                date=request.form['date'],
                title=request.form['title'],
                author=request.form['author'],
                publisher=request.form['publisher'],
                edition=request.form['edition'],
                isbn=request.form['isbn'],
                acc_no=request.form['acc_no'],
                remark=request.form['remark'],
                category="Technical"
            )

            db.session.add(new_book)
            db.session.commit()

            flash("Technical Book Added!")

        # ADMINISTRATIVE BOOK → PYTHON LIST
        elif category == "Administrative":

            new_admin_book = {
                "sno": request.form['sno'],
                "title": request.form['title'],
                "author": request.form['author'],
                "publisher": request.form['publisher'],
                "acc_no": request.form['acc_no']
            }

            admin_books.append(new_admin_book)

            flash("Administrative Book Added!")

        return redirect(url_for('available_books'))

    return render_template('add_book.html')


# VIEWERS PAGE
@app.route('/viewers')
def viewers():
    viewers = Viewer.query.all()
    return render_template('viewers.html', viewers=viewers)


# ADD VIEWERS FIXED
@app.route('/add_viewers', methods=['GET', 'POST'])
def add_viewers():

    if request.method == 'POST':

        new_viewer = Viewer(
            candidate_name=request.form['candidate_name'],
            candidate_id=request.form['candidate_id'],
            department=request.form['department'],
            phone=request.form['phone'],
            borrowed_book=request.form['borrowed_book'],
            username=request.form['username'],
            role="user"
        )

        db.session.add(new_viewer)
        db.session.commit()

        flash("User added successfully!")

        return redirect(url_for('viewers'))

    return render_template('add_viewers.html')



@app.route('/delete_book/<int:id>')
def delete_book(id):
    book = Book.query.get(id)

    if book:
        db.session.delete(book)
        db.session.commit()
        flash("Book deleted successfully!")

    return redirect(url_for('available_books'))
@app.route('/edit_issue/<int:id>', methods =['POST'])
def edit_issue(id):
    issue = IssueBook.query.get_or_404(id)

    issue.candidate_name = request.form['candidate_name']
        
    issue.book_title = request.form['book_title']
    db.session.commit()
    return redirect(url_for('view_issued_books'))

@app.route('/delete_candidate/<int:id>')
def delete_candidate(id):

    candidate = Candidate.query.get_or_404(id)

    db.session.delete(candidate)
    db.session.commit()

    flash("Candidate deleted successfully!")

    return redirect(url_for('view_issued_books'))

    

@app.route('/logout')
def logout():

    session.clear()

    flash("Logged out successfully!")

    return redirect(url_for('home'))
@app.route('/delete_viewer/<int:id>')
def delete_viewer(id):
    viewer = Viewer.query.get(id)

    if viewer:
        db.session.delete(viewer)
        db.session.commit()
        flash("viewer deleted successfully!")

    return redirect(url_for('viewers'))  # or 'viewers' based on your function name


# LOAD SAMPLE BOOKS


def load_initial_books():
    books = [
        Book(sno="1", date="30-04-2015", title="Ultra wideband short pulse electromagnetics", author="Carl E. Baum", publisher="Plenum", edition="", isbn="123", acc_no="1", remark=""),
        
        Book(sno="2", date="30-04-2015", title="Electromagnetic compatibility engineering", author="Henry W. Ott", publisher="Wiley", edition="", isbn="456", acc_no="2", remark=""),
        
        Book(sno="3", date="30-04-2015", title="Introduction to electromagnetic compatibility", author="Clayton R. Paul", publisher="John Wiley & Sons", edition="", isbn="978-0-471-75500-5", acc_no="3", remark=""),

        Book(sno="4", date="30-04-2015", title="EMI troubleshooting techniques-II", author="Michel Mardiguian", publisher="McGraw Hill", edition="SECOND", isbn="0-07-134418-7", acc_no="4", remark=""),

        Book(sno="5", date="30-04-2015", title="Electromagnetic shielding", author="Kenneth L. Kaiser", publisher="Taylor & Francis", edition="", isbn="0-8493-6372-1", acc_no="5", remark=""),

        Book(sno="6", date="30-04-2015", title="EMC for product Designers-IV", author="Tim Williams", publisher="Newnes", edition="FOURTH", isbn="0-7506-8170-5", acc_no="6", remark="Missing"),

        Book(sno="7", date="30-04-2015", title=" The Technician’s EMI Handbook", author="Joseph J. Carr", publisher="Newnes", edition="", isbn="978-0-7506-7233-7", acc_no="7", remark=""),

        Book(sno="8", date="30-04-2015", title="Testing for EMC compliance - Apporches and techniques", author="Mark I. Montrose", publisher="John Wiley & Sons", edition="", isbn="978-0-471-43308-8", acc_no="8", remark=""),
        
        Book(sno="9", date="13-05-2015", title="High-speed digital design - A handbook of black magic", author="Howard Johnson", publisher="Prentice Hall", edition="", isbn="0-13-395724-1", acc_no="9", remark=""),

        Book(sno="10", date="04-04-2024", title="Frontiers In Electronics", author="Douglas H. Wener Raj Mittra", publisher="IEEE Press", edition="", isbn="0-7803-4701-3", acc_no="25", remark=""),
        
        Book(sno="11", date="22-01-2024", title="Electrostatic Discharge and Electronic Equipment", author="Avarren Bostikiner", publisher="IEEE Press", edition="", isbn="0-87942-244-0", acc_no="27", remark=""),

        Book(sno="12", date="22-01-2024", title="Printed Circuit Board Design Techniques for EMC Compliance", author="Mark I. Montrose", publisher="IEEE Press", edition="", isbn="0-7803-1131-0", acc_no="28", remark=""),

        Book(sno="13", date="22-01-2024", title="A Handbook for EMC Testing and Measurement", author="David Morgan", publisher="The Institution of Engineering and Technology", edition="", isbn="978-086341756-6", acc_no="29", remark=""),

        Book(sno="14", date="06-02-2024", title="Modern EMC Analysis Techniques V-1", author="Kantartzis", publisher="Springer", edition="", isbn="978-3-031-00577-0", acc_no="31", remark=""),

        Book(sno="15", date="06-02-2024", title="Modern EMC Analysis Techniques V-2", author="Kantartzis", publisher="Springer", edition="", isbn="978-3-031-00587-7", acc_no="32", remark=""),

        Book(sno="16", date="06-02-2024", title="A Hand Book from circuits and systems 2ED (Grounding for Groundings)", author="Elya Joffe", publisher="IEEE Press", edition="SECOND", isbn="978-1-119-77093-0", acc_no="33", remark=""),

        Book(sno="17", date="06-02-2024", title="Spacecraft Electromagnetic Compatibility Technologies", author="Hua-Zhang", publisher="Springer", edition="", isbn="978-981-15-4781-2", acc_no="34", remark=""),

        Book(sno="18", date="06-02-2024", title="Design for Electromagnetic Compatibility - In a Nutshell", author="Keller", publisher="Springer", edition="", isbn="978-3-031-14188-1", acc_no="35", remark=""),

        Book(sno="19", date="06-02-2024", title="Shielding of Electromagnetic Waves", author="Kunkel", publisher="Springer", edition="", isbn="978-3-030-19237-2", acc_no="36", remark=""),

        Book(sno="20", date="04-04-2024", title="Electromagnetic Shielding", author="Kaiser", publisher="CRC Press Taylor & Francis", edition="", isbn="0-8493-6372-1", acc_no="37", remark=""),

        Book(sno="21", date="04-04-2024", title="Fundamentals of Engg Electromagnetics", author="Bansal", publisher="CRC Press Taylor & Francis", edition="", isbn="978-0-8493-7360-2", acc_no="38", remark=""),

        Book(sno="22", date="04-04-2024", title="Electromagnetic Compatibility in Medical", author="Kimmel", publisher="CRC Press Taylor & Francis", edition="", isbn="978-0-367-40156-6", acc_no="39", remark=""),

        Book(sno="23", date="04-04-2024", title="Advanced materials & Design for Electromagnetic Interference Shielding", author="Colin Tong", publisher="CRC Press Taylor & Francis", edition="", isbn="978-1-4200-7358-4", acc_no="40", remark=""),

        Book(sno="24", date="04-04-2024", title="Electromagnetic Compatibility Engineering", author="Henry Ott", publisher="John Wiley & Sons, INC", edition="", isbn="978-0-470-18930-6", acc_no="41", remark=""),

        Book(sno="25", date="04-04-2024", title="Testing for compliance Approaches & Techniques", author="Mark Montrose", publisher="IEEE Press", edition="", isbn="978-0-471-43308-8", acc_no="42", remark=""),

        Book(sno="26", date="04-04-2024", title="Broadband Planner: Antennas Design & Applications", author="Zhi Ning Chen Michael Y. W. Chia", publisher="A John Wiley & Sons, INC", edition="", isbn="0-470-87174-1", acc_no="43", remark=""),

        Book(sno="27", date="04-04-2024", title="Electromagnetic Compatibility Handbook Volume-1", author="Kenneth L. Kaiser", publisher="CRC Press Taylor & Francis", edition="", isbn="978-1-138-38762-1", acc_no="44", remark=""),

        Book(sno="28", date="04-04-2024", title="Electromagnetic Compatibility Handbook Volume-2", author="Kenneth L. Kaiser", publisher="CRC Press Taylor & Francis", edition="", isbn="978-1-138-38762-1", acc_no="45", remark=""),

        Book(sno="29", date="04-04-2024", title="Electromagnetic Compatibility Handbook Volume-3", author="Kenneth L. Kaiser", publisher="CRC Press Taylor & Francis", edition="", isbn="978-1-138-38762-1", acc_no="46", remark=""),

        Book(sno="30", date="04-04-2024", title="Electromagnetics of Time-Varying Complex Media 2nd Edition", author="Dikshitulu Kalluri", publisher="CRC Press Taylor & Francis", edition="SECOND", isbn="978-1-138-49424-9", acc_no="47", remark=""),

        Book(sno="31", date="04-04-2024", title="Electromagnetic and Acoustic Wave Tomography", author="Nathan Blaunstein, Vladimir Yakubov", publisher="CRC Press Taylor & Francis", edition="", isbn="978-1-138-49073-4", acc_no="48", remark=""),

        Book(sno="32", date="04-04-2024", title="Handbook of Biological Effects of Electromagnetic Fields 4E Volume-1", author="Ben Greenebaum, Frank Barnes", publisher="CRC Press Taylor & Francis", edition="4E", isbn="978-1-138-733114", acc_no="49", remark=""),

        Book(sno="33", date="04-04-2024", title="Electromagnetic Scattering and Material Characterization", author="Abbas Omar", publisher="Artech House Publishers", edition="", isbn="13:978-1-59693-216-6", acc_no="51", remark=""),

        Book(sno="34", date="04-04-2024", title="Signal Integrity Applied Electromagnetics and Professional Practice", author="Samuel H. Russ", publisher="Springer", edition="", isbn="978-3-319-29756-9", acc_no="52", remark=""),

        Book(sno="35", date="04-04-2024", title="Engineering Electromagnetics", author="Nathan Ida", publisher="Springer", edition="", isbn="978-3-030-15559-9", acc_no="53", remark=""),

        Book(sno="36", date="04-04-2024", title="Fundamentals of Applied Electromagnetics 8th Edition", author="Fawwaz T. Ulaby", publisher="Global Edition", edition="8th", isbn="13:978-1-292-43673-9", acc_no="54", remark=""),

        Book(sno="37", date="04-04-2024", title="Modern Electromagnetic Scattering Theory with Applications", author="Andrey V. Osipov", publisher="Wiley", edition="", isbn="978-0-470-51238-8", acc_no="55", remark=""),

        Book(sno="38", date="04-04-2024", title="The Physics and Mathematics of Electromagnetic Wave Propagation", author="", publisher="Wiley", edition="", isbn="978-1-119-39311-5", acc_no="56", remark=""),

        Book(sno="39", date="04-04-2024", title="Computational Methods for Electromagnetics", author="Andrew F. Peterson, Scott L. Ray, Raj Mittra", publisher="IEEE Press", edition="", isbn="978-0-7803-1122-0", acc_no="57", remark=""),

        Book(sno="40", date="04-04-2024", title="Electromagnetics for Engineers", author="Fawwaz T. Ulaby", publisher="Pearson Prentice Hall", edition="", isbn="0-13-149724-3", acc_no="58", remark=""),

        Book(sno="41", date="04-04-2024", title="Advanced Engineering Electromagnetics", author="Constantine A. Balanis", publisher="BSB Books Pvt. Ltd", edition="", isbn="978-81-265-1856-2", acc_no="59", remark=""),

        Book(sno="42", date="04-04-2024", title="The Finite Element Method in Electromagnetics 3rd Edition", author="Jian-Ming Jin", publisher="IEEE Press", edition="3rd", isbn="978-81-265-7430-8", acc_no="60", remark=""),
    ]  
    

    for b in books:
        existing = Book.query.filter_by(acc_no=b.acc_no).first()
        if not existing:    
            db.session.add(b)

    db.session.commit()
    
    return Book.query.all()


# ---------------- DB INIT ---------------- #

with app.app_context():
    db.create_all()
    load_initial_books()

# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.run(debug=True)