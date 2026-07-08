#!/usr/bin/env python3
"""Seed script to populate database with realistic sample data for development."""

import asyncio
import os
from datetime import datetime, timedelta

from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.models.room import Room, RoomMember
from app.models.message import Message
from app.models.moderation import ModerationAction, ModerationActionType
from app.core.security import get_password_hash


async def seed():
    async with AsyncSessionLocal() as session:
        # Clear existing data
        await session.execute("TRUNCATE TABLE moderation_actions CASCADE")
        await session.execute("TRUNCATE TABLE messages CASCADE")
        await session.execute("TRUNCATE TABLE room_members CASCADE")
        await session.execute("TRUNCATE TABLE rooms CASCADE")
        await session.execute("TRUNCATE TABLE users CASCADE")
        await session.commit()

        # Create users
        users = []
        for i in range(1, 11):
            user = User(
                email=f"user{i}@example.com",
                username=f"user{i}",
                hashed_password=get_password_hash(f"password{i}"),
                is_active=True,
                is_superuser=(i == 1),
            )
            session.add(user)
            users.append(user)
        await session.commit()

        # Create rooms
        rooms = []
        room_names = [
            "General Chat",
            "Tech Talk",
            "Music Lovers",
            "Gaming Hub",
            "Book Club",
            "Travel Enthusiasts",
            "Foodies",
            "Sports Fans",
            "Art & Design",
            "Science & Tech",
        ]
        for idx, name in enumerate(room_names):
            room = Room(
                name=name,
                slug=f"{name.lower().replace(' ', '-')}-{idx}",
                description=f"A room for {name.lower()}",
                is_private=False,
                max_members=100,
                owner_id=users[idx % len(users)].id,
            )
            session.add(room)
            rooms.append(room)
        await session.commit()

        # Add members to rooms (except owner already joined)
        for room in rooms:
            for user in users[:5]:  # Add first 5 users to each room
                if user.id != room.owner_id:
                    member = RoomMember(user_id=user.id, room_id=room.id)
                    session.add(member)
        await session.commit()

        # Create messages
        messages = []
        sample_messages = [
            "Hey everyone! How's it going?",
            "Does anyone have recommendations for a good book?",
            "Anyone up for a gaming session tonight?",
            "What's your favorite travel destination?",
            "New movie recommendations?",
            "Anyone into hiking? Let's plan a trip!",
            "What tech stack are you using these days?",
            "Anyone else excited for the concert next week?",
            "What's the best restaurant in town?",
            "Anyone want to join a study group?",
        ]
        for idx, content in enumerate(sample_messages):
            msg = Message(
                content=content,
                content_sanitized=content,
                author_id=users[idx % len(users)].id,
                room_id=rooms[idx % len(rooms)].id,
            )
            session.add(msg)
            messages.append(msg)
        await session.commit()

        # Create moderation actions
        mod_actions = []
        for i in range(3):
            action = ModerationAction(
                action_type=ModerationActionType.BAN if i % 2 == 0 else ModerationActionType.KICK,
                reason=f"Violation {i+1}" if i % 2 == 0 else "Spamming",
                target_user_id=users[i+2].id,
                target_message_id=messages[i].id if i < len(messages) else None,
                moderator_id=users[0].id,  # Superuser as moderator
                room_id=rooms[i % len(rooms)].id,
            )
            session.add(action)
            mod_actions.append(action)
        await session.commit()

        print("✅ Seed complete! Inserted:")
        print(f"  - {len(users)} users")
        print(f"  - {len(rooms)} rooms")
        print(f"  - {len(messages)} messages")
        print(f"  - {len(mod_actions)} moderation actions")


if __name__ == "__main__":
    asyncio.run(seed())
