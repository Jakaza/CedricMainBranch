import os
import django
import sys

# Add the backend directory to the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from settings_app.models import Service, PlanModification, WhyTrustUs, Certification, TeamMember

print("Clearing existing data...")
Service.objects.all().delete()
PlanModification.objects.all().delete()
WhyTrustUs.objects.all().delete()
Certification.objects.all().delete()
# Don't delete TeamMembers as they might have images we don't want to lose, or just create new ones if needed.
# Actually, let's create one team member for testing if none exist
if not TeamMember.objects.exists():
    TeamMember.objects.create(name="John Cedric", role="Founder", experience="25+ years", specialty="Design", order=1)

print("Creating Services...")
Service.objects.create(
    title="Standard House Plans", 
    description="Ready-to-use architectural plans with complete sets including floor plans, 3D renders, and elevations.", 
    icon_name="Home", 
    badge="Popular", 
    order=1
)
Service.objects.create(
    title="Custom House Design", 
    description="Personalized designs created from scratch based on your requirements, style preferences, and budget.", 
    icon_name="Pencil", 
    badge="Premium", 
    order=2
)
Service.objects.create(
    title="Plan Modifications", 
    description="Professional edits to existing plans including room additions/removals, façade changes, and layout adjustments.", 
    icon_name="Edit3", 
    order=3
)

print("Creating Plan Modifications...")
PlanModification.objects.create(title="Room Additions & Removals", description="Easily customize your plan layout", order=1)
PlanModification.objects.create(title="Façade Changes", description="Update the external appearance", order=2)

print("Creating Why Trust Us items...")
WhyTrustUs.objects.create(title="20+ Years", description="Over two decades of proven experience in residential architecture and design excellence.", order=1)
WhyTrustUs.objects.create(title="500+ Projects", description="Successfully completed over 500 residential projects with 98% client satisfaction rate.", order=2)

print("Creating Certifications...")
Certification.objects.create(name="AIA Certified", order=1)
Certification.objects.create(name="LEED Accredited", order=2)

print("Sample data created successfully.")
