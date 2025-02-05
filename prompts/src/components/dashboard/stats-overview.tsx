"use client"

import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"

interface Stats {
  totalArticles: number
  publishedArticles: number
  totalKeywords: number
  averageScore: number
}

export function StatsOverview() {
  const stats: Stats = {
    totalArticles: 25,
    publishedArticles: 18,
    totalKeywords: 150,
    averageScore: 85
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader>
          <CardTitle>Total Artículos</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.totalArticles}</div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Publicados</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.publishedArticles}</div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Keywords</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.totalKeywords}</div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Score Promedio</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.averageScore}%</div>
        </CardContent>
      </Card>
    </div>
  )
} 