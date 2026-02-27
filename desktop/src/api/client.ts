import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 300000, // 5 minutes for long operations
});

// Separate axios instance for file uploads (no default Content-Type)
const fileUploadClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes for file uploads
  maxContentLength: Infinity,
  maxBodyLength: Infinity,
});

// Add error interceptor for better error messages
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      error.message = 'Request timeout - the server took too long to respond. Please try again.';
    } else if (error.code === 'ERR_NETWORK' || !error.response) {
      error.message = 'Cannot connect to backend server. Make sure the backend is running on http://localhost:8001';
    } else if (error.response) {
      const status = error.response.status;
      const data = error.response.data;
      if (status === 413) {
        error.message = 'File too large. Please upload smaller files.';
      } else if (status === 400) {
        error.message = data?.detail || 'Invalid request. Please check your file format.';
      } else if (status >= 500) {
        error.message = `Server error: ${data?.detail || 'Internal server error'}`;
      } else {
        error.message = data?.detail || `Error ${status}: ${error.message}`;
      }
    }
    return Promise.reject(error);
  }
);

export async function ingestFiles(files: File[]) {
  if (!files || files.length === 0) {
    throw new Error('No files selected');
  }

  const maxSize = 50 * 1024 * 1024;
  for (const file of files) {
    if (file.size > maxSize) {
      throw new Error(`File "${file.name}" is too large (${(file.size / 1024 / 1024).toFixed(2)}MB). Maximum size is 50MB.`);
    }
  }

  // Legacy backend: upload one file at a time
  const results = [];
  for (const file of files) {
    const form = new FormData();
    form.append('file', file);
    
    try {
      const res = await fileUploadClient.post('/upload', form);
      results.push({
        filename: file.name,
        status: res.data.status === 'processing' ? 'ingested' : res.data.status,
        chunks_indexed: 0,
        tasks_extracted: 0
      });
    } catch (error: any) {
      results.push({
        filename: file.name,
        status: 'error',
        error: error.message || 'Upload failed'
      });
    }
  }
  
  return { results, detected_tasks: [] };
}

export async function ingestText(text: string, source = 'manual') {
  const res = await apiClient.post('/ingest/text', null, {
    params: { text, source },
  });
  return res.data as { status: string; chunks_indexed: number; detected_tasks: Task[] };
}

export async function researchQuery(query: string, max_results = 5) {
  const res = await apiClient.post('/search', { query });
  return res.data as { query: string; results: Array<any> };
}

export async function researchQuestion(query: string, context_limit = 5) {
  const res = await apiClient.post('/research/question', { query, context_limit });
  return res.data as { answer: string; citations: Array<any> };
}

export type Task = {
  id: number;
  title: string;
  description?: string | null;
  status: string;
  priority?: string | null;
  due_date?: string | null;
  scheduled_for?: string | null;
};

export async function getTasks(status?: string) {
  const res = await apiClient.get('/tasks', { params: status ? { status } : undefined });
  return res.data as { tasks: Task[] };
}

export async function createTask(task: Omit<Task, 'id'>) {
  const res = await apiClient.post('/tasks', task);
  return res.data as { task: Task };
}

export async function approveTask(taskId: number) {
  const res = await apiClient.post(`/tasks/approve/${taskId}`);
  return res.data as { message: string };
}

export async function rejectTask(taskId: number) {
  const res = await apiClient.post(`/tasks/reject/${taskId}`);
  return res.data as { message: string };
}

export async function meetingTranscript(title: string | null, transcript: string) {
  const res = await apiClient.post('/meetings/transcript', { title, transcript });
  return res.data as { meeting_id: number; summary: string; detected_tasks: Task[] };
}

export async function meetingSummaries() {
  const res = await apiClient.get('/meetings/summaries');
  return res.data as { summaries: Array<any> };
}

export async function scheduleProposals() {
  const res = await apiClient.get('/scheduler/proposals');
  return res.data as { proposals: Array<any> };
}

// Health check function
export async function checkBackendHealth(): Promise<boolean> {
  try {
    const res = await apiClient.get('/', { timeout: 5000 });
    return res.data?.status === 'running';
  } catch {
    return false;
  }
}


