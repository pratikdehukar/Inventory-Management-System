import { User } from './user.model';
import { Project } from './project.model';

export interface Ticket {
  id: number;
  ticket_id: string;
  title: string;
  description: string;
  project: number;
  project_name?: string;
  created_by: number;
  created_by_name?: string;
  assigned_to?: number;
  assigned_to_name?: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  status: 'open' | 'in_progress' | 'pending' | 'resolved' | 'closed';
  category: 'bug' | 'feature' | 'support' | 'question' | 'improvement';
  attachment?: string;
  comments_count?: number;
  created_at: string;
  updated_at: string;
  resolved_at?: string;
  closed_at?: string;
}

export interface TicketDetail extends Ticket {
  project_detail?: Project;
  created_by_detail?: User;
  assigned_to_detail?: User;
  comments?: TicketComment[];
}

export interface TicketCreate {
  title: string;
  description: string;
  project: number;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  category: 'bug' | 'feature' | 'support' | 'question' | 'improvement';
  attachment?: File;
}

export interface TicketUpdate {
  title?: string;
  description?: string;
  assigned_to?: number;
  priority?: 'low' | 'medium' | 'high' | 'urgent';
  status?: 'open' | 'in_progress' | 'pending' | 'resolved' | 'closed';
  category?: 'bug' | 'feature' | 'support' | 'question' | 'improvement';
  attachment?: File;
}

export interface TicketComment {
  id: number;
  ticket: number;
  user: number;
  user_name?: string;
  user_detail?: User;
  comment: string;
  attachment?: string;
  is_internal: boolean;
  created_at: string;
}

export interface TicketCommentCreate {
  ticket: number;
  comment: string;
  attachment?: File;
  is_internal: boolean;
}

export interface TicketStats {
  total_tickets: number;
  open_tickets: number;
  in_progress_tickets: number;
  closed_tickets: number;
  my_assigned_tickets?: number;
  my_open_tickets?: number;
  my_created_tickets?: number;
  high_priority_tickets?: number;
  urgent_tickets?: number;
}