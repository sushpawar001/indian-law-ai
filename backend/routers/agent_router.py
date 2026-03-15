from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from agent.agent_tool import run_agent_with_tool_memory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.postgre_db import get_db
from db.models import ChatThread, ThreadMessage, ThreadMessageRole
from pydantic import BaseModel

agent_router = APIRouter()


class ThreadInput(BaseModel):
    user_input: str


class MessageAbstract(BaseModel):
    message_role: str
    message_id: str
    content: str


class ThreadMessageOutput(BaseModel):
    user_message_id: str
    thread_id: str
    ai_message: MessageAbstract


# Send message in thread
@agent_router.post("/v1/thread-message")
async def send_message_in_thread(
    user_input: ThreadInput,
    thread_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> ThreadMessageOutput:
    messages: list[dict] = []
    if thread_id:
        thread = await db.get(ChatThread, thread_id)
        if thread:
            print(f"[DEBUG] Thread found")
            existing_messages_cursor = await db.execute(
                select(ThreadMessage).where(ThreadMessage.thread_id == thread_id)
            )
            existing_messages = existing_messages_cursor.scalars().all()
            messages = (
                [
                    {"role": m.message_role, "content": m.content}
                    for m in existing_messages
                ]
                if existing_messages
                else []
            )
            print(existing_messages)
            print(messages)
        else:
            thread = ChatThread()
            db.add(thread)
            await db.commit()
            await db.refresh(thread)
            print(f"[DEBUG] Thread created {thread.thread_id}")

    else:
        thread = ChatThread()
        db.add(thread)
        await db.commit()
        await db.refresh(thread)
        print(f"[DEBUG] Thread created {thread.thread_id}")

    messages.append({"role": "user", "content": user_input.user_input})

    llm_response = run_agent_with_tool_memory(messages)

    user_message = ThreadMessage(
        thread_id=thread.thread_id,
        message_role=ThreadMessageRole.user,
        content=user_input.user_input,
    )
    ai_message = ThreadMessage(
        thread_id=thread.thread_id,
        message_role=ThreadMessageRole.ai,
        content=llm_response,
    )
    db.add_all([user_message, ai_message])
    await db.commit()

    return ThreadMessageOutput(
        user_message_id=str(user_message.id),
        ai_message=MessageAbstract(
            message_role="ai",
            message_id=str(ai_message.id),
            content=llm_response,
        ),
        thread_id=str(thread.thread_id)
    )


# get all threads
@agent_router.get("/v1/threads")
async def get_threads(
    db: AsyncSession = Depends(get_db), page_size: int = 10, page_num: int = 1
):
    offset = (page_num - 1) * page_size
    results = await db.execute(select(ChatThread).limit(page_size).offset(offset))
    return results.scalars().all()


# get thread messages
@agent_router.get("/v1/messages")
async def get_messages(
    thread_id: str,
    db: AsyncSession = Depends(get_db),
):
    thread = await db.execute(
        select(ChatThread).where(ChatThread.thread_id == thread_id)
    )
    if not thread.scalar_one_or_none():
        raise HTTPException(400, "Thread not found")

    messages = await db.execute(
        select(ThreadMessage)
        .where(ThreadMessage.thread_id == thread_id)
        .order_by(ThreadMessage.sent_at.asc())
    )

    return messages.scalars().all()


# Delete thread
@agent_router.delete("/v1/thread")
async def delete_thread(
    thread_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ChatThread).where(ChatThread.thread_id == thread_id)
    )
    thread = result.scalar_one_or_none()

    if not thread:
        raise HTTPException(400, "Thread not found")

    await db.delete(thread)
    await db.commit()

    return {"status": "success"}


# Delete message
@agent_router.delete("/v1/message")
async def delete_message(
    message_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ChatThread).where(ThreadMessage.id == message_id))
    message = result.scalar_one_or_none()

    if not message:
        raise HTTPException(400, "Message not found")

    await db.delete(message)
    await db.commit()

    return {"status": "success"}
