// frontend/src/App.jsx
import { useState } from "react";
import InputForm from "./components/InputForm";
import ResultCard from "./components/ResultCard";
import SourceCard from "./components/SourceCard";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";
// ⚠️ API Key는 절대 여기에 넣지 않습니다

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleAnalyze(formData) {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          major: formData.major,
          skills: formData.skills,
          job_type: formData.jobType,
          experience_years: formData.experienceYears,
          preferred_company_size: formData.preferredCompanySize,
        }),
      });

      if (!response.ok) {
        let errorDetail = `서버 오류: ${response.status}`;
        try {
          const errData = await response.json();
          // FastAPI의 기본 에러 포맷인 detail 필드를 확인
          if (errData.detail) {
            errorDetail = typeof errData.detail === 'string' 
              ? errData.detail 
              : JSON.stringify(errData.detail);
          }
        } catch (e) {
          // JSON 파싱 실패 시 무시
        }
        throw new Error(errorDetail);
      }
      
      const data = await response.json();
      setResult(data);

    } catch (err) {
      // TypeError는 fetch API가 네트워크 오류(서버 꺼짐, CORS 등)일 때 발생시킵니다.
      if (err instanceof TypeError) {
        setError("서버에 연결할 수 없습니다. 백엔드 서버가 실행 중인지 확인하세요.");
      } else {
        setError(err.message);
      }
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-3xl mx-auto px-4 py-4 flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-indigo-600 text-white flex items-center justify-center font-bold text-sm shrink-0">
            CF
          </div>
          <div>
            <h1 className="text-lg font-bold text-slate-800 leading-tight">CareerFit AI</h1>
            <p className="text-slate-500 text-xs">취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치</p>
          </div>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-10">
        <InputForm onSubmit={handleAnalyze} isLoading={isLoading} />

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">{error}</div>
        )}

        {isLoading && (
          <div className="mt-8 text-center text-slate-500">분석 중입니다...</div>
        )}

        {result && (
          <div className="mt-8 space-y-4">
            <ResultCard answer={result.answer} />
            {result.sources && result.sources.length > 0 && (
              <SourceCard sources={result.sources} />
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;