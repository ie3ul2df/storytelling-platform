# Storygram

A Django-based storytelling platform where users collaboratively create, manage, and rate community-driven stories. Storygram empowers writers to contribute individual chapters, explore creative story branches, and engage with others through a shared narrative experience.

## 🎯 Project Purpose & Rationale

**Storygram** is designed for writers, readers, and storytelling enthusiasts who want to collaboratively build narratives in a flexible, branching format. It is ideal for users who enjoy sharing creative writing, exploring alternate story paths, and rating each other's contributions.

This application was built as part of the Level 5 Diploma in Web Application Development to demonstrate full-stack development skills using Django. The project aligns with real-world practices such as user authentication, CRUD operations, relational database modeling, and deployment to a cloud platform (Heroku).

Storygram solves the problem of fragmented creative collaboration by offering a centralised platform where users can:

- Create and contribute to shared stories, one chapter at a time.
- View and rate different versions of chapters created by other contributors.
- Organise stories into coherent branches while encouraging community participation.

The project demonstrates key backend development skills expected by assessors and employers, including:

- A responsive and accessible UX.
- Secure data management.
- Clean, PEP8-compliant Python code.
- Clear documentation and version control practices.

## 🧠 UX & UI Design

### Strategy

The primary goal of Storygram is to create a platform for collaborative storytelling.

**User Goals:**

- Allow users to write and share original stories.
- Enable collaboration by allowing contributions from other users.
- Provide chapter ranking to guide narrative progression.
- Offer visibility and control over each story's audience and contributors.

**Business/Educational Goals:**

- Demonstrate full-stack web development skills.
- Apply UX principles for real-world, user-centred design.
- Showcase coding proficiency and project planning for assessment and potential employers.

### Scope

The project includes the following core features:

- User authentication (register, login, logout).
- Story creation with title, image, description, and collaboration settings.
- Chapter creation and rating system (1–5 stars).
- Visibility settings for stories (public/private).
- Editable/deletable content for authors.
- Filtering and sorting stories on the homepage.

Planned or future features:

- Comment system.
- Follow/favourite authors and stories.
- Notification system for new contributions and ratings.

### Structure

The platform follows a simple, intuitive structure:

- Homepage: Shows top-ranked stories with filtering and search tools.
- Story Detail Page: Displays the story summary and list of chapters.
- Chapter Page: Displays chapter content and rating functionality.
- Profile Page: Allows users to edit profile and view their stories/chapters.
- Admin Panel: For site administrators to manage users and content.

Each story can have multiple chapters submitted by different users, and the best-rated version is promoted as the official continuation.

### Skeleton

Wireframes were created using Balsamiq to plan the responsive layout for:

- Mobile
- Tablet
- Desktop

Each view includes:

- Navigation bar
- Homepage story grid layout
- Story detail and chapter forms
- Rating and contribution interactions

**WIREFRAMES**

These wireframes were designed in Balsamiq and illustrate the responsive layout planned for Storygram across mobile, tablet, and desktop devices.

**🏠 Home Page**

- Mobile:  
  ![Home Mobile Wireframe](static/prototype/wireframes/Home-Mobile-Size.png)
- Tablet:  
  ![Home Tablet Wireframe](static/prototype/wireframes/Home-Tablet-Size.png)
- Desktop:  
  ![Home Desktop Wireframe](static/prototype/wireframes/Home-Wide-Screen.png)

**👤 Profile Page**

- Tablet & Mobile:  
  ![Profile Tablet Wireframe](static/prototype/wireframes/Profile-Tablet-and-Mobile-Size.png)
- Desktop:  
  ![Profile Desktop Wireframe](static/prototype/wireframes/Profile-Wide-Screen.png)

**📖 Story Page**

- Tablet & Mobile:  
  ![Story Tablet Wireframe](static/prototype/wireframes/StoryPage-Tablet-and-Mobile-Size.png)
- Desktop:  
  ![Story Desktop Wireframe](static/prototype/wireframes/StoryPage-Wide-Screen.png)

### Surface

**Design Choices:**

- **Framework:** Bootstrap 5.3 for consistent layout and responsive design.
- **Typography:** Sans-serif fonts (Bootstrap default) for readability.
- **Colour Scheme:** Dark navbar, white background, and primary action buttons in green/blue for clarity.
- **Icons:** Bootstrap Icons for bookmarks, ratings, and UI feedback.
- **Accessibility:** Used semantic HTML, colour contrast, alt text for images, and responsive layouts for mobile users.

**MOCKUPS**

These mockups reflect the final visual design and layout used in Storygram.

**🏠 Home Page**

- Mobile:  
  ![Home Mobile Mockup](static/prototype/mockups/Home-Mobile-Size.JPG)
- Tablet:  
  ![Home Tablet Mockup](static/prototype/mockups/Home-Tablet-Size.JPG)
- Desktop:  
  ![Home Desktop Mockup](static/prototype/mockups/Home-Wide-Screen.JPG)

**👤 Profile Page**

- Tablet & Mobile:  
  ![Profile Tablet Mockup](static/prototype/mockups/Profile-Tablet-and-Mobile-Size.jpg)
- Desktop:  
  ![Profile Desktop Mockup](static/prototype/mockups/Profile-Wide-Screen.jpg)

**📖 Story Page**

- Tablet & Mobile:  
  ![Story Tablet Mockup](static/prototype/mockups/StoryPage-Tablet-and-Mobile-Size.jpg)
- Desktop:  
  ![Story Desktop Mockup](static/prototype/mockups/StoryPage-Wide-Screen.jpg)
