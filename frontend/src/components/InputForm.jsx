import { useState } from "react";

function InputForm({ onSubmit, isLoading }) {
    const [major, setMajor] = useState("");
    const [skillsInput, setSkillsInput] = useState("");
    const [jobType, setJobType] = useState("");
    const [experienceYears, setExperienceYears] = useState(0);
    const [preferredCompanySize, setPreferredCompanySize] = useState("무관");

    function handleSubmit() {
        const skills = skillsInput.split(",").map(s => s.trim()).filter(Boolean);
        onSubmit({ major, skills, jobType, experienceYears, preferredCompanySize });
    }

    const parsedSkills = skillsInput.split(",").map(s => s.trim()).filter(Boolean);
    const isValid = major.trim() !== "" && parsedSkills.length > 0 && jobType.trim() !== "";

    return (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
            <h2 className="text-lg font-semibold text-slate-700 mb-4">내 정보 입력</h2>
            <div className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-slate-600 mb-1">전공</label>
                    <input type="text" value={major} onChange={e => setMajor(e.target.value)}
                        placeholder="예: 통계학과"
                        className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <div>
                    <label className="block text-sm font-medium text-slate-600 mb-1">보유 스킬 (쉼표 구분)</label>
                    <input type="text" value={skillsInput} onChange={e => setSkillsInput(e.target.value)}
                        placeholder="예: Python, SQL, R"
                        className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <div>
                    <label className="block text-sm font-medium text-slate-600 mb-1">관심 직무</label>
                    <input type="text" value={jobType} onChange={e => setJobType(e.target.value)}
                        placeholder="예: 데이터 분석"
                        className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <div>
                    <label className="block text-sm font-medium text-slate-600 mb-1">경력 (년)</label>
                    <input type="number" min="0" value={experienceYears}
                        onChange={e => setExperienceYears(Number(e.target.value))}
                        placeholder="예: 0"
                        className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <div>
                    <label className="block text-sm font-medium text-slate-600 mb-1">선호 기업 형태</label>
                    <select value={preferredCompanySize} onChange={e => setPreferredCompanySize(e.target.value)}
                        className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="무관">무관</option>
                        <option value="대기업">대기업</option>
                        <option value="중견기업">중견기업</option>
                        <option value="스타트업">스타트업</option>
                    </select>
                </div>
                <button onClick={handleSubmit}
                    disabled={isLoading || !isValid}
                    className="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-slate-300 text-white font-medium py-2 px-4 rounded-lg transition-colors text-sm">
                    {isLoading ? "분석 중..." : "역량 분석 요청"}
                </button>
            </div>
        </div>
    );
}

export default InputForm;