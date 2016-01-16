# MovieTixDemo
A very simple Django web app to build a movie ticket booking system.

This application demonstrates these aspects-

1. blocking (blocking timeout of 3 minutes on reservation till final confirmation after which the lock on the selected seat can be released)
2. concurrency (multiple users booking the same seat at the same time, and using ACID properties of the database to avoid them)
3. anonymous user management through per session id information

In this implementation
* you can create new movies and set num of rows and cols allowed
* there is no log in and user authentication, a unique session id is used to differentiate users
* when a ticket is blocked temporarily, a background process kicks in after 3 minutes and removes the lock on the seat if it has not been confirmed yet
* a rudimentary shopping cart allows to confirm a ticket which was temporarily blocked, and to cancel a ticket. This shopping cart is stored in the cookies and not persisted across sessions.
* Its not well tested, so might get cranky at some places.

The application is hosted on Heroku and uses PostgresSQL and Redis.
