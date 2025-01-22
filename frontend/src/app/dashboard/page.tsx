"use client"

import { StatsOverview } from "@/components/dashboard/stats-overview"
import { ProjectList } from "@/components/dashboard/project-list"
import { ActivityFeed } from "@/components/dashboard/activity-feed"
import { ProgressTracker } from "@/components/dashboard/progress-tracker"

export default function DashboardPage() {
  return (
    <div className="container space-y-8">
      <h1>Dashboard</h1>
      <StatsOverview />
      <div className="grid gap-8 md:grid-cols-2">
        <ProjectList />
        <ActivityFeed />
      </div>
      <ProgressTracker />
    </div>
  )
} 