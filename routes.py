import io, csv, dateutil.parser
from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash, make_response
from flask_login import login_required
from flask_mail import Message
from extensions import mail

main = Blueprint('main', __name__)

'''
specialty_queries is user-defined in constants; allows flexibility later
'''
@main.route('/homepage')
@login_required
def home():
    return render_template('home.html', specialties=specialty_queries)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    return redirect(url_for('main.login'))

'''
deprecated and extremely simple login; we'll make this better soon
'''
@main.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    else:
        if request.method == "POST":
            username = request.form['username']
            pw = request.form['password']
            if username in users and users[username]['password'] == pw:
                user = User(username)
                login_user(user)
                return redirect(url_for('main.homepage'))
            else: return "Invalid credentials", 401
        return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

'''
new search function. much faster
'''
@main.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query', '').strip()
    specialty = request.args.get('specialty', '').strip()
    search_term = specialty if specialty else query
    if not search_term:
        return render_template('home.html')

    results = current_app.search_engine.search(search_term, top_k=5000, threshold=0.5)
    return render_template(
        'search_results.html',
        results=results,
        query=search_term,
        length=len(results),
        display=specialty if specialty else query
        total_pages = (len(results) // 25) + 1 if results else 0
        )
'''
user feature request and bug reports
'''
@main.route('/contact', methods=["GET", "POST"])
@login_required
def contact():
    if request.method == "POST":
        request_type = request.form.get('request_type')
        user_email = request.form.get('user_email')
        msg_body = request.form.get('msg')
        priority= request.form.get('priority')
        msg = Message(
            subject=f"New {request_type} regarding rehab-research.com",
            sender=current_app.config.get("MAIL_USERNAME"),
            recipients=current_app.config.get("ADMINS")
        )
        msg.body = (f"User Email: {user_email}\n\n"
                    f"Request Type: {request_type}\n\n"
                    f"Priority: {priority}\n\n"
                    f"Message:\n{msg_body}")
        try:
            from app import mail
            mail.send(msg)
            flash("Thank you for your feedback! Your message has been received.", 'success')
            return redirect(url_for('main.homepage'))
        except Exception as e:
            current_app.logger.info(f"Exception: {e}")
            flash("Your message failed to send. Please try again later.", "error")
            return redirect(url_for('main.contact'))
    return render_template('contact.html')

def search_page(page, order_criteria, order_asc, show_trials, show_grants):
    per_page = 25
    from app import cache
    user_query = cache.get('query')
    display = cache.get('display')
    results = cache.get(f'search_results_{user_query}')

    if results is None and user_query:
        results = current_app.search_engine.search(user_query)
        cache.set(f"search_results_{user_query}", results)
    elif results is None:
        return redirect(url_for('main.homepage'))

    if not show_trials and not show_grants:
        filtered_results = []
    elif show_trials and show_grants:
        filtered_results = results
    elif show_trials:
        filtered_results = [row for row in results if not row[6]]
    elif show_grants:
        filtered_results = [row for row in results if row[6]]

    reverse = (order_asc == "DESC")
    if order_criteria == "due_date":
        filtered_results.sort(key=lambda x: dateutil.parser.parse(x[3]) if x[3] else dateutil.parser.parse("1900-01-01"),
                              reverse=reverse)
    else:
        filtered_results.sort(key=lambda x: float(x[4]),
                              reverse=reverse)
    total_pages = (len(filtered_results) + per_page - 1) // per_page

    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = filtered_results[start:end]
    return render_template('search_results.html',
                           query=user_query,
                           display=display,
                           show_trials=show_trials,
                           show_grants=show_grants,
                           length=len(filtered_results),
                           results=paginated_results,
                           total_pages=total_pages)

@main.route('/search/export')
@login_required
def export_csv():
    user_query = request.args.get('query')
    display = request.args.get('display')
    order_criteria = request.args.get('sort_criteria', 'similarity')
    order_asc = request.args.get('ascend', "DESC")
    show_trials = request.args.get('show_trials', 'true').lower() in ('1', 'true')
    show_grants = request.args.get('show_grants', 'true').lower() in ('1', 'true')
    results = current_app.search_engine.search(user_query)

    if not show_trials and not show_grants:
        results = []
    elif show_trials and show_grants:
        pass
    elif show_trials:
        results = [row for row in results if not row[6]]
    elif show_grants:
        results = [row for row in results if row[6]]

    reverse = (order_asc == "DESC")
    if order_criteria == "due_date":
        results.sort(key=lambda x: dateutil.parser.parse(x[3]) if x[3] else dateutil.parser.parse("1900-01-01"),
                     reverse=reverse)
    else:
        results.sort(key=lambda x: float(x[4]),
                     reverse=reverse)

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["Award Name", "Organization", "Due Date", "Brief Description", "Link", "isGrant"])
    for row in rows:
        writer.writerow([row[0], row[1], row[3], row[2], row[5], row[6]])
    csv_data = buffer.getvalue()
    filename = display if display else query

    response = make_response(csv_data)
    response.headers["Content-Disposition"] = f"attachment; filename=search_{filename}.csv"
    response.headers["Content-Type"] = "text/csv"
    return response


@main.route('/search/page/<int:page>')
@login_required
def search_page_router(page):
    order_criteria = request.args.get('sort_criteria', 'similarity')
    order_asc = request.args.get('ascend', "DESC")
    show_trials = request.args.get('show_trials', 'true').lower() in ('1', 'true')
    show_grants = request.args.get('show_grants', 'true').lower() in ('1', 'true')
    return search_page(page, order_criteria, order_asc, show_trials, show_grants)
