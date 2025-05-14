# CISBACapstone
Project repository for CIDM6395

## Project: Linkella
### Overview
Linkella is a web-based platform that connects Certified Nursing Assistants (CNAs) with clients who need in-home care services. The system functions like a localized healthcare marketplace, where CNAs can create listings to advertise themselves, and clients can search, filter, and contact CNAs based on their needs. <br>
The system also includes a financial tracker and forecasting tool, allowing CNAs to log weekly job summaries, estimate their upcoming income, and manage their care business more efficiently. <br>
This project was developed as the Capstone for the MSCISBA program. It synthesizes concepts from Software Systems, Business Analytics, and Data Management. 
### Purpose and Problem Addressed
Home healthcare CNAs often work independently, juggling multiple clients, hours, and different streams of income. However, no centralized tool exists to:
* Connect CNAs with clients efficiently
* Allow CNAs to manage their listings, hours, and finances
* Help clients make informed choices using ratings and reviews<br><br>
<b>Linkella solves this by combining marketplace functionality with financial tracking tools all within a secure, role-based Django web application.</b>
### Key Features
####  For CNAs:
* Create and manage listings (name, location, hourly rate, availability, experience)
* Receive real-time service requests from clients via internal notifications
* Access a financial dashboard  to log weekly job summaries
* View projected income via automated 4-week forecast
* Secure login and registration system- dashboard features tailored to the user type selected at signup
#### For Clients:
* Browse and filter available CNA listings by location and hourly rate
* Contact CNAs via servive reuqest form
* Leave ratings and written reviews for CNAs
### Project Highlights
* <b>User Authentication:</b> with role-based dashboards (CNA vs. Client)
* <b>Dynamic Forms:</b> for listing creation, service requests, and reviews
* <b>Internal Notification System:</b> for CNA alerts
* <b>Review and Rating System:</b> directly tied  to CNA listings
* <b>Forecast Engine:</b> using job data to predict future income
* <b>Responsive Design:</b> clean UI/UX
### Technologies Used
* Backend: Django, Django REST Framework
* Frontend: HTML, CSS, JavaScript
* Database: SQLite
* Authentication: Django's built-in user model + custom roles
### Project Structure
The project uses standard Django structure with modular apps, templates, and static files. All core logic resides in the `core/` app.
## License & Usage
This project is the intellectual property of **Aubrey Skinner** 
