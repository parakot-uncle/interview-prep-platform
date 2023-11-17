"use client";

import { useRouter } from "next/navigation";
import Card from "@/components/common/Card";
import categories from "@/data/categories.json";

const backgroundColors = [
  "bg-cyan-400",
  "bg-yellow-400",
  "bg-red-400",
  "bg-green-400",
];

function MockInterviewTech() {
  const router = useRouter();

  return (
    <div className="p-8 h-full flex flex-col justify-center items-center space-y-8">
      <div className="space-y-4 flex flex-col items-center">
        <h1 className="text-3xl font-semibold">Technical Mock Interviews</h1>
        <p className="text-lg text-gray-300">Choose a category</p>
      </div>
      <div className="grid grid-cols-2 gap-10">
        {categories?.map((category, index) => {
          return (
            <Card
              key={index}
              onClick={() => {
                router.push(`/mock-interview/tech/${category?.path}`);
              }}
              className={`cursor-pointer ${backgroundColors[index]} text-xl font-medium p-8 h-[200px] flex justify-center items-center hover:scale-110 transition duration-500`}
            >
              {category?.name}
            </Card>
          );
        })}
      </div>
    </div>
  );
}

export default MockInterviewTech;
