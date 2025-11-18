"""Initial migration with core models

Revision ID: 001
Revises:
Create Date: 2025-11-18 20:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create clients table
    op.create_table(
        'clients',
        sa.Column('client_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('contact_info', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('style_preferences', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('budget_range', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('project_history', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('ai_profile', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('client_id')
    )

    # Create users table
    op.create_table(
        'users',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('role', sa.String(length=50), nullable=True),
        sa.Column('subscription_tier', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email')
    )

    # Create product_catalog table
    op.create_table(
        'product_catalog',
        sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('supplier_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('style_tags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('specifications', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('pricing_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('availability', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('ai_compatibility_scores', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('images', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('product_id')
    )

    # Create projects table
    op.create_table(
        'projects',
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('client_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('project_type', sa.String(length=100), nullable=True),
        sa.Column('space_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('design_requirements', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('timeline_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('budget_allocation', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('ai_insights', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['client_id'], ['clients.client_id'], ),
        sa.PrimaryKeyConstraint('project_id')
    )

    # Create design_concepts table
    op.create_table(
        'design_concepts',
        sa.Column('concept_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('style_category', sa.String(length=100), nullable=True),
        sa.Column('mood_board', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('color_palette', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('design_elements', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('ai_confidence_score', sa.Float(), nullable=True),
        sa.Column('client_feedback', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_approved', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.project_id'], ),
        sa.PrimaryKeyConstraint('concept_id')
    )

    # Create indexes for better query performance
    op.create_index(op.f('ix_clients_created_at'), 'clients', ['created_at'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_is_active'), 'users', ['is_active'], unique=False)
    op.create_index(op.f('ix_projects_client_id'), 'projects', ['client_id'], unique=False)
    op.create_index(op.f('ix_projects_status'), 'projects', ['status'], unique=False)
    op.create_index(op.f('ix_design_concepts_project_id'), 'design_concepts', ['project_id'], unique=False)
    op.create_index(op.f('ix_product_catalog_category'), 'product_catalog', ['category'], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_product_catalog_category'), table_name='product_catalog')
    op.drop_index(op.f('ix_design_concepts_project_id'), table_name='design_concepts')
    op.drop_index(op.f('ix_projects_status'), table_name='projects')
    op.drop_index(op.f('ix_projects_client_id'), table_name='projects')
    op.drop_index(op.f('ix_users_is_active'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_clients_created_at'), table_name='clients')

    # Drop tables in reverse order (respecting foreign keys)
    op.drop_table('design_concepts')
    op.drop_table('projects')
    op.drop_table('product_catalog')
    op.drop_table('users')
    op.drop_table('clients')
