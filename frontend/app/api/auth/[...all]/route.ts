import { auth } from "@/lib/auth";

// Access the handler function from Better Auth
const handler = auth.handler;

export { handler as GET, handler as POST };