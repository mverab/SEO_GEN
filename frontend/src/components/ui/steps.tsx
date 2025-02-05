import { cn } from "@/lib/utils"
import { Check } from "lucide-react"

interface StepsProps {
  steps: string[]
  currentStep: number
  onChange?: (step: number) => void
}

export function Steps({ steps, currentStep, onChange }: StepsProps) {
  return (
    <div className="flex w-full items-center">
      {steps.map((step, index) => {
        const isCompleted = currentStep > index
        const isCurrent = currentStep === index
        
        return (
          <div key={step} className="flex flex-1 items-center">
            <div className="relative flex flex-col items-center">
              <button
                onClick={() => onChange?.(index)}
                className={cn(
                  "h-8 w-8 rounded-full border-2 transition-colors duration-200",
                  isCurrent && "border-primary bg-primary text-primary-foreground",
                  isCompleted && "border-primary bg-primary text-primary-foreground",
                  !isCurrent && !isCompleted && "border-muted bg-background"
                )}
              >
                {isCompleted ? (
                  <Check className="h-4 w-4" />
                ) : (
                  <span>{index + 1}</span>
                )}
              </button>
              <span className="absolute -bottom-6 w-max text-sm">
                {step}
              </span>
            </div>
            {index < steps.length - 1 && (
              <div
                className={cn(
                  "h-[2px] flex-1 transition-colors duration-200",
                  currentStep > index ? "bg-primary" : "bg-border"
                )}
              />
            )}
          </div>
        )
      })}
    </div>
  )
} 