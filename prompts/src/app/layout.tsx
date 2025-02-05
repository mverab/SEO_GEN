import type { Metadata } from "next"
import { Inter } from "next/font/google"
import Link from "next/link"
import "./globals.css"
import { Toaster } from "@/components/ui/toaster"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "SEO Generator",
  description: "Generador de contenido SEO optimizado",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body className={inter.className}>
        <header className="border-b">
          <nav className="container mx-auto px-4 py-4">
            <div className="flex items-center space-x-8">
              <Link href="/" className="text-xl font-bold">
                SEO Generator
              </Link>
              <Link href="/content-planner" className="hover:text-primary">
                Content Planner
              </Link>
              <Link href="/keywords" className="hover:text-primary">
                Keywords
              </Link>
              <Link href="/generation" className="hover:text-primary">
                Generación
              </Link>
            </div>
          </nav>
        </header>
        <main className="min-h-screen bg-background">
          {children}
        </main>
        <Toaster />
      </body>
    </html>
  )
} 