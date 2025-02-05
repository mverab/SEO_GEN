"use client"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
  Home,
  FileText,
  Settings,
  BarChart,
  Users,
  PlusCircle,
  Menu,
  Wand2,
  Layers,
  Bot,
  Palette
} from "lucide-react"
import Link from "next/link"
import { usePathname } from "next/navigation"

interface SidebarProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

const mainFeatures = [
  {
    title: "Start",
    icon: Home,
    href: "/dashboard"
  },
  {
    title: "Campaigns",
    icon: Layers,
    href: "/dashboard/campaigns"
  },
  {
    title: "Single Gen",
    icon: FileText,
    href: "/dashboard/single"
  },
  {
    title: "Bulk Gen",
    icon: FileText,
    href: "/dashboard/bulk"
  }
]

const aiTools = [
  {
    title: "Keyword Gen",
    icon: Wand2,
    href: "/dashboard/keyword-gen"
  },
  {
    title: "AI Detector",
    icon: Bot,
    href: "/dashboard/ai-detector"
  },
  {
    title: "Author Styles",
    icon: Palette,
    href: "/dashboard/styles"
  }
]

export function Sidebar({ open, onOpenChange }: SidebarProps) {
  const pathname = usePathname()

  return (
    <div
      className={cn(
        "fixed inset-y-0 left-0 z-50 flex h-full flex-col border-r bg-card transition-all duration-300",
        open ? "w-64" : "w-16"
      )}
    >
      <div className="flex h-16 items-center justify-between px-4">
        {open ? (
          <span className="text-lg font-semibold">SEO Generator</span>
        ) : null}
        <Button
          variant="ghost"
          size="icon"
          onClick={() => onOpenChange(!open)}
          className={cn("h-8 w-8", !open && "mx-auto")}
        >
          <Menu className="h-4 w-4" />
        </Button>
      </div>

      <ScrollArea className="flex-1 py-2">
        <nav className="grid gap-1 px-2">
          <div className="py-2">
            {mainFeatures.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:bg-accent hover:text-accent-foreground",
                  pathname === item.href && "bg-accent text-accent-foreground",
                  !open && "justify-center"
                )}
              >
                <item.icon className="h-4 w-4" />
                {open && <span>{item.title}</span>}
              </Link>
            ))}
          </div>

          <div className="relative py-2">
            <div className="absolute inset-x-0 -top-px h-px bg-border" />
            {aiTools.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:bg-accent hover:text-accent-foreground",
                  pathname === item.href && "bg-accent text-accent-foreground",
                  !open && "justify-center"
                )}
              >
                <item.icon className="h-4 w-4" />
                {open && <span>{item.title}</span>}
              </Link>
            ))}
          </div>
        </nav>
      </ScrollArea>

      <div className="p-4">
        <Button
          className={cn(
            "w-full gap-2",
            !open && "h-10 w-10 p-0"
          )}
        >
          <PlusCircle className="h-4 w-4" />
          {open && <span>Nuevo Contenido</span>}
        </Button>
      </div>

      <div className="border-t p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-green-500" />
            {open && <span className="text-sm">5 créditos</span>}
          </div>
          {open && (
            <Button variant="outline" size="sm">
              Comprar
            </Button>
          )}
        </div>
      </div>
    </div>
  )
} 