import csv
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

def generate_user():
    return {
        'user_id': fake.uuid4(),
        'join_date': fake.date_between(start_date='-2y', end_date='today'),
        'platform': fake.random_element(elements=('iOS', 'Android', 'Web', 'Desktop')),
        'country': fake.country_code(),
        'age': fake.random_int(min=18, max=80),
        'gender': fake.random_element(elements=('M', 'F', 'Other'))
    }

def generate_session(user):
    return {
        'user_id': user['user_id'],
        'session_date': fake.date_between(start_date=user['join_date'], end_date='today'),
        'duration_minutes': fake.random_int(min=1, max=120),
        'actions': fake.random_int(min=1, max=50)
    }

def generate_onboarding(user):
    steps = ['SignUp', 'ProfileCreation', 'Tutorial', 'FirstAction', 'Completed']
    onboarding_data = []
    current_date = user['join_date']
    
    for step in steps:
        if random.random() < 0.9:  # 90% chance to complete each step
            onboarding_data.append({
                'user_id': user['user_id'],
                'step': step,
                'completion_date': current_date
            })
            current_date += timedelta(days=random.randint(0, 3))
        else:
            break
    
    return onboarding_data

def save_to_csv(data, filename):
    if data:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

def generate_data(num_users):
    users = []
    sessions = []
    onboarding = []

    for _ in range(num_users):
        user = generate_user()
        users.append(user)
        
        # Generate 1-50 sessions per user
        user_sessions = [generate_session(user) for _ in range(random.randint(1, 50))]
        sessions.extend(user_sessions)
        
        # Generate onboarding data
        user_onboarding = generate_onboarding(user)
        onboarding.extend(user_onboarding)

    return users, sessions, onboarding

# Generate data
num_users = 10000
users, sessions, onboarding = generate_data(num_users)

# Save data to CSV files
save_to_csv(users, 'users.csv')
save_to_csv(sessions, 'sessions.csv')
save_to_csv(onboarding, 'onboarding.csv')

print("Data generation complete. Check users.csv, sessions.csv, and onboarding.csv for the generated data.")