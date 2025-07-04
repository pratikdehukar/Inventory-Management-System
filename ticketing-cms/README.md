# Ticketing CMS System

A comprehensive ticketing system built with Django REST Framework (Backend) and Angular (Frontend) for companies to manage client projects and support tickets.

## 🚀 Features

### For Companies
- **User Management**: Manage company staff and clients
- **Project Management**: Create and manage client projects
- **Ticket Management**: Handle support tickets from clients
- **Role-based Access**: Different permissions for admins, staff, and clients
- **Dashboard Analytics**: Overview of tickets, projects, and performance metrics
- **Internal Notes**: Add internal comments on tickets not visible to clients

### For Clients
- **Project Access**: View assigned projects
- **Ticket Creation**: Create support tickets for specific projects
- **Ticket Tracking**: Track ticket status and updates
- **Communication**: Comment on tickets and receive updates
- **File Attachments**: Attach files to tickets and comments

### General Features
- **Authentication**: Secure login/logout with token-based authentication
- **Real-time Updates**: Stay updated with ticket changes
- **File Management**: Upload and manage attachments
- **Search & Filter**: Find tickets and projects quickly
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🏗️ Architecture

### Backend (Django REST Framework)
- **Django 5.2.4**: Latest Django framework
- **Django REST Framework**: For API development
- **Token Authentication**: Secure API access
- **Custom User Model**: Extended user functionality
- **PostgreSQL/SQLite**: Database support
- **CORS Support**: For frontend integration

### Frontend (Angular)
- **Angular 17**: Modern Angular framework
- **Angular Material**: Material Design components
- **Standalone Components**: Modern Angular architecture
- **Lazy Loading**: Optimized routing
- **TypeScript**: Type-safe development
- **SCSS**: Advanced styling

## 📁 Project Structure

```
ticketing-cms/
├── backend/                 # Django REST API
│   ├── accounts/           # User and company management
│   ├── projects/           # Project management
│   ├── tickets/           # Ticket management
│   ├── ticketing_cms/     # Main Django settings
│   ├── manage.py
│   └── requirements.txt
├── frontend/              # Angular application
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/    # Angular components
│   │   │   ├── services/      # Angular services
│   │   │   ├── models/        # TypeScript interfaces
│   │   │   ├── guards/        # Route guards
│   │   │   └── interceptors/  # HTTP interceptors
│   │   ├── assets/           # Static assets
│   │   └── styles.scss       # Global styles
│   ├── angular.json
│   ├── package.json
│   └── tsconfig.json
└── README.md
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+ 
- Node.js 18+
- npm or yarn
- Git

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd ticketing-cms/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ticketing-cms/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:4200`

## 📊 Database Models

### User Model
- **Company Admin**: Full access to company data
- **Company Staff**: Can manage projects and tickets
- **Client**: Can view projects and create tickets

### Company Model
- Company information and settings
- Linked to users and projects

### Project Model
- Client projects managed by companies
- Linked to tickets and users

### Ticket Model
- Support tickets with priorities and statuses
- File attachments and comments support

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile

### Companies
- `GET /api/auth/companies/` - List companies
- `POST /api/auth/companies/` - Create company
- `GET /api/auth/companies/{id}/` - Get company details

### Projects
- `GET /api/projects/` - List projects
- `POST /api/projects/` - Create project
- `GET /api/projects/{id}/` - Get project details
- `PUT /api/projects/{id}/` - Update project

### Tickets
- `GET /api/tickets/` - List tickets
- `POST /api/tickets/` - Create ticket
- `GET /api/tickets/{id}/` - Get ticket details
- `PUT /api/tickets/{id}/` - Update ticket
- `GET /api/tickets/stats/` - Get ticket statistics

### Comments
- `GET /api/tickets/{id}/comments/` - List ticket comments
- `POST /api/tickets/{id}/comments/` - Add comment

## 🎨 Frontend Components

### Core Components
- **Login/Register**: User authentication
- **Dashboard**: Overview and statistics
- **Navbar**: Navigation and user menu
- **Ticket List**: Display and filter tickets
- **Ticket Detail**: View and manage individual tickets
- **Project List**: Display and manage projects
- **Profile**: User profile management

### Key Features
- **Material Design**: Modern UI components
- **Responsive Layout**: Works on all devices
- **Form Validation**: Client-side validation
- **File Upload**: Drag-and-drop file uploads
- **Search & Filter**: Advanced filtering options

## 🔒 Security Features

- **Token Authentication**: Secure API access
- **Role-based Permissions**: Different access levels
- **CORS Protection**: Secure cross-origin requests
- **Input Validation**: Prevent malicious inputs
- **File Upload Security**: Safe file handling

## 🚦 User Workflow

### For Company Users
1. Register/Login to the system
2. Create company profile
3. Add clients and assign projects
4. Manage tickets and assign to staff
5. Track project progress and statistics

### For Clients
1. Register/Login (may be invited by company)
2. View assigned projects
3. Create support tickets
4. Track ticket progress
5. Communicate with support team

## 🧪 Testing

### Backend Testing
```bash
cd backend
python manage.py test
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📈 Performance Optimization

- **Lazy Loading**: Components loaded on demand
- **Pagination**: Efficient data loading
- **Caching**: API response caching
- **Image Optimization**: Compressed images
- **Code Splitting**: Optimized bundles

## 🔧 Configuration

### Environment Variables
Create `.env` file in backend directory:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### API Configuration
Update `frontend/src/environments/environment.ts`:
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

## 🚀 Deployment

### Backend Deployment
1. Set `DEBUG=False` in settings
2. Configure production database
3. Collect static files: `python manage.py collectstatic`
4. Deploy to your preferred platform (Heroku, AWS, etc.)

### Frontend Deployment
1. Build for production: `npm run build`
2. Deploy dist folder to web server
3. Configure API URL for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🎯 Future Enhancements

- **Real-time Notifications**: WebSocket integration
- **Advanced Analytics**: Detailed reporting
- **Mobile App**: Native mobile applications
- **Integration APIs**: Third-party service integration
- **Multi-tenancy**: Support for multiple companies
- **Advanced Search**: Elasticsearch integration

---

Built with ❤️ using Django REST Framework and Angular