import Link from "next/link"
import { Button } from "@/components/ui/button"

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <span className="font-bold">SEO Generator</span>
          </Link>
          <nav className="flex items-center space-x-6 text-sm font-medium">
            <Link
              href="/keyword-research"
              className="transition-colors hover:text-foreground/80"
            >
              Keywords
            </Link>
            <Link
              href="/content-planning"
              className="transition-colors hover:text-foreground/80"
            >
              Planificación
            </Link>
            <Link
              href="/content-generation"
              className="transition-colors hover:text-foreground/80"
            >
              Generación
            </Link>
          </nav>
        </div>
      </div>
    </header>
  )
} 