import sys
import os
import random
from datetime import datetime, timedelta
from faker import Faker
from sqlmodel import Session, select
from sqlalchemy import insert

# Add backend directory to sys.path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine
from app.models import Area, WasteLog, WasteType
from app.nigeria_data import AREAS, TRUCK_IDS

fake = Faker()

def seed_areas():
    with Session(engine) as session:
        # Check if areas exist
        existing = session.exec(select(Area)).first()
        if existing:
            print("Areas already exist. Skipping Area seeding.")
            return

        print("Seeding Areas...")
        areas_to_create = []
        for name, desc in AREAS:
            code = f"{name[:3].upper()}-{random.randint(100, 999)}"
            area = Area(
                name=name,
                code=code,
                description=desc,
                population_density=random.uniform(500, 5000)
            )
            areas_to_create.append(area)
        
        session.add_all(areas_to_create)
        session.commit()
        print(f"Seeded {len(areas_to_create)} Areas.")

def seed_waste_logs(num_records=100000):
    print(f"Seeding {num_records} Waste Logs... This might take a moment.")
    
    with Session(engine) as session:
        areas = session.exec(select(Area)).all()
        area_ids = [a.id for a in areas]
        
        if not area_ids:
            print("No areas found. Cannot seed logs.")
            return

    # Bulk insert using SQLAlchemy Core for speed
    # Generating data in batches of 10k to manage memory
    batch_size = 10000
    waste_types = [wt.value for wt in WasteType]
    
    start_date = datetime.utcnow() - timedelta(days=365) # Last year
    
    total_inserted = 0
    
    with engine.connect() as conn:
        for _ in range(0, num_records, batch_size):
            batch = []
            current_batch_size = min(batch_size, num_records - total_inserted)
            
            for _ in range(current_batch_size):
                # Random date within last year
                random_days = random.randint(0, 365)
                log_date = start_date + timedelta(days=random_days)
                
                # Logic: Weekends might have more waste? Or specific types. 
                # Keeping it random for now but weighted slightly by 'density' via weight logic
                
                weight = random.uniform(10.0, 500.0)
                
                entry = {
                    "area_id": random.choice(area_ids),
                    "collection_date": log_date,
                    "waste_type": random.choice(waste_types),
                    "weight_kg": round(weight, 2),
                    "truck_id": random.choice(TRUCK_IDS)
                }
                batch.append(entry)
            
            conn.execute(insert(WasteLog), batch)
            conn.commit()
            total_inserted += current_batch_size
            print(f"Inserted {total_inserted}/{num_records} records...")

    print("Seeding Complete!")

if __name__ == "__main__":
    seed_areas()
    # You can change the number here or pass via args, defaulting to user request of 100k
    seed_waste_logs(100000)
