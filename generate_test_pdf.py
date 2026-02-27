"""Generate a sample PDF for testing upload functionality"""
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch
except ImportError:
    print("Installing reportlab...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'reportlab'])
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch

# Create PDF
pdf_file = "sample_test_document.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)
width, height = letter

# Title
c.setFont("Helvetica-Bold", 20)
c.drawString(1*inch, height - 1*inch, "Project Meeting Notes")

# Date
c.setFont("Helvetica", 12)
c.drawString(1*inch, height - 1.5*inch, "Date: December 20, 2024")

# Content
c.setFont("Helvetica", 11)
y = height - 2*inch

content = [
    "Meeting Attendees: John, Sarah, Mike, Lisa",
    "",
    "Agenda:",
    "1. Project status update",
    "2. Upcoming deadlines",
    "3. Resource allocation",
    "",
    "Discussion Points:",
    "- The Q4 report needs to be completed by December 31st",
    "- Design mockups should be ready by next Friday",
    "- Code review scheduled for Monday morning at 10 AM",
    "- Budget approval pending from finance team",
    "",
    "Action Items:",
    "- John: Complete the database migration by end of week",
    "- Sarah: Review and approve the new UI designs by Tuesday",
    "- Mike: Schedule follow-up meeting with stakeholders",
    "- Lisa: Prepare presentation slides for client demo",
    "",
    "Deadlines:",
    "- Database migration: December 22, 2024",
    "- UI design approval: December 24, 2024",
    "- Client demo: December 28, 2024",
    "- Q4 report submission: December 31, 2024",
    "",
    "Next Meeting: January 5, 2025 at 2:00 PM",
    "",
    "Priority: HIGH",
    "Status: In Progress"
]

for line in content:
    c.drawString(1*inch, y, line)
    y -= 0.25*inch

c.save()
print(f"[OK] Created: {pdf_file}")
print(f"[OK] File size: {round(len(open(pdf_file, 'rb').read())/1024, 2)} KB")
print(f"\nYou can now upload this file to test the system!")
