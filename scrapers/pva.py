import hashlib, pandas as pd

def generate_id(text):
    return hashlib.md5(text.strip().lower().encode()).hexdigest()[:12]

def scrape_pva():
    raw_data = [
        {
            "name": "PVA - Basic Science Research Grant",
            "link": "https://pva.org/research-resources/research-foundation/",
            "desc": "Basic Science - laboratory research in the basic sciences to find a cure for SCI/D. From transplanting cells and regenerating damaged nerve fibers to designing adaptive canoe seats, the Paralyzed Veterans of America Research Foundation supports innovative research and fellowships that improve the lives of those with spinal cord injury and disease (SCI/D). The Research Foundation, a 501(c)(3) nonprofit, last year funded $796,402 in grants, and since its inception in 1976, we've invested 644 grants for a total of $54,109,999.",
            "deadline": '2026-07-01',
        },
        {
            "name": "PVA - Clinical Research Grant",
            "link": "https://pva.org/research-resources/research-foundation/",
            "desc": "Clinical - clinical and functional studies of the medical, psychosocial and economic effects of SCI/D, and interventions to alleviate these effects. From transplanting cells and regenerating damaged nerve fibers to designing adaptive canoe seats, the Paralyzed Veterans of America Research Foundation supports innovative research and fellowships that improve the lives of those with spinal cord injury and disease (SCI/D). The Research Foundation, a 501(c)(3) nonprofit, last year funded $796,402 in grants, and since its inception in 1976, we've invested 644 grants for a total of $54,109,999.",
            "deadline": '2026-07-01',
        },
        {
            "name": "PVA - Design and Development Research Grant",
            "link": "https://pva.org/research-resources/research-foundation/",
            "desc": "Design and Development - of new or improved rehabilitative and assistive technology/devices for people with SCI/D to improve function, which also includes improving the identification, selection, and utilization of these devices. From transplanting cells and regenerating damaged nerve fibers to designing adaptive canoe seats, the Paralyzed Veterans of America Research Foundation supports innovative research and fellowships that improve the lives of those with spinal cord injury and disease (SCI/D). The Research Foundation, a 501(c)(3) nonprofit, last year funded $796,402 in grants, and since its inception in 1976, we've invested 644 grants for a total of $54,109,999.",
            "deadline": '2026-07-01',
        },
        {
            "name": "PVA - Fellowship Research Grant",
            "link": "https://pva.org/research-resources/research-foundation/",
            "desc": "Fellowships - for postdoctoral scientists, clinicians and engineers to encourage training and specialization in the field of spinal cord research. From transplanting cells and regenerating damaged nerve fibers to designing adaptive canoe seats, the Paralyzed Veterans of America Research Foundation supports innovative research and fellowships that improve the lives of those with spinal cord injury and disease (SCI/D). The Research Foundation, a 501(c)(3) nonprofit, last year funded $796,402 in grants, and since its inception in 1976, we've invested 644 grants for a total of $54,109,999.",
            "deadline": '2026-07-01',
        },
        {
            "name": "PVA - Consumer and Community Education Grant",
            "link": "https://pva.org/research-resources/education-foundation/",
            "desc": "Consumer and community education to improve the health, independence, and quality of life for individuals with SCI/D. From coordinating workshops for health professionals to producing educational materials to sponsoring fellowships in spinal cord medicine, the Paralyzed Veterans of America Education Foundation helps develop tools that share spinal cord injury and disease (SCI/D) knowledge and improve the lives of those with SCI/D. Since inception in 1986 we have funded 260 grants totalling $9,597,518. The Education Foundation, a 501(c)(3) nonprofit, provides funding in four project categories.",
            "deadline": '2026-12-01',
        },
        {
            "name": "PVA - Professional Development Education Grant",
            "link": "https://pva.org/research-resources/education-foundation/",
            "desc": "Professional development and education to improve the knowledge and competencies of health professionals who serve the SCI/D community, including fellowship and traineeship programs. From coordinating workshops for health professionals to producing educational materials to sponsoring fellowships in spinal cord medicine, the Paralyzed Veterans of America Education Foundation helps develop tools that share spinal cord injury and disease (SCI/D) knowledge and improve the lives of those with SCI/D. Since inception in 1986 we have funded 260 grants totalling $9,597,518. The Education Foundation, a 501(c)(3) nonprofit, provides funding in four project categories.",
            "deadline": '2026-12-01',
        },
        {
            "name": "PVA - Research Translation Education Grant",
            "link": "https://pva.org/research-resources/education-foundation/",
            "desc": "Research translation, projects that move research findings into practical application. From coordinating workshops for health professionals to producing educational materials to sponsoring fellowships in spinal cord medicine, the Paralyzed Veterans of America Education Foundation helps develop tools that share spinal cord injury and disease (SCI/D) knowledge and improve the lives of those with SCI/D. Since inception in 1986 we have funded 260 grants totalling $9,597,518. The Education Foundation, a 501(c)(3) nonprofit, provides funding in four project categories.",
            "deadline": '2026-12-01',
        },
        {
            "name": "PVA - Conference Education Grant",
            "link": "https://pva.org/research-resources/education-foundation/",
            "desc": "Conferences and symposia that provide education and collaboration opportunities for members of the SCI/D community. From coordinating workshops for health professionals to producing educational materials to sponsoring fellowships in spinal cord medicine, the Paralyzed Veterans of America Education Foundation helps develop tools that share spinal cord injury and disease (SCI/D) knowledge and improve the lives of those with SCI/D. Since inception in 1986 we have funded 260 grants totalling $9,597,518. The Education Foundation, a 501(c)(3) nonprofit, provides funding in four project categories.",
            "deadline": '2026-12-01',
        },
    ]
    results = []
    for item in raw_data:
        results.append({
            "id": generate_id(item['link'] + item['name'])
            "name": item['name'],
            "org": "Paralyzed Veterans of America",
            "desc": item['desc'],
            "deadline": item['deadline'],
            "link": item['link'],
            "isGrant": 1,
        })
    return pd.DataFrame(results)
