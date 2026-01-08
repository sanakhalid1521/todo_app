# UI Pages Specification

## Overview
This document specifies the pages and routing structure for the Todo application frontend built with Next.js App Router.

## Route Structure

### Authentication Routes (in (auth) group)
- `/signup` - User registration page
- `/signin` - User login page

### Main Application Routes
- `/` - Landing page (redirects to /signup)
- `/tasks` - Main dashboard with task management

## Page Specifications

### Landing Page (/)
- Redirects to /signup for new users
- Displays loading state with animation
- Minimal design focusing on conversion to signup

### Signup Page (/signup)
- Full user registration form
- Fields: Name, Email, Password, Confirm Password
- Form validation and error handling
- Link to signin page
- Branded with glass morphism design

### Signin Page (/signin)
- User login form
- Fields: Email, Password
- Forgot password link
- Link to signup page
- Branded with glass morphism design

### Tasks Dashboard (/tasks)
- Comprehensive task management interface
- Statistics panel showing completion progress
- Filter controls (all, pending, completed)
- Search functionality
- Task list with individual task cards
- Task creation/editing sidebar modal
- Support for all task properties (title, description, priority, category, due date)

## Page Components Structure

### Layout Components
- Root layout with HTML structure and providers
- Navbar component for navigation
- Authentication provider for user state
- Modal provider for modals
- Search provider for search/filter state

### Task Dashboard Components
- Statistics panel with progress visualization
- Filter bar with active filters
- Search integration
- Task list container
- Individual task cards with all properties
- Task form modal with all fields
- Empty state for no tasks

## Responsive Behavior
- Mobile-first design approach
- Stacked layouts on small screens
- Side-by-side layouts on larger screens
- Touch-friendly interactive elements
- Adaptive typography scaling

## User Experience Flow
1. User visits homepage -> redirected to signup
2. User registers -> redirected to tasks dashboard
3. User logs in -> redirected to tasks dashboard
4. User manages tasks via dashboard interface
5. User can filter, search, and sort tasks
6. User can create, update, delete, and complete tasks