import React from "react";

export default function DefaultThreadScreen({
    setMessageFromInput,
}: {
    setMessageFromInput: (input: string) => void;
}) {
    return (
        <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-8">
            <div className="max-w-2xl mx-auto flex flex-col items-center text-center mt-12">
                <div className="w-16 h-16 rounded-2xl bg-clay-300 text-charcoal-900 flex items-center justify-center text-3xl mb-6 shadow-sm border border-clay-400">
                    🏛️
                </div>
                <h2 className="text-3xl text-stone-900 mb-4 font-serif">
                    Indian Law, Simplified.
                </h2>
                <p className="text-stone-500 max-w-md">
                    Search across the Constitution, BNS, Corporate Law, and
                    localized Acts to get answers in plain English.
                </p>

                <div className="grid grid-cols-2 gap-3 mt-10 w-full">
                    <button
                        className="p-4 border border-clay-300 rounded-2xl text-left hover:bg-white hover:shadow-sm transition group"
                        onClick={() =>
                            setMessageFromInput(
                                "What are the grounds for eviction of a tenant under Indian law?",
                            )
                        }
                    >
                        <p className="text-sm font-semibold text-stone-800">
                            Draft a notice &rarr;
                        </p>
                        <p className="text-xs text-stone-500 mt-1">
                            Tenant eviction under state law
                        </p>
                    </button>
                    <button
                        className="p-4 border border-clay-300 rounded-2xl text-left hover:bg-white hover:shadow-sm transition group"
                        onClick={() =>
                            setMessageFromInput(
                                "Explain the difference between anticipatory bail and regular bail in Indian law.",
                            )
                        }
                    >
                        <p className="text-sm font-semibold text-stone-800">
                            Explain a concept &rarr;
                        </p>
                        <p className="text-xs text-stone-500 mt-1">
                            Anticipatory bail vs Regular bail
                        </p>
                    </button>
                </div>
            </div>

            <div className="h-32"></div>
        </div>
    );
}
