/* eslint-disable @typescript-eslint/no-unused-vars */
"use client";

import { useState, useEffect } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { useTheme } from "@/components/theme-provider";
import {
  format,
  addMonths,
  subMonths,
  startOfMonth,
  endOfMonth,
  eachDayOfInterval,
  isSameMonth,
  isSameDay,
} from "date-fns";
import { fr } from "date-fns/locale";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer";

import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";

const Calendar = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const { theme, toggleTheme } = useTheme();

  const monthStart = startOfMonth(currentDate);
  const monthEnd = endOfMonth(currentDate);
  const monthDays = eachDayOfInterval({ start: monthStart, end: monthEnd });

  const [slidesToScroll, setSlidesToScroll] = useState(6);

  const prevMonth = () => setCurrentDate(subMonths(currentDate, 1));
  const nextMonth = () => setCurrentDate(addMonths(currentDate, 1));

  useEffect(() => {
    const updateSlidesToScroll = () => {
      if (window.innerWidth >= 1024) {
        setSlidesToScroll(6);
      } else if (window.innerWidth >= 768) {
        setSlidesToScroll(5);
      } else if (window.innerWidth >= 640) {
        setSlidesToScroll(4);
      } else {
        setSlidesToScroll(3);
      }
    };

    updateSlidesToScroll();
    window.addEventListener("resize", updateSlidesToScroll);

    return () => {
      window.removeEventListener("resize", updateSlidesToScroll);
    };
  }, []);

  return (
    <div className="w-full max-w-4xl mx-auto mt-8">
      <div className="flex justify-between items-center mb-4">
        <Button
          aria-label="Bouton pour reculer d'un mois"
          onClick={prevMonth}
          variant="outline"
          size="icon"
        >
          <ChevronLeft className="h-4 w-4" />
        </Button>
        <h2 className="text-2xl font-bold">
          {format(currentDate, "MMMM yyyy", { locale: fr })}
        </h2>
        <Button
          aria-label="Bouton pour avancer d'un mois"
          onClick={nextMonth}
          variant="outline"
          size="icon"
        >
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>
      <div className="grid grid-cols-7 gap-2">
        {["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"].map((day) => (
          <div key={day} className="text-center font-bold">
            {day}
          </div>
        ))}
        {monthDays.map((day, index) => (
          <Drawer key={day.toString()}>
            <DrawerTrigger asChild>
              <Button
                aria-label="Bouton de date"
                variant="outline"
                className={`h-16 ${
                  !isSameMonth(day, currentDate) ? "text-gray-300" : ""
                } ${
                  isSameDay(day, selectedDate as Date)
                    ? theme === "dark"
                      ? "bg-blue-700"
                      : "bg-blue-300"
                    : ""
                }`}
                onClick={() => setSelectedDate(day)}
              >
                {format(day, "d")}
              </Button>
            </DrawerTrigger>
            <DrawerContent>
              <DrawerHeader>
                <DrawerTitle>
                  {format(day, "dd MMMM yyyy", { locale: fr })}
                </DrawerTitle>
                <DrawerDescription>
                  Détails des salles disponibles pour cette date
                </DrawerDescription>
              </DrawerHeader>
              <div className="p-4 w-full flex justify-around">
                <Carousel
                  opts={{
                    align: "start",
                    slidesToScroll,
                  }}
                  className="w-[80%] mx-auto"
                >
                  <CarouselContent>
                    {Array.from({ length: 100 }).map((_, index) => (
                      <CarouselItem
                        key={index}
                        className="basis-1/3 sm:basis-1/4 md:basis-1/5 lg:basis-1/6"
                      >
                        <div className="p-1">
                          <Card>
                            <CardContent className="flex aspect-square items-center justify-center p-3">
                              <span className="text-3xl font-semibold">
                                {index + 1}
                              </span>
                            </CardContent>
                          </Card>
                        </div>
                      </CarouselItem>
                    ))}
                  </CarouselContent>
                  <CarouselPrevious />
                  <CarouselNext />
                </Carousel>
              </div>
              <DrawerFooter>
                <DrawerClose asChild>
                  <Button aria-label="Ferme le drawer" variant="outline">
                    Fermer
                  </Button>
                </DrawerClose>
              </DrawerFooter>
            </DrawerContent>
          </Drawer>
        ))}
      </div>
    </div>
  );
};

export default Calendar;
