"""update priority to string

Revision ID: update_priority_str
Revises: 67b1e0e0d28c
Create Date: 2026-06-14 10:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# ID текущей миграции и ID предыдущей (берём из твоего initial_migration)
revision: str = 'update_priority_str'
down_revision: Union[str, None] = '67b1e0e0d28c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Меняем тип колонки с Integer на String с явным приведением типов
    op.alter_column('tasks', 'priority',
               existing_type=sa.Integer(),
               type_=sa.String(),
               existing_nullable=True,
               postgresql_using="priority::text")


def downgrade() -> None:
    # Отрезаем назад на Integer, если решим откатиться
    op.alter_column('tasks', 'priority',
               existing_type=sa.String(),
               type_=sa.Integer(),
               existing_nullable=True,
               postgresql_using="priority::integer")