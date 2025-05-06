"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { SallesPaginationProps } from "@/types";

export function SallesPagination({
  pageCourante,
  pagesTotales,
  onPageChange,
}: SallesPaginationProps) {
  return (
    <div className="flex justify-center items-center mt-6 gap-2">
      <Button
        variant="outline"
        size="sm"
        onClick={() => onPageChange(Math.max(1, pageCourante - 1))}
        disabled={pageCourante === 1}
      >
        <ChevronLeft className="h-4 w-4" />
      </Button>
      <span className="text-sm">
        Page {pageCourante} sur {pagesTotales}
      </span>
      <Button
        variant="outline"
        size="sm"
        onClick={() => onPageChange(Math.min(pagesTotales, pageCourante + 1))}
        disabled={pageCourante === pagesTotales}
      >
        <ChevronRight className="h-4 w-4" />
      </Button>
    </div>
  );
}
