'use client'

import { ContentPlanBuilder } from '@/components/ContentPlanning/ContentPlanBuilder'
import { ArticleScheduler } from '@/components/ContentPlanning/ArticleScheduler'
import { CSVExporter } from '@/components/ContentPlanning/CSVExporter'
import { useState } from 'react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card } from '@/components/ui/card'
import { Toaster } from '@/components/ui/toaster'

interface Article {
  title: string
  keyword: string
  secondary_keywords?: string
  plannedDate?: Date
  status: 'pending' | 'scheduled' | 'completed'
}

export default function ContentPlannerPage() {
  const [articles, setArticles] = useState<Article[]>([])

  const handlePlanGenerated = (plan: any[]) => {
    const newArticles = plan.map(item => ({
      title: item.title,
      keyword: item.keyword,
      secondary_keywords: item.secondary_keywords,
      status: 'pending' as const
    }))
    setArticles(newArticles)
  }

  return (
    <>
      <div className="container mx-auto py-8">
        <h1 className="text-3xl font-bold mb-8">Content Planner</h1>
        
        <Tabs defaultValue="plan" className="space-y-4">
          <TabsList>
            <TabsTrigger value="plan">Generar Plan</TabsTrigger>
            <TabsTrigger value="schedule">Calendario</TabsTrigger>
          </TabsList>

          <TabsContent value="plan">
            <ContentPlanBuilder onPlanGenerated={handlePlanGenerated} />
          </TabsContent>

          <TabsContent value="schedule">
            <Card className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-semibold">Calendario de Contenido</h2>
                <CSVExporter data={articles} />
              </div>
              <ArticleScheduler articles={articles} />
            </Card>
          </TabsContent>
        </Tabs>
      </div>
      <Toaster />
    </>
  )
} 