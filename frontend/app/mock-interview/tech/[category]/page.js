"use client";

import MockInterview from "@/components/mock-interview/MockInterview";

function MockInterviewCategory({ params }) {
  return <MockInterview category={params?.category} />;
}

export default MockInterviewCategory;
