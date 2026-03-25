from models import Business, BusinessDirectory

directory = BusinessDirectory()

sample_data = [
    Business("Kano Tech Hub", "Technology", "Kano, Nigeria",
             "A co-working space and incubator for tech startups in northern Nigeria.",
             "kanotechhub@gmail.com", 2020, "https://kanotechhub.com"),
    Business("FarmConnect NG", "Agriculture", "Zaria, Nigeria",
             "Connecting smallholder farmers directly to urban markets via mobile.",
             "+234-801-000-0001", 2021, "https://farmconnect.ng"),
    Business("MediQuick Pharmacy", "Healthcare", "Kaduna, Nigeria",
             "Fast-delivery pharmacy serving residential estates across Kaduna.",
             "mediquick@ng.com", 2019, "https://mediquick.ng"),
    Business("EduBridge Tutorials", "Education", "Kano, Nigeria",
             "Affordable JAMB and WAEC preparation centre for secondary school students.",
             "+234-802-000-0002", 2018, "https://edubrideng.org"),
    Business("GreenBuild Materials", "Construction", "Abuja, Nigeria",
             "Supplier of eco-friendly building materials for modern construction projects.",
             "greenbuild@abuja.ng", 2022, "https://greenbuild.ng"),
]

for b in sample_data:
    directory.add_business(b)
