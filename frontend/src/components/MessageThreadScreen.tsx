import React from "react";
import ChatMessage from "./ChatMessage";
import LoadingChatMessage from "./LoadingChatMessage";
import type { ThreadMessage } from "./../types/index";

export default function MessageThreadScreen({
    messages,
    isWaitingAiResponse,
}: {
    messages: ThreadMessage[];
    isWaitingAiResponse: boolean;
}) {
    return (
        <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-8">
            <div className="max-w-3xl mx-auto flex flex-col items-center text-center mt-12">
                {messages.map((message) => (
                    <ChatMessage
                        chat_role={message.message_role}
                        message={message.content}
                        key={message.id}
                    />
                ))}
                {isWaitingAiResponse ? <LoadingChatMessage /> : null}
            </div>
            {messages.length > 0 ? <div className="h-20" /> : ""}
        </div>
    );
}
