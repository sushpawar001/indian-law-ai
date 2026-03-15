import React from "react";

const ChatMessage = ({
    chat_role,
    message,
}: {
    chat_role: string;
    message: string;
}) => {
    const isAi = chat_role === "ai";

    return (
        <div
            className={`flex w-full mb-6 ${isAi ? "justify-start" : "justify-end"}`}
        >
            {/* AI Avatar */}
            {isAi && (
                <div className="w-10 h-10 rounded-xl bg-clay-300 text-charcoal-900 flex items-center justify-center text-lg mr-3 mt-1 flex-shrink-0 shadow-sm border border-clay-400">
                    🏛️
                </div>
            )}

            {/* Message Bubble */}
            <div
                className={`max-w-[85%] md:max-w-[75%] px-5 py-3.5 text-sm md:text-base leading-relaxed ${
                    isAi
                        ? "bg-white text-stone-800 rounded-2xl rounded-tl-sm border border-clay-300 shadow-sm text-left"
                        : "bg-charcoal-900 text-white rounded-2xl rounded-tr-sm shadow-md text-right"
                }`}
            >
                <p>{message}</p>
            </div>
        </div>
    );
};

export default ChatMessage;
