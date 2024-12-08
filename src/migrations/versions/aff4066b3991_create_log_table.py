"""create log table

Revision ID: aff4066b3991
Revises: eb9310f1f9b0
Create Date: 2024-12-06 17:06:17.284747

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aff4066b3991"
down_revision: Union[str, None] = "eb9310f1f9b0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "request_response_log",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.INTEGER(), nullable=True),
        sa.Column("ip", sa.VARCHAR(), nullable=False),
        sa.Column("port", sa.INTEGER(), nullable=False),
        sa.Column("agent", sa.VARCHAR(), nullable=False),
        sa.Column("method", sa.VARCHAR(length=20), nullable=False),
        sa.Column("path", sa.VARCHAR(length=20), nullable=False),
        sa.Column("response_status", sa.SMALLINT(), nullable=False),
        sa.Column(
            "request_id",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("request_response_log")
    # ### end Alembic commands ###
