from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('username', sa.String(length=100), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, default=False),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Rooms table
    op.create_table(
        'rooms',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_private', sa.Boolean(), nullable=False, default=False),
        sa.Column('max_members', sa.Integer(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=False),
    )
    op.create_foreign_key('fk_rooms_owner_id_users', 'rooms', 'users', ['owner_id'], ['id'])
    op.create_index(op.f('ix_rooms_slug'), 'rooms', ['slug'], unique=True)

    # Room members association
    op.create_table(
        'room_members',
        sa.Column('user_id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('room_id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('joined_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_foreign_key('fk_room_members_user_id_users', 'room_members', 'users', ['user_id'], ['id'])
    op.create_foreign_key('fk_room_members_room_id_rooms', 'room_members', 'rooms', ['room_id'], ['id'])

    # Messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('content_sanitized', sa.Text(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=False),
    )
    op.create_foreign_key('fk_messages_author_id_users', 'messages', 'users', ['author_id'], ['id'])
    op.create_foreign_key('fk_messages_room_id_rooms', 'messages', 'rooms', ['room_id'], ['id'])
    op.create_index(op.f('ix_messages_room_id_created_at'), 'messages', ['room_id', 'created_at'])
    op.create_index(op.f('ix_messages_author_id'), 'messages', ['author_id'])

    # Moderation actions table
    op.create_table(
        'moderation_actions',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('action_type', postgresql.ENUM('ban', 'kick', 'report', name='moderationactiontype'), nullable=False),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('target_user_id', sa.Integer(), nullable=False),
        sa.Column('target_message_id', sa.Integer(), nullable=True),
        sa.Column('moderator_id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=False),
    )
    op.create_foreign_key('fk_moderation_actions_target_user_id_users', 'moderation_actions', 'users', ['target_user_id'], ['id'])
    op.create_foreign_key('fk_moderation_actions_target_message_id_messages', 'moderation_actions', 'messages', ['target_message_id'], ['id'])
    op.create_foreign_key('fk_moderation_actions_moderator_id_users', 'moderation_actions', 'users', ['moderator_id'], ['id'])
    op.create_foreign_key('fk_moderation_actions_room_id_rooms', 'moderation_actions', 'rooms', ['room_id'], ['id'])
    op.create_index(op.f('ix_moderation_room_id_created_at'), 'moderation_actions', ['room_id', 'created_at'])


def downgrade():
    # Drop tables in reverse order
    op.drop_table('moderation_actions')
    op.drop_table('messages')
    op.drop_table('room_members')
    op.drop_table('rooms')
    op.drop_table('users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_rooms_slug'), table_name='rooms')
    op.drop_index(op.f('ix_messages_room_id_created_at'), table_name='messages')
    op.drop_index(op.f('ix_messages_author_id'), table_name='messages')
    op.drop_index(op.f('ix_moderation_room_id_created_at'), table_name='moderation_actions')
