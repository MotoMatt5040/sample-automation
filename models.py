import os
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

# Ensure that the environment variable is set
uri = os.environ.get('db_uri')
assert uri is not None, "Please set the db_uri environment variable"

# Initialize the base class and engine
Base = declarative_base()
engine = create_engine(uri)
Session = sessionmaker(bind=engine)
session = Session()


# Vendors Table
class Vendors(Base):
    __tablename__ = 'tblVendors'
    vendor_id = Column(Integer, primary_key=True)
    vendor_name = Column(String(50))

    def __repr__(self):
        return f"<Vendor(vendor_id={self.vendor_id}, vendor_name={self.vendor_name})>"


# Headers Table
class Headers(Base):
    __tablename__ = 'tblHeaders'
    header_id = Column(Integer, primary_key=True)
    header_name = Column(String(50))

    # Establishing the relationship with DerivedHeaders using back_populates
    derived_headers = relationship("DerivedHeaders", back_populates="header")

    def __repr__(self):
        return f"<Header(header_id={self.header_id}, header_name={self.header_name})>"


# DerivedHeaders Table
class DerivedHeaders(Base):
    __tablename__ = 'tblDerivedHeaders'
    derived_id = Column(Integer, primary_key=True)
    header_id = Column(Integer, ForeignKey('tblHeaders.header_id'))
    derived_header = Column(String(50))

    # Establishing the relationship with Headers using back_populates
    header = relationship("Headers", back_populates="derived_headers")

    def __repr__(self):
        return f'<DerivedHeader(derived_id={self.derived_id}, header_id={self.header_id}, derived_header={self.derived_header})>'


# VendorDerivedHeaderMapping Table
class VendorDerivedHeaderMapping(Base):
    __tablename__ = 'tblVendorDerivedHeaderMapping'

    vendor_id = Column(Integer, ForeignKey('tblVendors.vendor_id'), primary_key=True)
    derived_id = Column(Integer, ForeignKey('tblDerivedHeaders.derived_id'), primary_key=True)
    mapped_header_id = Column(Integer, ForeignKey('tblHeaders.header_id'))

    # Establishing relationships with Vendors and DerivedHeaders using backrefs
    vendor = relationship("Vendors", backref="vendor_derived_header_mapping")
    derived_header = relationship("DerivedHeaders", backref="vendor_derived_header_mapping")

    def __repr__(self):
        return f'<VendorDerivedHeaderMapping(vendor_id={self.vendor_id}, derived_id={self.derived_id}, mapped_header_id={self.mapped_header_id})>'


# VendorHeaderPadding Table
class VendorHeaderPadding(Base):
    __tablename__ = 'tblVendorHeaderPadding'
    vendor_id = Column(Integer, ForeignKey('tblVendors.vendor_id'), primary_key=True)
    header_id = Column(Integer, ForeignKey('tblHeaders.header_id'), primary_key=True)
    padding_spec = Column(Integer)

    vendor = relationship("Vendors", backref="vendor_header_padding")
    header = relationship("Headers", backref="vendor_header_padding")

    def __repr__(self):
        return f'<VendorHeaderPadding(vendor_id={self.vendor_id}, header_id={self.header_id}, padding_spec={self.padding_spec})>'


def create_tables():
    Base.metadata.create_all(engine)


def drop_tables():
    Base.metadata.drop_all(engine)


def add_vendor(vendor_name):
    vendor = Vendors(vendor_name=vendor_name)
    session.add(vendor)
    session.commit()


if __name__ == "__main__":
    create_tables()
    # drop_tables()
