import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";
import Chatbot from "@/components/Chatbot";
import { ModalProvider } from "@/context/ModalContext";
import { AuthProvider } from "@/context/AuthContext";
import { SearchProvider } from "@/context/SearchContext";

export const metadata: Metadata = {
  title: "TodoPro | Manage tasks efficiently",
  description: "A premium modern Todo application built with Next.js",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 antialiased overflow-x-hidden">
        <AuthProvider>
          <SearchProvider>
            <ModalProvider>
              <Navbar />
              {children}
              <Chatbot />
            </ModalProvider>
          </SearchProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
