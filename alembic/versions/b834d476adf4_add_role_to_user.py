from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b834d476adf4'
down_revision = '396cb2a26dde'
branch_labels = None
depends_on = None

# Step 1: Define the ENUM
user_role_enum = postgresql.ENUM('admin', 'seller', 'customer', name='userrole')

def upgrade():
    # Step 2: Create the ENUM in the database
    user_role_enum.create(op.get_bind())

    # Step 3: Add the column with `nullable=True` temporarily
    op.add_column('users', sa.Column('role', user_role_enum, nullable=True))

    # Step 4: Set a default value for existing users
    op.execute("UPDATE users SET role = 'customer'")  # or 'admin', based on your logic

    # Step 5: Alter the column to be NOT NULL
    op.alter_column('users', 'role', nullable=False)

def downgrade():
    # Step 6: Drop the column
    op.drop_column('users', 'role')

    # Step 7: Drop the ENUM type
    user_role_enum.drop(op.get_bind())
