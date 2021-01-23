import os
import sys
import logging
from sqlite3 import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import sessionmaker
from policy_sentry.querying.all import get_all_service_prefixes

logger = logging.getLogger(__name__)
Base = declarative_base()  # pylint: disable=invalid-name

ALL_SERVICE_PREFIXES = get_all_service_prefixes()
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "../data", "compliance.db")


def connect_db():
    engine = create_engine(f"sqlite:///{DATABASE_PATH}", echo=False)
    try:
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)  # pylint: disable=invalid-name
        Session.configure(bind=engine)
        db_session = Session()
    except OperationalError as o_e:
        logger.critical(o_e)
        sys.exit()
    return db_session


class RawScrapingDataTable(Base):
    """The table that contains the compliance data, as presented by the 'Services in Scope' documentation"""

    __tablename__ = "rawscrapingdatatable"
    id = Column(Integer, primary_key=True)
    sdk_name = Column(String(50))
    service_name = Column(String(50))
    compliance_standard_name = Column(String(50))

    def __repr__(self):
        return (
            f"<RawScrapingDataTable(compliance_standard_name={self.compliance_standard_name}, "
            f"sdk_name={self.sdk_name}, "
            f"service_name='{self.service_name}')>"
        )


class TransformedScrapingDataTable(Base):
    """The table that contains the compliance data, as presented by the 'Services in Scope' documentation"""

    __tablename__ = "transformedscrapingdatatable"
    id = Column(Integer, primary_key=True)
    sdk_name = Column(String(50))
    service_name = Column(String(50))
    compliance_standard_name = Column(String(50))

    def __repr__(self):
        return (
            f"<TransformedScrapingDataTable(compliance_standard_name={self.compliance_standard_name}, "
            f"sdk_name={self.sdk_name}, "
            f"service_name='{self.service_name}')>"
        )


class ComplianceTable(Base):
    """The table that you query for Compliance status using IAM names"""

    __tablename__ = "compliancetable"
    id = Column(Integer, primary_key=True)
    service_prefix = Column(String(50))
    name = Column(String(50))
    SOC = Column(String(50))
    PCI = Column(String(50))
    ISO = Column(String(50))
    FedRAMP_High = Column(String(50))
    FedRAMP_Moderate = Column(String(50))
    HIPAA = Column(String(50))
    HITRUST = Column(String(50))
    IRAP = Column(String(50))
    OSPAR = Column(String(50))
    FINMA = Column(String(50))

    def __repr__(self):
        return (
            f"<ComplianceTable(service_prefix={self.service_prefix}, "
            f"name='{self.name}', "
            f"SOC='{self.SOC}', "
            f"PCI='{self.PCI}', "
            f"ISO='{self.ISO}', "
            f"FedRAMP_High='{self.FedRAMP_High}', "
            f"FedRAMP_Moderate='{self.FedRAMP_Moderate}', "
            f"HIPAA='{self.HIPAA}', "
            f"HITRUST='{self.HITRUST}', "
            f"IRAP='{self.IRAP}', "
            f"OSPAR='{self.OSPAR}', "
            f"FINMA='{self.FINMA}')>"
        )
