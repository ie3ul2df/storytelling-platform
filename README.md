# Storytelling Platform

A Django-based collaborative storytelling web application that allows users to create, share, and contribute to narrative stories chapter by chapter. Built with HTML, CSS, JavaScript, and Python, the platform supports user authentication, CRUD operations, contribution control, chapter ratings, and responsive design.

---

## 🧠 UX & UI Design

### Project Goals

- Enable users to write and share their own stories.
- Allow users to continue stories with new chapters.
- Enable community-based ranking to guide the story direction.
- Provide visibility and collaboration controls to the story owners.

### User Stories

#### Must Have

- As a **visitor**, I want to **register and log in** so I can **write and interact with stories**.
- As a **registered user**, I want to **create a new story** so I can **share my writing**.
- As a **user**, I want to **write multiple chapters** so I can **continue the narrative over time**.
- As a **user**, I want to **rank each chapter** so I can **express how much I liked it**.
- As a **story owner**, I want to **set my story as public or private** so I can **control who sees it**.
- As a **visitor or user**, I want to **see a homepage with top-ranked stories** so I can **discover engaging content**.
- As a **user**, I want to **edit or delete my stories and chapters** so I can **maintain and update my content**.
- As a **user**, I want to **log out securely** to **protect my account and privacy**.
- As a **user**, I want to **view and read full stories and their chapters** so I can **enjoy complete narratives**.

#### Should Have

- As a **story creator**, I want to **allow or disallow contributions** so I can **retain creative control**.
- As a **logged-in user**, I want to **write a new chapter for someone else's story** so I can **collaborate on ongoing stories**.
- As a **contributor**, I want to **receive rankings for each chapter** so I can **gain feedback and recognition**.
- As the **system**, I want to **automatically choose the highest-ranked chapter** as the **official next chapter**.
- As a **user**, I want to **enable or disable contributions** before publishing my story so I can **decide on collaboration**.

#### Could Have

- As a **user**, I want to **comment on stories** so I can **give feedback or ask questions**.
- As a **user**, I want to **follow my favourite authors or stories** so I can **stay updated on new chapters**.
- As a **user**, I want to **get notified when someone contributes or ranks my story** so I can **track engagement**.
- As a **visitor**, I want to **search or filter stories by category, tag, or author** so I can **find stories that interest me**.

### Wireframes

Wireframes were created using Balsamiq to plan the layout for:

- Mobile
- Tablet
- Desktop

[Insert wireframe images or links here]

---

## 🔧 Features

- User registration and login
- Story creation with privacy and collaboration settings
- Chapter writing and ranking
- Auto-selection of best-rated chapters
- Responsive layout for mobile/tablet/desktop
- Admin panel for managing content

---

## 🗃️ Data Models

- `User`: Django’s built-in User model
- `Story`: title, description, author, is_public, allow_contributions
- `Chapter`: title, content, story FK, author
- `Rating`: chapter FK, user FK, rating (1–5), unique per user per chapter

Refer to `erd.png` for the full entity-relationship diagram.

---

## 🛠️ Technologies Used

- **Python 3 / Django 4**
- **HTML5, CSS3, Bootstrap**
- **JavaScript**
- **PostgreSQL** (Heroku)
- **Crispy Forms**
- **Gunicorn + dj_database_url for deployment**

---

## 🚀 Deployment

This app is deployed to [Heroku](https://www.heroku.com/).

### Local Setup

1. Clone the repo:

   ```bash
   git clone https://github.com/yourusername/storytelling-platform.git
   cd storytelling-platform
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Add `.env` with your environment variables (keep this file out of Git):

   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_URL=your-local-db
   ```

5. Run migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### Heroku Deployment Steps

1. Push to GitHub
2. Connect Heroku app
3. Set config vars (SECRET_KEY, DEBUG=False, ALLOWED_HOSTS, DATABASE_URL)
4. Run:
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

---

## 🧪 Testing

- Manual testing across:
  - Chrome, Firefox, Safari
  - Mobile, Tablet, Desktop views
- Online validators used:
  - [W3C HTML Validator](https://validator.w3.org/)
  - [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)
  - [PEP8 checker](http://pep8online.com/)
- Lighthouse performance and accessibility reports documented below:

[Insert screenshots or descriptions]

### Bug Fixes

- Bug: Ratings were duplicated by same user.
  - Fix: Added `unique_together` constraint in `Rating` model.

---

## 📝 Credits

- Story concept inspired by collaborative fiction platforms
- Bootstrap and Crispy Forms from official docs
- [Images/icons/wireframes] from [source with URL]

---

## 📄 License

This project is for educational purposes as part of a Level 5 Diploma in Web Application Development.
