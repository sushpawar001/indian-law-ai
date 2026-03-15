import { useState } from "react";
import { SendHorizontal } from "lucide-react";

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
                    className="p-3 bg-charcoal-900 text-white rounded-xl hover:bg-black transition cursor-pointer duration-500 hover:-rotate-90"
                    onClick={() => {
                        sendMessage(userMessage);
                        setUserMessage("");
                    }}
                >
                    <SendHorizontal size={22}/>
                </button>
            </div>
        </div>
    );
}
