import { auth } from "better-auth/next";

// Initialize Better Auth with Next.js App Router
export const {
  GET,
  POST
} = auth({
  secret: process.env.AUTH_SECRET || "fallback-secret-change-in-production",
  baseURL: process.env.NEXTAUTH_URL || "http://localhost:3000",
  // Note: Better Auth will handle its own database connection
  // Add any additional configuration as needed
});