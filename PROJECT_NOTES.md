# Fresher Project Checklist

Before putting this on GitHub:

- [ ] Replace demo credentials in your own version.
- [ ] Add screenshots to README.
- [ ] Add a database ER diagram.
- [ ] Make 8–12 meaningful Git commits instead of one huge commit.
- [ ] Add one feature yourself (CSV export, pagination, email, or REST API).
- [ ] Deploy the application.
- [ ] Be able to explain every model and route.

Recommended Git commit sequence:

1. Initialize Flask project
2. Add database models
3. Add authentication
4. Add employee CRUD
5. Add search and filters
6. Add attendance module
7. Add leave workflow
8. Add dashboard
9. Add tests
10. Improve documentation and UI

## Role update
- Admin users can review/update leave status but cannot apply for leave.
- The Apply Leave button is hidden for Admin in the dashboard and Leave Requests page.
- The `/leaves/new` endpoint is restricted to HR and Employee roles, so an Admin cannot bypass the UI by entering the URL directly.
