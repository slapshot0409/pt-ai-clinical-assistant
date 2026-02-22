export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-blue-700">promPT</h1>
          <p className="mt-2 text-gray-600">AI-powered Physical Therapy Clinical Decision Support</p>
        </div>
        <div className="bg-white rounded-2xl shadow p-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Patient Assessment Input</h2>
          <form className="space-y-6">

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Injury</label>
              <input
                type="text"
                placeholder="e.g. ACL tear, rotator cuff strain"
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Symptoms</label>
              <input
                type="text"
                placeholder="e.g. pain, swelling, limited range of motion"
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Diagnosis</label>
              <input
                type="text"
                placeholder="e.g. Grade II lateral ankle sprain"
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Stage of Healing</label>
              <select className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="">Select stage</option>
                <option value="acute">Acute</option>
                <option value="subacute">Subacute</option>
                <option value="chronic">Chronic</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Functional Limitations</label>
              <input
                type="text"
                placeholder="e.g. unable to bear weight, difficulty climbing stairs"
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Pain Level (0–10)</label>
              <input
                type="number"
                min={0}
                max={10}
                placeholder="0"
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Constraints</label>
              <input
                type="text"
                placeholder="e.g. no weight bearing, avoid overhead movements"
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-blue-700 hover:bg-blue-800 text-white font-semibold py-3 rounded-lg transition"
            >
              Generate Treatment Plan
            </button>

          </form>
        </div>
      </div>
    </main>
  );
}
