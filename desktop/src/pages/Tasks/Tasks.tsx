import { useEffect, useState } from 'react';
import { approveTask, getTasks, rejectTask, Task } from '../../api/client';

function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filter, setFilter] = useState<'all' | 'detected' | 'approved' | 'pending'>('all');
  const [loading, setLoading] = useState(false);

  async function refresh() {
    setLoading(true);
    try {
      const res = await getTasks();
      setTasks(res.tasks);
    } catch (e: any) {
      console.error('Failed to load tasks:', e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function onApprove(id: number) {
    try {
      await approveTask(id);
      await refresh();
    } catch (e: any) {
      console.error('Failed to approve task:', e);
    }
  }

  async function onReject(id: number) {
    try {
      await rejectTask(id);
      await refresh();
    } catch (e: any) {
      console.error('Failed to reject task:', e);
    }
  }

  const filteredTasks = tasks.filter((t) => {
    if (filter === 'all') return true;
    return t.status === filter;
  });

  const detectedCount = tasks.filter((t) => t.status === 'detected').length;
  const approvedCount = tasks.filter((t) => t.status === 'approved').length;

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Tasks</h1>
        <button
          className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
          onClick={() => refresh()}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-800">
          <strong>Note:</strong> Tasks are automatically extracted from uploaded documents and meeting
          transcripts. Review and approve detected tasks below.
        </p>
      </div>

      {/* Status Filter */}
      <div className="flex gap-2">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded ${
            filter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-200 hover:bg-gray-300'
          }`}
        >
          All ({tasks.length})
        </button>
        <button
          onClick={() => setFilter('detected')}
          className={`px-4 py-2 rounded ${
            filter === 'detected' ? 'bg-blue-600 text-white' : 'bg-gray-200 hover:bg-gray-300'
          }`}
        >
          Needs Review ({detectedCount})
        </button>
        <button
          onClick={() => setFilter('approved')}
          className={`px-4 py-2 rounded ${
            filter === 'approved' ? 'bg-blue-600 text-white' : 'bg-gray-200 hover:bg-gray-300'
          }`}
        >
          Approved ({approvedCount})
        </button>
      </div>

      {/* Tasks List */}
      <div className="bg-white p-6 rounded-lg shadow">
        {filteredTasks.length === 0 ? (
          <div className="text-center py-12 text-gray-600">
            {filter === 'detected' ? (
              <>
                <div className="text-4xl mb-4">✅</div>
                <p>No tasks need review.</p>
                <p className="text-sm mt-2">Upload documents or process meeting transcripts to extract tasks.</p>
              </>
            ) : (
              <>
                <div className="text-4xl mb-4">📋</div>
                <p>No tasks found.</p>
                <p className="text-sm mt-2">Tasks will appear here after you upload documents or process meetings.</p>
              </>
            )}
          </div>
        ) : (
          <ul className="space-y-3">
            {filteredTasks.map((t) => (
              <li
                key={t.id}
                className={`border rounded-lg p-4 ${
                  t.status === 'detected' ? 'border-yellow-300 bg-yellow-50' : ''
                }`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold">{t.title}</span>
                      <span
                        className={`text-xs px-2 py-1 rounded ${
                          t.status === 'detected'
                            ? 'bg-yellow-200 text-yellow-800'
                            : t.status === 'approved'
                              ? 'bg-green-200 text-green-800'
                              : 'bg-gray-200 text-gray-800'
                        }`}
                      >
                        {t.status}
                      </span>
                    </div>
                    {t.description && (
                      <div className="text-sm text-gray-700 mt-2">{t.description}</div>
                    )}
                    <div className="text-xs text-gray-500 mt-2 flex gap-4">
                      {t.due_date && <span>📅 Due: {t.due_date}</span>}
                      {t.priority && <span>⚡ Priority: {t.priority}</span>}
                      {t.scheduled_for && <span>⏰ Scheduled: {t.scheduled_for}</span>}
                    </div>
                  </div>
                  {t.status === 'detected' && (
                    <div className="flex gap-2">
                      <button
                        className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                        onClick={() => onApprove(t.id)}
                      >
                        ✓ Approve
                      </button>
                      <button
                        className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                        onClick={() => onReject(t.id)}
                      >
                        ✗ Reject
                      </button>
                    </div>
                  )}
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default Tasks;

