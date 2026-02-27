import { useState, useCallback, useEffect } from 'react';
import { ingestFiles, checkBackendHealth } from '../../api/client';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const [isDragging, setIsDragging] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<any[] | null>(null);
  const [detectedTasks, setDetectedTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [backendConnected, setBackendConnected] = useState<boolean | null>(null);
  const navigate = useNavigate();

  // Check backend connection on mount
  useEffect(() => {
    checkBackendHealth().then(setBackendConnected);
  }, []);

  const handleFiles = useCallback(async (files: FileList | File[]) => {
    const fileArray = Array.from(files);
    if (fileArray.length === 0) return;

    setLoading(true);
    setUploadStatus(null);
    setDetectedTasks([]);

    try {
      const res = await ingestFiles(fileArray);
      setUploadStatus(res.results || []);
      if (res.detected_tasks && res.detected_tasks.length > 0) {
        setDetectedTasks(res.detected_tasks);
      }
      
      // Check if all files succeeded
      const allSucceeded = (res.results || []).every((r: any) => r.status === 'ingested');
      if (!allSucceeded) {
        // Some files failed, but show results anyway
        console.warn('Some files failed to upload');
      }
    } catch (e: any) {
      // Extract detailed error message
      const errorMessage = e?.response?.data?.detail || e?.message || 'Failed to upload files';
      const errorDetails = [];
      
      // Add filename if available
      fileArray.forEach((file) => {
        errorDetails.push({
          filename: file.name,
          status: 'error',
          error: errorMessage,
        });
      });
      
      setUploadStatus(errorDetails.length > 0 ? errorDetails : [{ status: 'error', error: errorMessage }]);
      console.error('Upload error:', e);
    } finally {
      setLoading(false);
    }
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);
      if (e.dataTransfer.files) {
        handleFiles(e.dataTransfer.files);
      }
    },
    [handleFiles]
  );

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.files) {
        handleFiles(e.target.files);
      }
    },
    [handleFiles]
  );

  return (
    <div className="p-8 space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>

      {/* Backend Connection Status */}
      {backendConnected === false && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800 text-sm">
            <strong>⚠️ Backend not connected:</strong> Cannot reach backend server at http://localhost:8001.
            <br />
            Please make sure the backend is running: <code className="bg-red-100 px-2 py-1 rounded">python src\api.py</code>
          </p>
        </div>
      )}

      {/* File Drop Zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
          isDragging
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 bg-gray-50 hover:border-gray-400'
        }`}
      >
        <div className="space-y-4">
          <div className="text-4xl">📁</div>
          <div>
            <h2 className="text-xl font-semibold mb-2">Drop files here or click to upload</h2>
            <p className="text-gray-600 mb-4">
              Supports: PDF, DOCX, XLSX, PPTX, TXT
              <br />
              Files will be indexed and tasks will be automatically extracted
            </p>
            <input
              type="file"
              multiple
              accept=".pdf,.docx,.xlsx,.pptx,.txt"
              onChange={handleFileInput}
              className="hidden"
              id="file-upload"
            />
            <label
              htmlFor="file-upload"
              className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg cursor-pointer hover:bg-blue-700 disabled:opacity-60"
            >
              {loading ? 'Processing...' : 'Choose Files'}
            </label>
          </div>
        </div>
      </div>

      {/* Upload Results */}
      {uploadStatus && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-3">Upload Results</h3>
          <ul className="space-y-2">
            {uploadStatus.map((r, idx) => (
              <li key={idx} className="text-sm">
                <span className="font-medium">{r.filename}:</span>{' '}
                <span className={r.status === 'error' ? 'text-red-600' : 'text-green-600'}>
                  {r.status}
                </span>
                {r.chunks_indexed != null && ` (${r.chunks_indexed} chunks)`}
                {r.tasks_extracted != null && ` • ${r.tasks_extracted} tasks extracted`}
                {r.error && <span className="text-red-600"> — {r.error}</span>}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Detected Tasks Preview */}
      {detectedTasks.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-lg font-semibold">
              {detectedTasks.length} Task{detectedTasks.length !== 1 ? 's' : ''} Detected
            </h3>
            <button
              onClick={() => navigate('/tasks')}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Review All Tasks →
            </button>
          </div>
          <ul className="space-y-2">
            {detectedTasks.slice(0, 5).map((t) => (
              <li key={t.id} className="text-sm border-l-4 border-blue-500 pl-3">
                <span className="font-medium">{t.title}</span>
                {t.description && <span className="text-gray-600"> — {t.description}</span>}
              </li>
            ))}
            {detectedTasks.length > 5 && (
              <li className="text-sm text-gray-500 italic">
                ...and {detectedTasks.length - 5} more
              </li>
            )}
          </ul>
        </div>
      )}

      {/* Quick Links */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div
          className="bg-white p-6 rounded-lg shadow cursor-pointer hover:shadow-lg transition-shadow"
          onClick={() => navigate('/tasks')}
        >
          <h2 className="text-xl font-semibold mb-2">✅ Tasks</h2>
          <p className="text-gray-600">Review and approve detected tasks</p>
        </div>
        <div
          className="bg-white p-6 rounded-lg shadow cursor-pointer hover:shadow-lg transition-shadow"
          onClick={() => navigate('/meetings')}
        >
          <h2 className="text-xl font-semibold mb-2">🎤 Meetings</h2>
          <p className="text-gray-600">Process meeting transcripts</p>
        </div>
        <div
          className="bg-white p-6 rounded-lg shadow cursor-pointer hover:shadow-lg transition-shadow"
          onClick={() => navigate('/research')}
        >
          <h2 className="text-xl font-semibold mb-2">🔍 Research</h2>
          <p className="text-gray-600">Search your indexed documents</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

