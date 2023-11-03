# heart_to_homes
# heart_to_homes

User views and urls:

Login:
url: /login/
view: accounts.views.login
Create an account:
url: /signup/
view: accounts.views.signup
View a listing of available children's homes:
url: /children_homes/
view: children_homes.views.list_children_homes
Search for a specific children's home based on location or name:
url: /children_homes/search/
view: children_homes.views.search_children_homes
View more details about a children's home:
url: /children_homes/<pk>/
view: children_homes.views.children_home_detail
Offer donations to individual or multiple children's homes:
url: /donations/
view: donations.views.make_donations
Select a visit date to a desired children's home based on location:
url: /visits/
view: visits.views.schedule_visit
Give a review to a specific children's home:
url: /reviews/
view: reviews.views.submit_review

Admin views and urls:

Add users to the account:
url: /admin/users/add/
view: admin.views.user_add

Perform CRUD operations on children's home organizations:
url: /admin/children_homes/
view: admin.views.children_home_changelist

View analytics about children's homes, i.e., in terms of:
Which has been visited the most:
url: /admin/children_homes/analytics/most_visited/
view: children_homes.views.admin_most_visited_children_homes

Which is in more need of donations and help:
url: /admin/children_homes/analytics/most_in_need/
view: children_homes.views.admin_most_in_need_children_homes