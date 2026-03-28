import io, csv, dateutil.parser
from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash, make_response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from flask_mail import Message
from extensions import mail, cache

from user import User, get_user_from_db

main = Blueprint('main', __name__)

'''
specialty_queries is user-defined in constants; allows flexibility later
'''
@main.route('/homepage')
@login_required
def homepage():
    specialty_queries = [
        {"name": "Neuropsychology", "query": "Neuropsychology is a specialty that focuses on brain functioning. A neuropsychologist is a licensed psychologist with expertise in how behavior and skills are related to brain structures and systems. Neuropsychology evaluates brain function by testing memory and thinking skills.Individuals who suffer from cognitive difficulties may feel overwhelmed, disorganized, and frustrated because of reduced information-processing abilities. "},
    {"name": "Interventional MSK/Arthritis", "query": "Musculoskeletal diseases and injuries can limit your day-to-day activities by limiting your movement and strength. Our goal is to help you eliminate or reduce musculoskeletal pain so you can return to the activities you need and want to do. Our physiatrists specialize in conservative, non-surgical treatment of diseases and injuries. Some of our treatments include: prescription of non-narcotic medications, injections to relieve pain and inflammation, such as cortisone injections for the hip, knee, and shoulder, viscosupplementation (gel injections) for the knee, non-surgical treatments such as Coolief (nerve ablation) for the knee, trigger point injections for myofascial neck pain, use of braces and other orthotic devices, physical and occupational therapy."},
    {"name": "Pain Management", "query": "There are chronic conditions that are recalcitrant to standard non-operative rehabilitative and surgical treatment. We offer patients a multidisciplinary and in-depth means of managing their conditions. We treat the following conditions: disc herniation and degenerative disc disease, sciatica, spinal stenosis, scoliosis, brain and spine tumors, among other chronic pain-causing conditions."},
    {"name": "Acquired Brain Injury", "query": "Meeting the inpatient rehabilitation needs of patients with both traumatic and non-traumatic acquired brain injuries including medical conditions, hemorrhage, cancer or infection causing temporary or permanent disabilities. The team is comprised of rehabilitation nurses, physical therapists, occupational therapists, speech and language pathologists, recreational therapists, care managers, dietitians, and psychologists."},
    {"name": "Stroke", "query": "The Stroke Specialty Program accepts all types of strokes including thrombotic, embolic, hemorrhagic, and subarachnoid hemorrhage. We accept patients 6 years of age and older, and patients 5 years or younger will be considered on a case-by-case basis. The program is designed to: build strength, improve function and build skills needed to complete daily activities, improve balance, mobility, and safety awareness, improve speech, cognition, and swallowing, prevent future stroke by promoting lifestyle changes to reduce modifiable risk factors and secondary complications, facilitate community inclusion and participation in life roles and interests, introduce resources for assistive technology, community support, advocacy, aging with disability, wellness, driving, promote health coping and adaptation skills."},
    {"name": "Spinal Cord Injury", "query": "Spinal cord injury/disease is life-altering, usually resulting in either paraplegia or quadriplegia. Patients face the loss of sensory function, motor strength, bowel and bladder control, sexual function, and more. We provide both acute inpatient and follow-up outpatient rehabilitation services for spinal cord injury patients. This group includes patients with trauma, multiple sclerosis, tumors (either primary or metastatic), herniated intervertebral discs with significant neurologic deficit, spontaneous vascular accidents, and spinal cord compression secondary to osteomyelitis or degenerative changes."},
    {"name": "Sports Medicine", "query": "Recovering from a sports injury requires strength and conditioning work, as well as the right mindset. In addition to helping you recover from injury and reduce pain, sports rehabilitation utilizes exercises, movements, and therapeutic interventions to help you get back in the game. Services offered are: fitness science training, active release technique, acupuncture, performance psychology, dry needling, and more."},
    {"name": "Cancer Rehabilitation", "query": "Cancer rehabilitation is a supportive service that aims to prevent, relieve, and reduce symptoms at any point during your cancer treatment. It will get you ready for treatment, along with the following: balance issues, difficulty swallowing, fatigue, incontinence, constipation, peripheral neuropathy, pain, sexual dysfunction, lymphedema, brain fog, mood disorders, anxiety, and panic attacks."},
    {"name": "Limb Loss", "query": "Provision of amputation management including: prevention of contractures, limb edema management, skin complications, evaluation and monitoring of physical therapy and occupational therapy needs, assessment of need for an assistive device or durable medical equipment, on-site work with a prosthetist for customized prosthesis design and evaluation for proper fit and gait, montoring and treatment of related issues such as phantom pain and neuromas, help connecting with community resources"},
    {"name": "Electrodiagnostics", "query": "An electrodiagnostic study (EMG study) consists of nerve conduction studies and electromyography. Nerve conduction studies stimulate the nerves with small amounts of electricity to evaluate the electrical properties and function of nerves to help detect diseases or injury. Electromyography studies consist of the insertion of a needle through the skin into a muscle to examine electrical properties and function. Will help diagnose individual nerve or nerve root entrapments, generalized neuropathies, inflammatory demyelinating neuropathies, small fiber sensory neuropathies, myotonia in myotonic myopathies, and disorders of muscles."},
    {"name": "Ultrasound", "query": "Rehabilitative ultrasound imaging is a non-invasive tool that can be used to visualize muscles and more accurately assess the origin of musculoskeletal pain and dysfunction. It can successfully evaluate morphologic characteristics of muscles and tendons, muscle activation patterns, outcomes of rehabilitation, pathologic conditions, muscle or tendon stiffness, and biofeedback for muscle retraining."},
    {"name": "Interventional Spine", "name": "Spine treatments: education (spine biomechanics), activity modification, orthotics/braces, topical treatments (ultrasound, electrical stimulation), spine-specific physical therapy, spinal manipulation and manual treatments, pain psychology, corticosteroid injections, radiofrequency ablation, vertebral body ablation, spinal cord stimulator implantation, discectomy (relieve pressure on spinal nerve), foraminotomy (treat spinal stenosis, disc herniations, facet arthritis), laminotomy and laminectomy, and spinal fusion (treat degenerative disc disease, spondylolisthesis, scoliosis, spinal tumors, and spinal trauma)."},
    {"name": "Spasticity", "query": "Spasticity is an abnormal increase in muscle tone due to a central nervous system disease. Symptoms include: abnormal increase in muscle tone (stiff, tight, painful), difficulty moving joints or relaxing muscles, overactive reflexes, muscle spasms or abnormal movements, limited or loss of range of motion. Treatments include physical or occupational therapy, bracing/orthotics, oral medication, botulinum toxin injections, adult intrathecal baclofen pump, and surgical interventions such as tendon lengthening."},
    {"name": "General Awards", "query": "These are general administrative or non-specific awards which provide funding for researchers to put where most needed. Examples may include: upgrading technology available to researchers, funding for increased support staff for researchers, and more. These are specifically to assist researchers in their projects, but are not tied down to any one project."}
]
    return render_template('homepage.html', specialties=specialty_queries)

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
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user_data = get_user_from_db(username)
        if user_data and check_password_hash(user_data[1], password):
            user = User(username)
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.homepage'))
        else:
            flash("Invalid username or password. Please try again.", "error")
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", 'info')
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
        return render_template('homepage.html')

    results = current_app.search_engine.search(search_term, top_k=5000, threshold=0.5)
    return render_template(
        'search.html',
        results=results,
        query=search_term,
        length=len(results),
        display=specialty if specialty else query,
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
    return render_template('search.html',
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