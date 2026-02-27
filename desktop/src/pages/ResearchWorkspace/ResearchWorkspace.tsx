import { useState } from 'react';
import { ingestFiles, researchQuestion } from '../../api/client';

function ResearchWorkspace() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState<string | null>(null);
  const [citations, setCitations] = useState<any[]>([]);
  const [uploadStatus, setUploadStatus] = useState<any[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onAsk() {
    setError(null);
    setLoading(true);
    setAnswer(null);
    setCitations([]);
    try {
      const res = await researchQuestion(query, 5);
      setAnswer(res.answer);
      setCitations(res.citations || []);
    } catch (e: any) {
      setError(e?.message ?? 'Failed to query');
    } finally {
      setLoading(false);
    }
  }

  async function onUpload(files: FileList | null) {
    if (!files || files.length === 0) return;
    setError(null);
    setUploadStatus(null);
    setLoading(true);
    try {
      const res = await ingestFiles(Array.from(files));
      setUploadStatus(res.results || []);
    } catch (e: any) {
      setError(e?.message ?? 'Failed to ingest files');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-8 space-y-6">
      <h1 className="text-3xl font-bold">Research Workspace</h1>

      <div className="bg-white p-6 rounded-lg shadow space-y-4">
        <div>
          <h2 className="text-xl font-semibold">Ingest Documents</h2>
          <p className="text-gray-600">
            Upload local docs to index them into the offline vector database.
          </p>
        </div>
        <input
          type="file"
          multiple
          accept=".pdf,.docx,.xlsx,.txt"
          onChange={(e) => onUpload(e.target.files)}
        />
        {uploadStatus && (
          <div className="text-sm">
            <div className="font-medium mb-2">Ingestion results</div>
            <ul className="list-disc pl-5 space-y-1">
              {uploadStatus.map((r, idx) => (
                <li key={idx}>
                  {r.filename}: {r.status} {r.chunks_indexed != null ? `(chunks: ${r.chunks_indexed})` : ''}
                  {r.error ? ` — ${r.error}` : ''}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <div className="bg-white p-6 rounded-lg shadow space-y-4">
        <div>
          <h2 className="text-xl font-semibold">Ask Questions (RAG)</h2>
          <p className="text-gray-600">
            Ask questions over your ingested documents. The answer will include citations.
          </p>
        </div>

        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about your documents..."
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <div className="flex gap-3">
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-60"
            disabled={loading || !query.trim()}
            onClick={onAsk}
          >
            {loading ? 'Working…' : 'Ask'}
          </button>
          <button
            className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-60"
            disabled={loading}
            onClick={() => {
              setQuery('');
              setAnswer(null);
              setCitations([]);
              setError(null);
            }}
          >
            Clear
          </button>
        </div>

        {error && <div className="text-red-600 text-sm">{error}</div>}

        {answer && (
          <div className="border rounded-lg p-4 bg-gray-50">
            <div className="font-semibold mb-2">Answer</div>
            <div className="whitespace-pre-wrap text-sm">{answer}</div>
          </div>
        )}

        {citations.length > 0 && (
          <div className="text-sm space-y-2">
            <div className="font-semibold">Citations</div>
            <ul className="space-y-2">
              {citations.map((c, idx) => (
                <li key={idx} className="border rounded p-3">
                  <div className="text-xs text-gray-600 mb-1">
                    [{idx + 1}] {c?.metadata?.source ?? 'unknown'}
                  </div>
                  <div className="whitespace-pre-wrap">{c?.text}</div>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default ResearchWorkspace;

