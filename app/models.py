import uuid
from database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    name = Column(String,  nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    verified = Column(Boolean, nullable=False, server_default='False')
    verification_code = Column(String, nullable=True, unique=True)
    role = Column(String, server_default='user', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


class Post(Base):
    __tablename__ = 'posts'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category = Column(String, nullable=False)
    image = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    user = relationship('User')

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    manufacturer = Column(String(255), nullable=False)
    units = Column(String(255), nullable=False)
    
    # Establish a one-to-many relationship with Purchase
    purchases = relationship("Purchase", back_populates="product")

class Resource(Base):
    __tablename__ = 'resource'
    resource_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_of_measure = Column(String(50), nullable=False)
    description = Column(Text)

class Location(Base):
    __tablename__ = 'location'
    location_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    country = Column(String(100))
    region = Column(String(100))
    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))

class ExtractionSite(Base):
    __tablename__ = 'extraction_site'
    site_id = Column(Integer, primary_key=True)
    site_name = Column(String(255), nullable=False)
    location_id = Column(Integer, ForeignKey("location.location_id"))
    capacity = Column(Integer)
    established_date = Column(Date)

class Worker(Base):
    __tablename__ = 'worker'
    worker_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    hire_date = Column(Date)
    salary = Column(DECIMAL(10, 2))

class ExtractionLog(Base):
    __tablename__ = 'extraction_log'
    log_id = Column(Integer, primary_key=True)
    resource_id = Column(Integer, ForeignKey("resource.resource_id"))
    site_id = Column(Integer, ForeignKey("extraction_site.site_id"))
    worker_id = Column(Integer, ForeignKey("worker.worker_id"))
    extraction_date = Column(Date, nullable=False)
    quantity_extracted = Column(Integer, nullable=False)
    notes = Column(Text)

if __name__ == "__main__":
    engine = create_engine(f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}")
    Base.metadata.create_all(bind=engine)

    # Add more data to the tables
    with engine.connect() as connection:
        # Insert data into the products table
        connection.execute(Product.__table__.insert(), [
            {"manufacturer": "Manufacturer A", "units": "Unit A"},
            {"manufacturer": "Manufacturer B", "units": "Unit B"},
            {"manufacturer": "Manufacturer C", "units": "Unit C"}
        ])

        # Insert data into the resource table
        connection.execute(Resource.__table__.insert(), [
            {"name": "Resource A", "quantity": 1000, "unit_of_measure": "Unit A", "description": "Description A"},
            {"name": "Resource B", "quantity": 500, "unit_of_measure": "Unit B", "description": "Description B"},
            {"name": "Resource C", "quantity": 200, "unit_of_measure": "Unit C", "description": "Description C"}
        ])

        # Insert data into the location table
        connection.execute(Location.__table__.insert(), [
            {"name": "Location A", "country": "Country A", "region": "Region A", "latitude": 12.345, "longitude": 45.678},
            {"name": "Location B", "country": "Country B", "region": "Region B", "latitude": 23.456, "longitude": 56.789},
            {"name": "Location C", "country": "Country C", "region": "Region C", "latitude": 34.567, "longitude": 67.890}
        ])

        # Insert data into the extraction_site table
        connection.execute(ExtractionSite.__table__.insert(), [
            {"site_name": "Site A", "location_id": 1, "capacity": 500, "established_date": datetime(2020, 1, 1)},
            {"site_name": "Site B", "location_id": 2, "capacity": 700, "established_date": datetime(2018, 5, 15)},
            {"site_name": "Site C", "location_id": 3, "capacity": 1000, "established_date": datetime(2019, 11, 20)}
        ])

        # Insert data into the worker table
        connection.execute(Worker.__table__.insert(), [
            {"name": "Worker A", "position": "Position A", "hire_date": datetime(2019, 2, 10), "salary": 50000.0},
            {"name": "Worker B", "position": "Position B", "hire_date": datetime(2020, 5, 20), "salary": 75000.0},
            {"name": "Worker C", "position": "Position C", "hire_date": datetime(2018, 10, 15), "salary": 60000.0}
        ])

        # Insert data into the extraction_log table
        connection.execute(ExtractionLog.__table__.insert(), [
            {"resource_id": 1, "site_id": 1, "worker_id": 1, "extraction_date": datetime(2022, 1, 5), "quantity_extracted": 200, "notes": "Initial extraction"},
            {"resource_id": 2, "site_id": 2, "worker_id": 2, "extraction_date": datetime(2022, 2, 10), "quantity_extracted": 100, "notes": "Secondary extraction"},
            {"resource_id": 3, "site_id": 3, "worker_id": 3, "extraction_date": datetime(2022, 3, 15), "quantity_extracted": 300, "notes": "Another extraction"}
        ])