import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "@/styles/globals.css"
import { Header } from "@/components/layout/header"
import { Shell } from "@/components/layout/shell"
import { Providers } from "@/components/layout/providers"

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
        <Providers>
          <div className="relative flex min-h-screen flex-col">
            <Header />
            <Shell>{children}</Shell>
          </div>
        </Providers>
      </body>
    </html>
  )
} 