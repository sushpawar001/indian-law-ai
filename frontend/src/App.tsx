import { useState, useEffect } from "react";
import "./App.css";
import MessageThreadScreen from "./components/MessageThreadScreen";
import ChatInput from "./components/ChatInput";
import DefaultThreadScreen from "./components/DefaultThreadScreen";
import type { ThreadMessage } from "./types/index";
import { MoreVertical, Trash2 } from "lucide-react";
import { API_URL } from "../constants";

interface ThreadsData {
    thread_id: string;
    thread_name: string;
}

export interface MessageAbstract {
    message_role: string;
    message_id: string;
    content: string;
}

export interface ThreadMessageOutput {
    user_message_id: string;
    thread_id: string;
    thread_name: string;
    ai_message: MessageAbstract;
}

function App() {
    const [threads, setThreads] = useState<ThreadsData[]>([]);
    const [selectedThread, setSelectedThread] = useState<string | null>(null);
    const [selectedThreadMessages, setSelectedThreadMessages] = useState<
        ThreadMessage[]
    >([]);
    const [isWaitingAiResponse, setIsWaitingAiResponse] =
        useState<boolean>(false);

    const [message, setMessage] = useState<string>("");

    const setMessageFromInput = (input: string) => {
        setMessage(input);
    };

    useEffect(() => {
        const fetchData = async () => {
            const data = await fetch(`${API_URL}/v1/threads`);
            const jData = await data.json();
            setThreads(jData);
        };
        fetchData();
    }, []);

    useEffect(() => {
        const fetchThreadMessages = async () => {
            if (selectedThread) {
                const data = await fetch(
                    `${API_URL}/v1/messages?thread_id=${selectedThread}`,
                );
                const jData = await data.json();
                setSelectedThreadMessages(jData);
            }
        };
        fetchThreadMessages();
    }, [selectedThread]);

    const sendMessage = async (content: string) => {
        const msg: ThreadMessage = {
            id: "temp_id_" + Date.now(),
            message_role: "user",
            content: content,
            sent_at: new Date(),
        };
        setSelectedThreadMessages((prev) => [...prev, msg]);
        console.log("sending message");
        const url = selectedThread
            ? `${API_URL}/v1/thread-message?thread_id=${selectedThread}`
            : `${API_URL}/v1/thread-message`;

        setIsWaitingAiResponse(true);
        const res = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ user_input: content }),
        });
        setIsWaitingAiResponse(false);
        const data: ThreadMessageOutput = await res.json();
        const newData: ThreadMessage = {
            id: data.ai_message.message_id,
            message_role: data.ai_message.message_role,
            content: data.ai_message.content,
            sent_at: new Date(),
        };
        console.log("ai response", data);
        setSelectedThreadMessages((prev) => [...prev, newData]);
        if (selectedThread === null) {
            setThreads((prev) => [
                ...prev,
                { thread_id: data.thread_id, thread_name: data.thread_name },
            ]);
        }
    };

    const deleteThread = async (thread_id: string) => {
        console.log("deleting thread", thread_id);
        const res = await fetch(`${API_URL}/v1/thread?thread_id=${thread_id}`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
        });
        const data = await res.json();
        console.log("delete response", data);
        setThreads((prev) =>
            prev.filter((thread) => thread.thread_id !== thread_id),
        );
        if (selectedThread === thread_id) {
            setSelectedThread(null);
            setSelectedThreadMessages([]);
        }
    };

    return (
        <div className="bg-clay-300 text-stone-800 h-screen flex p-2 md:p-4 gap-4 font-sans">
            <aside className="w-64 bg-clay-100 rounded-3xl shadow-sm shrink-0 hidden md:flex flex-col border border-clay-400 overflow-hidden">
                <div className="p-6 mt-2">
                    <h1 className="font-bold text-2xl text-stone-900 font-serif">
                        IndianLawAI.
                    </h1>
                </div>
                <div className="px-4">
                    <button
                        className="w-full py-3 rounded-2xl bg-charcoal-900 text-white hover:bg-black text-sm font-medium transition shadow-md cursor-pointer"
                        onClick={() => {
                            setSelectedThread(null);
                            setSelectedThreadMessages([]);
                        }}
                    >
                        + New Inquiry
                    </button>
                </div>
                <div className="flex-1 overflow-y-auto px-4 mt-8 space-y-1 text-sm text-stone-600">
                    <p className="text-[10px] font-bold text-stone-400 uppercase tracking-widest mb-2 ml-2">
                        History
                    </p>
                    {threads.length > 0 &&
                        threads.map((thread) => (
                            <div
                                key={thread.thread_id}
                                className={`group relative flex items-center justify-between py-1.5 px-2 rounded-xl hover:bg-clay-300 cursor-pointer transition font-medium ${selectedThread === thread.thread_id ? "bg-clay-300" : "bg-transparent"}`}
                                onClick={() =>
                                    setSelectedThread(thread.thread_id)
                                }
                            >
                                <span className="truncate flex-1">
                                    {thread.thread_name}
                                </span>

                                <div className="relative">
                                    <button className="p-1 hover:bg-clay-400 rounded-md transition opacity-0 group-hover:opacity-100">
                                        <MoreVertical
                                            size={16}
                                            className="text-stone-500"
                                        />
                                    </button>

                                    <div className="absolute right-0 mt-1 w-32 bg-white border border-stone-200 rounded-lg shadow-lg py-1 z-10 hidden group-focus-within:block">
                                        <button
                                            className="w-full flex items-center px-3 py-2 text-xs text-red-600 hover:bg-red-50 transition gap-2 cursor-pointer"
                                            onClick={async () => {
                                                await deleteThread(
                                                    thread.thread_id,
                                                );
                                            }}
                                        >
                                            <Trash2 size={14} />
                                            Delete
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))}
                </div>
            </aside>

            <main className="flex-1 bg-clay-50 rounded-3xl shadow-sm flex flex-col h-full relative border border-clay-400 overflow-hidden">
                {selectedThreadMessages.length > 0 ? (
                    <MessageThreadScreen
                        messages={selectedThreadMessages}
                        isWaitingAiResponse={isWaitingAiResponse}
                    />
                ) : (
                    <DefaultThreadScreen
                        setMessageFromInput={setMessageFromInput}
                    />
                )}
                <ChatInput sendMessage={sendMessage} message={message} />
            </main>
        </div>
    );
}

export default App;
