import { Routes } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () => import('./components/auth/login/login.component').then(m => m.LoginComponent)
  },
  {
    path: 'register',
    loadComponent: () => import('./components/auth/register/register.component').then(m => m.RegisterComponent)
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./components/dashboard/dashboard.component').then(m => m.DashboardComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'tickets',
    loadComponent: () => import('./components/tickets/ticket-list/ticket-list.component').then(m => m.TicketListComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'tickets/create',
    loadComponent: () => import('./components/tickets/ticket-create/ticket-create.component').then(m => m.TicketCreateComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'tickets/:id',
    loadComponent: () => import('./components/tickets/ticket-detail/ticket-detail.component').then(m => m.TicketDetailComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'projects',
    loadComponent: () => import('./components/projects/project-list/project-list.component').then(m => m.ProjectListComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'projects/create',
    loadComponent: () => import('./components/projects/project-create/project-create.component').then(m => m.ProjectCreateComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'projects/:id',
    loadComponent: () => import('./components/projects/project-detail/project-detail.component').then(m => m.ProjectDetailComponent),
    canActivate: [AuthGuard]
  },
  {
    path: 'profile',
    loadComponent: () => import('./components/profile/profile.component').then(m => m.ProfileComponent),
    canActivate: [AuthGuard]
  },
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  },
  {
    path: '**',
    loadComponent: () => import('./components/not-found/not-found.component').then(m => m.NotFoundComponent)
  }
];