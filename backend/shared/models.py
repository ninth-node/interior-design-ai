"""
Shared database models
"""
from sqlalchemy import Column, String, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from .database import Base


class Client(Base):
    """Client information and preferences"""
    __tablename__ = "clients"

    client_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contact_info = Column(JSON, nullable=False)
    style_preferences = Column(JSON)
    budget_range = Column(JSON)
    project_history = Column(JSON, default=list)
    ai_profile = Column(JSON)  # AI-learned preferences
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    projects = relationship("Project", back_populates="client")


class Project(Base):
    """Design projects"""
    __tablename__ = "projects"

    project_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.client_id"))
    project_type = Column(String(100))  # residential, commercial, renovation
    space_data = Column(JSON)  # room dimensions, existing features
    design_requirements = Column(JSON)
    timeline_data = Column(JSON)
    budget_allocation = Column(JSON)
    status = Column(String(50), default="planning")
    ai_insights = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    client = relationship("Client", back_populates="projects")
    design_concepts = relationship("DesignConcept", back_populates="project")


class DesignConcept(Base):
    """AI-generated design concepts"""
    __tablename__ = "design_concepts"

    concept_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.project_id"))
    style_category = Column(String(100))
    mood_board = Column(JSON)
    color_palette = Column(JSON)
    design_elements = Column(JSON)
    ai_confidence_score = Column(Float)
    client_feedback = Column(JSON)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="design_concepts")


class Product(Base):
    """Furniture and decor products"""
    __tablename__ = "product_catalog"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    supplier_id = Column(UUID(as_uuid=True))
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    style_tags = Column(JSON)
    specifications = Column(JSON)
    pricing_data = Column(JSON)
    availability = Column(JSON)
    ai_compatibility_scores = Column(JSON)
    images = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class User(Base):
    """Interior designers and team members"""
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(String(50), default="designer")  # designer, admin, viewer
    subscription_tier = Column(String(50), default="starter")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
