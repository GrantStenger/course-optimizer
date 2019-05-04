def get_departments():
    print('Hellooooo')

def add_departments(user, departments):
    for dept in departments:
        dept_obj = Department(title=dept.title, user=user)
        print(dept_obj)
        # db.session.add(dept_obj)
    # db.session.commit()

if __name__ == "__main__":
    get_departments()
