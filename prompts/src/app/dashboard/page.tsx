"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { FileText, Users, BarChart2, TrendingUp } from "lucide-react"
import { ContentTable } from "@/components/dashboard/content-table"
import { StartPopover } from "@/components/start/start-popover"
import { useState } from "react"

const stats = [
  {
    title: "Total Contenidos",
    value: "124",
    icon: FileText,
    trend: "+12.5%",
    description: "vs. mes anterior"
  },
  {
    title: "Promedio AI Score",
    value: "0.32",
    icon: BarChart2,
    trend: "-5.2%",
    description: "vs. mes anterior"
  },
  {
    title: "Visitas Totales",
    value: "45.2K",
    icon: Users,
    trend: "+28.4%",
    description: "vs. mes anterior"
  },
  {
    title: "Conversión",
    value: "3.2%",
    icon: TrendingUp,
    trend: "+1.1%",
    description: "vs. mes anterior"
  }
]

export default function DashboardPage() {
  const [showStart, setShowStart] = useState(true)

  return (
    <>
      <div className={showStart ? "pointer-events-none blur-sm" : ""}>
        <div className="space-y-8">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {stats.map((stat) => (
              <Card key={stat.title}>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    {stat.title}
                  </CardTitle>
                  <stat.icon className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <div className="flex items-center text-xs text-muted-foreground">
                    <span
                      className={
                        stat.trend.startsWith("+")
                          ? "text-green-500"
                          : "text-red-500"
                      }
                    >
                      {stat.trend}
                    </span>
                    <span className="ml-1">{stat.description}</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          <ContentTable />
        </div>
      </div>

      <StartPopover 
        open={showStart} 
        onOpenChange={setShowStart}
      />
    </>
  )
} 