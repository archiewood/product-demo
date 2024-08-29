import csv
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

# Define North American and European country codes
COUNTRIES = ['US', 'CA', 'MX',  # North America
             'GB', 'DE', 'FR', 'IT', 'ES', 'NL', 'BE', 'SE', 'NO', 'DK', 'FI', 'PL', 'AT', 'CH', 'IE', 'PT']  # Europe

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 6, 30)

def weighted_date(start_date, end_date, initial_spike_prob=0.3, weight=2):
    if random.random() < initial_spike_prob:
        date_range = (end_date - start_date).days
        initial_period = date_range // 6
        return start_date + timedelta(days=random.randint(0, initial_period))
    else:
        # Use the weighted distribution for the rest
        date_range = (end_date - start_date).days
        weighted_days = int((random.random() ** weight) * date_range)
        return end_date - timedelta(days=weighted_days)

def generate_user():
    return {
        'user_id': fake.uuid4(),
        'join_date': weighted_date(start_date, end_date),
        'platform': random.choices(['iOS', 'Android', 'Web', 'Desktop'], weights=[0.35, 0.45, 0.05, 0.15])[0],
        'country': random.choice(COUNTRIES),
        'age': random.choices(range(18, 81), weights=[3] * 23 + [2] * 20 + [1] * 20)[0],
        'gender': random.choices(['M', 'F', 'Other'], weights=[0.48, 0.48, 0.04])[0]
    }

def generate_session(user):
    return {
        'user_id': user['user_id'],
        'session_date': fake.date_between(start_date=user['join_date'], end_date=end_date),
        'duration_minutes': fake.random_int(min=1, max=120),
        'actions': fake.random_int(min=1, max=50)
    }

def generate_onboarding(user):
    steps = ['SignUp', 'ProfileCreation', 'Tutorial', 'FirstAction', 'Completed']
    onboarding_data = []
    current_date = user['join_date']
    
    for step in steps:
        if random.random() < 0.898:  # 90% chance to complete each step
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
        
        # Ensure there's always a session on the join date
        first_session = generate_session(user)
        first_session['session_date'] = user['join_date']
        sessions.append(first_session)
        
        # Generate 0-49 additional sessions per user, dependent on the number of days since signup
        days_since_signup = (end_date - user['join_date']).days
        max_sessions = min(49, max(0, days_since_signup - 1))  # -1 to account for the first session
        additional_sessions = [generate_session(user) for _ in range(random.randint(0, max_sessions))]
        sessions.extend(additional_sessions)
        
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