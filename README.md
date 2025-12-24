# Task Board App for TEB Education

This document describes the basic entities (Teams, Users, Boards, Cards) and access rules for the app.

---

## Roles & Permissions

### Team Roles
- **Admin**
  - Can create teams and manage users
  - Can delete boards
  - Can delete cards
- **Manager**
  - Can create, edit, and delete boards (within their team)
  - Can add people to a board (grant board access / viewers)
- **Team Member**
  - Can view boards they were added to
  - Can create cards within team boards

> Notes:
> - Board creation is allowed only for **Manager**
> - Board deletion is allowed only for **Admin**
> - Card creation is allowed for **any team member**
> - Card deletion is allowed only for **Admin**

---

## Teams

Admin creates teams, adds people, and assigns roles (**Manager** / **Team Member**).

**Fields**
- `team_id` — format: `TM-$`
- `team_name`
- `team_member_id`
- `team_member_role` — enum:
  - `1` = `admin`
  - `2` = `manager`
  - `3` = `team_member`
- `team_board_id`
- `team_create`
- `team_update`

---

## Users

Admin creates and edits users and assigns their roles and teams.

When creating a user, admin sets:
- name
- email
- password
- role

Admin can see a list of all users in the system, their teams, and boards.

**Fields**
- `user_id`
- `user_name`
- `user_mail`
- `user_team_member`
- `user_status` — enum:
  - `1` = `active`
  - `2` = `disabled`
- `user_create`
- `user_update`

---

## Boards

Only a **Team Manager** can create boards. Only an **Admin** can delete boards.

**Fields**
- `board_id` — format: `BD-$`
- `board_name`
- `board_create`
- `board_update`

---

## Cards

Any team member can create cards. Only an **Admin** can delete cards.

**Fields**
- `card_id` — format: `$board_name-$`
- `card_board_id`
- `card_name`
- `card_assign`
- `card_status` — enum:
  - `Backlog`
  - `To Do`
  - `In progress`
  - `Review`
  - `Done`
- `card_priority` — enum:
  - `Higth`
  - `Normal`
  - `Low`
- `card_time_create`
- `card_last_update`
- `card_create_by`
- `card_last_update_by`
- `card_reporter`
- `card_description`
- `card_attach`
- `card_comment_id`
