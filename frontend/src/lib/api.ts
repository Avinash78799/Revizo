const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'https://discount-restructuring-hawk-enhancing.trycloudflare.com/api/v1';

export interface UserProfile {
  id: string;
  email: string;
  role: 'student' | 'medical_reviewer' | 'admin';
  full_name: string | null;
  target_exam_year: number | null;
  daily_question_goal: number;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user_id: string;
  email: string;
  role: 'student' | 'medical_reviewer' | 'admin';
  full_name: string | null;
}

export interface Concept {
  id: string;
  topic_id: string;
  name: string;
  high_yield_notes?: string;
  clinical_pearl?: string;
  exam_relevance_score: number;
  created_at: string;
}

export interface Topic {
  id: string;
  chapter_id: string;
  name: string;
  order_index: number;
  concepts: Concept[];
  created_at: string;
}

export interface Chapter {
  id: string;
  subject_id: string;
  name: string;
  order_index: number;
  topics: Topic[];
  created_at: string;
}

export interface SubjectTree {
  id: string;
  name: string;
  code: string;
  description?: string;
  order_index: number;
  chapters: Chapter[];
  created_at: string;
}

export interface SanitizedOption {
  option_key: 'A' | 'B' | 'C' | 'D';
  option_text: string;
}

export interface SanitizedQuestion {
  id: string;
  concept_id: string;
  concept_name?: string;
  topic_name?: string;
  subject_name?: string;
  trust_class: string;
  question_type: string;
  difficulty: string;
  is_high_yield: boolean;
  question_text: string;
  options: SanitizedOption[];
}

export interface TestSession {
  session_id: string;
  user_id: string;
  mode: string;
  total_questions: number;
  completed_questions: number;
  score: number;
  started_at: string;
  questions: SanitizedQuestion[];
}

export interface EvaluationResult {
  is_correct: boolean;
  selected_option_key: string;
  correct_option_key: string;
  correct_explanation: string;
  why_selected_was_wrong?: string | null;
  remember_takeaway: string;
  exam_connection?: string | null;
  detailed_explanation?: string | null;
  concept_id: string;
  concept_name: string;
  is_danger_zone_item: boolean;
  revision_interval_days: number;
  next_revision_due?: string | null;
  is_duplicate_submission?: boolean;
}

export interface TestScoring {
  total_questions: number;
  attempted_count: number;
  correct_count: number;
  incorrect_count: number;
  unanswered_count: number;
  score: number;
  max_possible_score: number;
  accuracy_percentage: number;
  total_time_seconds: number;
  avg_time_per_question_seconds: number;
  calibration_percentage?: number;
  danger_zone_count: number;
  confidence_breakdown: Record<string, { total: number; correct: number; incorrect: number }>;
}

export interface QuestionBreakdown {
  question_id: string;
  concept_id: string;
  concept_name: string;
  question_text: string;
  selected_option_key: string | null;
  correct_option_key: string;
  is_correct: boolean;
  confidence: string;
  time_spent_seconds: number;
  is_danger_zone_item: boolean;
  correct_explanation: string;
  remember_takeaway: string;
}

export interface TestResultData {
  session_id: string;
  mode: string;
  status: string;
  started_at: string;
  submitted_at: string | null;
  scoring: TestScoring;
  question_breakdowns: QuestionBreakdown[];
}

export interface DueRevisionItem {
  concept_id: string;
  concept_name: string;
  topic_name: string;
  subject_name: string;
  revision_interval_days: number;
  next_revision_due: string;
}

export interface DangerZoneItem {
  concept_id: string;
  concept_name: string;
  topic_name: string;
  subject_name: string;
  high_confidence_wrong_count: number;
  last_practiced_at: string;
  clinical_pearl?: string;
}

export interface WeakAreaItem {
  topic_id: string;
  topic_name: string;
  subject_name: string;
  mastery_percentage: number;
  total_attempts: number;
}

export interface DashboardData {
  todays_practice_count: number;
  todays_practice_est_minutes: number;
  due_revisions: DueRevisionItem[];
  weak_areas: WeakAreaItem[];
  danger_zone_count: number;
  total_mistakes_count: number;
  total_questions_attempted: number;
  overall_accuracy_percentage: number;
  calibration_percentage?: number;
}

export interface MistakeItem {
  attempt_id: string;
  question_id: string;
  question_text: string;
  concept_id: string;
  concept_name: string;
  selected_option_key: string | null;
  correct_explanation: string;
  remember_takeaway: string;
  confidence: string;
  is_danger_zone: boolean;
  time_spent_seconds?: number;
  time_trap_tag?: string;
  time_trap_type?: 'quick_gap' | 'overthinking' | 'reasoning';
  answered_at: string;
}

export interface ConceptMasterySummary {
  concept_id: string;
  concept_name: string;
  topic_name: string;
  subject_name: string;
  total_attempts: number;
  correct_attempts: number;
  mastery_percentage: number;
  high_confidence_wrong_count: number;
  revision_interval_days: number;
  next_revision_due: string;
}

// Client API Helper
export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const url = `${API_BASE}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorMessage = 'An error occurred';
    try {
      const errorData = await response.json();
      errorMessage = errorData?.error?.message || errorData?.detail || errorMessage;
    } catch {
      errorMessage = response.statusText || errorMessage;
    }
    throw new Error(errorMessage);
  }

  return response.json();
}
