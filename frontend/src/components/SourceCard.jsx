const AVATAR_COLORS = ["bg-indigo-500", "bg-emerald-500", "bg-amber-500", "bg-rose-500", "bg-sky-500"];

function getRelevance(distance) {
    const pct = Math.max(0, Math.min(100, Math.round((1 - distance) * 100)));
    if (pct >= 70) return { pct, label: "관련도 높음", className: "bg-emerald-50 text-emerald-700 border-emerald-200" };
    if (pct >= 40) return { pct, label: "관련도 보통", className: "bg-amber-50 text-amber-700 border-amber-200" };
    return { pct, label: "관련도 낮음", className: "bg-slate-100 text-slate-600 border-slate-200" };
}

function SourceCard({ sources }) {
    if (!sources || sources.length === 0) {
        return (
            <div className="bg-slate-50 rounded-2xl border border-slate-200 p-4 text-sm text-slate-500">
                참고한 공고 데이터가 없습니다.
            </div>
        );
    }

    return (
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
            <h2 className="text-lg font-semibold text-slate-800 mb-4">📄 참고한 공고 출처</h2>
            <div className="space-y-3">
                {sources.map((source, index) => {
                    const skills = (source.required_skills || "")
                        .split(",")
                        .map((s) => s.trim())
                        .filter(Boolean);
                    const relevance = typeof source.distance === "number" ? getRelevance(source.distance) : null;
                    const avatarColor = AVATAR_COLORS[index % AVATAR_COLORS.length];

                    return (
                        <div
                            key={index}
                            className="flex gap-3 border border-slate-100 rounded-xl p-4 hover:border-slate-200 transition-colors"
                        >
                            <div
                                className={`w-10 h-10 shrink-0 rounded-full ${avatarColor} text-white flex items-center justify-center font-semibold text-sm`}
                            >
                                {source.company ? source.company[0] : "?"}
                            </div>
                            <div className="flex-1 min-w-0">
                                <div className="flex items-center justify-between gap-2">
                                    <p className="text-sm font-semibold text-slate-800 truncate">
                                        {source.title || "제목 없음"}
                                    </p>
                                    {relevance && (
                                        <span
                                            className={`shrink-0 text-xs font-medium px-2 py-0.5 rounded-full border ${relevance.className}`}
                                        >
                                            {relevance.label} {relevance.pct}%
                                        </span>
                                    )}
                                </div>
                                <p className="text-xs text-slate-500 mt-0.5">{source.company}</p>
                                {skills.length > 0 && (
                                    <div className="flex flex-wrap gap-1.5 mt-2">
                                        {skills.map((skill) => (
                                            <span
                                                key={skill}
                                                className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full"
                                            >
                                                {skill}
                                            </span>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
export default SourceCard;
