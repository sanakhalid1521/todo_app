# Todo App Frontend

This is the frontend for the full-stack todo application built with Next.js and TypeScript.

## Features

- Task management with create, read, update, and delete operations
- Task filtering and search functionality
- Modern glassmorphism UI design
- Authentication integration
- Responsive design for all devices

## Tech Stack

- Next.js 16.1.1
- React 19.2.3
- TypeScript
- Tailwind CSS
- Lucide React for icons
- Better Auth for authentication

## Environment Variables

Create a `.env.local` file in the root of the frontend directory with the following variables:

```env
NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app
```

For local development, use:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Getting Started

First, install the dependencies:

```bash
npm install
```

Then, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

## Building for Production

To build the application for production:

```bash
npm run build
```

## Deploying to Vercel

This application is configured for deployment to Vercel. The `vercel.json` file contains the necessary configuration.

To deploy:

1. Install the Vercel CLI: `npm install -g vercel`
2. Run `vercel` and follow the prompts

## API Integration

The application communicates with the backend API for all task operations. The API endpoints follow this pattern:

- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{task_id}/toggle` - Toggle task completion status

## Authentication

Authentication is handled through the Better Auth library. The application expects a Bearer token in the Authorization header for API requests.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request