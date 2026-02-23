"use client";
import { useState } from "react";

const initialForm = {
  symptoms: "",
  diagnosis: "",
  healing_stage: "",
  functional_limitations: "",
  pain_level: "",
  pain_with_movement: "",
  tenderness_to_palpation: "",
  constraints: "",
};

const LETTERS = ["A", "B", "C", "D", "E", "F"];

export default function Home() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const payload = {
        symptoms: form.symptoms.split(",").map((s) => s.trim()).filter(Boolean),
        diagnosis: form.diagnosis,
        healing_stage: form.healing_stage,
        functional_limitations: form.functional_limitations.split(",").map((s) => s.trim()).filter(Boolean),
        pain_level: form.pain_level === "" ? 0 : Number(form.pain_level),
        pain_with_movement: form.pain_with_movement.split(",").map((s) => s.trim()).filter(Boolean),
        tenderness_to_palpation: form.tenderness_to_palpation.split(",").map((s) => s.trim()).filter(Boolean),
        constraints: form.constraints.split(",").map((s) => s.trim()).filter(Boolean),
      };

      const res = await fetch("http://localhost:8000/api/v1/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Failed to generate treatment plan");
      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-blue-700">promPT</h1>
          <p className="mt-2 text-gray-600">AI-powered Physical Therapy Clinical Decision Support</p>
        </div>

        <div className="bg-white rounded-2xl shadow p-8 mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Patient Assessment Input</h2>
          <div className="space-y-6">

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Diagnosis</label>
              <input type="text" placeholder="e.g. Grade II lateral ankle sprain"
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={form.diagnosis} onChange={(e) => setForm({ ...form, diagnosis: e.target.value })} />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Symptoms <span className="text-gray-400">(comma separated)</span></label>
              <input type="text" placeholder="e.g. pain, swelling, limited range of motion"
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={form.symptoms} onChange={(e) => setForm({ ...form, symptoms: e.target.value })} />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Pain with Movement <span className="text-gray-400">(comma separated)</span></label>
              <input type="text" placeholder="e.g. pain with resisted shoulder external rotation, pain with overhead reach"
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={form.pain_with_movement} onChange={(e) => setForm({ ...form, pain_with_movement: e.target.value })} />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Tenderness to Palpation <span className="text-gray-400">(comma separated)</span></label>
              <input type="text" placeholder="e.g. anterior shoulder, bicipital groove, AC joint"
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={form.tenderness_to_palpation} onChange={(e) => setForm({ ...form, tenderness_to_palpation: e.target.value })} />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Stage of Healing</label>
              <select className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={form.healing_stage} onChange={(e) => setForm({ ...form, healing_stage: e.target.value })}>
                <option value="">Select stage</option>
                <option value="acute">Acute</option>
                <option value="subacute">Subacute</option>
                <option value="chronic">Chronic</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Functional Limitations <span className="text-gray-400">(comma separated)</span></label>
              <input type="text" placeholder="e.g. unable to bear weight, difficulty climbing stairs"
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={form.functional_limitations} onChange={(e) => setForm({ ...form, functional_limitations: e.target.value })} />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Pain Level (0-10)</label>
              <input type="number" min={0} max={10} placeholder="0"
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={form.pain_level} onChange={(e) => setForm({ ...form, pain_level: e.target.value })} />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Constraints <span className="text-gray-400">(comma separated)</span></label>
              <input type="text" placeholder="e.g. no weight bearing, avoid overhead movements"
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={form.constraints} onChange={(e) => setForm({ ...form, constraints: e.target.value })} />
            </div>

            {error && <p className="text-red-500 text-sm">{error}</p>}

            <button onClick={handleSubmit} disabled={loading}
              className="w-full bg-blue-700 hover:bg-blue-800 disabled:bg-blue-300 text-white font-semibold py-3 rounded-lg transition">
              {loading ? "Generating Treatment Plan..." : "Generate Treatment Plan"}
            </button>
          </div>
        </div>

        {result && (
          <div className="bg-white rounded-2xl shadow p-8 space-y-8">
            <h2 className="text-xl font-semibold text-blue-700">Clinical Decision Support</h2>

            {/* Differential Diagnosis - lettered */}
            <div>
              <h3 className="font-semibold text-gray-800 mb-3">Differential Diagnosis</h3>
              <ol className="space-y-2">
                {result.differential_diagnosis.map((d: string, i: number) => (
                  <li key={i} className="flex gap-3 text-sm text-gray-700">
                    <span className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center font-semibold text-xs">{LETTERS[i]}</span>
                    <span>{d}</span>
                  </li>
                ))}
              </ol>
            </div>

            {/* Special Tests */}
            <div>
              <h3 className="font-semibold text-gray-800 mb-3">Recommended Special Tests</h3>
              <div className="space-y-3">
                {result.special_tests.map((t: any, i: number) => (
                  <div key={i} className="border border-purple-200 bg-purple-50 rounded-lg p-4">
                    <p className="font-medium text-purple-800">{t.name}</p>
                    <p className="text-sm text-gray-700 mt-1"><span className="font-medium">Procedure:</span> {t.procedure}</p>
                    <p className="text-sm text-gray-700 mt-1"><span className="font-medium">Positive finding:</span> {t.positive_finding}</p>
                    <p className="text-sm text-gray-500 mt-1"><span className="font-medium">Indicates:</span> {t.indicates}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Treatment Plan */}
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">Treatment Plan</h3>
              <p className="text-gray-700 text-sm leading-relaxed">{result.treatment_plan}</p>
            </div>

            {/* Manual Therapy */}
            <div>
              <h3 className="font-semibold text-gray-800 mb-3">Manual Therapy</h3>
              <div className="space-y-3">
                {result.manual_therapy.map((m: any, i: number) => (
                  <div key={i} className="bg-green-50 rounded-lg p-4">
                    <p className="font-medium text-green-800">{m.technique}</p>
                    <p className="text-sm text-gray-600">Target: {m.target}</p>
                    {m.rationale && <p className="text-sm text-gray-500 mt-1">{m.rationale}</p>}
                  </div>
                ))}
              </div>
            </div>

            {/* Exercise Protocol */}
            <div>
              <h3 className="font-semibold text-gray-800 mb-3">Exercise Protocol</h3>
              <div className="space-y-3">
                {result.exercise_protocol.map((ex: any, i: number) => (
                  <div key={i} className="bg-blue-50 rounded-lg p-4">
                    <p className="font-medium text-blue-800">{ex.name}</p>
                    {ex.description && <p className="text-sm text-gray-700 mt-1">{ex.description}</p>}
                    <p className="text-sm text-gray-600 mt-2">{ex.sets} sets x {ex.reps} — {ex.frequency}</p>
                    {ex.notes && <p className="text-sm text-gray-500 mt-1 italic">{ex.notes}</p>}
                  </div>
                ))}
              </div>
            </div>

            {/* Progression Criteria */}
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">Progression Criteria</h3>
              <ul className="list-disc list-inside space-y-1">
                {result.progression_criteria.map((c: string, i: number) => (
                  <li key={i} className="text-sm text-gray-700">{c}</li>
                ))}
              </ul>
            </div>

            {/* Contraindications */}
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">Contraindications</h3>
              <ul className="list-disc list-inside space-y-1">
                {result.contraindications.map((c: string, i: number) => (
                  <li key={i} className="text-sm text-red-600">{c}</li>
                ))}
              </ul>
            </div>

            {/* Recovery Timeline */}
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">Recovery Timeline</h3>
              <p className="text-sm text-gray-700">{result.recovery_timeline}</p>
            </div>

            {/* Evidence Citations - numbered with anchors */}
            <div>
              <h3 className="font-semibold text-gray-800 mb-2">Evidence Citations</h3>
              <div className="space-y-2">
                {result.citations.map((c: any, i: number) => (
                  <div key={i} id={`citation-${i + 1}`} className="border border-gray-200 rounded-lg p-3 flex gap-3 scroll-mt-8">
                    <span className="flex-shrink-0 w-6 h-6 bg-gray-100 text-gray-600 rounded-full flex items-center justify-center font-semibold text-xs">{i + 1}</span>
                    <div>
                      <a href={c.url} target="_blank" rel="noopener noreferrer"
                        className="text-blue-600 hover:underline text-sm font-medium">{c.title}</a>
                      <p className="text-xs text-gray-500 mt-1">{c.authors?.join(", ")} — {c.year} — {c.source}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

          </div>
        )}
      </div>
    </main>
  );
}
