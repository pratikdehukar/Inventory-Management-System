import { User, Company } from './user.model';

export interface Project {
  id: number;
  name: string;
  description: string;
  company: number;
  company_name?: string;
  client: number;
  client_name?: string;
  project_manager?: number;
  project_manager_name?: string;
  status: 'planning' | 'active' | 'on_hold' | 'completed' | 'cancelled';
  start_date: string;
  end_date?: string;
  budget?: number;
  total_tickets?: number;
  open_tickets?: number;
  closed_tickets?: number;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface ProjectDetail extends Project {
  company_detail?: Company;
  client_detail?: User;
  project_manager_detail?: User;
}

export interface ProjectCreate {
  name: string;
  description: string;
  company: number;
  client: number;
  project_manager?: number;
  status: 'planning' | 'active' | 'on_hold' | 'completed' | 'cancelled';
  start_date: string;
  end_date?: string;
  budget?: number;
}