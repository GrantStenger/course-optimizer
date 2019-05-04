# Course Optimizer

I created a Flask web app where USC students can select courses they’re interested in and, given unit limits and pre-requisite requirements, compute their optimal course schedule. This optimization problem is solved with a clever network flow construction. The course data is from a scraper I wrote that pulled from USC’s public [course catalogue](http://catalogue.usc.edu/).

This project was inspired by my ISE 632 class “Network Flows and Combinatorial Optimization” taught by [Professor John Gunnar Carlsson](http://www-bcf.usc.edu/~jcarlsso/).

### New User
- user = User.query.filter_by(username='username').one()
- title = Department(title='title', user=user)
