// answer는 항상 "1. 현재 역량 평가 / 2. 추천 공고 또는 공모전 / 3. 부족한 역량 및 준비 방향"
// 3단계 형식을 따르도록 프롬프트가 지시하지만(backend/services/llm_service.py의 build_rag_prompt),
// LLM이 형식을 어기거나 Mock/에러 메시지가 오면 파싱이 실패할 수 있어 항상 폴백을 둔다.
const SECTION_LABELS = [
    { icon: "✅", title: "현재 역량 평가" },
    { icon: "🎯", title: "추천 공고 및 공모전" },
    { icon: "📌", title: "부족한 역량 및 준비 방향" },
];

function findMarker(text, marker, from) {
    // 줄 시작의 "1.", "2.", "3." (앞에 #, * 같은 마크다운 기호가 붙어도 허용)만 구분자로 삼는다.
    const re = new RegExp(`(?:^|\\n)[ \\t]*[#*]*[ \\t]*${marker}[.)][ \\t]*`);
    const match = text.slice(from).match(re);
    if (!match) return null;
    return { start: from + match.index, end: from + match.index + match[0].length };
}

function parseSections(answer) {
    // 1 -> 2 -> 3 순서로만 탐색해서, 답변 안의 중첩 번호 목록(예: 3번 섹션 본문 안의 "1. ...")이
    // 새 섹션 시작으로 잘못 인식되지 않게 한다.
    const m1 = findMarker(answer, "1", 0);
    if (!m1) return null;
    const m2 = findMarker(answer, "2", m1.end);
    if (!m2) return null;
    const m3 = findMarker(answer, "3", m2.end);
    if (!m3) return null;

    return [
        answer.slice(m1.end, m2.start).trim(),
        answer.slice(m2.end, m3.start).trim(),
        answer.slice(m3.end).trim(),
    ];
}

function ResultCard({ answer }) {
    const sections = parseSections(answer);

    return (
        <div className="bg-white rounded-2xl shadow-sm border-l-4 border-emerald-500 p-6">
            <span className="inline-block text-[11px] font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full mb-2">
                AI 매칭 리포트
            </span>
            <h2 className="text-lg font-semibold text-slate-800 mb-3">📊 AI 분석 결과</h2>
            {sections ? (
                <div className="space-y-4">
                    {SECTION_LABELS.map((label, i) => (
                        <div key={label.title}>
                            <h3 className="text-sm font-medium text-slate-700 mb-1">
                                {label.icon} {label.title}
                            </h3>
                            <p className="text-slate-600 text-sm leading-relaxed whitespace-pre-line">
                                {sections[i]}
                            </p>
                        </div>
                    ))}
                </div>
            ) : (
                <p className="text-slate-600 text-sm leading-relaxed whitespace-pre-line">{answer}</p>
            )}
        </div>
    );
}
export default ResultCard;