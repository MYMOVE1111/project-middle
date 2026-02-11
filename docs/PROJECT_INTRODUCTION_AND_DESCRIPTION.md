# Recipe Sharing — Introduction and Project Description

---

## 2. Introduction

### Purpose of the project

The **Recipe Sharing** project is a web application that allows users to discover, create, and share recipes within a single community. The purpose of the project is to:

- **Centralise recipes** — Provide one place where users can browse, search, and filter recipes by category and tags.
- **Enable sharing** — Let registered users publish their own recipes (with title, description, ingredients, instructions, images, difficulty, time, and servings) and manage them (create, edit).
- **Support interaction** — Allow users to view recipes, leave comments, and rate recipes to help others choose what to cook.
- **Organise content** — Use categories (e.g. cuisines) and tags (e.g. dietary, meal type) so that recipes are easy to find and explore.
- **Offer a REST API** — Expose recipes, categories, comments, and ratings via API for integration with other systems or clients.

The project is built with Django and is suitable both for learning full‑stack web development and for deployment as a small community recipe site.

---

## 3. Project Description

### Overview of the application

**Recipe Sharing** is a Django-based web application that works as a community recipe platform. It consists of:

- **Web interface** — Bootstrap-styled pages for home, recipe list/detail, categories, tags, user profiles, and forms for creating/editing recipes and profiles.
- **Backend** — Django (Python): models (Recipe, Category, Tag, User Profile, Comment, Rating), views, forms, and REST API (Django REST Framework).
- **Data** — SQLite by default (development), with support for PostgreSQL in production (e.g. on Render). Media files (recipe and profile images) are stored on the server and served via Django in development and via the chosen hosting in production.

Users can use the site without an account to browse and search recipes; registration and login are required to create and edit recipes, comment, and rate.

---

### Main features and functionality

| Area | Features |
|------|----------|
| **Recipes** | Create, edit, and delete (author only) recipes. Fields: title, description, ingredients, instructions, category, tags, optional image, prep/cook time, servings, difficulty. View recipe detail with image, stats (views, likes), and related content. |
| **Categories** | List of categories (e.g. cuisines). Clicking a category opens a page with all recipes in that category. Categories are shown in the sidebar on the home page. |
| **Tags** | List of tags (e.g. dietary, meal type). Clicking a tag opens a page with all recipes that have that tag. Tags are shown in the sidebar and are clickable. |
| **Search** | Search bar on the home page. Search runs over recipe title, description, ingredients, and instructions (case-insensitive). Results are paginated; the search query is kept in the URL and in pagination links. |
| **Comments and ratings** | On the recipe detail page, logged-in users can add comments and give a 1–5 star rating. Comments can be edited; one rating per user per recipe. |
| **User profiles** | Public profile page per user (username, bio, avatar, list of their recipes). Logged-in users can edit their own profile (bio, avatar) via the “Edit profile” page. |
| **Authentication** | Registration, login, logout. Redirects after login/logout to the home page. Create/edit recipe and edit profile are protected (login required). |
| **Images** | Recipe image: optional upload when creating or editing a recipe; shown on the recipe detail page and in recipe cards on the home page. Profile avatar: optional upload in “Edit profile”; shown on the profile page. |
| **REST API** | REST API (under `/api/`) for recipes, categories, comments, and ratings (Django REST Framework). Supports CRUD where applicable; can be used for mobile or external clients. |
| **UI/UX** | Responsive layout (Bootstrap). Sidebar with compact Categories and Popular Tags panels. Statistics on the home page (total recipes, users, categories, tags). Pagination for recipe list and search results. |

---

*This document describes the purpose (Introduction) and the application overview and main features (Project Description) of the Recipe Sharing project.*
