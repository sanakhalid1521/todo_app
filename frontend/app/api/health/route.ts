import { NextResponse } from 'next/server';

export async function GET() {
  try {
    const healthData = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      checks: {
        frontend: 'ok',
        backend_connectivity: 'pending',
      }
    };

    // Optionally check backend connectivity if API URL is available
    const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
    if (backendUrl) {
      try {
        // Simple connectivity check to backend
        const backendHealthUrl = `${backendUrl}/health`;
        // Note: In a real scenario, we might want to check backend health,
        // but for now we'll just verify the environment variable exists
        healthData.checks.backend_connectivity = 'configured';
      } catch (backendError) {
        healthData.checks.backend_connectivity = 'error';
      }
    }

    return NextResponse.json(healthData);
  } catch (error) {
    return NextResponse.json(
      {
        status: 'error',
        error: error.message,
        timestamp: new Date().toISOString()
      },
      { status: 500 }
    );
  }
}