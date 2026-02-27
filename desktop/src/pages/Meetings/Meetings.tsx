import { useState } from 'react';
import { meetingTranscript, Task, approveTask, rejectTask } from '../../api/client';

function Meetings() {
  const [title, setTitle] = useState('');
  const [transcript, setTranscript] = useState('');
  const [summary, setSummary] = useState<string | null>(null);
  const [detectedTasks, setDetectedTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onProcess() {
    setError(null);
    setLoading(true);
    setSummary(null);
    setDetectedTasks([]);
    try {
      const res = await meetingTranscript(title || null, transcript);
      setSummary(res.summary);
      setDetectedTasks(res.detected_tasks || []);
    } catch (e: any) {
      setError(e?.message ?? 'Failed to process transcript');
    } finally {
      setLoading(false);
    }
  }

  async function onApprove(id: number) {
    await approveTask(id);
    setDetectedTasks((prev) => prev.map((t) => (t.id === id ? { ...t, status: 'approved' } : t)));
  }

  async function onReject(id: number) {
    await rejectTask(id);
    setDetectedTasks((prev) => prev.map((t) => (t.id === id ? { ...t, status: 'rejected' } : t)));
  }

  return (
    <div className="p-8 space-y-6">
      <h1 className="text-3xl font-bold">Meetings</h1>

      <div className="bg-white p-6 rounded-lg shadow space-y-4">
        <div>
          <h2 className="text-xl font-semibold">Transcript → Summary → Tasks</h2>
          <p className="text-gray-600">
            Paste a transcript to generate an offline summary and extract action items (tasks).
          </p>
        </div>

        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Meeting title (optional)"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg"
        />

        <textarea
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          placeholder="Paste meeting transcript here…"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg"
          rows={10}
        />

        <button
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-60"
          disabled={loading || !transcript.trim()}
          onClick={onProcess}
        >
          {loading ? 'Processing…' : 'Summarize & extract tasks'}
        </button>

        {error && <div className="text-red-600 text-sm">{error}</div>}

        {summary && (
          <div className="border rounded-lg p-4 bg-gray-50">
            <div className="font-semibold mb-2">Summary</div>
            <div className="whitespace-pre-wrap text-sm">{summary}</div>
          </div>
        )}

        {detectedTasks.length > 0 && (
          <div className="space-y-2">
            <div className="font-semibold">Detected tasks</div>
            <ul className="space-y-2">
              {detectedTasks.map((t) => (
                <li key={t.id} className="border rounded p-3 flex items-start justify-between gap-4">
                  <div>
                    <div className="font-medium">{t.title}</div>
                    {t.description && <div className="text-sm text-gray-700 mt-1">{t.description}</div>}
                    <div className="text-xs text-gray-500 mt-1">status: {t.status}</div>
                  </div>
                  {t.status === 'detected' ? (
                    <div className="flex gap-2">
                      <button
                        className="px-3 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                        onClick={() => onApprove(t.id)}
                      >
                        Approve
                      </button>
                      <button
                        className="px-3 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                        onClick={() => onReject(t.id)}
                      >
                        Reject
                      </button>
                    </div>
                  ) : null}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default Meetings;

