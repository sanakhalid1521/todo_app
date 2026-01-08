// Mock authentication API for frontend development
export async function authenticateUser(email: string, password: string) {
  // Simulate an API call to authenticate user
  // In a real app, this would make an actual API request
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        user: {
          id: `user-${email.split('@')[0]}`,
          email,
          name: email.split('@')[0],
        },
        token: `mock-token-${Date.now()}`,
      });
    }, 300);
  });
}

export async function registerUser(email: string, password: string, name: string) {
  // Simulate an API call to register user
  // In a real app, this would make an actual API request
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        user: {
          id: `user-${email.split('@')[0]}`,
          email,
          name,
        },
        token: `mock-token-${Date.now()}`,
      });
    }, 300);
  });
}

export async function getUserInfo() {
  // Simulate getting user info from storage or API
  const userId = localStorage.getItem('userId') || 'user-demo';
  const email = localStorage.getItem('userEmail') || 'demo@example.com';
  const name = localStorage.getItem('userName') || 'Demo User';

  return {
    id: userId,
    email,
    name,
  };
}