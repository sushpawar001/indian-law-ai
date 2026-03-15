import { useState } from "react";

export default function ChatInput({
    sendMessage,
}: {
    sendMessage: CallableFunction;
}) {
    const [userMessage, setUserMessage] = useState<string>("");
    return (
        <div className="absolute bottom-6 left-0 w-full px-4 md:px-12">
            <div className="max-w-3xl mx-auto relative bg-white rounded-2xl shadow-xl border border-clay-300 p-2 flex items-end">
                <textarea
                    className="w-full bg-transparent pl-4 pr-4 py-3 focus:outline-none resize-none overflow-hidden text-stone-800 placeholder-stone-400"
                    // rows="1"
                    placeholder="Ask your legal question..."
                    value={userMessage}
                    onChange={(e) => {
                        setUserMessage(e.target.value);
                    }}
                ></textarea>
                <button
                    className="p-3 bg-charcoal-900 text-white rounded-xl hover:bg-black transition cursor-pointer"
                    onClick={() => {
                        sendMessage(userMessage);
                        setUserMessage("");
                    }}
                >
                    <svg
                        className="w-4 h-4"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                    >
                        <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"></path>
                    </svg>
                </button>
            </div>
        </div>
    );
}
