"use client"

import { Button } from "@/components/ui/button"
import { Plus, Edit, Wand2, FileText } from "lucide-react"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

interface Campaign {
  id: string
  name: string
  mainKeyword: string
  articlesGenerated: number
  keywordsCount: number
  lastUpdated: string
}

// Mock data - esto vendrá de la API
const campaigns: Campaign[] = [
  {
    id: "1",
    name: "marketing digital",  // Si no hay nombre, usamos la keyword principal
    mainKeyword: "marketing digital",
    articlesGenerated: 5,
    keywordsCount: 8,
    lastUpdated: "Jan 27, 12:05 AM"
  }
]

export default function CampaignsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Campaigns</h2>
        <Button className="bg-purple-600 hover:bg-purple-700">
          <Plus className="mr-2 h-4 w-4" />
          New Campaign
        </Button>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Main Keywords</TableHead>
              <TableHead>SEO #plans</TableHead>
              <TableHead>Articles Generated</TableHead>
              <TableHead className="text-right">Last Updated On</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {campaigns.map((campaign) => (
              <TableRow key={campaign.id}>
                <TableCell>{campaign.name}</TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <span>{campaign.keywordsCount}</span>
                    <Button variant="ghost" size="sm" className="h-7 px-2">
                      <Edit className="h-4 w-4" />
                    </Button>
                  </div>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <Button variant="ghost" size="sm" className="h-7 px-2">
                      <Wand2 className="h-4 w-4" />
                    </Button>
                    <Button variant="ghost" size="sm" className="h-7 px-2">
                      <Edit className="h-4 w-4" />
                    </Button>
                  </div>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <span>{campaign.articlesGenerated}</span>
                    <div className="flex items-center gap-1">
                      <Button variant="ghost" size="sm" className="h-7 px-2" title="Create Single">
                        <FileText className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm" className="h-7 px-2" title="Create Batch">
                        <FileText className="h-4 w-4" />+
                      </Button>
                    </div>
                  </div>
                </TableCell>
                <TableCell className="text-right text-muted-foreground">
                  {campaign.lastUpdated}
                </TableCell>
              </TableRow>
            ))}

            {campaigns.length === 0 && (
              <TableRow>
                <TableCell colSpan={5} className="h-24 text-center">
                  No campaigns found
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  )
} 